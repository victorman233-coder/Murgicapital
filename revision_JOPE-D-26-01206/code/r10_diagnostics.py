"""Stage 1A: identification diagnostics and inference for the main specification.

Outputs out/r10_diagnostics.json and out/r10_rotemberg.csv, out/r10_shocks.csv
"""
import numpy as np, pandas as pd, pyfixest as pf
from rev_common import *
from rev_design import *

sc, fsx, cvx = load_panel()
d = sc.reset_index(drop=True)
fs_cols = fsx.split(' + '); cv_cols = cvx.split(' + ')
S, Gl, Gn = obs_matrices(d)
d['Zchk'] = (S * Gl).sum(axis=1)
res = {'check_instrument_maxdiff': float((d['Zchk'] - d['Zc']).abs().max())}

# ------------------------------------------------------------------ sample flow
pan = pd.read_parquet(f'{REP}/data/clean/panel_muni_nacim.parquet')
pg = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
res['sample_flow'] = dict(
    municipalities_padron=int(pg[pg.cmun != '00000'].cmun.nunique()),
    municipalities_with_ipva=int(pan.cmun.nunique()),
    muni_years_ipva_2012_2024=int(pan[(pan.year >= 2012) & (pan.year <= 2024) & pan.dlnR.notna()].shape[0]),
    analysis_obs=int(len(d)), analysis_munis=int(d.cmun.nunique()), analysis_provinces=int(d.cpro.nunique()),
    years=[int(d.year.min()), int(d.year.max())])

# ------------------------------------------------------------------ residualisation (covariate spec, weighted)
out = {}
for spec, ctrls in [('min', fs_cols), ('cov', fs_cols + cv_cols)]:
    for w in ['w', None]:
        tag = f'{spec}_{"w" if w else "u"}'
        Rm = Resid(d, ['cy'], ctrls, w)
        K = Rm.rank + 1
        wt = Rm.w
        yr, xr, zr = Rm(d['dlnR']), Rm(d['xc']), Rm(d['Zc'])
        r = tsls(yr, xr, zr, wt, d['cpro'].values, K)
        grid = np.round(np.arange(-1.5, 3.0001, 0.01), 3)
        r['ar_analytic'] = ar_analytic(yr, xr, zr, wt, d['cpro'].values, K, grid)
        r['ar_wcr'] = ar_wcr(yr, xr, zr, wt, d['cpro'].values, K, grid)
        # recentred instrument, permutations across all origins and within continents
        strata_all = ['all'] * len(GROUPS)
        strata_cont = [REGION[o] for o in GROUPS]
        for sname, strata in [('all', strata_all), ('cont', strata_cont)]:
            z, mu, Zp = perm_instruments(S, Gl, strata, n_perm=2000)
            zt_r = Rm(z - mu)
            Zp_r = Rm((Zp - mu[None, :]).T).T
            rr = tsls(yr, xr, zt_r, wt, d['cpro'].values, K)
            ci, pv = ri_ar(yr, xr, wt, zt_r, Zp_r, grid)
            # first-stage randomisation p-value
            fs_obs = abs(np.sum(wt * zt_r * xr)); fs_p = np.mean(np.abs(Zp_r @ (wt * xr)) >= fs_obs)
            r[f'recentred_{sname}'] = dict(b=rr['b'], se=rr['se'], F=rr['F'], ri_ci=ci, ri_p0=pv[0.0], ri_fs_p=float(fs_p))
        out[tag] = r
        print(tag, {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk in ('b', 'se', 'ri_ci', 'ri_p0')}) for k, v in r.items()})
res['main'] = out

# ------------------------------------------------------------------ validation against pyfixest
m = pf.feols(f'dlnR ~ {fsx} + {cvx} | cy | xc ~ Zc', data=d, vcov={'CRV1': 'cpro'}, weights='w')
res['pyfixest_check'] = coef(m, 'xc')

# ------------------------------------------------------------------ Rotemberg decomposition (leave-out shocks, cov, weighted)
Rm = Resid(d, ['cy'], fs_cols + cv_cols, 'w'); wt = Rm.w
yr, xr = Rm(d['dlnR']), Rm(d['xc'])
Zo = S * Gl                                  # N x O components
Zo_r = Rm(Zo)
den = np.sum(wt[:, None] * Zo_r * xr[:, None], axis=0)
num = np.sum(wt[:, None] * Zo_r * yr[:, None], axis=0)
alpha = den / den.sum(); beta_o = num / den
Fo = []
for j in range(len(GROUPS)):
    rr = tsls(yr, xr, Zo_r[:, j], wt, d['cpro'].values, Rm.rank + 1); Fo.append(rr['F'])
gn, gp, s, P0, Fstock = shock_arrays()
rot = pd.DataFrame({'origin': GROUPS, 'region': [REGION[o] for o in GROUPS], 'alpha': alpha, 'beta': beta_o, 'F': Fo,
                    'share2003': (Fstock[GROUPS] / Fstock[GROUPS].sum()).values,
                    'g_2012_2024': [float(gn.loc[2012:2024, o].sum()) for o in GROUPS],
                    'g_2015_2024': [float(gn.loc[2015:2024, o].sum()) for o in GROUPS],
                    'g_2012_2014': [float(gn.loc[2012:2014, o].sum()) for o in GROUPS]})
rot['contrib'] = rot.alpha * rot.beta
rot = rot.sort_values('alpha', ascending=False)
rot.to_csv(os.path.join(OUT, 'r10_rotemberg.csv'), index=False)
res['rotemberg'] = dict(beta_total=float((alpha * beta_o).sum()), sum_neg_alpha=float(alpha[alpha < 0].sum()),
                        top6_alpha=float(rot.alpha.head(6).sum()), top6_contrib=float(rot.contrib.head(6).sum()),
                        by_region=rot.groupby('region')[['alpha', 'contrib']].sum().to_dict())
print(rot.round(3).to_string())

# ------------------------------------------------------------------ shock summary statistics
G = gn.loc[2012:2024, GROUPS]
expo = pd.Series((S * wt[:, None]).sum(axis=0), index=GROUPS)       # exposure weight by origin
sw = expo / expo.sum()
ac = {o: float(G[o].autocorr(1)) for o in GROUPS}
cont_corr = {}
for reg in ['Europa', 'Africa', 'America', 'Asia']:
    gs = [o for o in GROUPS if REGION[o] == reg]
    C = G[gs].corr().values; iu = np.triu_indices(len(gs), 1)
    cont_corr[reg] = float(np.nanmean(C[iu])) if len(gs) > 1 else None
allC = G.corr().values; iu = np.triu_indices(len(GROUPS), 1)
res['shocks'] = dict(mean=float(G.values.mean()), sd=float(G.values.std()), iqr=[float(np.percentile(G.values, 25)), float(np.percentile(G.values, 75))],
                     eff_n_origins=float(1 / (sw ** 2).sum()), largest_weight=float(sw.max()), largest_origin=sw.idxmax(),
                     mean_autocorr=float(np.nanmean(list(ac.values()))), mean_corr_within_continent=cont_corr,
                     mean_corr_all=float(np.nanmean(allC[iu])),
                     eff_n_origin_years=float(1 / ((np.outer(np.ones(len(G)), sw) / len(G)) ** 2).sum()))
pd.DataFrame({'exposure_weight': sw, 'autocorr': pd.Series(ac)}).join(G.T).to_csv(os.path.join(OUT, 'r10_shocks.csv'))

# ------------------------------------------------------------------ LIML and overidentification with 33 instruments
from linearmodels.iv import IVLIML, IVGMM
Zdf = pd.DataFrame(Zo_r, columns=[f'z{j}' for j in range(Zo_r.shape[1])])
keep = Zdf.columns[(Zdf.abs().sum() > 0).values]
lim = IVLIML(pd.Series(yr), None, pd.Series(xr, name='x'), Zdf[keep], weights=pd.Series(wt)).fit(cov_type='clustered', clusters=pd.Series(pd.factorize(d['cpro'])[0]))
gmm = IVGMM(pd.Series(yr), None, pd.Series(xr, name='x'), Zdf[keep], weights=pd.Series(wt)).fit(cov_type='clustered', clusters=pd.Series(pd.factorize(d['cpro'])[0]))
t2 = IVGMM(pd.Series(yr), None, pd.Series(xr, name='x'), Zdf[keep], weights=pd.Series(wt))
res['overid'] = dict(liml_b=float(lim.params['x']), liml_se=float(lim.std_errors['x']), liml_kappa=float(lim.kappa),
                     gmm_b=float(gmm.params['x']), gmm_se=float(gmm.std_errors['x']),
                     J=float(gmm.j_stat.stat), J_p=float(gmm.j_stat.pval), J_df=int(gmm.j_stat.df))

# ------------------------------------------------------------------ national-shock instrument, BHJ equivalence, AKM0
d['Zn'] = (S * Gn).sum(axis=1)
zn_r = Rm(d['Zn'].values)
rn = tsls(yr, xr, zn_r, wt, d['cpro'].values, Rm.rank + 1)
# exact shock-level representation: beta = sum_n g_n * sum_i w s_in y~_i / sum_n g_n * sum_i w s_in x~_i
years = sorted(d.year.unique())
cols, gvec, gid, gyear = [], [], [], []
for t in range(min(years) - 1, max(years) + 1):
    for j, o in enumerate(GROUPS):
        e = S[:, j] * (0.5 * (d['year'].values == t) + 0.5 * (d['year'].values == t + 1))
        if e.sum() == 0:
            continue
        cols.append(e); gvec.append(gn.loc[t, o]); gid.append(o); gyear.append(t)
Sexp = np.column_stack(cols); gvec = np.array(gvec)
Sexp_r = Rm(Sexp)
num_s = np.sum(gvec * (Sexp_r.T @ (wt * yr))); den_s = np.sum(gvec * (Sexp_r.T @ (wt * xr)))
# shock-level control: year fixed effects (exposure-weighted demeaning of shocks within year)
sbar = (Sexp * wt[:, None]).sum(axis=0)
gdf = pd.DataFrame({'g': gvec, 'year': gyear, 's': sbar})
gdf['gm'] = gdf.groupby('year').apply(lambda x: np.average(x.g, weights=x.s)).reindex(gdf.year).values
g_hat = (gdf.g - gdf.gm).values
grid = np.round(np.arange(-1.5, 3.0001, 0.01), 3)
res['national_shocks'] = dict(iv=rn, shock_level_equivalent=float(num_s / den_s),
                              akm0_ci=akm0(yr, xr, wt, Sexp_r, g_hat, gid, grid),
                              akm0_ci_cluster_origin_year=akm0(yr, xr, wt, Sexp_r, g_hat, [f'{a}_{b}' for a, b in zip(gid, gyear)], grid),
                              n_shocks=int(len(gvec)))
# author's shock-level regression (for the reconciliation): weights s_n, year FE, cluster origin
Q = pd.DataFrame({'origin': gid, 'year': gyear, 'g': gvec, 's': sbar,
                  'ybar': (Sexp_r.T @ (wt * yr)) / sbar, 'xbar': (Sexp_r.T @ (wt * xr)) / sbar})
mq = pf.feols('ybar ~ 1 | year | xbar ~ g', data=Q, weights='s', vcov={'CRV1': 'origin'})
res['national_shocks']['shock_level_year_fe'] = coef(mq, 'xbar')
mq0 = pf.feols('ybar ~ 1 | xbar ~ g', data=Q, weights='s', vcov={'CRV1': 'origin'})
res['national_shocks']['shock_level_no_fe'] = coef(mq0, 'xbar')

# ------------------------------------------------------------------ shock-level balance (2015-2024 growth vs exposure-weighted characteristics)
ext = pd.read_parquet(f'{WORK}/clean/muni_extended.parquet')
mc = pd.read_parquet(f'{REP}/data/clean/muni_chars.parquet')
base = d.drop_duplicates('cmun').set_index('cmun')
chars = pd.DataFrame(index=base.index)
chars['lnpop11'] = np.log(mc['pop11']).reindex(chars.index)
chars['rent11'] = mc['rent11'].reindex(chars.index)
chars['vac11'] = mc['vac11'].reindex(chars.index)
chars['tert11'] = ext['tert11'].replace(np.inf, np.nan).reindex(chars.index)
chars['sh65_11'] = ext['sh65_11'].reindex(chars.index)
chars['coastal'] = ext['coastal'].reindex(chars.index)
chars['sh_constr12'] = ext['sh_constr12'].reindex(chars.index)
chars['sh_trade_hosp12'] = ext['sh_trade_hosp12'].reindex(chars.index)
# pre-period rent growth 2012-2014 (cumulative)
pre = d[d.year <= 2014].groupby('cmun')['dlnR'].sum()
chars['rent_growth_12_14'] = pre.reindex(chars.index)
Sm = s.reindex(chars.index).fillna(0)[GROUPS]
wm = base['w']
bal = []
G1524 = gn.loc[2015:2024, GROUPS].sum()
for c_ in chars.columns:
    v = chars[c_]
    ok = v.notna()
    num_ = (Sm[ok].multiply(wm[ok] * v[ok], axis=0)).sum(); den_ = (Sm[ok].multiply(wm[ok], axis=0)).sum()
    xbar = num_ / den_
    Qb = pd.DataFrame({'g': G1524, 'x': (xbar - xbar.mean()) / xbar.std(), 's': den_ / den_.sum(), 'reg': [REGION[o] for o in GROUPS]})
    mb = pf.feols('g ~ x', data=Qb, weights='s', vcov='hetero')
    mbc = pf.feols('g ~ x | reg', data=Qb, weights='s', vcov='hetero')
    bal.append(dict(var=c_, coef=coef(mb, 'x'), coef_within_continent=coef(mbc, 'x')))
res['shock_balance'] = bal
save('r10_diagnostics.json', res)
print(json.dumps({k: res[k] for k in ['check_instrument_maxdiff', 'pyfixest_check', 'overid', 'national_shocks', 'shocks', 'rotemberg', 'sample_flow']}, indent=1, default=float))
for b in bal: print(b['var'], round(b['coef']['b'], 4), round(b['coef']['p'], 3), '| within cont', round(b['coef_within_continent']['b'], 4), round(b['coef_within_continent']['p'], 3))

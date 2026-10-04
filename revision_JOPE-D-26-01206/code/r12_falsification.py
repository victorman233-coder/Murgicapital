"""Stage 1B: pre-trends, placebos, dynamics (JRS), stability and symmetry.
Output: out/r12_falsification.json, out/r12_lp.csv"""
import numpy as np, pandas as pd, pyfixest as pf
from rev_common import *
from rev_design import *
import analysis_main as am

cwd = os.getcwd(); os.chdir(REP)
p = am.load('nacim')
os.chdir(cwd)
p = p.sort_values(['cmun', 'year']).reset_index(drop=True)
mc = pd.read_parquet(f'{REP}/data/clean/muni_chars.parquet')
ext = pd.read_parquet(f'{WORK}/clean/muni_extended.parquet')
p['lninc15'] = np.log(p['inc2015']); p['lnpop11'] = np.log(p['pop11'])
g = p.groupby('cmun')
p['x1'] = p.d_FOR / p.P; p['z1'] = p.Zcount / p.P
for L in [1, 2, 3]:
    p[f'z1_l{L}'] = g.z1.shift(L); p[f'Zc_l{L}'] = g.Zc.shift(L)
for k in [1, 2]:
    p[f'Zc_f{k}'] = g.Zc.shift(-k)
p['x1_l1'] = g.x1.shift(1)
res = {}
grid = np.round(np.arange(-3, 4.0001, 0.01), 3)


def prep_controls(d, cov=True, extra=()):
    d = d.copy()
    names = []
    ys = sorted(d.year.unique())[1:]
    vars_ = ['forsh_base'] + (COVS if cov else []) + list(extra)
    for v in vars_:
        for y in ys:
            n = f'c_{v}_{y}'; d[n] = d[v] * (d.year == y); names.append(n)
    return d, names


def iv(d, y, x, z, ctrls, w='w', fe=('cy',), exog=()):
    Rm = Resid(d, list(fe), ctrls + list(exog), w)
    yr, xr, zr = Rm(d[y]), Rm(d[x]), Rm(d[z])
    r = tsls(yr, xr, zr, Rm.w, d['cpro'].values, Rm.rank + 1)
    r['ar'] = ar_analytic(yr, xr, zr, Rm.w, d['cpro'].values, Rm.rank + 1, grid)
    r['n'] = len(d)
    return r


def ols_coef(d, y, xs, ctrls, w='w', fe=('cy',)):
    f = f'{y} ~ {" + ".join(xs + ctrls)} | {"+".join(fe)}'
    m = pf.feols(f, data=d, vcov={'CRV1': 'cpro'}, weights=w)
    return {x: coef(m, x) for x in xs}


# ------------------------------------------------------------------ (F1) future-shock placebo on 2011-2014 rents
gn, gp, s, P0, Fo = shock_arrays()
def cum_instr(d, t0, t1, national=False):
    """Predicted change (stock Jan t0 -> Jan t1) over P_i,2003, leave-own-province-out."""
    cpro = d['cmun'].str[:2]
    Sx = s.reindex(d['cmun']).fillna(0)[GROUPS].values
    Gn_ = gn.loc[t0:t1 - 1, GROUPS].sum().values
    out = np.empty(len(d))
    for i, (pr) in enumerate(cpro.values):
        Gp_ = gp.loc[(pr, slice(t0, t1 - 1)), GROUPS].sum().values if not national else 0
        out[i] = Sx[i] @ (Gn_ - Gp_)
    return out

cs = p[p.year == 2015][['cmun', 'cpro', 'w', 'forsh_base', 'P_base', 'inc2015', 'pop11', 'rent11', 'vac11', 'lninc15', 'lnpop11']].copy()
lnR = p.pivot_table(index='cmun', columns='year', values='lnR')
for (a, b) in [(2011, 2014), (2015, 2024), (2011, 2024), (2015, 2019), (2019, 2024)]:
    cs[f'dR_{a}_{b}'] = cs['cmun'].map(lnR[b] - lnR[a])
pg = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
pad = pg[pg.src == 'padron'].set_index(['cmun', 'year'])
cen = pg[pg.src == 'censo'].set_index(['cmun', 'year'])
def stock(v, y):
    src = pad if y <= 2021 else cen
    return cs['cmun'].map(src[v].xs(y, level=1))
P03 = stock('P', 2003)
cs['Zpost'] = cum_instr(cs, 2015, 2024); cs['Zpre'] = cum_instr(cs, 2011, 2014)
cs['Zboom'] = cum_instr(cs, 2003, 2008); cs['Zbust'] = cum_instr(cs, 2008, 2012)
cs['Zpost_n'] = cum_instr(cs, 2015, 2024, national=True)
# realised inflows 2015-2024 (chain padrón to 2021 and census from 2022 within source)
fb = (stock('FOR', 2021) - stock('FOR', 2015)) + (stock('FOR', 2025) - stock('FOR', 2022)) * 0  # placeholder
dF = flows_by_origin(['FOR', 'NAT', 'P'])
fl = dF.reset_index()
cs['M_15_24'] = cs['cmun'].map(fl[(fl.year >= 2015) & (fl.year <= 2023)].groupby('cmun').FOR.sum()) / stock('P', 2015)
cs['M_11_14'] = cs['cmun'].map(fl[(fl.year >= 2011) & (fl.year <= 2013)].groupby('cmun').FOR.sum()) / stock('P', 2011)
# pre-2011 demographic placebos (Padrón)
cs['dNAT_03_08'] = (stock('NAT', 2008) - stock('NAT', 2003)) / P03
cs['dNAT_08_11'] = (stock('NAT', 2011) - stock('NAT', 2008)) / stock('P', 2008)
cs['dP_03_08'] = (stock('P', 2008) - stock('P', 2003)) / P03
cs['dFOR_03_08'] = (stock('FOR', 2008) - stock('FOR', 2003)) / P03
cs = cs.dropna(subset=['dR_2011_2014', 'dR_2015_2024', 'Zpost', 'Zpre']).reset_index(drop=True)
csc = ['forsh_base', 'lninc15', 'lnpop11', 'rent11', 'vac11']
def xreg(y, xs, ctrl=csc, w='w', fe='cpro'):
    m = pf.feols(f'{y} ~ {" + ".join(xs + ctrl)} | {fe}', data=cs, vcov={'CRV1': 'cpro'}, weights=w)
    return {x: coef(m, x) for x in xs}
F1 = {}
for w in ['w', None]:
    t = 'w' if w else 'u'
    F1[t] = dict(placebo_11_14=xreg('dR_2011_2014', ['Zpost', 'Zpre'], w=w),
                 rf_15_24=xreg('dR_2015_2024', ['Zpost'], w=w),
                 rf_15_24_ctrl_pre=xreg('dR_2015_2024', ['Zpost', 'Zpre'], w=w),
                 fs_15_24=xreg('M_15_24', ['Zpost'], w=w),
                 iv_15_24=coef(pf.feols(f'dR_2015_2024 ~ {" + ".join(csc)} | cpro | M_15_24 ~ Zpost', data=cs, vcov={'CRV1': 'cpro'}, weights=w), 'M_15_24'),
                 placebo_demog=dict(dNAT_03_08=xreg('dNAT_03_08', ['Zpost'], w=w), dNAT_08_11=xreg('dNAT_08_11', ['Zpost'], w=w),
                                    dP_03_08=xreg('dP_03_08', ['Zpost'], w=w)))
F1['corr'] = dict(w=cs[['Zboom', 'Zbust', 'Zpre', 'Zpost']].apply(lambda c: c * np.sqrt(cs.w)).corr().round(3).to_dict(),
                  u=cs[['Zboom', 'Zbust', 'Zpre', 'Zpost']].corr().round(3).to_dict())
ext2 = pd.read_parquet(f'{WORK}/clean/muni_extended.parquet')
for v in ['tert11', 'sh65_11', 'sh_constr12', 'sh_ind12', 'sh_trade_hosp12', 'firms12_pc', 'coastal', 'city_core']:
    cs[v] = cs['cmun'].map(ext2[v].replace([np.inf, -np.inf], np.nan))
CENX = ['forsh_base', 'lnpop11', 'rent11', 'vac11', 'tert11', 'sh65_11', 'sh_constr12', 'sh_ind12', 'sh_trade_hosp12', 'firms12_pc', 'coastal', 'city_core']
csn = cs.dropna(subset=CENX)
def xreg_c(y, xs, w):
    m = pf.feols(f'{y} ~ {" + ".join(xs + CENX)} | cpro', data=csn, vcov={'CRV1': 'cpro'}, weights=w)
    return {x: coef(m, x) for x in xs}
for w in ['w', None]:
    t = 'w' if w else 'u'
    F1[t + '_central'] = dict(placebo_11_14=xreg_c('dR_2011_2014', ['Zpost', 'Zpre'], w), rf_15_24=xreg_c('dR_2015_2024', ['Zpost'], w),
                              placebo_demog=dict(dNAT_03_08=xreg_c('dNAT_03_08', ['Zpost'], w), dNAT_08_11=xreg_c('dNAT_08_11', ['Zpost'], w)))
res['F1_F2_longdiff'] = F1
print(json.dumps(F1, indent=1, default=float)[:4000])

# ------------------------------------------------------------------ main annual sample and controls
base = p[(p.year >= 2012) & (p.year <= 2024)].dropna(subset=['dlnR', 'xc', 'Zc', 'w', 'forsh_base'] + COVS).copy()
base = base[base.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
bc, ctrls = prep_controls(base)
res['baseline'] = iv(bc, 'dlnR', 'xc', 'Zc', ctrls)

# (F3a) leads of the instrument
dl = bc.dropna(subset=['Zc_f1', 'Zc_f2', 'Zc_l1']).reset_index(drop=True)
res['F3a_leads'] = dict(
    same_sample=iv(dl, 'dlnR', 'xc', 'Zc', ctrls),
    with_leads=ols_coef(dl.assign(**{}), 'dlnR', ['Zc', 'Zc_f1', 'Zc_f2', 'Zc_l1'], ctrls))

# (JRS) boom-era legacy controls
bj = bc.merge(cs[['cmun', 'Zboom', 'Zbust']], on='cmun', how='left').dropna(subset=['Zboom'])
bj, cj = prep_controls(bj, extra=('Zboom', 'Zbust'))
res['JRS_boom_control'] = iv(bj, 'dlnR', 'xc', 'Zc', cj)

# (F8) symmetry and subperiod stability
bc['pos'] = (bc.Zc > 0).astype(float)
bc['xc_pos'] = bc.xc * bc.pos; bc['xc_neg'] = bc.xc * (1 - bc.pos)
bc['Zc_pos'] = bc.Zc * bc.pos; bc['Zc_neg'] = bc.Zc * (1 - bc.pos)
bc['post'] = (bc.year >= 2020).astype(float)
bc['xc_post'] = bc.xc * bc.post; bc['Zc_post'] = bc.Zc * bc.post
bc['out_yrs'] = (bc.year <= 2014).astype(float)
bc['xc_out'] = bc.xc * bc.out_yrs; bc['Zc_out'] = bc.Zc * bc.out_yrs
def iv2(d, y, xs, zs, ctrls, w='w'):
    return iv_multi(d, y, xs, zs, ctrls, w)
res['subperiod_interaction'] = iv2(bc, 'dlnR', ['xc', 'xc_post'], ['Zc', 'Zc_post'], ctrls)
res['inflow_outflow_years'] = iv2(bc, 'dlnR', ['xc', 'xc_out'], ['Zc', 'Zc_out'], ctrls)
res['symmetry_sign'] = iv2(bc, 'dlnR', ['xc_pos', 'xc_neg'], ['Zc_pos', 'Zc_neg'], ctrls)
res['share_obs_Zc_negative'] = float((bc.Zc <= 0).mean())
for (a, b) in [(2012, 2014), (2015, 2019), (2012, 2019), (2020, 2024), (2015, 2024), (2016, 2024)]:
    sb = bc[(bc.year >= a) & (bc.year <= b)].reset_index(drop=True)
    sb = sb[sb.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
    res[f'window_{a}_{b}'] = iv(sb, 'dlnR', 'xc', 'Zc', [c for c in ctrls if int(c.split('_')[-1]) in set(sb.year)])

# (policy) Catalan rent controls and tensioned zones; excluding 2024
bp = bc.merge(ext[['cat_rc2020', 'cat_zmrt1', 'cat_zmrt2']], left_on='cmun', right_index=True, how='left').fillna({'cat_rc2020': 0, 'cat_zmrt1': 0, 'cat_zmrt2': 0})
bp, cp = prep_controls(bp, extra=('cat_rc2020', 'cat_zmrt1'))
res['policy_controls'] = iv(bp, 'dlnR', 'xc', 'Zc', cp)
bx = bp[(bp.cat_rc2020 == 0) & (bp.cat_zmrt1 == 0)].reset_index(drop=True)
bx = bx[bx.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
res['excl_catalan_controlled'] = iv(bx, 'dlnR', 'xc', 'Zc', ctrls)
b24 = bc[bc.year <= 2023].reset_index(drop=True)
res['excl_2024'] = iv(b24, 'dlnR', 'xc', 'Zc', [c for c in ctrls if not c.endswith('_2024')])
b2 = bp[bp.year >= 2020].reset_index(drop=True)
b2 = b2[b2.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
b2c, c2 = prep_controls(b2, extra=('cat_rc2020', 'cat_zmrt1'))
res['window_2020_2024_policy_controls'] = iv(b2c, 'dlnR', 'xc', 'Zc', c2)

# ------------------------------------------------------------------ local projections (balanced, non-overlapping flows)
def lp_block(spec_cov=True, w='w', H=range(-4, 5), years=(2015, 2020), lags=1):
    rows = []; psi = {}
    q = p.copy()
    gq = q.groupby('cmun')
    bR = gq.lnR.shift(1)
    for h in H:
        q[f'yh{h}'] = gq.lnR.shift(-h) - bR if h != -1 else 0.0
    lagz = [f'z1_l{L}' for L in range(1, lags + 1)]
    need = ['x1', 'z1', 'w', 'forsh_base'] + COVS + lagz + [f'yh{h}' for h in H]
    dd = q[(q.year >= years[0]) & (q.year <= years[1])].dropna(subset=need).copy()
    dd = dd[dd.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
    dd, cc = prep_controls(dd, cov=spec_cov)
    Rm = Resid(dd, ['cy'], cc + lagz, w)
    xr, zr = Rm(dd.x1), Rm(dd.z1)
    den = np.sum(Rm.w * zr * xr)
    cl = dd.cpro.values
    for h in H:
        if h == -1:
            rows.append(dict(h=-1, b=0.0, se=0.0)); continue
        yr = Rm(dd[f'yh{h}'])
        r = tsls(yr, xr, zr, Rm.w, cl, Rm.rank + 1)
        e = yr - r['b'] * xr
        psi[h] = pd.Series(Rm.w * zr * e / den).groupby(cl).sum()
        rows.append(dict(h=h, b=r['b'], se=r['se'], F=r['F'], n=len(dd)))
    pre = [h for h in H if h <= -2]
    Pm = pd.concat([psi[h] for h in pre], axis=1).values
    ng = Pm.shape[0]; N = len(dd)
    V = Pm.T @ Pm * ng / (ng - 1) * (N - 1) / (N - Rm.rank - 1)
    bpre = np.array([[r['b'] for r in rows if r['h'] == h][0] for h in pre])
    W = float(bpre @ np.linalg.solve(V, bpre))
    from scipy import stats
    out = pd.DataFrame(rows)
    b0 = out.loc[out.h == 0, 'b'].item(); s0 = out.loc[out.h == 0, 'se'].item()
    mpre = np.max(np.abs(bpre))
    # relative-magnitudes style bound: post bias <= Mbar * max|pre|; breakdown Mbar where CI covers zero
    Mbreak = max(0.0, (abs(b0) - 1.96 * s0) / mpre) if mpre > 0 else np.inf
    return out, dict(joint_pre_wald=W, df=len(pre), p=float(1 - stats.chi2.cdf(W, len(pre))), max_abs_pre=float(mpre),
                     breakdown_Mbar=float(Mbreak), n=len(dd), years=list(years), lags=lags)

lp_rows = []; lp_tests = {}
for cov in ([True, False] if os.environ.get('SKIP_LP') != '1' else []):
    for w in ['w', None]:
        for lags in [1, 3]:
            tag = f'{"cov" if cov else "min"}_{"w" if w else "u"}_L{lags}'
            o, t = lp_block(cov, w, lags=lags)
            o['spec'] = tag; lp_rows.append(o); lp_tests[tag] = t
            print(tag, o.round(3).to_dict('records'), t)
if lp_rows:
    pd.concat(lp_rows).to_csv(os.path.join(OUT, 'r12_lp.csv'), index=False)
    res['lp_tests'] = lp_tests
else:
    res['lp_tests'] = json.load(open(os.path.join(OUT, 'r12_lp_tests.json')))
json.dump(res['lp_tests'], open(os.path.join(OUT, 'r12_lp_tests.json'), 'w'), default=float)

# ------------------------------------------------------------------ JRS two-instrument model with Sanderson-Windmeijer F, and reconciliation
dr = bc.dropna(subset=['x1', 'z1', 'x1_l1', 'z1_l1', 'Zc_l1']).reset_index(drop=True)
dr = dr[np.isfinite(dr[['x1', 'z1', 'x1_l1', 'z1_l1', 'Zc_l1', 'dlnR', 'xc', 'Zc']]).all(axis=1)].reset_index(drop=True)
dr = dr[dr.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
def sw_F(d, xs, zs, ctrls, w='w'):
    Rm = Resid(d, ['cy'], ctrls, w); W_ = Rm.w
    X = np.column_stack([Rm(d[x]) for x in xs]); Z = np.column_stack([Rm(d[z]) for z in zs])
    cl = d.cpro.values; out = {}
    for j in range(len(xs)):
        xj = X[:, j]; xo = np.delete(X, j, axis=1)
        # 2SLS of xj on other endogenous using Z
        Pz = Z @ np.linalg.solve((Z * W_[:, None]).T @ Z, (Z * W_[:, None]).T @ xo)
        delta = np.linalg.solve((Pz * W_[:, None]).T @ xo, (Pz * W_[:, None]).T @ xj)
        e = xj - xo @ delta
        # cluster-robust Wald of e on Z
        ZWZ = (Z * W_[:, None]).T @ Z
        pi = np.linalg.solve(ZWZ, (Z * W_[:, None]).T @ e)
        u = e - Z @ pi
        sc_ = pd.DataFrame(Z * (W_ * u)[:, None]).groupby(cl).sum().values
        Vb = np.linalg.solve(ZWZ, np.linalg.solve(ZWZ, (sc_.T @ sc_)).T)
        wald = float(pi @ np.linalg.solve(Vb, pi))
        out[xs[j]] = wald / (len(zs) - len(xs) + 1)
    return out
res['JRS_two_instruments'] = dict(
    est=iv2(dr, 'dlnR', ['x1', 'x1_l1'], ['z1', 'z1_l1'], ctrls),
    SW_F=sw_F(dr, ['x1', 'x1_l1'], ['z1', 'z1_l1'], ctrls))
mm = res['JRS_two_instruments']['est']; V = np.array(mm['_V'])
res['JRS_two_instruments']['sum'] = dict(b=mm['x1']['b'] + mm['x1_l1']['b'], se=float(np.sqrt(V[0, 0] + V[1, 1] + 2 * V[0, 1])))
res['reconciliation_same_sample'] = dict(
    a_centred_level=iv(dr, 'dlnR', 'xc', 'Zc', ctrls),
    b_centred_municipal_FE=iv(dr, 'dlnR', 'xc', 'Zc', ctrls, fe=('cy', 'cmun')),
    c_calendar_level=iv(dr, 'dlnR', 'x1', 'z1', ctrls),
    d_calendar_control_lag=iv(dr, 'dlnR', 'x1', 'z1', ctrls, exog=('z1_l1',)),
    e_centred_control_lag=iv(dr, 'dlnR', 'xc', 'Zc', ctrls, exog=('Zc_l1',)),
    n=len(dr), years=[int(dr.year.min()), int(dr.year.max())])
save('r12_falsification.json', res)
for k in ['baseline', 'F3a_leads', 'JRS_boom_control', 'subperiod_interaction', 'inflow_outflow_years', 'symmetry_sign', 'policy_controls',
          'excl_catalan_controlled', 'excl_2024', 'window_2020_2024_policy_controls', 'JRS_two_instruments', 'reconciliation_same_sample'] + [k for k in res if k.startswith('window_')]:
    print(k, json.dumps(res[k], default=float)[:900])

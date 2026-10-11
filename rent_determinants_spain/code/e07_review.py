"""Entry-gap paper: analyses added in the multi-agent review.
(a) The entry gap in changes: INE provincial indices of new and existing leases (base 2015 = 100), so that
    ln(new/existing) in 2024 measures the change in the gap since 2015, on the provincial inflow (2SLS).
(b) Recent (2020-2024) versus earlier (2015-2019) inflows: the stock-flow model implies that the 2024 gap responds
    mainly to recent shocks.
(c) Over-identification by origin: separate instruments for Colombia, Peru, Romania and the rest; Hansen J test.
(d) Control for the 2003-2014 foreign-born inflow (persistence of settlement; Jaeger, Ruist and Stuhler 2018).
(e) Weights and influential provinces: square-root weights; without Madrid and Barcelona provinces; without Málaga;
    leave-one-province-out range.
(f) Geography and coast: inflow x undevelopable land and inflow x coast jointly.
(g) Value adjustment with elasticities below one; composition of new leases (value and floor area).
(h) Wild cluster restricted bootstrap Anderson-Rubin sets for the main outcomes.
(i) Households: implied household size from income per household and per person; number of households.
(j) Tourism: annual Catalan register 2014-2025, exposure bins x year, pre-trends before the collapse.
(k) Basque Country: within-region association between the inflow and the entry-income gap.
(l) Base-year sensitivity of the entry facts (Catalonia, Aragón).
Output: out/e07_review.json"""
import numpy as np, pandas as pd
import pyfixest as pf
from linearmodels.iv import IVGMM
from rd_common import *
from rev_common import GROUPS, flows_by_origin, instrument, shares
from rev_design import Resid, tsls, ar_analytic, ar_wcr, iv_multi
from ld_shiftshare import components

res = {}
X = pd.read_parquet(f'{CL}/e01_X.parquet')
LD = pd.read_parquet(f'{CL}/ld_instrument_all.parquet').set_index('cmun')
CEN = PRED + ECON
GRID = np.round(np.arange(-4, 8.0001, 0.01), 3)


def iv(d, y, x='x2024', z='Z2024', ctrls=CEN, w='P15', fe='cpro', wcr=False):
    d = d.dropna(subset=[y, x, z] + ctrls + [w]).copy()
    R = Resid(d, [fe] if fe else [], ctrls, w=w)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values); wt = d[w].values.astype(float)
    o = {k: float(v) for k, v in tsls(yr, xr, zr, wt, d.cpro.values, R.rank + 1).items()}
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, R.rank + 1, GRID); o['n'] = len(d)
    if wcr:
        o['ar_wcr'] = ar_wcr(yr, xr, zr, wt, d.cpro.values, R.rank + 1, GRID[::2], B=4999, seed=1)
    return o


# ------------------------------------------------------------------ (a) the gap in changes, provinces
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.prov != '00') & (pa.typ == 'Índice')].pivot_table(index=['prov', 'year'], columns='age', values='val').reset_index()
pa['G'] = np.log(pa['Nuevo contrato'] / pa['Contrato existente'])
Gp = pa.pivot_table(index='prov', columns='year', values='G')
L = LD.reset_index(); L['prov'] = L.cmun.str[:2]
L = L.dropna(subset=['x2024', 'Z2024', 'P15'])
agg = L.groupby('prov').apply(lambda q: pd.Series({'x': np.average(q.x2024, weights=q.P15), 'z': np.average(q.Z2024, weights=q.P15),
                                                  'P': q.P15.sum()}))
P = Gp.join(agg, how='inner').reset_index().rename(columns={2021: 'G21', 2024: 'G24'})
P['lnP'] = np.log(P.P); P['dG'] = P.G24 - P.G21
prov = {}
for y in ['G24', 'dG']:
    for lab, ctrl, w in [('w', '', 'P'), ('w_lnP', ' + lnP', 'P'), ('unw', '', None)]:
        kw = dict(vcov='hetero')
        if w:
            kw['weights'] = w
        m = pf.feols(f'{y} ~ 1{ctrl} | x ~ z', data=P, **kw)
        t = m.tidy().loc['x']
        fs = pf.feols(f'x ~ z{ctrl}', data=P, vcov='hetero', **({'weights': w} if w else {})).tidy().loc['z']
        prov[f'{y}|{lab}'] = dict(b=float(t['Estimate']), se=float(t['Std. Error']), p=float(t['Pr(>|t|)']), F=float((fs['Estimate'] / fs['Std. Error']) ** 2), n=int(m._N))
res['provincial_changes'] = prov
print('provincial', {k: (round(v['b'], 3), round(v['se'], 3), round(v['p'], 3), round(v['F'], 1)) for k, v in prov.items()})

# ------------------------------------------------------------------ instrument and inflow by window, inflow 2003-2014
dF = flows_by_origin().reset_index()
munis = sorted(X.cmun.unique())
my = pd.DataFrame([(m_, y_) for m_ in munis for y_ in range(2015, 2025)], columns=['cmun', 'year'])
my['Z'] = instrument(my).values
s_, lam_, P0 = shares(2003)
sc = (P0.reindex(munis) / LD.P15.reindex(munis))
for lab, (a, b) in [('old', (2015, 2019)), ('new', (2020, 2024))]:
    X[f'Z_{lab}'] = X.cmun.map(my[my.year.between(a, b)].groupby('cmun').Z.sum() * sc)
    X[f'x_{lab}'] = X.cmun.map(dF[dF.year.between(a, b)].groupby('cmun').FOR.sum() / LD.P15)
X['x0314'] = X.cmun.map(dF[dF.year.between(2003, 2014)].groupby('cmun').FOR.sum() / LD.P03)
print('window check: corr(Z_old+Z_new, Z2024) =', round(np.corrcoef((X.Z_old + X.Z_new).dropna(), X.loc[(X.Z_old + X.Z_new).notna(), 'Z2024'])[0, 1], 4))

# ------------------------------------------------------------------ (b) recent vs earlier inflows
win = {}
for y in ['G_vr', 'dlnR', 'entry']:
    d = X.dropna(subset=[y, 'x_old', 'x_new', 'Z_old', 'Z_new'] + CEN).copy()
    o = iv_multi(d, y, ['x_old', 'x_new'], ['Z_old', 'Z_new'], CEN, w='P15', fe=('cpro',), cluster='cpro')
    win[y] = {k: o[k] for k in ['x_old', 'x_new']}; win[y]['n'] = o['_n']
    R = Resid(d, ['cpro'], CEN, 'P15')
    for xv in ['x_old', 'x_new']:                                   # first stages: each endogenous on both instruments
        A = np.column_stack([R(d.Z_old.values), R(d.Z_new.values)]); b_ = R(d[xv].values)
        coef = np.linalg.lstsq(A * np.sqrt(R.w)[:, None], b_ * np.sqrt(R.w), rcond=None)[0]
        win[y][f'fs_{xv}'] = [float(c) for c in coef]
    win[y]['corr_Z'] = float(np.corrcoef(d.Z_old, d.Z_new)[0, 1])
res['windows'] = win
print('windows', {y: {k: (round(v['b'], 3), round(v['se'], 3)) for k, v in w_.items() if isinstance(v, dict)} for y, w_ in win.items()})

# ------------------------------------------------------------------ (c) over-identification by origin
TOP = ['Colombia', 'Perú', 'Rumanía']
ovr = {}
for y, T in [('G_vr', 2024), ('entry', 2024), ('dlnR', 2024)]:
    d = X.dropna(subset=[y, f'x{T}', f'Z{T}'] + CEN).reset_index(drop=True)
    S, Gl, _ = components(d, T)
    for o_ in TOP:
        d[f'Z_{o_}'] = S[:, GROUPS.index(o_)] * Gl[:, GROUPS.index(o_)]
    rest = [j for j, g in enumerate(GROUPS) if g not in TOP]
    d['Z_rest'] = (S[:, rest] * Gl[:, rest]).sum(1)
    zs = [f'Z_{o_}' for o_ in TOP] + ['Z_rest']
    R = Resid(d, ['cpro'], CEN, 'P15')
    rr = pd.DataFrame({c: R(d[c].values) for c in [y, f'x{T}'] + zs})
    m = IVGMM(rr[y], None, rr[[f'x{T}']], rr[zs], weights=d.P15).fit(cov_type='clustered', clusters=d.cpro)
    single = {}
    for zc in zs:
        q = tsls(rr[y].values, rr[f'x{T}'].values, rr[zc].values, R.w, d.cpro.values, R.rank + 1)
        single[zc] = dict(b=float(q['b']), se=float(q['se']), F=float(q['F']))
    ovr[y] = dict(b_gmm=float(m.params[f'x{T}']), se_gmm=float(m.std_errors[f'x{T}']), J=float(m.j_stat.stat), J_p=float(m.j_stat.pval),
                  J_df=int(m.j_stat.df), single=single)
res['overid_origin'] = ovr
print('overid', {y: (round(v['b_gmm'], 3), round(v['J'], 2), round(v['J_p'], 3), {k: (round(s2['b'], 2), round(s2['F'], 1)) for k, s2 in v['single'].items()}) for y, v in ovr.items()})

# ------------------------------------------------------------------ (d) control for the 2003-2014 inflow; (e) weights and provinces
X['sqrtP'] = np.sqrt(X.P15)
rob = {}
for y in ['G_vr', 'entry', 'dlnR', 'd_hhsize']:
    T = 2023 if y == 'd_hhsize' else 2024
    rob[f'{y}|x0314'] = iv(X, y, f'x{T}', f'Z{T}', ctrls=CEN + ['x0314'])
    rob[f'{y}|sqrtP'] = iv(X, y, f'x{T}', f'Z{T}', w='sqrtP')
    rob[f'{y}|no28_08'] = iv(X[~X.cpro.isin(['28', '08'])], y, f'x{T}', f'Z{T}')
    rob[f'{y}|no29'] = iv(X[X.cpro != '29'], y, f'x{T}', f'Z{T}')
lopo = []
for p_ in sorted(X.dropna(subset=['G_vr']).cpro.unique()):
    o = iv(X[X.cpro != p_], 'G_vr')
    lopo.append(dict(prov=p_, b=o['b'], lo=o['ar'][0], hi=o['ar'][1]))
lp = pd.DataFrame(lopo)
rob['lopo_G_vr'] = dict(b_min=float(lp.b.min()), b_max=float(lp.b.max()), prov_min=lp.loc[lp.b.idxmin(), 'prov'], prov_max=lp.loc[lp.b.idxmax(), 'prov'],
                        n_lo_le0=int((lp.lo <= 0).sum()), provs_lo_le0=lp.loc[lp.lo <= 0, 'prov'].tolist())
res['robust'] = rob
print('robust', {k: (round(v['b'], 3), round(v['F'], 1), v['ar']) for k, v in rob.items() if 'b' in v and 'b_min' not in v}, rob['lopo_G_vr'])

# ------------------------------------------------------------------ (f) geography and coast jointly
def wstd(v, w):
    mu = np.average(v, weights=w); return (v - mu) / np.sqrt(np.average((v - mu) ** 2, weights=w))


geo = {}
for y in ['G_vr', 'entry']:
    for r in ['undev10', 'sea10', 'steep10']:
        d = X.dropna(subset=[y, 'x2024', 'Z2024', r] + CEN).copy()
        d['U'] = wstd(d[r], d.P15); d['C'] = d.coastal.astype(float)
        d['xU'] = d.x2024 * d.U; d['zU'] = d.Z2024 * d.U; d['xC'] = d.x2024 * d.C; d['zC'] = d.Z2024 * d.C
        o = iv_multi(d, y, ['x2024', 'xU', 'xC'], ['Z2024', 'zU', 'zC'], CEN + ['U'], w='P15', fe=('cpro',), cluster='cpro')
        geo[f'{y}|{r}'] = {k: o[k] for k in ['x2024', 'xU', 'xC']}
        geo[f'{y}|{r}']['n'] = o['_n']
    d = X.dropna(subset=[y, 'x2024', 'Z2024'] + CEN).copy(); d['C'] = d.coastal.astype(float)
    d['xC'] = d.x2024 * d.C; d['zC'] = d.Z2024 * d.C
    o = iv_multi(d, y, ['x2024', 'xC'], ['Z2024', 'zC'], CEN, w='P15', fe=('cpro',), cluster='cpro')
    geo[f'{y}|coast_only'] = {k: o[k] for k in ['x2024', 'xC']}
res['geo_coast'] = geo
print('geo', {k: {kk: (round(vv['b'], 3), round(vv['se'], 3)) for kk, vv in v.items() if isinstance(vv, dict)} for k, v in geo.items()})

# ------------------------------------------------------------------ (g) value adjustment and composition
AE_ = pd.read_parquet(f'{CL}/aeat_entry_gap_2024.parquet').set_index('cmun')
X['lvr'] = X.cmun.map(np.log(AE_.vr_new / AE_.vr)); X['lm2'] = X.cmun.map(np.log(AE_.m2_new / AE_.m2))
for th in [0.0, 0.5, 0.7]:
    X[f'G_th{int(10 * th)}'] = X.G - th * X.lvr
val = {f'theta_{c[-1] if c[-1] != "0" else "0"}': iv(X, c) for c in ['G_th0', 'G_th5', 'G_th7']}
val['theta_1'] = iv(X, 'G_vr')
val['comp_value'] = iv(X, 'lvr'); val['comp_m2'] = iv(X, 'lm2')
d = X.dropna(subset=['G', 'lvr'])
val['mean_G_theta'] = {str(th): float(100 * np.average(d.G - th * d.lvr, weights=d.P15)) for th in [0.0, 0.5, 0.7, 1.0]}
res['value_adjustment'] = val
print('value', {k: (round(v['b'], 3), v['ar']) for k, v in val.items() if isinstance(v, dict) and 'b' in v}, val['mean_G_theta'])

# ------------------------------------------------------------------ (h) wild cluster restricted AR sets
wcr = {}
for y, T in [('G_vr', 2024), ('entry', 2024), ('AE', 2024), ('dlnR', 2024), ('d_uc', 2023), ('d_hhsize', 2023), ('dlnviv', 2024), ('dP2024', 2024)]:
    wcr[y] = iv(X, y, f'x{T}', f'Z{T}', wcr=True)['ar_wcr']
res['ar_wcr'] = wcr
print('wcr', wcr)

# ------------------------------------------------------------------ (i) households; entrants' affordability with aligned windows
X['dP2023'] = X.cmun.map(LD.dP2023)
X['hh_n'] = np.log1p(X.dP2023) - X.d_hhsize
X['size_inc'] = X.d_hh - X.d_pp
X['AE23'] = X.dlnR23 + X.G_vr - X.d_uc
hh = {y: iv(X, y, 'x2023', 'Z2023') for y in ['hh_n', 'size_inc', 'd_hhsize', 'AE23']}
res['households'] = hh
print('households', {k: (round(v['b'], 3), v['ar']) for k, v in hh.items()})

# ------------------------------------------------------------------ (j) tourism: annual Catalan register, pre-trends
Cq = pd.read_parquet(f'{CL}/cat_q.parquet')
b19 = Cq[Cq.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
keep = b19[(b19['count'] == 4) & (b19['sum'] >= 40)].index
expo = Cq[Cq.cmun.isin(keep)].groupby('cmun').vutpct_2020M08.first().fillna(0)
P19 = Cq[Cq.year == 2019].groupby('cmun').P.first()
La = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = La[La['Període'] == 'gener-desembre'].copy()
La['cmun'] = La['Codi territorial'].astype(int).astype(str).str.zfill(5)
La = La[La.cmun.isin(keep)].rename(columns={'Any': 'year'})
La['lnn'] = np.log(pd.to_numeric(La.Habitatges, errors='coerce')); La['lnrent'] = np.log(pd.to_numeric(La.Renda, errors='coerce'))
La = La[La.year.between(2014, 2025)].copy()
La['E'] = La.cmun.map(expo); La['P19'] = La.cmun.map(P19)
La['bin'] = pd.cut(La.E, [-0.01, 1, 3, 8, 100], labels=['b0', 'b1', 'b2', 'b3']).astype(str)
names = []
for b in ['b1', 'b2', 'b3']:
    for yv in range(2014, 2026):
        if yv == 2019:
            continue
        nm = f'{b}_{yv}'; La[nm] = ((La.bin == b) & (La.year == yv)).astype(float); names.append(nm)
tour = {}
for y in ['lnn', 'lnrent']:
    q = La.dropna(subset=[y, 'P19'])
    m = pf.feols(f'{y} ~ ' + ' + '.join(names) + ' | cmun + year', data=q, weights='P19', vcov={'CRV1': 'cmun'})
    bt = m.coef(); V = m._vcov; nm_ = list(bt.index)
    out = {}
    for b in ['b1', 'b2', 'b3']:
        pre = [f'{b}_{yv}' for yv in range(2014, 2019)]
        idx = [nm_.index(p_) for p_ in pre]
        bb = bt[pre].values; VV = V[np.ix_(idx, idx)]
        W_ = float(bb @ np.linalg.solve(VV, bb))
        from scipy.stats import chi2
        out[b] = dict(coefs={int(k.split('_')[1]): float(bt[k]) for k in nm_ if k.startswith(b + '_')},
                      ses={int(k.split('_')[1]): float(np.sqrt(V[nm_.index(k), nm_.index(k)])) for k in nm_ if k.startswith(b + '_')},
                      pre_wald=W_, pre_p=float(1 - chi2.cdf(W_, len(pre))))
    tour[y] = out
res['tourism_annual'] = tour
res['tourism_annual_n'] = int(La.cmun.nunique())
print('tourism annual pre-trend p', {y: {b: round(v['pre_p'], 4) for b, v in t_.items()} for y, t_ in tour.items()})

# ------------------------------------------------------------------ (k) Basque Country within-region; (l) base years
A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
uc = A[A.indicator == 'Mediana de la renta por unidad de consumo'].pivot_table(index='cmun', columns='year', values='value')
Em = pd.read_parquet(f'{CL}/emal_muni.parquet'); pm = Em.pivot_table(index='cmun', columns='year', values='rent_m2_new')
Bq = pd.DataFrame({'AE': np.log(pm[2023] / pm[2016]) - np.log(uc[2023] / uc[2016]).reindex(pm.index)}).join(LD[['x2023', 'P15']]).dropna()
Bq['cpro'] = Bq.index.str[:2]
m = pf.feols('AE ~ x2023 | cpro', data=Bq.reset_index(), weights='P15', vcov='hetero')
t = m.tidy().loc['x2023']
res['basque_within'] = dict(b=float(t['Estimate']), se=float(t['Std. Error']), n=int(m._N),
                            inflow_mean=float(np.average(Bq.x2023, weights=Bq.P15)))
M = pd.read_parquet(f'{CL}/muni_panel.parquet'); ip = M.pivot_table(index='cmun', columns='year', values='lnR')
Lc = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv'); Lc = Lc[Lc['Període'] == 'gener-desembre'].copy()
Lc['cmun'] = Lc['Codi territorial'].astype(int).astype(str).str.zfill(5)
nw = Lc.pivot_table(index='cmun', columns='Any', values='Renda'); nn = Lc.pivot_table(index='cmun', columns='Any', values='Habitatges')
Ar = pd.read_parquet(f'{CL}/aragon_muni.parquet'); ai = Ar.pivot_table(index='cmun', columns='year', values='idx_street')
base = {}
for b in [2015, 2016, 2018]:
    for reg, dn in [('CAT', np.log(nw[2023] / nw[b]).where(nn[b] >= 30)), ('ARA', ai[2023] - ai[b])]:
        q = pd.DataFrame({'d_new': dn, 'd_uc': np.log(uc[2023] / uc[b]).reindex(dn.index), 'd_stock': (ip[2023] - ip[b]).reindex(dn.index)}).join(LD.P15).dropna(subset=['d_new', 'd_uc', 'P15'])
        qs = q.dropna(subset=['d_stock'])
        base[f'{reg}|{b}'] = dict(n=len(q), d_new=float(100 * np.average(q.d_new, weights=q.P15)), d_uc=float(100 * np.average(q.d_uc, weights=q.P15)),
                                  gap=float(100 * np.average(q.d_new - q.d_uc, weights=q.P15)), share_pos=float(((q.d_new - q.d_uc) > 0).mean()),
                                  d_stock=float(100 * np.average(qs.d_stock, weights=qs.P15)) if len(qs) else None, n_stock=len(qs))
res['base_years'] = base
print('basque', res['basque_within']); print('base', {k: (round(v['d_new'], 1), round(v['d_uc'], 1), round(v['gap'], 1), round(v['share_pos'], 2)) for k, v in base.items()})
save('e07_review.json', res)

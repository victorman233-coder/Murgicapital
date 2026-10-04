"""Entry-gap paper: main estimates.
Unit: municipality; long differences 2015-2023/24; province fixed effects; predetermined controls (census 2011, firms 2012);
treatment: cumulative net foreign-born inflow relative to 2015 population, instrumented with the long-difference shift-share.
Outcomes: stock rent growth (IPVA), entry gap in 2024 (AEAT: raw, per m2, per euro of cadastral value), implied entry-rent growth,
income per consumption unit and per person/household, household size, population, dwellings; affordability for insiders
and entrants. Mechanisms: geographic supply constraints (Copernicus DEM), tourism, spillovers within functional urban areas,
tenure (price-to-income before 2022)."""
import numpy as np, pandas as pd
import pyfixest as pf
from linearmodels.iv import IV2SLS
from rd_common import *
from rev_design import Resid, tsls, ar_analytic

res = {}
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
st = M.drop_duplicates('cmun').set_index('cmun')
LD = pd.read_parquet(f'{CL}/ld_instrument_all.parquet').set_index('cmun')
A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
inc = A.pivot_table(index=['cmun', 'year'], columns='indicator', values='value')
gi = lambda ind, a, b: np.log(inc[ind].unstack('year')[b] / inc[ind].unstack('year')[a])
pr = M.pivot_table(index='cmun', columns='year', values='lnR'); viv = M.pivot_table(index='cmun', columns='year', values='viv')
AE = pd.read_parquet(f'{CL}/aeat_entry_gap_2024.parquet').set_index('cmun')
RG = pd.read_parquet(f'{CL}/rigidity_dem.parquet').set_index('cmun')
X = pd.DataFrame({'dlnR': pr[2024] - pr[2015], 'dlnR23': pr[2023] - pr[2015], 'dlnR_pre': pr[2015] - pr[2012],
                  'dlnviv': np.log(viv[2024] / viv[2015]),
                  'd_uc': gi('Mediana de la renta por unidad de consumo', 2015, 2023), 'd_pp': gi('Renta neta media por persona', 2015, 2023),
                  'd_hh': gi('Renta neta media por hogar', 2015, 2023),
                  'd_uc_pre': np.nan})
X = X.join(LD[['x2023', 'Z2023', 'x2024', 'Z2024', 'dP2024', 'P15']], how='inner').join(AE[['G', 'G_m2', 'G_vr']], how='left')
X = X.join(st[PRED + ECON + ['cpro', 'ccaa', 'vutpct_2020M08', 'cat_zmrt1', 'area_km2', 'fua']], how='left').join(RG[['undev10', 'sea10', 'steep10', 'undev20']], how='left')
X['vut20'] = X.vutpct_2020M08.fillna(0)
X['entry'] = X.dlnR + X.G_vr                         # implied growth of entry rents (quality-adjusted gap added to stock growth)
X['AI'] = X.dlnR23 - X.d_uc                          # insiders: stock rent vs income per consumption unit, 2015-2023
X['AE'] = X.entry - X.d_uc                           # entrants (entry rent 2024 vs income 2023: one-year mismatch noted)
# household size and foreign share from ADRH demographic indicators, if available
if os.path.exists(f'{CL}/adrh_30832_muni.parquet'):
    Dm = pd.read_parquet(f'{CL}/adrh_30832_muni.parquet').pivot_table(index=['cmun', 'year'], columns='indicator', values='value')
    hs = [c for c in Dm.columns if 'Tamaño medio del hogar' in c]; nat = [c for c in Dm.columns if 'española' in c.lower()]
    if hs:
        h = Dm[hs[0]].unstack('year'); X['d_hhsize'] = np.log(h[2023] / h[2015])
    if nat:
        n_ = Dm[nat[0]].unstack('year'); X['d_foreign_pp'] = (100 - n_[2023]) - (100 - n_[2015])
X = X[X.P15.notna() & X.dlnR.notna()].reset_index().rename(columns={'index': 'cmun'})
X = X.dropna(subset=PRED + ECON).copy()
X.to_parquet(f'{CL}/e01_X.parquet')
CEN = PRED + ECON
res['n'] = len(X); res['n_aeat'] = int(X.G_vr.notna().sum())


def iv(y, d=None, x='x2024', z='Z2024', ctrls=CEN, w='P15', fe='cpro'):
    d = (X if d is None else d).dropna(subset=[y, x, z] + ctrls).copy()
    if w is None:
        d['one'] = 1.0; w = 'one'
    R = Resid(d, [fe] if fe else [], ctrls, w=w)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values); wt = d[w].values.astype(float)
    o = tsls(yr, xr, zr, wt, d.cpro.values, R.rank + 1)
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, R.rank + 1, np.linspace(-6, 6, 2401)); o['n'] = len(d)
    o['ymean'] = wmean(d[y].values, wt)
    return o


# ---------------------------------------------------------------- main table: demand shock on rents, gap, incomes, affordability
OUT = ['dlnR', 'G_vr', 'G_m2', 'G', 'entry', 'd_uc', 'd_pp', 'd_hh', 'AI', 'AE', 'dP2024', 'dlnviv', 'dlnR_pre']
OUT += [c for c in ['d_hhsize', 'd_foreign_pp'] if c in X]
res['main'] = {y: iv(y, x='x2023' if y in ('d_uc', 'd_pp', 'd_hh', 'AI', 'd_hhsize', 'd_foreign_pp', 'dlnR23') else 'x2024',
                     z='Z2023' if y in ('d_uc', 'd_pp', 'd_hh', 'AI', 'd_hhsize', 'd_foreign_pp', 'dlnR23') else 'Z2024') for y in OUT}
Xa = X[X.G_vr.notna()]
res['main_aeat_sample'] = {y: iv(y, d=Xa) for y in ['dlnR', 'entry', 'AE']}
res['main_unw'] = {y: iv(y, w=None) for y in ['dlnR', 'G_vr', 'entry']}

# ---------------------------------------------------------------- supply rigidity: demand x geographic constraint
def iv_inter(y, r, d=None):
    d = (X if d is None else d).dropna(subset=[y, 'x2024', 'Z2024', r] + CEN).copy()
    d['R'] = (d[r] - np.average(d[r], weights=d.P15)) / d[r].std()
    d['xR'] = d.x2024 * d.R; d['ZR'] = d.Z2024 * d.R
    Rs = Resid(d, ['cpro'], CEN + ['R'], w='P15')
    rr = pd.DataFrame({c: Rs(d[c].values) for c in [y, 'x2024', 'xR', 'Z2024', 'ZR']}, index=d.index)
    m = IV2SLS(rr[y], None, rr[['x2024', 'xR']], rr[['Z2024', 'ZR']], weights=d.P15).fit(cov_type='clustered', clusters=d.cpro)
    fs = m.first_stage.diagnostics
    return dict(b_x=float(m.params['x2024']), se_x=float(m.std_errors['x2024']), b_xR=float(m.params['xR']), se_xR=float(m.std_errors['xR']),
                p_xR=float(m.pvalues['xR']), n=int(m.nobs), F_part=[float(v) for v in fs['f.stat'].values],
                cov=float(m.cov.loc['x2024', 'xR']))
res['rigidity'] = {f'{y}|{r}': iv_inter(y, r) for y in ['dlnR', 'G_vr', 'entry', 'dlnviv', 'AE'] for r in ['undev10', 'steep10', 'sea10']}
# split by terciles of undevelopable land (simpler, transparent)
X['undev_t'] = pd.qcut(X.undev10.rank(method='first'), 3, labels=['low', 'mid', 'high'])
res['rigidity_split'] = {f'{y}|{k}': iv(y, d=q) for y in ['dlnR', 'G_vr', 'dlnviv'] for k, q in X.groupby('undev_t', observed=True)}

# ---------------------------------------------------------------- tourism: non-linear exposure and the entry gap (conditional associations)
X['vut_bin'] = pd.cut(X.vut20, [-0.01, 1, 3, 8, 100], labels=['b0_1', 'b1_3', 'b3_8', 'b8p'])
for b in ['b1_3', 'b3_8', 'b8p']:
    X[b] = (X.vut_bin == b).astype(float)
d = X.dropna(subset=['G_vr']).copy()
m = pf.feols('G_vr ~ b1_3 + b3_8 + b8p + ' + ' + '.join(CEN) + ' | cpro', data=d, weights='P15', vcov={'CRV1': 'cpro'})
res['tourism_gap_bins'] = coefs(m, ['b1_3', 'b3_8', 'b8p'])
m = pf.feols('dlnR ~ b1_3 + b3_8 + b8p + ' + ' + '.join(CEN) + ' | cpro', data=X, weights='P15', vcov={'CRV1': 'cpro'})
res['tourism_stock_bins'] = coefs(m, ['b1_3', 'b3_8', 'b8p'])
res['tourism_bin_counts'] = X.vut_bin.value_counts().to_dict()

# ---------------------------------------------------------------- spillovers within functional urban areas (reduced form)
F = X.dropna(subset=['fua']).copy()
core = F[F.city_core == 1].sort_values('P15', ascending=False).drop_duplicates('fua').set_index('fua')
F['Z_core'] = F.fua.map(core.Z2024); F['x_core'] = F.fua.map(core.x2024)
per = F[(F.city_core != 1) & F.Z_core.notna()].copy()
sp = {}
for y in ['dlnR', 'G_vr', 'dP2024', 'x2024', 'dlnviv']:
    q = per.dropna(subset=[y])
    m = pf.feols(f'{y} ~ Z2024 + Z_core + ' + ' + '.join(CEN) + ' | cpro', data=q, weights='P15', vcov={'CRV1': 'fua'})
    sp[y] = coefs(m, ['Z2024', 'Z_core'])
res['spillovers_rf'] = sp; res['spill_n_periphery'] = int(len(per)); res['spill_n_fua'] = int(per.fua.nunique())

# ---------------------------------------------------------------- tenure: price-to-income in 2021 x the 2022-23 rate shock
V = pd.read_parquet(f'{CL}/mivau_vt.parquet')
vt21 = V[V.year == 2021].groupby('cmun').vt.mean()
hhinc = inc['Renta neta media por hogar'].unstack('year')
pti = (vt21 * 80 / hhinc[2021].reindex(vt21.index)).dropna()
res['pti_n'] = int(len(pti)); res['pti_mean'] = float(pti.mean()); res['pti_sd'] = float(pti.std())
Q = M[(M.year >= 2015) & M.lnR.notna() & M.cmun.isin(pti.index)].copy()
Q['P15'] = Q.cmun.map(M[M.year == 2015].set_index('cmun').P)
Q['pti_s'] = (Q.cmun.map(pti) - pti.mean()) / pti.std()
Q = Q.dropna(subset=['P15'] + PRED); Q['py'] = Q.cpro + '_' + Q.year.astype(str)
nm = []
for y in range(2015, 2025):
    if y == 2021:
        continue
    n = f'pti_{y}'; Q[n] = Q.pti_s * (Q.year == y); nm.append(n)
cc = []
for v in ['lnpop11', 'rent11', 'tert11', 'sh65_11', 'coastal']:
    for y in range(2015, 2025):
        n = f'c_{v}_{y}'; Q[n] = Q[v].fillna(0) * (Q.year == y); cc.append(n)
m = pf.feols('lnR ~ ' + ' + '.join(nm + cc) + ' | cmun + py', data=Q, weights='P15', vcov={'CRV1': 'cpro'})
res['tenure_event_ipva'] = coefs(m, nm)
X['pti_s'] = X.cmun.map((pti - pti.mean()) / pti.std())
d = X.dropna(subset=['G_vr', 'pti_s']).copy()
m = pf.feols('G_vr ~ pti_s + ' + ' + '.join(CEN) + ' | cpro', data=d, weights='P15', vcov={'CRV1': 'cpro'})
res['tenure_gap_pti'] = coefs(m, ['pti_s'])

save('e01_main.json', res)
print('n', res['n'], 'aeat', res['n_aeat'])
for k, v in res['main'].items():
    print(f"{k:12s} b={v['b']:+.3f} se={v['se']:.3f} F={v['F']:.1f} AR={[round(a, 2) for a in v['ar'][:2]]} n={v['n']} mean={v['ymean']:.3f}")
for k, v in res['main_aeat_sample'].items():
    print('aeat-sample', k, round(v['b'], 3), round(v['se'], 3), [round(a, 2) for a in v['ar'][:2]])
for k, v in res['rigidity'].items():
    print('rig', k, 'b_x', round(v['b_x'], 3), 'b_xR', round(v['b_xR'], 3), 'se', round(v['se_xR'], 3), 'p', round(v['p_xR'], 3), 'F', [round(f, 1) for f in v['F_part']])
for k, v in res['rigidity_split'].items():
    print('rigsplit', k, round(v['b'], 3), round(v['se'], 3), 'F', round(v['F'], 1), v['n'])
print('tourism gap', {k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res['tourism_gap_bins'].items() if isinstance(v, dict)}, res['tourism_bin_counts'])
print('tourism stock', {k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res['tourism_stock_bins'].items() if isinstance(v, dict)})
print('spill', {y: {k: (round(v['b'], 3), round(v['se'], 3)) for k, v in s.items() if isinstance(v, dict)} for y, s in res['spillovers_rf'].items()}, res['spill_n_periphery'], res['spill_n_fua'])
print('tenure ipva', {k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res['tenure_event_ipva'].items() if isinstance(v, dict)})
print('tenure gap', res['tenure_gap_pti'], res['pti_n'])

# ---------------------------------------------------------------- robustness: rigidity interaction net of tourism x demand; companion-paper instrument
def iv_inter2(y, r, extra):
    d = X.dropna(subset=[y, 'x2024', 'Z2024', r] + CEN).copy()
    d['R'] = (d[r] - np.average(d[r], weights=d.P15)) / d[r].std(); d['T'] = (d.vut20 - np.average(d.vut20, weights=d.P15)) / d.vut20.std()
    d['xR'] = d.x2024 * d.R; d['ZR'] = d.Z2024 * d.R; d['xT'] = d.x2024 * d['T']; d['ZT'] = d.Z2024 * d['T']
    Rs = Resid(d, ['cpro'], CEN + ['R', 'T'], w='P15')
    en = ['x2024', 'xR'] + (['xT'] if extra else []); ins = ['Z2024', 'ZR'] + (['ZT'] if extra else [])
    rr = pd.DataFrame({c: Rs(d[c].values) for c in [y] + en + ins}, index=d.index)
    m = IV2SLS(rr[y], None, rr[en], rr[ins], weights=d.P15).fit(cov_type='clustered', clusters=d.cpro)
    return {k: dict(b=float(m.params[k]), se=float(m.std_errors[k]), p=float(m.pvalues[k])) for k in en}
res['rigidity_net_tourism'] = {f'{y}|{r}': iv_inter2(y, r, True) for y in ['G_vr', 'entry', 'AE'] for r in ['undev10', 'sea10', 'steep10']}
L2 = load('a02_local.json'); B3 = load('b03_aeat_entry_gap.json')
res['companion_instrument'] = dict(stock=L2['rent_inflow_w'], G_vr=B3['iv']['G_vr'], G_m2=B3['iv']['G_m2'], G=B3['iv']['G'])
save('e01_main.json', res)
for k, v in res['rigidity_net_tourism'].items():
    print('rig+T', k, {kk: (round(vv['b'], 3), round(vv['se'], 3), round(vv['p'], 3)) for kk, vv in v.items()})

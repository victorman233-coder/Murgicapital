"""Feasibility and falsification tests for the rent-income divergence hypothesis (redesign of the paper).
T1  National: real stock rents, new-lease rents and household income (ADRH), 2015-2023/24.
T2  Catalonia: entry gap (new-lease rents vs index of all leases) and new-lease rent-to-income, by municipality.
T3  Shift-share demand shock: effect on rents, on income (per person, per household, median per consumption unit),
    and on the rent-to-income gap (beta_aff = beta_rent - beta_income); composition check.
T4  Catalonia: demand shock and new-lease rents / entry gap (long differences).
T5  Demand shock x supply rigidity (two endogenous regressors, instruments Z and Z x rigidity).
T6  Mortgage shock 2022-23 x pre-existing mortgaged-owner share (census 2011): event study on the index of all leases.
T7  Provinces: entry gap (new vs existing index) 2021-2024 and demographic pressure (descriptive)."""
import glob
import numpy as np, pandas as pd
import pyfixest as pf
from linearmodels.iv import IV2SLS
from rd_common import *
from rev_design import Resid, tsls, ar_analytic

res = {}
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
N = pd.read_parquet(f'{CL}/national.parquet')
A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
inc = A.pivot_table(index=['cmun', 'year'], columns='indicator', values='value').reset_index()
inc.columns.name = None
ren = {'Renta neta media por persona': 'inc_pp', 'Renta neta media por hogar': 'inc_hh', 'Mediana de la renta por unidad de consumo': 'inc_med_uc',
       'Renta bruta media por persona': 'ginc_pp', 'Renta bruta media por hogar': 'ginc_hh'}
inc = inc.rename(columns=ren)[['cmun', 'year'] + [v for v in ren.values() if v in inc.rename(columns=ren)]]
res['adrh_indicators'] = list(A.indicator.unique())

# ---------------------------------------------------------------- T1 national
P = M[M.year == 2015].set_index('cmun').P
I15 = inc[inc.year == 2015].set_index('cmun'); I23 = inc[inc.year == 2023].set_index('cmun')
lev = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
pall = lev[(lev.src == 'padron') & (lev.year == 2015) & (lev.cmun != '00000')].set_index('cmun').P
nat = {}
for v in ['inc_pp', 'inc_hh', 'inc_med_uc']:
    ok = I15.index.intersection(I23.index).intersection(pall.index)
    w = pall.reindex(ok).values
    nat[v] = float(np.log(np.average(I23.loc[ok, v], weights=w) / np.average(I15.loc[ok, v], weights=w)))
nat['ipva_2015_2023'] = float(np.log(N.ipva[2023] / N.ipva[2015])); nat['cpi_2015_2023'] = float(np.log(N.cpi[2023] / N.cpi[2015]))
nat['gap_stock_vs_inc_hh'] = nat['ipva_2015_2023'] - nat['inc_hh']; nat['gap_stock_vs_inc_pp'] = nat['ipva_2015_2023'] - nat['inc_pp']
nat['real_inc_hh'] = nat['inc_hh'] - nat['cpi_2015_2023']; nat['real_inc_pp'] = nat['inc_pp'] - nat['cpi_2015_2023']
nat['new_2021_2024'] = float(np.log(N.ipva_new[2024] / N.ipva_new[2021])); nat['existing_2021_2024'] = float(np.log(N.ipva_existing[2024] / N.ipva_existing[2021]))
nat['cpi_2021_2024'] = float(np.log(N.cpi[2024] / N.cpi[2021]))
I21 = inc[inc.year == 2021].set_index('cmun'); ok = I21.index.intersection(I23.index).intersection(pall.index)
nat['inc_hh_2021_2023'] = float(np.log(np.average(I23.loc[ok, 'inc_hh'], weights=pall.reindex(ok)) / np.average(I21.loc[ok, 'inc_hh'], weights=pall.reindex(ok))))
nat['new_2021_2023'] = float(np.log(N.ipva_new[2023] / N.ipva_new[2021])); nat['existing_2021_2023'] = float(np.log(N.ipva_existing[2023] / N.ipva_existing[2021]))
res['T1_national'] = nat

# ---------------------------------------------------------------- T2 Catalonia: entry gap and new-lease rent-to-income
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = L[L['Període'] == 'gener-desembre'].assign(cmun=lambda d: d['Codi territorial'].astype(int).astype(str).str.zfill(5))
nw = La.pivot_table(index='cmun', columns='Any', values='Renda'); cnt = La.pivot_table(index='cmun', columns='Any', values='Habitatges')
ip = M.pivot_table(index='cmun', columns='year', values='R')
hh = inc.pivot_table(index='cmun', columns='year', values='inc_hh')
cat = nw.index.intersection(ip.index).intersection(hh.index)
C = pd.DataFrame({'d_new': np.log(nw.loc[cat, 2023] / nw.loc[cat, 2015]), 'd_stock': np.log(ip.loc[cat, 2023] / ip.loc[cat, 2015]),
                  'd_inc': np.log(hh.loc[cat, 2023] / hh.loc[cat, 2015]),
                  'rti_new15': 12 * nw.loc[cat, 2015] / hh.loc[cat, 2015], 'rti_new23': 12 * nw.loc[cat, 2023] / hh.loc[cat, 2023],
                  'P': P.reindex(cat)}).dropna()
C['gap_entry'] = C.d_new - C.d_stock; C['aff_new'] = C.d_new - C.d_inc; C['aff_stock'] = C.d_stock - C.d_inc
w = C.P.values
res['T2_catalonia'] = dict(n=len(C), d_new=wmean(C.d_new.values, w), d_stock=wmean(C.d_stock.values, w), d_inc_hh=wmean(C.d_inc.values, w),
                           aff_new=wmean(C.aff_new.values, w), aff_stock=wmean(C.aff_stock.values, w), gap_entry=wmean(C.gap_entry.values, w),
                           rti_new15=wmean(C.rti_new15.values, w), rti_new23=wmean(C.rti_new23.values, w),
                           corr_dnew_dinc=float(np.corrcoef(C.d_new, C.d_inc)[0, 1]),
                           share_munis_aff_new_pos=float((C.aff_new > 0).mean()), share_munis_aff_stock_pos=float((C.aff_stock > 0).mean()))
C.to_parquet(f'{CL}/b01_catalonia_ld.parquet')

# ---------------------------------------------------------------- T3 demand shock: rents vs incomes
X = pd.read_parquet(f'{CL}/ld_2015_2024.parquet')
hp = inc.pivot_table(index='cmun', columns='year', values=['inc_pp', 'inc_hh', 'inc_med_uc'])
for v in ['inc_pp', 'inc_hh', 'inc_med_uc']:
    X[f'd_{v}'] = X.cmun.map(np.log(hp[v][2023] / hp[v][2015]))
pr = M.pivot_table(index='cmun', columns='year', values='lnR')
X['dlnR23'] = X.cmun.map(pr[2023] - pr[2015])
cum23 = M[M.in_sample & (M.year >= 2016) & (M.year <= 2023)].groupby('cmun')[['xc', 'Zc']].sum()
X['xc23'] = X.cmun.map(cum23.xc); X['Zc23'] = X.cmun.map(cum23.Zc)
for v in ['inc_pp', 'inc_hh', 'inc_med_uc']:
    X[f'aff_{v}'] = X.dlnR23 - X[f'd_{v}']
CEN = PRED + ECON


def iv(y, x, z, d, ctrls=CEN, w='P15'):
    d = d.dropna(subset=[y, x, z] + ctrls)
    R = Resid(d, ['cpro'], ctrls, w=w)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values); wt = d[w].values.astype(float)
    o = tsls(yr, xr, zr, wt, d.cpro.values, R.rank + 1)
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, R.rank + 1, np.linspace(-4, 4, 1601)); o['n'] = len(d)
    return o


T3 = {}
for y in ['dlnR23', 'd_inc_pp', 'd_inc_hh', 'd_inc_med_uc', 'aff_inc_pp', 'aff_inc_hh', 'aff_inc_med_uc']:
    T3[y] = iv(y, 'xc23', 'Zc23', X)
res['T3_demand_rent_vs_income'] = T3

# ---------------------------------------------------------------- T4 Catalonia: demand shock and new-lease rents
XC = X.merge(C[['d_new', 'gap_entry', 'aff_new']], left_on='cmun', right_index=True, how='inner')
T4 = {}
for y in ['d_new', 'gap_entry', 'aff_new', 'dlnR23']:
    try:
        T4[y] = iv(y, 'xc23', 'Zc23', XC, ctrls=['lnpop11', 'rent11', 'tert11'])
    except Exception as e:
        T4[y] = {'err': str(e)}
res['T4_catalonia_iv'] = T4

# ---------------------------------------------------------------- T5 demand shock x supply rigidity
X['lndens'] = np.log(X.P15 / X.area_km2)
cat_ = pd.read_parquet(f'{WORK}/replication_package/data/clean/catastro_muni.parquet').pivot_table(index='cmun', columns='year', values='viv')
X['constr_13_15'] = X.cmun.map(np.log(cat_[2015] / cat_[2013]))      # pre-period construction rate
T5 = {}
for r in ['lndens', 'vac11', 'constr_13_15']:
    d = X.dropna(subset=['dlnR', 'dlnviv', 'xc', 'Zc', r] + CEN).copy()
    d['R'] = (d[r] - np.average(d[r], weights=d.P15)) / d[r].std()
    d['xR'] = d.xc * d.R; d['ZR'] = d.Zc * d.R
    Rs = Resid(d, ['cpro'], CEN + ['R'], w='P15')                       # FWL: partial out province FE and controls
    rr = pd.DataFrame({c: Rs(d[c].values) for c in ['dlnR', 'dlnviv', 'xc', 'xR', 'Zc', 'ZR']}, index=d.index)
    for y in ['dlnR', 'dlnviv']:
        ok = rr[y].notna() & d[y].notna()
        m = IV2SLS(rr.loc[ok, y], None, rr.loc[ok, ['xc', 'xR']], rr.loc[ok, ['Zc', 'ZR']], weights=d.P15[ok]).fit(cov_type='clustered', clusters=d.cpro[ok])
        T5[f'{y}|{r}'] = dict(b_x=float(m.params['xc']), se_x=float(m.std_errors['xc']), b_xR=float(m.params['xR']), se_xR=float(m.std_errors['xR']),
                              p_xR=float(m.pvalues['xR']), n=int(m.nobs))
res['T5_rigidity'] = T5

# ---------------------------------------------------------------- T6 mortgage exposure x 2022-23 rate shock
fs = []
for f in sorted(glob.glob(f'{WORK}/raw/c2011/C2011_ccaa*_Indicadores.csv')):
    e = pd.read_csv(f, dtype={'cpro': str, 'cmun': str}, usecols=['cpro', 'cmun', 't18_1', 't18_2', 't18_3', 't18_4', 't18_5', 't18_6'])
    fs.append(e)
E = pd.concat(fs); E['cm'] = E.cpro.str.zfill(2) + E.cmun.str.zfill(3)
E = E.groupby('cm')[[f't18_{k}' for k in range(1, 7)]].sum()
mort = (E.t18_2 / E.sum(axis=1)).rename('mort11')
Q = M[(M.year >= 2015) & M.lnR.notna()].copy()
Q['mort11'] = Q.cmun.map(mort); Q['P15'] = Q.cmun.map(P)
Q = Q.dropna(subset=['mort11', 'P15'] + PRED); Q['py'] = Q.cpro + '_' + Q.year.astype(str)
Q['m_s'] = (Q.mort11 - Q.mort11.mean()) / Q.drop_duplicates('cmun').mort11.std()
nm = []
for y in range(2015, 2025):
    if y == 2021:
        continue
    n = f'm_{y}'; Q[n] = Q.m_s * (Q.year == y); nm.append(n)
cc = []
for v in ['lnpop11', 'rent11', 'tert11', 'sh65_11', 'coastal']:
    for y in range(2015, 2025):
        n = f'c_{v}_{y}'; Q[n] = Q[v].fillna(0) * (Q.year == y); cc.append(n)
m = pf.feols('lnR ~ ' + ' + '.join(nm + cc) + ' | cmun + py', data=Q, weights='P15', vcov={'CRV1': 'cpro'})
res['T6_mortgage_event'] = coefs(m, nm); res['T6_mort11_mean'] = float(mort.mean()); res['T6_mort11_sd'] = float(Q.drop_duplicates('cmun').mort11.std())

# ---------------------------------------------------------------- T7 provinces: entry gap 2021-2024
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.typ == 'Índice') & (pa.prov != '00')].pivot_table(index=['prov', 'year'], columns='age', values='val')
g = pa.unstack('year')
G = pd.DataFrame({'gap_entry': np.log(g[('Nuevo contrato', 2024)] / g[('Nuevo contrato', 2021)]) - np.log(g[('Contrato existente', 2024)] / g[('Contrato existente', 2021)])})
pp = lev[(lev.cmun.str.len() == 5) & (lev.cmun != '00000')].assign(prov=lambda d: d.cmun.str[:2])
c21 = pp[(pp.src == 'censo') & (pp.year == 2021)].groupby('prov')[['P', 'FOR']].sum(); c24 = pp[(pp.src == 'censo') & (pp.year == 2024)].groupby('prov')[['P', 'FOR']].sum()
G['dlnP'] = np.log(c24.P / c21.P); G['inflow'] = (c24.FOR - c21.FOR) / c21.P; G['P'] = c21.P
G = G.dropna()
m = pf.feols('gap_entry ~ inflow', data=G.reset_index(), weights='P', vcov='hetero')
res['T7_prov_gap_inflow'] = coefs(m, ['inflow']); res['T7_gap_mean'] = wmean(G.gap_entry.values, G.P.values)
res['T7_gap_range'] = [float(G.gap_entry.min()), float(G.gap_entry.max())]
save('b01_affordability.json', res)
import json
print(json.dumps({k: v for k, v in res.items() if k not in ('T6_mortgage_event',)}, indent=1, default=float)[:6000])
print({k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res['T6_mortgage_event'].items() if isinstance(v, dict)})

# ---------------------------------------------------------------- T8 mortgage exposure x rate shock on Catalan NEW leases (quarterly)
Cq = pd.read_parquet(f'{CL}/cat_q.parquet'); Cq = Cq[Cq.year <= 2025].copy()
b19 = Cq[Cq.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
Cq = Cq[Cq.cmun.isin(b19[(b19['count'] == 4) & (b19['sum'] >= 40)].index)].copy()
Cq['mort11'] = Cq.cmun.map(mort); Cq = Cq.dropna(subset=['mort11']).copy()
Cq['m_s'] = (Cq.mort11 - Cq.drop_duplicates('cmun').mort11.mean()) / Cq.drop_duplicates('cmun').mort11.std()
Cq['E'] = Cq.vutpct_2020M08.fillna(0); Cq['lnn'] = np.log(Cq.n); Cq['lnrent'] = np.log(Cq.rent)
Cq['t'] = (Cq.year - 2019) * 4 + Cq.q - 1
Cq['P19'] = Cq.cmun.map(Cq[Cq.year == 2019].groupby('cmun').P.first())
ctr = []
for k in (2, 3, 4):
    Cq[f'Eq{k}'] = Cq.E * (Cq.q == k); ctr.append(f'Eq{k}')
Cq['E_cov'] = Cq.E * Cq.t.between(5, 9); Cq['E_rec'] = Cq.E * Cq.t.between(12, 19); ctr += ['E_cov', 'E_rec']
Cq['cap1'] = ((Cq.zmrt == 1) & (Cq.t >= 21)).astype(float); Cq['cap2'] = ((Cq.zmrt == 2) & (Cq.t >= 23)).astype(float); ctr += ['cap1', 'cap2']
Cq['m_post'] = Cq.m_s * (Cq.t >= 14)          # 2022Q3 onwards: Euribor rises above 1%
Cq['m_mid'] = Cq.m_s * Cq.t.between(10, 13)   # 2021Q3-2022Q2: placebo window before the rise
T8 = {}
for y in ['lnrent', 'lnn']:
    m = pf.feols(f'{y} ~ m_mid + m_post + ' + ' + '.join(ctr) + ' | cmun + t', data=Cq, weights='P19', vcov={'CRV1': 'cmun'})
    T8[y] = coefs(m, ['m_mid', 'm_post'])
res['T8_mortgage_newleases_cat'] = T8; res['T8_n_munis'] = int(Cq.cmun.nunique())
save('b01_affordability.json', res)
print('T8', T8)

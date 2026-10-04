"""Tourist dwellings and long-term rents (P2): the 2020-21 collapse of tourism as a reversal of tourist demand.
(a) Spain, IPVA municipalities, annual 2012-2024: event study on the INE share of dwellings in tourist use (Aug 2020).
(b) Catalonia, new leases by quarter 2019Q1-2025Q4: event study of new-lease counts and rents on the same exposure,
    with the tourist-stay tax paid by tourist dwellings (IEET) as the measure of the collapse in tourist activity.
(c) Spain, 2020-2024/26: growth of tourist dwellings and rent growth (descriptive)."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *

res = {}
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
st = M.drop_duplicates('cmun').set_index('cmun')
# ---------------------------------------------------------------- (a) annual event study, IPVA (stock of leases)
A = M[(M.year >= 2012) & M.lnR.notna()].copy()
A['P15'] = A.cmun.map(M[M.year == 2015].set_index('cmun').P)
A = A.dropna(subset=['P15', 'vutpct_2020M08'] + PRED)
A['E'] = A.vutpct_2020M08                                 # % of dwellings in tourist use, Aug 2020
A['py'] = A.cpro + '_' + A.year.astype(str)
names = []
for y in range(2012, 2025):
    if y == 2019:
        continue
    n = f'E_{y}'; A[n] = A.E * (A.year == y); names.append(n)
ctr = []
for v in ['lnpop11', 'rent11', 'tert11', 'sh65_11', 'coastal']:
    for y in range(2012, 2025):
        n = f'c_{v}_{y}'; A[n] = A[v].fillna(0) * (A.year == y); ctr.append(n)
m = pf.feols('lnR ~ ' + ' + '.join(names + ctr) + ' | cmun + py', data=A, weights='P15', vcov={'CRV1': 'cpro'})
res['ipva_event'] = coefs(m, names)
res['ipva_event_sdE'] = float(A.drop_duplicates('cmun').E.std())
res['ipva_event_meanE'] = float(A.drop_duplicates('cmun').E.mean())

# ---------------------------------------------------------------- (b) Catalonia, new leases by quarter
C = pd.read_parquet(f'{CL}/cat_q.parquet')
C = C[(C.year <= 2025)].copy()
C['E'] = C.vutpct_2020M08
C = C.dropna(subset=['E', 'P']).copy()
# balanced set of municipalities with leases in every quarter of 2019 (stable denominators)
base = C[C.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
keep = base[(base['count'] == 4) & (base['sum'] >= 40)].index
C = C[C.cmun.isin(keep)].copy()
C['lnn'] = np.log(C.n); C['lnrent'] = np.log(C.rent)
C['P19'] = C.cmun.map(C[C.year == 2019].groupby('cmun').P.first())
C['qq'] = C.year.astype(str) + 'Q' + C.q.astype(str)
qs = sorted(C.qq.unique()); ref = ['2019Q1', '2019Q2', '2019Q3', '2019Q4']   # reference year 2019 (one per calendar quarter)
nm = []
for q in qs:
    if q in ref:
        continue
    n = 'E_' + q.replace('Q', 'q'); C[n] = C.E * (C.qq == q); nm.append(n)
cc = []
for k in (2, 3, 4):                                        # exposure-specific seasonal profile (tourist season)
    n = f'Eq{k}'; C[n] = C.E * (C.q == k); cc.append(n)
for v in ['lnP19']:
    C['lnP19'] = np.log(C.P19)
    for q in qs:
        n = f'c_{v}_' + q.replace('Q', 'q'); C[n] = C[v] * (C.qq == q); cc.append(n)
for y in ['lnn', 'lnrent']:
    m = pf.feols(f'{y} ~ ' + ' + '.join(nm + cc) + ' | cmun + qq', data=C, weights='P19', vcov={'CRV1': 'cmun'})
    res[f'cat_event_{y}'] = coefs(m, nm)
res['cat_n_munis'] = int(C.cmun.nunique()); res['cat_sdE'] = float(C.drop_duplicates('cmun').E.std())
res['cat_meanE'] = float(C.drop_duplicates('cmun').E.mean())
# pooled: COVID window (2020Q2-2021Q2) and recovery (2022Q1-2023Q4) relative to 2019Q1-2020Q1
C['covid'] = C.qq.isin([f'2020Q{k}' for k in (2, 3, 4)] + ['2021Q1', '2021Q2']).astype(float)
C['q120'] = (C.qq == '2020Q1').astype(float)
C['recov'] = C.qq.isin([f'{y}Q{k}' for y in (2022, 2023) for k in (1, 2, 3, 4)]).astype(float)
C['late'] = C.qq.isin([f'{y}Q{k}' for y in (2024, 2025) for k in (1, 2, 3, 4)]).astype(float)
for v in ['q120', 'covid', 'recov', 'late']:
    C[f'E_{v}'] = C.E * C[v]
for y in ['lnn', 'lnrent']:
    m = pf.feols(f'{y} ~ E_q120 + E_covid + E_recov + E_late + ' + ' + '.join(cc) + ' | cmun + qq', data=C, weights='P19', vcov={'CRV1': 'cmun'})
    res[f'cat_pooled_{y}'] = coefs(m, ['E_q120', 'E_covid', 'E_recov', 'E_late'])
# first stage: tourist-stay tax paid by tourist dwellings, 2019 -> 2020 and 2021, by exposure
IE = pd.read_parquet(f'{CL}/ieet_ht.parquet')
cols = [c for c in IE.columns]
yr = lambda y: [c for c in cols if c.startswith(f'ht_{str(y)[2:]}S')]
ht = pd.DataFrame({y: IE[yr(y)].sum(axis=1, min_count=1) for y in range(2017, 2026) if yr(y)})
F1 = ht.join(st[['vutpct_2020M08', 'P']], how='inner').dropna(subset=[2019, 'vutpct_2020M08'])
F1 = F1[F1[2019] > 0]
for y in [2020, 2021, 2022, 2023, 2024]:
    if y in F1:
        F1[f'r{y}'] = np.log(F1[y].clip(lower=1) / F1[2019])
res['ieet_total'] = {int(y): float(ht[y].sum()) for y in ht.columns}
res['ieet_ratio_2020_2019'] = float(ht[2020].sum() / ht[2019].sum()) if 2020 in ht else None
res['ieet_ratio_2021_2019'] = float(ht[2021].sum() / ht[2019].sum()) if 2021 in ht else None
res['ieet_munis'] = int(len(F1))

# ---------------------------------------------------------------- (c) Spain: growth of tourist dwellings 2020-2024 and rents (descriptive)
V = pd.read_parquet(f'{CL}/vut_muni.parquet')
X = pd.read_parquet(f'{CL}/ld_2015_2024.parquet').set_index('cmun')
pvR = M.pivot_table(index='cmun', columns='year', values='lnR')
X['dlnR_2024_2020'] = pvR[2024] - pvR[2020]
X['dvut'] = (V['vutpct_2024M08'] - V['vutpct_2020M08']).reindex(X.index)
X['vut24'] = V['vutpct_2024M08'].reindex(X.index)
Xs = X.dropna(subset=['dlnR_2024_2020', 'dvut']).reset_index()
m = pf.feols('dlnR_2024_2020 ~ dvut + vut20 + ' + ' + '.join(PRED + ECON) + ' | cpro', data=Xs, weights='P15', vcov={'CRV1': 'cpro'})
res['ld_2020_2024_vut'] = coefs(m, ['dvut', 'vut20'])
# national totals
res['vut_national'] = {p: float(V[f'vut_{p}'].sum()) for p in ['2020M08', '2024M08', '2026M05'] if f'vut_{p}' in V}
res['vutpct_quantiles_2020'] = {str(q): float(V['vutpct_2020M08'].quantile(q)) for q in (.5, .9, .99)}
save('a03_tourism.json', res)
for k in ['ipva_event', 'cat_event_lnn', 'cat_event_lnrent']:
    print(k, {kk: (round(v['b'], 4), round(v['se'], 4)) for kk, v in res[k].items() if isinstance(v, dict)})
for k in ['cat_pooled_lnn', 'cat_pooled_lnrent', 'ld_2020_2024_vut']:
    print(k, res[k])
print({k: res[k] for k in ['ipva_event_sdE', 'ipva_event_meanE', 'cat_n_munis', 'cat_sdE', 'cat_meanE', 'ieet_ratio_2020_2019', 'ieet_ratio_2021_2019', 'ieet_munis', 'vut_national']})

"""Regulation (P3 and the index identity).
(a) Catalan cap on new-contract rents in tensioned residential markets (Ley 12/2023): 140 municipalities from 16 March 2024
    (ZMRT 1, first full quarter 2024Q2) and 131 from October 2024 (ZMRT 2, first full quarter 2024Q4). Stacked event studies
    on new-lease rents and counts with clean controls: ZMRT 1 vs not-yet-treated (ZMRT 2) and never-treated up to 2024Q3;
    ZMRT 2 vs never-treated up to 2025Q4; ZMRT 1 vs never-treated up to 2025Q4 (less comparable controls).
(b) Provinces: INE IPVA for new contracts, Catalan provinces vs the rest, 2021-2024.
(c) The 2022-2023 cap on annual updates of existing leases: counterfactual stock index if existing leases had followed the CPI."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *

res = {}
C = pd.read_parquet(f'{CL}/cat_q.parquet')
C = C[C.year <= 2025].copy()
base = C[C.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
C = C[C.cmun.isin(base[(base['count'] == 4) & (base['sum'] >= 40)].index)].copy()
C['lnn'] = np.log(C.n); C['lnrent'] = np.log(C.rent)
C['E'] = C.vutpct_2020M08.fillna(0)
C['P19'] = C.cmun.map(C[C.year == 2019].groupby('cmun').P.first())
C['t'] = (C.year - 2019) * 4 + C.q - 1                     # 0 = 2019Q1
for k in (2, 3, 4):
    C[f'Eq{k}'] = C.E * (C.q == k)
C['covid'] = ((C.t >= 5) & (C.t <= 9)).astype(float); C['recov'] = ((C.t >= 12) & (C.t <= 19)).astype(float)
C['E_covid'] = C.E * C.covid; C['E_recov'] = C.E * C.recov
CTRL = ['Eq2', 'Eq3', 'Eq4', 'E_covid', 'E_recov']
T1, T2 = (2024 - 2019) * 4 + 1, (2024 - 2019) * 4 + 3          # 2024Q2, 2024Q4


def stack(treat, controls, g, tmax, label, weight=None):
    d = C[(C.zmrt.isin([treat] + controls)) & (C.t <= tmax)].copy()
    d['D'] = (d.zmrt == treat).astype(float)
    d['rel'] = np.where(d.D == 1, d.t - g, -99)
    names = []
    for k in sorted(set(d.loc[d.D == 1, 'rel'])):
        if k == -1 or k < -12:
            continue
        n = f'r_m{-k}' if k < 0 else f'r_p{k}'; d[n] = ((d.rel == k)).astype(float); names.append(n)
    d['post'] = ((d.D == 1) & (d.rel >= 0)).astype(float)
    out = {}
    for y in ['lnrent', 'lnn']:
        kw = dict(data=d, vcov={'CRV1': 'cmun'})
        if weight:
            kw['weights'] = weight
        early = [n for n in names if n.startswith('r_m')]
        # pre-period dummies beyond 12 quarters are pooled into the reference to keep the window balanced
        m = pf.feols(f'{y} ~ ' + ' + '.join(names) + ' + ' + ' + '.join(CTRL) + ' | cmun + t', **kw)
        es = coefs(m, names)
        pre = [n for n in early]
        try:
            wt = m.wald_test(R=np.eye(len(m._coefnames))[[m._coefnames.index(n) for n in pre]])
            es['pretest_p'] = float(wt['pvalue']) if isinstance(wt, dict) else float(wt.iloc[-1] if hasattr(wt, 'iloc') else wt)
        except Exception as e:
            es['pretest_p'] = None
        m2 = pf.feols(f'{y} ~ post + ' + ' + '.join(CTRL) + ' | cmun + t', **kw)
        # robustness: remove a treated-group linear trend estimated on pre-treatment quarters only
        pre_d = d[d.t < g].copy(); pre_d['Dt'] = pre_d.D * pre_d.t
        kwp = dict(kw); kwp['data'] = pre_d
        mt = pf.feols(f'{y} ~ Dt + ' + ' + '.join(CTRL) + ' | cmun + t', **kwp)
        slope = float(mt.coef()['Dt'])
        dd = d.copy(); dd[y] = dd[y] - slope * dd.D * dd.t
        kwd = dict(kw); kwd['data'] = dd
        m3 = pf.feols(f'{y} ~ post + ' + ' + '.join(CTRL) + ' | cmun + t', **kwd)
        out[y] = dict(event=es, pooled=coefs(m2, ['post']), detrended=coefs(m3, ['post']), pre_slope=slope)
    out['n_treat'] = int(d[d.D == 1].cmun.nunique()); out['n_ctrl'] = int(d[d.D == 0].cmun.nunique())
    out['tmax'] = int(tmax); out['g'] = int(g)
    res[label] = out


stack(1, [0, 2], T1, T2 - 1, 'zmrt1_vs_notyet')
stack(2, [0], T2, 27, 'zmrt2_vs_never')
stack(1, [0], T1, 27, 'zmrt1_vs_never')
stack(1, [0, 2], T1, T2 - 1, 'zmrt1_vs_notyet_w', weight='P19')
stack(2, [0], T2, 27, 'zmrt2_vs_never_w', weight='P19')
# aggregate counts of new leases in Catalonia, same quarter of the year
agg = C.groupby(['year', 'q']).n.sum().unstack()
res['cat_leases_by_year_q'] = {int(y): {int(q): float(v) for q, v in r.items()} for y, r in agg.iterrows()}

# ---------------------------------------------------------------- (b) provincial IPVA for new contracts
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.typ == 'Índice') & (pa.prov != '00')].pivot_table(index=['prov', 'year'], columns='age', values='val').reset_index()
pa.columns = ['prov', 'year', 'existing', 'new', 'total']
pa = pa.sort_values(['prov', 'year'])
for c in ['existing', 'new', 'total']:
    pa[f'g_{c}'] = pa.groupby('prov')[c].transform(lambda s: np.log(s).diff())
pa['cat'] = pa.prov.isin(['08', '17', '25', '43']).astype(float)
pa['cat24'] = pa.cat * (pa.year == 2024)
d = pa[pa.year >= 2022].dropna(subset=['g_new'])
for c in ['new', 'existing', 'total']:
    m = pf.feols(f'g_{c} ~ cat24 | prov + year', data=d, vcov={'CRV1': 'prov'})
    res[f'prov_new_contracts_{c}'] = coefs(m, ['cat24'])
res['prov_g_new_2024'] = {p: float(v) for p, v in d[d.year == 2024].set_index('prov').g_new.items()}

# ---------------------------------------------------------------- (c) the 2022-2023 cap on updates of existing leases
N = pd.read_parquet(f'{CL}/national.parquet')
cf = {}
lvl_act, lvl_cf = 1.0, 1.0
for y in [2022, 2023]:
    wn = N.w_new[y]; gn = N.ipva_new[y] / N.ipva_new[y - 1] - 1; ge = N.ipva_existing[y] / N.ipva_existing[y - 1] - 1
    cpi = N.cpi[y] / N.cpi[y - 1] - 1
    # December-to-December CPI is what most leases use; annual average CPI is used here as a conservative proxy
    lvl_act *= 1 + wn * gn + (1 - wn) * ge; lvl_cf *= 1 + wn * gn + (1 - wn) * cpi
    cf[y] = dict(existing=ge, cpi=cpi, w_new=wn, gap_pp=100 * (1 - wn) * (cpi - ge))
res['update_cap'] = dict(by_year=cf, cumulative_gap=lvl_cf / lvl_act - 1)
save('a04_regulation.json', res)
for k in ['zmrt1_vs_notyet', 'zmrt2_vs_never', 'zmrt1_vs_never', 'zmrt1_vs_notyet_w', 'zmrt2_vs_never_w']:
    r = res[k]
    print(k, 'treat', r['n_treat'], 'ctrl', r['n_ctrl'],
          {y: (round(r[y]['pooled']['post']['b'], 4), round(r[y]['pooled']['post']['se'], 4), r[y]['event'].get('pretest_p'),
               'detr', round(r[y]['detrended']['post']['b'], 4), round(r[y]['detrended']['post']['se'], 4)) for y in ['lnrent', 'lnn']})
print({k: res[k] for k in ['prov_new_contracts_new', 'prov_new_contracts_existing', 'update_cap']})

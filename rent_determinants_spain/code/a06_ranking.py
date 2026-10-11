"""Ranking of determinants.
A. National stock index 2015-2024: inflation (accounting), the 2022-23 update cap (accounting), and the identified local channels
   aggregated under explicit assumptions (no spillovers across municipalities, national = local elasticity).
B. Within-province cross-municipal differences in rent growth 2015-2024: covariance shares of each local factor.
C. New leases in Catalonia 2019-2025: tourism reversal and the tensioned-zone cap.
D. By municipality size: exposure to each channel times the common elasticity."""
import numpy as np, pandas as pd
from rd_common import *
from rev_design import Resid

F = load('a01_facts.json'); L2 = load('a02_local.json'); T = load('a03_tourism.json'); R = load('a04_regulation.json'); I = load('a05_investors_credit.json')
X = pd.read_parquet(f'{CL}/ld_2015_2024.parquet')
N = pd.read_parquet(f'{CL}/national.parquet')
res = {}
w = X.P15.values
Mx = wmean(X.xc.values, w); MP = wmean(X.dlnP.values, w)
bN = L2['rent_inflow_w']; bP = L2['rent_dlnP_w']
E = X.vut20.values; Em = wmean(E, w)
ev = T['ipva_event']
b15_19 = 0 - ev['E_2015']['b']; b19_24 = ev['E_2024']['b'] - 0; b15_24 = ev['E_2024']['b'] - ev['E_2015']['b']
A = dict(total=float(np.log(N.ipva[2024] / N.ipva[2015])), cpi=float(np.log(N.cpi[2024] / N.cpi[2015])))
A['real'] = A['total'] - A['cpi']
A['population'] = dict(b=bN['b'], ar=bN['ar'], M=Mx, contrib=bN['b'] * Mx, lo=bN['ar'][0] * Mx, hi=bN['ar'][1] * Mx)
A['population_total'] = dict(b=bP['b'], ar=bP['ar'], M=MP, contrib=bP['b'] * MP, lo=bP['ar'][0] * MP, hi=bP['ar'][1] * MP)
A['tourism'] = dict(mean_exposure=Em, per_pp_2015_2019=b15_19, per_pp_2019_2024=b19_24, per_pp_2015_2024=b15_24,
                    contrib_2015_2019=b15_19 * Em, contrib_2019_2024=b19_24 * Em, contrib_2015_2024=b15_24 * Em)
A['supply'] = dict(b_viv_inflow=L2['viv_inflow_w']['b'], ar=L2['viv_inflow_w']['ar'], dlnviv_mean=wmean(X.dlnviv.values, w))
A['update_cap'] = dict(contrib=-float(np.log(1 + R['update_cap']['cumulative_gap'])))
if 'dlninc' in X:
    oi = L2.get('ols_horse_race', {}).get('dlninc_s')
    sd = L2.get('ols_sd', {}).get('dlninc')
    if oi and sd:
        real = wmean(X.dlninc.values, w) - float(np.log(N.cpi[2023] / N.cpi[2015]))      # real income growth 2015-2023
        A['income_ols'] = dict(b_per_sd=oi['b'], se=oi['se'], sd=sd, elasticity=oi['b'] / sd, mean_nominal=wmean(X.dlninc.values, w), mean_real=real,
                               contrib=oi['b'] / sd * real, lo=oi['lo'] / sd * real, hi=oi['hi'] / sd * real)
res['A_national_stock'] = A

# ---------------------------------------------------------------- B. within-province covariance shares
Rs = Resid(X, ['cpro'], [], w='P15')
y = Rs(X.dlnR.values)
comps = {'population (2SLS)': bN['b'] * Rs(X.xc.values)}
pre = PRED + ECON
o = L2['ols_horse_race']
for c in ['vut20', 'dlnviv'] + (['dlninc'] if 'dlninc' in X else []):
    if c + '_s' in o:
        comps[{'vut20': 'tourist dwellings 2020 (OLS)', 'dlnviv': 'dwelling stock growth (OLS)', 'dlninc': 'income growth (OLS)'}[c]] = \
            o[c + '_s']['b'] / L2['ols_sd'][c] * Rs(X[c].fillna(X[c].mean()).values)
vy = np.average(y ** 2, weights=w)
B = {k: float(np.average(v * y, weights=w) / vy) for k, v in comps.items()}
B['province (between)'] = F['variance_share_ld_province']
res['B_within_province_shares'] = B
res['B_note'] = 'shares of the within-province variance of 2015-2024 log rent growth; province share is of total variance'

# ---------------------------------------------------------------- C. new leases in Catalonia
C = pd.read_parquet(f'{CL}/cat_q.parquet')
c19 = C[C.year == 2019].groupby('cmun').apply(lambda q: np.average(q.rent, weights=q.n), include_groups=False)
c25 = C[C.year == 2025].groupby('cmun').apply(lambda q: np.average(q.rent, weights=q.n), include_groups=False)
P19 = C[C.year == 2019].groupby('cmun').P.first()
ok = c19.index.intersection(c25.index)
g = np.log(c25[ok] / c19[ok])
Ec = C.drop_duplicates('cmun').set_index('cmun').vutpct_2020M08.reindex(ok).fillna(0)
zm = C.drop_duplicates('cmun').set_index('cmun').zmrt.reindex(ok)
pc = T['cat_pooled_lnrent']
res['C_catalonia_new'] = dict(growth_2019_2025=wmean(g.values, P19[ok].values), mean_exposure=wmean(Ec.values, P19[ok].values),
                              tourism_covid_per_pp=pc['E_covid']['b'], tourism_recovery_per_pp=pc['E_recov']['b'], tourism_late_per_pp=pc['E_late']['b'],
                              tourism_late_contrib=pc['E_late']['b'] * wmean(Ec.values, P19[ok].values),
                              cap_wave1=R['zmrt1_vs_never']['lnrent']['pooled']['post']['b'], cap_wave1_se=R['zmrt1_vs_never']['lnrent']['pooled']['post']['se'],
                              cap_share_pop=float(P19[ok][zm > 0].sum() / P19[ok].sum()))

# ---------------------------------------------------------------- D. by municipality size
D = {}
for k, q in X.groupby('size'):
    wq = q.P15.values
    D[k] = dict(n=len(q), dlnR=wmean(q.dlnR.values, wq), inflow=wmean(q.xc.values, wq), dlnP=wmean(q.dlnP.values, wq),
                pop_contrib=bN['b'] * wmean(q.xc.values, wq), vut20=wmean(q.vut20.values, wq),
                tour_contrib_15_19=b15_19 * wmean(q.vut20.values, wq), vut20_p90=float(q.vut20.quantile(.9)),
                dlnviv=wmean(q.dlnviv.values, wq) if q.dlnviv.notna().any() else None, zmrt_share=float((q.cat_zmrt1 > 0).mean()))
res['D_by_size'] = D
save('a06_ranking.json', res)
import json; print(json.dumps(res, indent=1, default=float))

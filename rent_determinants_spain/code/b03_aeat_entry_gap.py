"""Entry-rent gap in 2024 from AEAT tax statistics (dwellings declared in IRPF, new contracts vs all leases),
municipalities above 20,000 inhabitants, and its relation to cumulative demand shocks (shift-share IV), tourism,
the Catalan cap and rigidity proxies. Quality adjustment: rent per m2 and rent per euro of cadastral reference value."""
import io, re
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *
from rev_design import Resid, tsls, ar_analytic

html = open(f'{RAW}/aeat/aeat_newcontracts_muni_2024.html', encoding='utf-8', errors='replace').read()
t = pd.read_html(io.StringIO(html), decimal=',', thousands='.')[0]
t.columns = ['loc', 'rent', 'rent_new', 'm2', 'm2_new', 'vr', 'vr_new', 'yld', 'yld_new']
t['cmun'] = t['loc'].str.extract(r'-(\d{5})\s*$')[0]
A = t.dropna(subset=['cmun']).copy()
for c in ['rent', 'rent_new', 'm2', 'm2_new', 'vr', 'vr_new', 'yld', 'yld_new']:
    A[c] = pd.to_numeric(A[c], errors='coerce')
A['G'] = np.log(A.rent_new / A.rent)                                         # raw entry gap
A['G_m2'] = np.log((A.rent_new / A.m2_new) / (A.rent / A.m2))                # per m2
A['G_vr'] = np.log((A.rent_new / A.vr_new) / (A.rent / A.vr))                # per euro of reference value (quality-adjusted)
A.to_parquet(f'{CL}/aeat_entry_gap_2024.parquet')
res = {'n_munis': int(len(A)), 'national': t.iloc[0][['rent', 'rent_new', 'm2', 'm2_new', 'vr', 'vr_new', 'yld', 'yld_new']].astype(float).to_dict()}
X = pd.read_parquet(f'{CL}/ld_2015_2024.parquet').merge(A[['cmun', 'G', 'G_m2', 'G_vr', 'rent', 'rent_new']], on='cmun', how='inner')
X['lndens'] = np.log(X.P15 / X.area_km2)
w = X.P15.values
res['desc'] = {v: dict(mean_w=wmean(X[v].values, w), p10=float(X[v].quantile(.1)), p50=float(X[v].median()), p90=float(X[v].quantile(.9)),
                      share_pos=float((X[v] > 0).mean())) for v in ['G', 'G_m2', 'G_vr']}
res['n_merged'] = int(len(X))
CEN = PRED + ECON


def iv(y, d, x='xc', z='Zc', ctrls=CEN, w='P15'):
    d = d.dropna(subset=[y, x, z] + ctrls)
    R = Resid(d, ['cpro'], ctrls, w=w)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values); wt = d[w].values.astype(float)
    o = tsls(yr, xr, zr, wt, d.cpro.values, R.rank + 1)
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, R.rank + 1, np.linspace(-4, 4, 1601)); o['n'] = len(d)
    return o


res['iv'] = {y: iv(y, X) for y in ['G', 'G_m2', 'G_vr', 'dlnR']}
res['iv_unw'] = {y: iv(y, X.assign(one=1.0), w='one') for y in ['G_m2', 'G_vr']}
# descriptive correlates within province: tourism exposure, Catalan cap (ZMRT wave 1), density
X['zm1'] = X.cat_zmrt1.fillna(0)
m = pf.feols('G_vr ~ vut20 + zm1 + lndens + ' + ' + '.join(CEN) + ' | cpro', data=X, weights='P15', vcov={'CRV1': 'cpro'})
res['ols_correlates_Gvr'] = coefs(m, ['vut20', 'zm1', 'lndens'])
m = pf.feols('G_vr ~ zm1 + vut20 + lndens + ' + ' + '.join([c for c in CEN]) , data=X[X.cpro.isin(['08', '17', '25', '43'])], weights='P15', vcov='hetero')
res['cat_zmrt_Gvr'] = coefs(m, ['zm1'])
save('b03_aeat_entry_gap.json', res)
import json
print(json.dumps({k: res[k] for k in ['n_munis', 'n_merged', 'national', 'desc']}, indent=0, default=float))
for k, v in res['iv'].items():
    print('IV', k, round(v['b'], 3), round(v['se'], 3), 'F', round(v['F'], 1), v['ar'], v['n'])
for k, v in res['iv_unw'].items():
    print('IVunw', k, round(v['b'], 3), round(v['se'], 3), 'F', round(v['F'], 1), v['ar'])
print(res['ols_correlates_Gvr']); print(res['cat_zmrt_Gvr'])

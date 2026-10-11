"""Pre-specified heterogeneity (H1 supply slack/density, H2 rental depth, H3 effective rental-demand shock)
with Benjamini-Hochberg q-values; and validation of the stock index against new-contract rents in Catalonia
(Incasòl deposit register). Output: out/r17_het.json, out/r18_catalonia.json"""
import numpy as np, pandas as pd, pyfixest as pf
from rev_common import *
from rev_design import *

d = load_revision_panel()
grid = np.round(np.arange(-3, 5.0001, 0.01), 3)
CEN = PRED + ECON
d['dens11'] = np.log(d.pop11 / d.area_km2)
res = {}
# ------------------------------------------------------------------ H1/H2: interactions with predetermined characteristics
def interact(dd, hvar, w='w'):
    dd = dd.dropna(subset=[hvar] + CEN).copy().reset_index(drop=True)
    dd['h'] = (dd[hvar] - np.average(dd[hvar], weights=dd['w'] if w else None)) / dd[hvar].std()
    dd['xh'] = dd.xc * dd.h; dd['zh'] = dd.Zc * dd.h
    c = year_ctrls(dd, ['forsh_base', 'h'] + CEN)
    r = iv_multi(dd, 'dlnR', ['xc', 'xh'], ['Zc', 'zh'], c, w)
    t = r['xh']['b'] / r['xh']['se']
    from scipy import stats
    r['p_inter'] = float(2 * (1 - stats.norm.cdf(abs(t))))
    return r
fam = {}
for hvar, lab in [('vac11', 'H1a vacancy 2011'), ('dens11', 'H1b log density 2011'), ('rent11', 'H2 renting share 2011')]:
    for w in ['w', None]:
        r = interact(d, hvar, w); fam[f'{lab}|{w or "unw"}'] = r
        print(lab, w, r['xc'], r['xh'], r['p_inter'])
# ------------------------------------------------------------------ H3: effective rental-demand shock (kappa x renting propensity by continent, census 2011)
kap = {'Europa': 1.0979, 'Africa': 0.6372, 'America': 0.9597, 'Asia': 0.6811, 'Otros': 1.0}
rentp = json.load(open(f'{REP}/out/kappa.json'))
S, Gl, Gn = obs_matrices(d)
# renting propensity by region from the author's kappa.json if available, else 1
rp = {}
try:
    kr = rentp['rent_region'] if 'rent_region' in rentp else None
except Exception:
    kr = None
REGMAP = {'Europa': 'born_eu', 'Africa': 'born_afr', 'America': 'born_lat', 'Asia': 'born_asia', 'Otros': 'born_oce'}
print(list(rentp.keys()))
wts = np.array([kap[REGION[o]] for o in GROUPS])
d['ZR'] = (S * Gl * wts[None, :]).sum(axis=1)
for w in ['w', None]:
    dd = d.dropna(subset=CEN).reset_index(drop=True)
    c = year_ctrls(dd, ['forsh_base'] + CEN)
    m = pf.feols(f'dlnR ~ Zc + ZR + {" + ".join(c)} | cy', data=dd, vcov={'CRV1': 'cpro'}, weights=w)
    fam[f'H3 effective-demand horse race (reduced form)|{w or "unw"}'] = {'Zc': coef(m, 'Zc'), 'ZR': coef(m, 'ZR'), 'p_inter': coef(m, 'ZR')['p']}
    print('H3', w, coef(m, 'Zc'), coef(m, 'ZR'))
# BH q-values over the family
ps = pd.Series({k: v['p_inter'] for k, v in fam.items()}).sort_values()
m_ = len(ps); q = (ps * m_ / np.arange(1, m_ + 1)).iloc[::-1].cummin().iloc[::-1].clip(upper=1)
for k in fam:
    fam[k]['q_BH'] = float(q[k])
res['heterogeneity'] = fam
save('r17_het.json', res)
print(q.round(3).to_string())

# ------------------------------------------------------------------ Catalonia: new-contract rents (Incasòl) vs IPVA stock index
F = pd.read_csv(f'{WORK}/raw/cat/lloguer_municipi.csv')
F = F[F['Període'] == 'gener-desembre'].copy()
F['cmun'] = F['Codi territorial'].astype(int).astype(str).str.zfill(5)
F = F.rename(columns={'Any': 'year', 'Habitatges': 'ncontracts', 'Renda': 'rent_new'})[['cmun', 'year', 'ncontracts', 'rent_new']]
F = F.sort_values(['cmun', 'year'])
F['ln_new'] = np.log(F.rent_new)
F['dln_new'] = F.groupby('cmun').ln_new.diff()
c = d[d.cpro.isin(['08', '17', '25', '43'])].merge(F, on=['cmun', 'year'], how='inner')
c['turnover'] = c.ncontracts / c.renters11
c['ln_contracts_pc'] = np.log(c.ncontracts / c.pop11)
c = c.sort_values(['cmun', 'year']); c['dln_contracts'] = c.groupby('cmun').ln_contracts_pc.diff()
cat = {'n_munis': int(c.cmun.nunique()), 'years': [int(c.year.min()), int(c.year.max())],
       'turnover_median': float(c.turnover.median()), 'turnover_mean_w': float(np.average(c.turnover.dropna(), weights=c.loc[c.turnover.notna(), 'w']))}
cc = c.dropna(subset=['dln_new', 'dlnR', 'xc', 'Zc'] + CEN).reset_index(drop=True)
cc = cc[cc.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
cat['corr_dln_new_dlnR'] = float(cc[['dln_new', 'dlnR']].corr().iloc[0, 1])
for spec, cv in [('author', ['lninc15', 'lnpop11', 'rent11', 'vac11']), ('central', CEN)]:
    for w in ['w', None]:
        dd = cc.dropna(subset=cv).reset_index(drop=True)
        ctr = year_ctrls(dd, ['forsh_base'] + cv)
        Rm = Resid(dd, ['cy'], ctr, w)
        xr, zr = Rm(dd.xc), Rm(dd.Zc)
        for y in ['dlnR', 'dln_new', 'dln_contracts']:
            dy = dd[y].fillna(0) if y == 'dln_contracts' else dd[y]
            yr = Rm(dy)
            r = tsls(yr, xr, zr, Rm.w, dd.cmun.values, Rm.rank + 1)        # municipality clusters (4 provinces only)
            r['ar'] = ar_analytic(yr, xr, zr, Rm.w, dd.cmun.values, Rm.rank + 1, grid)
            r['n'] = len(dd)
            cat[f'{spec}|{w or "unw"}|{y}'] = r
            print('CAT', spec, w, y, {k: (round(float(v), 3) if not isinstance(v, list) else v) for k, v in r.items()})
# OLS association new-contract vs stock index growth (same municipality-years)
mo = pf.feols('dlnR ~ dln_new | cmun + year', data=cc, vcov={'CRV1': 'cmun'})
cat['ols_stock_on_new'] = coef(mo, 'dln_new')
mo2 = pf.feols('dlnR ~ dln_new + dln_new_l1 + dln_new_l2 | cmun + year', data=cc.assign(dln_new_l1=cc.groupby('cmun').dln_new.shift(1), dln_new_l2=cc.groupby('cmun').dln_new.shift(2)).dropna(subset=['dln_new_l2']), vcov={'CRV1': 'cmun'})
cat['ols_stock_on_new_lags'] = {k: coef(mo2, k) for k in ['dln_new', 'dln_new_l1', 'dln_new_l2']}
print(cat['ols_stock_on_new'], cat['ols_stock_on_new_lags'], cat['turnover_median'], cat['n_munis'])
save('r18_catalonia.json', cat)

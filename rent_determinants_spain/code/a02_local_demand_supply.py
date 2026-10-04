"""Local demand and supply, long differences 2015-2024 within province (P1 in section 3).
Population: foreign-born net inflow 2016-2024 relative to population, instrumented with the shift-share prediction
(33 origins, 2003 shares, leave-own-province-out national growth) of the companion paper.
Supply: cadastral dwellings; income: ADRH net income per person (OLS, not identified); tourist intensity: INE share
of dwellings used as tourist dwellings in August 2020 (reduced form, not identified)."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *
from rev_design import Resid, tsls, ar_analytic

M = pd.read_parquet(f'{CL}/muni_panel.parquet')
S = M[M.in_sample].copy()
cum = S[(S.year >= 2016) & (S.year <= 2024)].groupby('cmun')[['xc', 'Zc']].sum()           # cumulative inflow and prediction
pv = S.pivot_table(index='cmun', columns='year', values=['lnR', 'P', 'viv', 'inc_pp'] if 'inc_pp' in S else ['lnR', 'P', 'viv'])
st = S.drop_duplicates('cmun').set_index('cmun')
X = pd.DataFrame({'dlnR': pv['lnR'][2024] - pv['lnR'][2015], 'dlnR_pre': pv['lnR'][2015] - pv['lnR'][2012],
                  'dlnP': np.log(pv['P'][2024] / pv['P'][2015]), 'dlnviv': np.log(pv['viv'][2024] / pv['viv'][2015]),
                  'lnR15lvl': np.nan, 'P15': pv['P'][2015]}).join(cum)
if 'inc_pp' in S:
    X['dlninc'] = np.log(pv['inc_pp'][2023] / pv['inc_pp'][2015])
X = X.join(st[PRED + ECON + ['cpro', 'ccaa', 'vutpct_2020M08', 'cat_zmrt1', 'area_km2']])
X['dens'] = np.log(X.P15 / X.area_km2)
X['size'] = pd.cut(X.P15, SIZE_EDGES, labels=SIZE_LABELS).astype(str)
X['big'] = (X.P15 >= 50000).astype(float)
X['vut20'] = X.vutpct_2020M08.fillna(0)
X = X.replace([np.inf, -np.inf], np.nan).dropna(subset=['dlnR', 'xc', 'Zc', 'P15'] + PRED + ECON).reset_index()
X.to_parquet(f'{CL}/ld_2015_2024.parquet')
CEN = PRED + ECON
res = {'n': len(X)}


def iv(y, x, z, ctrls, w='P15', d=None, fe='cpro'):
    d = X if d is None else d
    d = d.dropna(subset=[y, x, z] + ctrls)
    R = Resid(d, [fe] if fe else [], ctrls, w=w if w else None)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values)
    wt = d[w].values.astype(float) if w else np.ones(len(d))
    K = R.rank + 1
    o = tsls(yr, xr, zr, wt, d.cpro.values, K)
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, K, np.linspace(-3, 5, 1601))
    o['n'] = len(d)
    return o


# population (foreign-born inflow) and total population growth
for w in ['P15', None]:
    tag = 'w' if w else 'unw'
    res[f'rent_inflow_{tag}'] = iv('dlnR', 'xc', 'Zc', CEN, w)
    res[f'rent_dlnP_{tag}'] = iv('dlnR', 'dlnP', 'Zc', CEN, w)
    res[f'dlnP_inflow_{tag}'] = iv('dlnP', 'xc', 'Zc', CEN, w)              # natives' response: 1 = no displacement
    res[f'viv_inflow_{tag}'] = iv('dlnviv', 'xc', 'Zc', CEN, w)               # supply response (cadastre)
    res[f'pre_inflow_{tag}'] = iv('dlnR_pre', 'xc', 'Zc', CEN, w)             # falsification: 2012-2015 rent change
# heterogeneity by size (P1): split samples
for g, q in X.groupby('big'):
    res[f'rent_inflow_big{int(g)}'] = iv('dlnR', 'xc', 'Zc', CEN, 'P15', d=q)
    res[f'viv_inflow_big{int(g)}'] = iv('dlnviv', 'xc', 'Zc', CEN, 'P15', d=q)
for g, q in X.groupby('coastal'):
    res[f'rent_inflow_coast{int(g)}'] = iv('dlnR', 'xc', 'Zc', [c for c in CEN if c != 'coastal'], 'P15', d=q)

# descriptive horse race (OLS, province FE): which local changes co-move with rent growth?
cols = ['xc', 'dlnviv', 'vut20'] + (['dlninc'] if 'dlninc' in X else [])
Xs = X.dropna(subset=cols).copy()
for c in cols:
    Xs[c + '_s'] = (Xs[c] - Xs[c].mean()) / Xs[c].std()
f = 'dlnR ~ ' + ' + '.join(c + '_s' for c in cols) + ' + ' + ' + '.join(CEN) + ' | cpro'
m = pf.feols(f, data=Xs, weights='P15', vcov={'CRV1': 'cpro'})
res['ols_horse_race'] = coefs(m, [c + '_s' for c in cols])
res['ols_sd'] = {c: float(Xs[c].std()) for c in cols}
save('a02_local.json', res)
for k, v in res.items():
    if isinstance(v, dict) and 'b' in v:
        print(f"{k:28s} b={v['b']:.3f} se={v['se']:.3f} F={v['F']:.1f} AR={v['ar']} n={v['n']}")
print(res['ols_horse_race'])

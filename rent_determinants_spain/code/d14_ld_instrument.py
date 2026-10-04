"""Long-difference shift-share instrument for ALL municipalities (not only the IPVA sample of the companion paper).
x_i = sum_{t=2015}^{T} dFOR_it / P_i2015   (net foreign-born inflow, flows within source: register to 2021, census from 2022)
Z_i = sum_{t=2015}^{T} Z_it * P_i2003 / P_i2015, with Z_it the companion paper's leave-own-province-out shift-share prediction.
T = 2023 (stocks Jan 2015 -> Jan 2024) and T = 2024 (-> Jan 2025)."""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'revision_JOPE-D-26-01206', 'code'))
from rev_common import flows_by_origin, shares, instrument, pop_groups, WORK
CL = f'{WORK}/rent/clean'
dF = flows_by_origin()
pad, cen = pop_groups()
P15 = pad.xs(2015, level=1).P
s, lam, P0 = shares(2003)
munis = sorted(set(P15.index) & set(P0.index) - {'00000'})
my = pd.DataFrame([(m, y) for m in munis for y in range(2015, 2025)], columns=['cmun', 'year'])
my['Z'] = instrument(my).values
fl = dF.reset_index()[['cmun', 'year', 'FOR', 'P']].rename(columns={'FOR': 'dFOR', 'P': 'dP'})
my = my.merge(fl, on=['cmun', 'year'], how='left')
out = pd.DataFrame(index=munis)
for T in (2023, 2024):
    q = my[my.year <= T].groupby('cmun')[['Z', 'dFOR', 'dP']].sum(min_count=1)
    out[f'x{T}'] = q.dFOR / P15.reindex(q.index)
    out[f'dP{T}'] = q.dP / P15.reindex(q.index)
    out[f'Z{T}'] = q.Z * P0.reindex(q.index) / P15.reindex(q.index)
out['P15'] = P15.reindex(out.index); out['P03'] = P0.reindex(out.index)
out.index.name = 'cmun'
out.reset_index().to_parquet(f'{CL}/ld_instrument_all.parquet')
w = out.P15
print(out.describe().round(4).to_string())
print('corr x,Z (2024), pop-weighted:', np.corrcoef(out.dropna().x2024, out.dropna().Z2024)[0, 1])

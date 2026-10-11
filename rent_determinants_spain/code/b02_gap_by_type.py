"""Rents of all leases (IPVA) against incomes, 2015-2023, by municipality size, tourist exposure and coast.
Population-weighted means of the log change in the IPVA and in median income per consumption unit and the share of
municipalities in which rents outgrew incomes. Output: out/b02_gap_by_type.json (used by t02_v2_tables.py)."""
import numpy as np, pandas as pd
from rd_common import *

M = pd.read_parquet(f'{CL}/muni_panel.parquet'); A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
inc = A.pivot_table(index=['cmun', 'year'], columns='indicator', values='value')


def g(ind):
    s = inc[ind].unstack('year'); return np.log(s[2023] / s[2015])


pr = M.pivot_table(index='cmun', columns='year', values='lnR'); st = M[M.year == 2015].set_index('cmun')
X = pd.DataFrame({'dR': pr[2023] - pr[2015], 'pp': g('Renta neta media por persona'), 'hh': g('Renta neta media por hogar'),
                  'uc': g('Mediana de la renta por unidad de consumo')}).join(st[['P', 'coastal', 'vutpct_2020M08']]).dropna(subset=['dR', 'P'])
X['size'] = pd.cut(X.P, SIZE_EDGES, labels=SIZE_LABELS)
X['vt'] = pd.qcut(X.vutpct_2020M08.rank(method='first'), 3, labels=['low', 'mid', 'high'])
out = {}
for col in ['size', 'vt', 'coastal']:
    for k, q in X.groupby(col, observed=True):
        q = q.dropna(subset=['uc']); w = q.P.values
        out[f'{col}:{k}'] = {'n': len(q), 'dR': round(100 * wmean(q.dR.values, w), 1), 'inc_uc': round(100 * wmean(q.uc.values, w), 1),
                             'inc_hh': round(100 * wmean(q.hh.values, w), 1), 'gap_uc': round(100 * wmean((q.dR - q.uc).values, w), 1),
                             'share_gap_pos': round(float(((q.dR - q.uc) > 0).mean()), 2)}
q = X.dropna(subset=['uc'])
out['all'] = {'n': len(q), 'dR': round(100 * wmean(q.dR.values, q.P.values), 1), 'inc_uc': round(100 * wmean(q.uc.values, q.P.values), 1),
              'gap_uc': round(100 * wmean((q.dR - q.uc).values, q.P.values), 1), 'share_gap_pos': round(float(((q.dR - q.uc) > 0).mean()), 2)}
for k, v in out.items():
    print(k, v)
save('b02_gap_by_type.json', out)

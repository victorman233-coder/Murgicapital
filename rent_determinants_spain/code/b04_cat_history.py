"""Catalan deposit register, 2007-2025: mean rent of new leases (all municipalities in the register, weighted by the number
of leases), to place the 2015 base year of the entry facts in the cycle. Descriptive: not adjusted for composition, and the
set of municipalities with published data changes over time.
Output: out/b04_cat_history.json"""
import numpy as np, pandas as pd
from rd_common import *

L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
L = L[(L['Període'] == 'gener-desembre') & (L['Àmbit territorial'] == 'Municipi')].copy()
L['R'] = pd.to_numeric(L.Renda, errors='coerce'); L['N'] = pd.to_numeric(L.Habitatges, errors='coerce')
L = L.dropna(subset=['R', 'N'])
g = L.groupby('Any')[['R', 'N']].apply(lambda q: pd.Series({'mean': np.average(q.R, weights=q.N), 'leases': q.N.sum(), 'munis': len(q)}))
res = {'mean_rent': g['mean'].round(2).to_dict(), 'leases': g.leases.astype(int).to_dict(), 'munis': g.munis.astype(int).to_dict()}
lr = np.log(g['mean'])
res['d_2008_2015'] = float(lr[2015] - lr[2008]); res['d_2015_2023'] = float(lr[2023] - lr[2015]); res['d_2008_2023'] = float(lr[2023] - lr[2008])
res['d_2018_2023'] = float(lr[2023] - lr[2018])
print({k: round(v, 3) for k, v in res.items() if k.startswith('d_')})
save('b04_cat_history.json', res)

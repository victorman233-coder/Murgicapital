"""Parse the Eurostat JSON-stat file migr_imm3ctb (immigration by country of birth) for the 28 origin countries."""
import json, numpy as np, pandas as pd
from rev_common import WORK
CODES = ['DE', 'BG', 'FR', 'IT', 'PL', 'PT', 'RO', 'UK', 'RU', 'UA', 'DZ', 'MA', 'NG', 'SN', 'AR', 'BO', 'BR', 'CL', 'CO', 'CU', 'EC', 'PY',
         'PE', 'DO', 'UY', 'VE', 'CN', 'PK']
d = json.load(open(f'{WORK}/raw/eurostat/migr_imm3ctb.json'))
dims, sizes = d['id'], d['size']
cats = {k: list(d['dimension'][k]['category']['index'].keys()) for k in dims}
strides = np.cumprod([1] + sizes[::-1])[::-1][1:]
rows = []
for k, v in d['value'].items():
    k = int(k); pos = []
    for s in strides:
        pos.append(k // s); k %= s
    rec = {dims[i]: cats[dims[i]][pos[i]] for i in range(len(dims))}; rec['v'] = v; rows.append(rec)
D = pd.DataFrame(rows); D = D[D.c_birth.isin(CODES)]
D.to_parquet(f'{WORK}/clean/eurostat_imm_cbirth.parquet')
print(D.shape)

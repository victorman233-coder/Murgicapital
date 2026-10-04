"""Randomisation inference (Borusyak-Hull 2023) with recentred instruments, several assignment strata
and three test statistics. Output: out/r11_ri.json"""
import numpy as np, pandas as pd
from rev_common import *
from rev_design import *

sc, fsx, cvx = load_panel()
d = sc.reset_index(drop=True)
fs_cols = fsx.split(' + '); cv_cols = cvx.split(' + ')
S, Gl, Gn = obs_matrices(d)
gn, gp, s, P0, Fstock = shock_arrays()
size = Fstock[GROUPS]
terc = pd.qcut(size.rank(method='first'), 3, labels=['small', 'mid', 'large'])
half_in_cont = {}
for reg in ['Europa', 'Africa', 'America', 'Asia', 'Otros']:
    gs = [o for o in GROUPS if REGION[o] == reg]
    med = size[gs].median()
    for o in gs:
        half_in_cont[o] = reg + ('_L' if size[o] >= med else '_S')
STRATA = {'all': ['all'] * len(GROUPS),
          'continent': [REGION[o] for o in GROUPS],
          'size_tercile': [str(terc[o]) for o in GROUPS],
          'continent_x_size': [half_in_cont[o] for o in GROUPS]}
grid = np.round(np.arange(-1.5, 3.0001, 0.01), 3)
res = {}
for spec, ctrls in [('min', fs_cols), ('cov', fs_cols + cv_cols)]:
    for w in ['w', None]:
        tag = f'{spec}_{"w" if w else "u"}'
        Rm = Resid(d, ['cy'], ctrls, w); wt = Rm.w
        yr, xr = Rm(d['dlnR']), Rm(d['xc'])
        res[tag] = {}
        for sname, strata in STRATA.items():
            z, mu, Zp = perm_instruments(S, Gl, strata, n_perm=2000)
            zt_r = Rm(z - mu); Zp_r = Rm((Zp - mu[None, :]).T).T
            rr = tsls(yr, xr, zt_r, wt, d['cpro'].values, Rm.rank + 1)
            ri = ri_ar_full(yr, xr, wt, zt_r, Zp_r, d['cpro'].values, grid)
            ri.update(dict(b=rr['b'], se=rr['se'], F=rr['F']))
            res[tag][sname] = ri
            print(tag, sname, {k: v for k, v in ri.items()})
res['strata_definition'] = {k: dict(zip(GROUPS, v)) for k, v in STRATA.items()}
save('r11_ri.json', res)

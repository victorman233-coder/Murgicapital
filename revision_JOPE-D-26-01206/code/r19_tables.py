"""Final numbers for the revised manuscript: main table with all inference procedures for the original,
central and size-FE specifications; spatial spillovers under the central specification; magnitudes.
Output: out/r19_main.json"""
import numpy as np, pandas as pd
from rev_common import *
from rev_design import *

d = load_revision_panel()
Y0 = int(os.environ.get('Y0', 2012))
d = d[d.year >= Y0].reset_index(drop=True)
S, Gl, Gn = obs_matrices(d)
grid = np.round(np.arange(-2, 4.0001, 0.01), 3)
AUTH = ['lninc15', 'lnpop11', 'rent11', 'vac11']
gn, gp, s_, P0, Fo = shock_arrays()
size = Fo[GROUPS]; terc = pd.qcut(size.rank(method='first'), 3, labels=['small', 'mid', 'large'])
STR = {'all': ['all'] * len(GROUPS), 'size': [str(terc[o]) for o in GROUPS], 'continent': [REGION[o] for o in GROUPS]}
perm = {k: perm_instruments(S, Gl, v, n_perm=2000) for k, v in STR.items()}
# AKM exposure matrix (national shocks)
years = sorted(d.year.unique())
cols, gvec, gid, gyear = [], [], [], []
for t in range(min(years) - 1, max(years) + 1):
    for j, o in enumerate(GROUPS):
        e = S[:, j] * (0.5 * (d['year'].values == t) + 0.5 * (d['year'].values == t + 1))
        if e.sum() == 0:
            continue
        cols.append(e); gvec.append(gn.loc[t, o]); gid.append(o); gyear.append(t)
Sexp = np.column_stack(cols); gvec = np.array(gvec)
d['Zn'] = (S * Gn).sum(axis=1)
SPECS = {'original (author covariates)': dict(cv=AUTH, fe=('cy',)), 'central (predetermined + structure)': dict(cv=PRED + ECON, fe=('cy',)),
         'central + province x size FE': dict(cv=PRED + ECON, fe=('cy_size',)), 'minimal': dict(cv=[], fe=('cy',))}
out = {}
for name, sp in SPECS.items():
    for w in ['w', 'w_rent', None]:
        keep = d[sp['cv']].notna().all(axis=1).values & (d.groupby(sp['fe'][0]).cmun.transform('size') > 1).values
        dd = d[keep].reset_index(drop=True)
        c = year_ctrls(dd, ['forsh_base'] + sp['cv'])
        Rm = Resid(dd, list(sp['fe']), c, w); W_ = Rm.w; K = Rm.rank + 1; cl = dd.cpro.values
        yr, xr, zr = Rm(dd.dlnR), Rm(dd.xc), Rm(dd.Zc)
        r = tsls(yr, xr, zr, W_, cl, K)
        r['rf'] = float(np.sum(W_ * zr * yr) / np.sum(W_ * zr * zr))
        r['ols'] = float(np.sum(W_ * xr * yr) / np.sum(W_ * xr * xr))
        r['ar'] = ar_analytic(yr, xr, zr, W_, cl, K, grid)
        r['ar_wcr'] = ar_wcr(yr, xr, zr, W_, cl, K, grid, B=4999)
        for k, (z, mu, Zp) in perm.items():
            zt = Rm((z - mu)[keep]); Zpr = Rm((Zp[:, keep] - mu[keep][None, :]).T).T
            ri = ri_ar_full(yr, xr, W_, zt, Zpr, cl, grid)
            r[f'ri_{k}'] = dict(ci_t=ri['ci_t'], ci_coef=ri['ci_coef'], p0_t=ri['p0']['t'], fs_p_t=ri['fs_p_t'])
        znr = Rm(dd.Zn); rn = tsls(yr, xr, znr, W_, cl, K)
        Sr = Rm(Sexp[keep])
        sbar = (Sexp[keep] * W_[:, None]).sum(axis=0)
        gdf = pd.DataFrame({'g': gvec, 'year': gyear, 's': sbar})
        gm = gdf.groupby('year').apply(lambda x: np.average(x.g, weights=x.s) if x.s.sum() > 0 else 0).reindex(gdf.year).values
        r['national_shock_iv'] = dict(b=rn['b'], se=rn['se'], F=rn['F'], akm0=akm0(yr, xr, W_, Sr, gvec - gm, gid, grid))
        r['n'] = len(dd)
        out[f'{name}|{w or "unw"}'] = r
        print(name, w, {k: v for k, v in r.items() if k in ('b', 'se', 'F', 'ar', 'ar_wcr', 'rf', 'ols')}, r['ri_all'], r['ri_continent']['ci_t'], r['national_shock_iv'])
# ------------------------------------------------------------------ spatial spillovers under the central specification
rings = pd.read_parquet(f'{REP}/data/clean/spatial_rings.parquet')
sp_ = {}
dr = d.merge(rings, on=['cmun', 'year'], how='left')
for ring in ['contig', 'r0_15', 'r15_40']:
    for w in ['w', None]:
        dd = dr.dropna(subset=[f'xc_{ring}', f'Zc_{ring}'] + PRED + ECON).reset_index(drop=True)
        c = year_ctrls(dd, ['forsh_base'] + PRED + ECON)
        r = iv_multi(dd, 'dlnR', ['xc', f'xc_{ring}'], ['Zc', f'Zc_{ring}'], c, w)
        sp_[f'{ring}|{w or "unw"}'] = {k: v for k, v in r.items() if not k.startswith('_')}
        print('spatial', ring, w, sp_[f'{ring}|{w or "unw"}'])
# ------------------------------------------------------------------ magnitudes
M, G = 0.065, 0.206
mag = {'M': M, 'G': G, 'factor': M / G}
save(f'r19_main{"" if Y0 == 2012 else "_" + str(Y0)}.json', dict(main=out, spatial=sp_, magnitudes=mag))

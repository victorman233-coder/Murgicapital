"""Stage 2 (MI-2): alternative 'push' shocks from inflows of each origin into other European countries
(Eurostat migr_imm3ctb, immigration by country of birth), excluding Spain. The shift for origin o in year t is
I_ot^other / F_o,2003^Spain (gross inflows into a balanced set of destinations over Spain's 2003 stock).
Output: out/r15_alt_shocks.json"""
import numpy as np, pandas as pd
from rev_common import *
from rev_design import *

CODE = dict(zip(COUNTRIES, ['DE', 'BG', 'FR', 'IT', 'PL', 'PT', 'RO', 'UK', 'RU', 'UA', 'DZ', 'MA', 'NG', 'SN', 'AR', 'BO', 'BR', 'CL',
                            'CO', 'CU', 'EC', 'PY', 'PE', 'DO', 'UY', 'VE', 'CN', 'PK']))
DEST = ['AT', 'CZ', 'FI', 'HR', 'IT', 'LU', 'NL', 'NO', 'SE', 'SI', 'SK', 'BG']
E = pd.read_parquet(f'{WORK}/clean/eurostat_imm_cbirth.parquet')
E['time'] = E.time.astype(int)
E = E[E.geo.isin(DEST) & (E.time >= 2010)]
P = E.pivot_table(index=['geo', 'c_birth'], columns='time', values='v')
P = P.T.interpolate(limit_area='inside').bfill().T            # fill isolated gaps inside the window, backfill BG 2011
I = P.groupby(level='c_birth').sum()                            # inflows of origin into the destination set, by year
d = load_revision_panel()
s, lam, P0 = shares(2003)
gn, gp, _, _, Fo = shock_arrays()
galt = pd.DataFrame({o: I.loc[CODE[o]] / Fo[o] for o in COUNTRIES}).sort_index()    # year x origin
S28 = s.reindex(d.cmun).fillna(0)[COUNTRIES].values
def zt(t):
    return np.array([S28[i] @ galt.loc[t].values if t in galt.index else np.nan for i, t in enumerate(t)])
d['Zalt'] = (zt(d.year.values) + zt(d.year.values - 1)) / 2
d['S28'] = S28.sum(axis=1)
# instrument restricted to the same 28 countries with Spanish (leave-out) shocks, for comparison
S_all, Gl_all, Gn_all = obs_matrices(d)
idx28 = [GROUPS.index(o) for o in COUNTRIES]
d['Z28'] = (S_all[:, idx28] * Gl_all[:, idx28]).sum(axis=1)
grid = np.round(np.arange(-3, 5.0001, 0.01), 3)
res = {'destinations': DEST, 'corr_galt_gspain': {}}
for o in COUNTRIES:
    a = galt[o].loc[2011:2024]; b = gn[o].loc[2011:2024]
    res['corr_galt_gspain'][o] = float(np.corrcoef(a, b)[0, 1])
for spec, cv in [('author_cov', ['lninc15', 'lnpop11', 'rent11', 'vac11']), ('S4_central', PRED + ECON)]:
    for w in ['w', 'w_rent', None]:
        dd = d.dropna(subset=['Zalt'] + cv).reset_index(drop=True)
        c = year_ctrls(dd, ['S28', 'forsh_base'] + cv)
        Rm = Resid(dd, ['cy'], c, w)
        yr, xr = Rm(dd.dlnR), Rm(dd.xc)
        for z in ['Zalt', 'Z28']:
            zr = Rm(dd[z])
            r = tsls(yr, xr, zr, Rm.w, dd.cpro.values, Rm.rank + 1)
            r['ar'] = ar_analytic(yr, xr, zr, Rm.w, dd.cpro.values, Rm.rank + 1, grid)
            r['n'] = len(dd)
            res[f'{spec}|{w or "unw"}|{z}'] = r
            print(spec, w, z, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
save('r15_alt_shocks.json', res)
print(pd.Series(res['corr_galt_gspain']).round(2).to_string())

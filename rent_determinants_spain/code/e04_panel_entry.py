"""Entry-gap paper: annual panel with year-varying shocks for the regions with new-lease registers.
Sample: the companion paper's analysis panel (IPVA municipalities, 2012-2024; instrument Zc, inflow xc, province-by-year
fixed effects, 2003 foreign share x year and predetermined covariates x year, population weights), merged with annual
new-lease rents: Catalonia (deposit register, rent per contract, 2012-2024), Basque Country (EMAL, rent per m2,
2017-2024) and Comunitat Valenciana (median deposit, 2021-2024) and Aragón (street-adjusted index from the deposit register, 2012-2024).
Outcomes: annual growth of entry rents, of the rent of all leases (IPVA) and their difference (change in the entry gap).
Inference: CRV1 by municipality and by province; randomisation inference permuting origin shock paths (all origins and
within continents), recentred instrument, Anderson-Rubin sets with the cluster-robust t statistic (Borusyak and Hull 2023).
Also: the long-difference design of e01 with the Borusyak-Hull-Jaravel sum-of-shares control, Rotemberg balance tests."""
import numpy as np, pandas as pd
from rd_common import *
from rev_common import load_panel, GROUPS, REGION, shares
from rev_design import Resid, tsls, ar_analytic, obs_matrices, perm_instruments, ri_ar_full

res = {}
sc, fsx, cvx = load_panel()
d0 = sc.reset_index(drop=True)
ctrls = fsx.split(' + ') + cvx.split(' + ')

# ------------------------------------------------------------------ annual entry rents by region
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
L = L[L['Període'] == 'gener-desembre'].copy()
L['cmun'] = L['Codi territorial'].astype(int).astype(str).str.zfill(5)
L['rent'] = pd.to_numeric(L.Renda, errors='coerce'); L['n'] = pd.to_numeric(L.Habitatges, errors='coerce')
cat = L.rename(columns={'Any': 'year'})[['cmun', 'year', 'rent', 'n']].dropna()
cat = cat[cat.n >= 30]                                   # municipalities with at least 30 new leases in the year
E = pd.read_parquet(f'{CL}/emal_muni.parquet').rename(columns={'rent_m2_new': 'rent', 'n_new': 'n'})[['cmun', 'year', 'rent', 'n']]
E = E[E.n >= 30]
V = pd.read_parquet(f'{CL}/gva_muni.parquet').rename(columns={'dep_med': 'rent'})[['cmun', 'year', 'rent', 'n']]
V = V[V.n >= 30]
AR = pd.read_parquet(f'{CL}/aragon_muni.parquet').dropna(subset=['idx_street'])
AR = AR[AR.n >= 30].assign(rent=lambda q: np.exp(q.idx_street))[['cmun', 'year', 'rent', 'n']]   # street-adjusted index
N = pd.concat([cat.assign(reg='CAT'), E.assign(reg='PV'), V.assign(reg='VAL'), AR.assign(reg='ARA')])
N = N.sort_values(['cmun', 'year'])
N['dln_new'] = np.log(N.rent).groupby(N.cmun).diff()
N.loc[N.year.diff().ne(1) & N.cmun.eq(N.cmun.shift()), 'dln_new'] = np.nan
N = N.dropna(subset=['dln_new'])
d = d0.merge(N[['cmun', 'year', 'dln_new', 'reg', 'n']], on=['cmun', 'year'], how='inner')
d['dG'] = d.dln_new - d.dlnR
d = d[d.dln_new.abs() < 0.5].reset_index(drop=True)        # drop implausible jumps (|growth| > 65%)
res['sample'] = dict(n=len(d), munis=int(d.cmun.nunique()), by_region=d.groupby('reg').cmun.nunique().to_dict(),
                     years=[int(d.year.min()), int(d.year.max())], provinces=int(d.cpro.nunique()))
print(res['sample'])

S, Gl, Gn = obs_matrices(d)
grid = np.round(np.arange(-4, 6.0001, 0.01), 3)


def panel_iv(dd, y, S_, Gl_, ri=True, cl='cmun'):
    R = Resid(dd, ['cy'], ctrls, 'w'); wt = R.w; K = R.rank + 1
    yr, xr, zr = R(dd[y].values), R(dd['xc'].values), R(dd['Zc'].values)
    o = tsls(yr, xr, zr, wt, dd[cl].values, K)
    o = {k: float(v) for k, v in o.items()}
    o['se_prov'] = float(tsls(yr, xr, zr, wt, dd.cpro.values, K)['se'])
    o['ar'] = ar_analytic(yr, xr, zr, wt, dd[cl].values, K, grid)
    o['n'] = len(dd); o['ymean'] = wmean(dd[y].values, dd.w.values)
    if ri:
        o['ri'] = {}
        for sname, strata in [('all', ['all'] * len(GROUPS)), ('continent', [REGION[g] for g in GROUPS])]:
            z, mu, Zp = perm_instruments(S_, Gl_, strata, n_perm=2000, seed=5)
            zt_r = R(z - mu); Zp_r = R((Zp - mu[None, :]).T).T
            rr = tsls(yr, xr, zt_r, wt, dd[cl].values, K)
            r2 = ri_ar_full(yr, xr, wt, zt_r, Zp_r, dd[cl].values, grid)
            o['ri'][sname] = dict(b=float(rr['b']), se=float(rr['se']), F=float(rr['F']), ci_t=r2['ci_t'],
                                  p0_t=r2['p0'].get('t'), fs_p_t=r2['fs_p_t'])
    return o


res['panel'] = {}
for y in ['dln_new', 'dlnR', 'dG']:
    res['panel'][y] = panel_iv(d, y, S, Gl)
    o = res['panel'][y]
    print('panel', y, round(o['b'], 3), round(o['se'], 3), 'seprov', round(o['se_prov'], 3), 'F', round(o['F'], 1), o['ar'], o['ri'])
# by region (no RI)
for reg in ['CAT', 'ARA']:                         # the Basque Country is outside the IPVA panel (foral regime)
    m = (d.reg == reg).values
    dd = d[m].reset_index(drop=True)
    res['panel_' + reg] = {y: panel_iv(dd, y, S[m], Gl[m], ri=False) for y in ['dln_new', 'dlnR', 'dG']}
    print(reg, {y: (round(v['b'], 3), round(v['se'], 3), round(v['F'], 1), v['ar']) for y, v in res['panel_' + reg].items()})
# pre-2020 window (before the update caps of 2022)
m = (d.year <= 2019).values
dd = d[m].reset_index(drop=True)
res['panel_pre2020'] = {y: panel_iv(dd, y, S[m], Gl[m], ri=False) for y in ['dln_new', 'dlnR', 'dG']}
print('pre2020', {y: (round(v['b'], 3), round(v['se'], 3), round(v['F'], 1), v['ar']) for y, v in res['panel_pre2020'].items()})
# placebo: next year's inflow should not move this year's entry rent once this year's is controlled -> lead test
d = d.sort_values(['cmun', 'year']).reset_index(drop=True)
d['Zc_lead'] = d.groupby('cmun').Zc.shift(-1)
dl = d.dropna(subset=['Zc_lead']).reset_index(drop=True)
R = Resid(dl, ['cy'], ctrls + ['Zc'], 'w')
lead = {}
for y in ['dln_new', 'dG']:
    m_ = np.sum(R.w * R(dl.Zc_lead.values) * R(dl[y].values)) / np.sum(R.w * R(dl.Zc_lead.values) ** 2)
    e = R(dl[y].values) - m_ * R(dl.Zc_lead.values)
    G_ = pd.Series(R.w * R(dl.Zc_lead.values) * e).groupby(dl.cmun.values).sum().values
    se = np.sqrt(np.sum(G_ ** 2)) / np.sum(R.w * R(dl.Zc_lead.values) ** 2)
    lead[y] = dict(b=float(m_), se=float(se))
res['lead_rf'] = lead
print('lead reduced form', lead)
d[['cmun', 'year', 'reg', 'dln_new', 'dlnR', 'dG', 'xc', 'Zc', 'w']].to_parquet(f'{CL}/e04_panel.parquet')

# ------------------------------------------------------------------ long difference with the sum-of-shares control
X = pd.read_parquet(f'{CL}/e01_X.parquet')
s, lam, P0 = shares(2003)
X['Ssum'] = s.reindex(X.cmun)[GROUPS].sum(1).values * P0.reindex(X.cmun).values / X.P15
CEN = PRED + ECON
ld = {}
for y, T in [('G_vr', 2024), ('G_m2', 2024), ('entry', 2024), ('dlnR', 2024), ('AE', 2024), ('d_uc', 2023), ('d_hhsize', 2023), ('dP2024', 2024), ('dlnviv', 2024), ('dlnR_pre', 2024)]:
    dd = X.dropna(subset=[y, f'x{T}', f'Z{T}', 'Ssum'] + CEN).copy()
    R = Resid(dd, ['cpro'], CEN + ['Ssum'], 'P15')
    yr, xr, zr = R(dd[y].values), R(dd[f'x{T}'].values), R(dd[f'Z{T}'].values)
    o = tsls(yr, xr, zr, R.w, dd.cpro.values, R.rank + 1)
    o = {k: float(v) for k, v in o.items()}
    o['ar'] = ar_analytic(yr, xr, zr, R.w, dd.cpro.values, R.rank + 1, np.linspace(-6, 6, 2401)); o['n'] = len(dd)
    ld[y] = o
    print('LD+Ssum', y, round(o['b'], 3), round(o['se'], 3), round(o['F'], 1), o['ar'])
res['ld_sumshares'] = ld

# ------------------------------------------------------------------ top Rotemberg origins: balance and leave-one-origin-out
from ld_shiftshare import components                      # noqa: E402
rot = pd.read_csv(os.path.join(OUT, 'e03_rotemberg_Gvr.csv')).head(5).origin.tolist()
bal = {}
for o_ in rot[:3]:
    X[f'sh_{o_}'] = s.reindex(X.cmun)[o_].values
    for y in ['dlnR_pre', 'rent11', 'vac11', 'tert11', 'sh65_11', 'coastal']:
        dd = X.dropna(subset=[y, f'sh_{o_}'] + CEN).copy()
        cc = [c for c in CEN if c != y] + ['Ssum']               # conditional on the controls of the main specification
        R = Resid(dd, ['cpro'], cc, 'P15')
        a, b_ = R(dd[f'sh_{o_}'].values), R(dd[y].values)
        sa, sb = np.sqrt(np.average(a ** 2, weights=R.w)), np.sqrt(np.average(b_ ** 2, weights=R.w))
        bb = np.sum(R.w * a * b_) / np.sum(R.w * a * a)
        e = b_ - bb * a
        G_ = pd.Series(R.w * a * e).groupby(dd.cpro.values).sum().values
        se = np.sqrt(np.sum(G_ ** 2)) / np.sum(R.w * a * a)
        bal[f'{o_}|{y}'] = dict(b_std=float(bb * sa / sb), t=float(bb / se))
res['rotemberg_balance'] = bal
print(pd.DataFrame(bal).T.round(3))
loo = {}
for y in ['G_vr', 'entry', 'dlnR', 'd_hhsize']:
    T = 2023 if y == 'd_hhsize' else 2024
    dd = X.dropna(subset=[y, f'x{T}', f'Z{T}'] + CEN).reset_index(drop=True)
    Sx, Glx, _ = components(dd, T)
    R = Resid(dd, ['cpro'], CEN, 'P15')
    yr, xr = R(dd[y].values), R(dd[f'x{T}'].values)
    for o_ in ['none'] + rot:
        keep = [j for j, g in enumerate(GROUPS) if g != o_]
        zr = R((Sx[:, keep] * Glx[:, keep]).sum(1))
        o = tsls(yr, xr, zr, R.w, dd.cpro.values, R.rank + 1)
        loo[f'{y}|{o_}'] = dict(b=float(o['b']), se=float(o['se']), F=float(o['F']),
                                ar=ar_analytic(yr, xr, zr, R.w, dd.cpro.values, R.rank + 1, np.linspace(-6, 6, 2401)))
res['leave_one_origin_out'] = loo
print(pd.DataFrame(loo).T)
save('e04_panel_entry.json', res)

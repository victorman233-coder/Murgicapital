"""Entry-gap paper: extensions.
(1) Turnover lambda: lease survival in the Aragón deposit register (share of each cohort's deposits not yet returned),
    fitted with S(a) = p + (1 - p) exp(-h a); compared with the weight of new leases implied by the INE indices.
(2) Caps on updates (2022-2024): national accounting with the stock-flow identity and CPI; provincial test that the cap
    decoupled existing-lease growth from new-lease growth (cross-province dispersion and correlation by year).
(3) Tourism threshold (Hansen 2000): Catalan quarterly new leases (count and mean rent); the slope of the collapse
    (2020Q2-2021Q2), recovery and late-period effects in tourist-dwelling exposure differs above and below a threshold;
    threshold by least squares over a grid, likelihood-ratio confidence set, wild cluster bootstrap test of a common slope.
(4) Pre-specified heterogeneity of the entry-gap response: municipality size, coast, rental share in 2011, FUA core.
(5) AEAT 2024 by postal code: between- and within-city variation of the entry gap; gradient with neighbourhood rent level."""
import numpy as np, pandas as pd
import pyfixest as pf
from scipy.optimize import curve_fit
from rd_common import *
from rev_design import Resid, tsls, ar_analytic, iv_multi

res = {}
# ------------------------------------------------------------------ (1) turnover from lease survival (Aragón)
Sv = pd.read_parquet(f'{CL}/aragon_survival.parquet')
Sv = Sv[Sv.cohort.between(2012, 2025)].copy()
Sv['age'] = 2026.0 - Sv.cohort                          # register downloaded in 2026; mid-cohort to snapshot ~ age
f = lambda a, p, h: p + (1 - p) * np.exp(-h * a)
out = {}
for col in ['open_share', 'open_share_zgz']:
    (p, h), cov = curve_fit(f, Sv.age.values, Sv[col].values, p0=[0.1, 0.2], bounds=([0, 0], [1, 2]))
    out[col] = dict(p_never=float(p), hazard=float(h), annual_exit=float(1 - np.exp(-h)), se_h=float(np.sqrt(cov[1, 1])),
                    median_duration=float(np.log(2) / h))
N = pd.read_parquet(f'{CL}/national.parquet')
out['ine_w_new'] = N.w_new.dropna().round(4).to_dict()
out['survival'] = Sv[['cohort', 'open_share', 'open_share_zgz']].round(4).to_dict('records')
res['turnover'] = out
print('turnover', {k: v for k, v in out.items() if k != 'survival'})

# ------------------------------------------------------------------ (2) caps on updates
n = N.loc[2021:2024]
g = lambda s: np.log(s / s.shift(1))
cap = pd.Series({2022: 0.02, 2023: 0.02, 2024: 0.03})
inside = pd.Series({2022: 0.75, 2023: 1.0, 2024: 1.0})           # share of the year with the cap in force (from 31 March 2022)
pi = g(N.cpi).loc[2022:2024]
ex = g(n.ipva_existing).loc[2022:2024]
wedge = (pi - cap).clip(lower=0) * inside                         # update foregone by leases with CPI clauses
G_obs = np.log(n.ipva_new / n.ipva_existing)
ex_cf = ex + wedge
G_cf_2024 = float(G_obs.loc[2021] + (g(n.ipva_new).loc[2022:2024] - ex_cf).sum())
res['update_cap_national'] = dict(pi=pi.round(4).to_dict(), existing=ex.round(4).to_dict(), new=g(n.ipva_new).loc[2022:2024].round(4).to_dict(),
                                  wedge=wedge.round(4).to_dict(), G_2021=float(G_obs.loc[2021]), G_2024=float(G_obs.loc[2024]),
                                  G_2024_no_cap=G_cf_2024, share_widening_cap=float((G_obs.loc[2024] - G_cf_2024) / (G_obs.loc[2024] - G_obs.loc[2021])))
print('update cap', res['update_cap_national'])
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.prov != '00') & (pa.typ == 'Variación anual')].pivot_table(index=['prov', 'year'], columns='age', values='val').reset_index()
pa.columns = ['prov', 'year', 'exist', 'new', 'total']
pa['lam'] = (pa.total - pa.exist) / (pa.new - pa.exist)
pa.loc[(pa.new - pa.exist).abs() < 1.0, 'lam'] = np.nan         # identity uninformative when the two indices move together
byyr = {}
for y, q in pa.groupby('year'):
    byyr[int(y)] = dict(sd_exist=float(q.exist.std()), sd_new=float(q.new.std()), mean_exist=float(q.exist.mean()), mean_new=float(q.new.mean()),
                        corr=float(np.corrcoef(q.exist, q.new)[0, 1]), slope=float(np.polyfit(q.new, q.exist, 1)[0]),
                        lam_med=float(q.lam.median()), n=int(len(q)))
res['update_cap_provinces'] = byyr
print(pd.DataFrame(byyr).T.round(3))

# ------------------------------------------------------------------ (3) tourism threshold (Catalonia, quarterly new leases)
Cq = pd.read_parquet(f'{CL}/cat_q.parquet'); Cq = Cq[Cq.year <= 2025].copy()
b19 = Cq[Cq.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
Cq = Cq[Cq.cmun.isin(b19[(b19['count'] == 4) & (b19['sum'] >= 40)].index)].copy()
Cq['E'] = Cq.vutpct_2020M08.fillna(0); Cq['lnn'] = np.log(Cq.n); Cq['lnrent'] = np.log(Cq.rent)
Cq['t'] = (Cq.year - 2019) * 4 + Cq.q - 1; Cq['P19'] = Cq.cmun.map(Cq[Cq.year == 2019].groupby('cmun').P.first())
Cq = Cq.dropna(subset=['lnn', 'lnrent', 'P19']).reset_index(drop=True)
per = {'covid': Cq.t.between(5, 9).values, 'recov': Cq.t.between(12, 19).values, 'late': Cq.t.between(20, 27).values}
from pyfixest.estimation import demean as pf_demean


def dm(M):
    fe = np.column_stack([pd.factorize(Cq.cmun)[0], pd.factorize(Cq.t)[0]]).astype(np.uint64)
    out, ok = pf_demean(np.asarray(M, dtype=float), fe, Cq.P19.values.astype(float))
    return out


lin = np.column_stack([per[p] * Cq.E.values for p in per] + [(Cq.q.values == k) * Cq.E.values for k in (2, 3, 4)])
Xlin = dm(lin)
uniq = np.sort(Cq.drop_duplicates('cmun').E.values)
grid_tau = np.unique(np.round(np.quantile(uniq, np.linspace(0.10, 0.95, 60)), 2))
sw = np.sqrt(Cq.P19.values)
thr = {}
for y in ['lnn', 'lnrent']:
    Y = dm(Cq[y].values[:, None])[:, 0]

    def ssr(Yv, Xm):
        A = Xm * sw[:, None]; b = np.linalg.lstsq(A, Yv * sw, rcond=None)[0]
        e = Yv - Xm @ b
        return float(np.sum(Cq.P19.values * e ** 2)), b, e
    Xstep = {}
    for tau in grid_tau:
        D = (Cq.E.values > tau).astype(float)
        st = np.column_stack([per[p] * Cq.E.values * D for p in per] + [(Cq.q.values == k) * Cq.E.values * D for k in (2, 3, 4)])
        Xstep[tau] = np.column_stack([Xlin, dm(st)])
    S = {tau: ssr(Y, Xs)[0] for tau, Xs in Xstep.items()}
    tau_hat = min(S, key=S.get)
    s0, b0_, e0 = ssr(Y, Xlin)
    nobs = len(Y)
    LR = {tau: nobs * (S[tau] - S[tau_hat]) / S[tau_hat] for tau in S}
    ci = [float(min(t for t in LR if LR[t] <= 7.35)), float(max(t for t in LR if LR[t] <= 7.35))]
    Fsup = nobs * (s0 - S[tau_hat]) / S[tau_hat]
    # wild cluster bootstrap under the linear null (Rademacher by municipality)
    rng = np.random.default_rng(3); cl = pd.factorize(Cq.cmun)[0]; B = 499; Fb = []
    fit0 = Y - e0
    for b in range(B):
        v = rng.choice([-1.0, 1.0], size=cl.max() + 1)[cl]
        Yb = fit0 + e0 * v
        sb0 = ssr(Yb, Xlin)[0]
        sbt = min(ssr(Yb, Xs)[0] for Xs in Xstep.values())
        Fb.append(nobs * (sb0 - sbt) / sbt)
    pval = float(np.mean(np.array(Fb) >= Fsup))
    _, bh, _ = ssr(Y, Xstep[tau_hat])
    thr[y] = dict(tau_hat=float(tau_hat), ci=ci, Fsup=float(Fsup), p_boot=pval, B=B,
                  slope_below=dict(covid=float(bh[0]), recov=float(bh[1]), late=float(bh[2])),
                  slope_above=dict(covid=float(bh[0] + bh[6]), recov=float(bh[1] + bh[7]), late=float(bh[2] + bh[8])),
                  grid=[float(grid_tau.min()), float(grid_tau.max())], munis_above=int((uniq > tau_hat).sum()), munis=int(len(uniq)),
                  ssr_path={float(k): float(v) for k, v in S.items()})
    print('threshold', y, {k: v for k, v in thr[y].items() if k != 'ssr_path'})
res['tourism_threshold'] = thr

# ------------------------------------------------------------------ (4) heterogeneity of the entry-gap response
X = pd.read_parquet(f'{CL}/e01_X.parquet')
M = pd.read_parquet(f'{CL}/muni_panel.parquet').drop_duplicates('cmun').set_index('cmun')
X['big'] = (X.cmun.map(M.pop11) >= 100000).astype(float)
X['rent_hi'] = (X.rent11 >= np.average(X.rent11, weights=X.P15)).astype(float)
X['core'] = X.city_core.astype(float)
X['coast'] = X.coastal.astype(float)
CEN = PRED + ECON
het = {}
for D in ['big', 'coast', 'rent_hi', 'core']:
    for y in ['G_vr', 'dlnR']:
        d = X.dropna(subset=[y, 'x2024', 'Z2024'] + CEN).copy()
        d['xD'] = d.x2024 * d[D]; d['zD'] = d.Z2024 * d[D]
        o = iv_multi(d, y, ['x2024', 'xD'], ['Z2024', 'zD'], [c for c in CEN if c != D] + [D], w='P15', fe=('cpro',), cluster='cpro')
        het[f'{D}|{y}'] = dict(b=o['x2024']['b'], se=o['x2024']['se'], b_int=o['xD']['b'], se_int=o['xD']['se'],
                               n=o['_n'], share=float(np.average(d[D], weights=d.P15)), nD=int(d[D].sum()))
res['heterogeneity'] = het
print(pd.DataFrame(het).T.round(3))

# ------------------------------------------------------------------ (5) AEAT 2024 by postal code
CP = pd.read_parquet(f'{CL}/aeat_cp_2024.parquet').dropna(subset=['G_vr'])
CP['lrent'] = np.log(CP.rent); CP['lvr'] = np.log(CP.vr / CP.m2)
tot = CP.G_vr.var(); within = (CP.G_vr - CP.groupby('cmun').G_vr.transform('mean')).var()
m1 = pf.feols('G_vr ~ lrent | cmun', data=CP, vcov='hetero')
m2 = pf.feols('G_vr ~ lvr | cmun', data=CP, vcov='hetero')
res['aeat_cp'] = dict(n_cp=int(len(CP)), n_cities=int(CP.cmun.nunique()), mean=float(CP.G_vr.mean()), share_pos=float((CP.G_vr > 0).mean()),
                      sd=float(CP.G_vr.std()), share_within=float(within / tot),
                      grad_rent=coefs(m1, ['lrent']), grad_vr=coefs(m2, ['lvr']),
                      cities=CP.groupby('cmun').size().to_dict())
print('AEAT CP', {k: v for k, v in res['aeat_cp'].items() if k != 'cities'})
save('e05_extensions.json', res)

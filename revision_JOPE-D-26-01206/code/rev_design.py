"""Design matrices for the shift-share analyses: shares, (leave-out) growth shocks,
residual-maker for controls + FE, 2SLS, cluster SE, AR tests (analytic, WCR, randomisation),
AKM0-type exposure-robust tests.
"""
import numpy as np, pandas as pd
from rev_common import *


def shock_arrays(base=2003, years=range(2003, 2025)):
    """g_nat[t, o] and g_prov[(pro), t, o]: changes during calendar year t over F_o,base (national)."""
    dF = flows_by_origin()
    nat, prv = shocks_counts(dF)
    s, lam, P0 = shares(base)
    Fo = s.multiply(P0, axis=0).sum()                     # national base stock by origin (excl. '00000')
    gn = nat[GROUPS].div(Fo[GROUPS], axis=1)
    gp = prv[GROUPS].div(Fo[GROUPS], axis=1)
    return gn, gp, s, P0, Fo


def obs_matrices(d, base=2003):
    """For each observation (i, t) in d: shares S (N x O) and centred leave-out growth Gl (N x O),
    centred national growth Gn (N x O). Centred = average of calendar years t-1 and t (author's timing)."""
    gn, gp, s, P0, Fo = shock_arrays(base)
    S = s.reindex(d['cmun']).fillna(0)[GROUPS].values
    cpro = d['cmun'].str[:2].values
    def leave(t):
        gnt = gn.reindex(t)[GROUPS].values
        idx = pd.MultiIndex.from_arrays([cpro, t])
        gpt = gp.reindex(idx)[GROUPS].fillna(0).values
        return gnt - gpt, gnt
    l0, n0 = leave(d['year'].values)
    l1, n1 = leave(d['year'].values - 1)
    Gl = (l0 + l1) / 2
    Gn = (n0 + n1) / 2
    return S, Gl, Gn


class Resid:
    """Weighted residual-maker for FE dummies + controls (FWL)."""
    def __init__(self, d, fe_cols, ctrl_cols, w=None):
        mats = []
        for f in fe_cols:
            mats.append(pd.get_dummies(d[f].astype(str), drop_first=False, dtype=float).values)
        if ctrl_cols:
            mats.append(d[ctrl_cols].values.astype(float))
        self.D = np.hstack(mats) if mats else np.ones((len(d), 1))
        self.w = d[w].values.astype(float) if w else np.ones(len(d))
        self.sw = np.sqrt(self.w)
        Dw = self.D * self.sw[:, None]
        U, sv, Vt = np.linalg.svd(Dw, full_matrices=False)
        r = (sv > sv.max() * 1e-10).sum()
        self.U = U[:, :r]
        self.rank = r

    def __call__(self, v):
        v = np.asarray(v, dtype=float)
        if v.ndim == 1:
            vw = v * self.sw
            return (vw - self.U @ (self.U.T @ vw)) / self.sw
        vw = v * self.sw[:, None]
        return (vw - self.U @ (self.U.T @ vw)) / self.sw[:, None]


def tsls(yr, xr, zr, w, clusters, K):
    """Just-identified 2SLS on residualised data with CRV1 SE (pyfixest-type small-sample correction)."""
    b = np.sum(w * zr * yr) / np.sum(w * zr * xr)
    e = yr - b * xr
    G = pd.Series(w * zr * e).groupby(clusters).sum().values
    ng = len(G); N = len(yr)
    c = ng / (ng - 1) * (N - 1) / (N - K)
    se = np.sqrt(c * np.sum(G ** 2)) / abs(np.sum(w * zr * xr))
    # first stage
    pi = np.sum(w * zr * xr) / np.sum(w * zr * zr)
    u = xr - pi * zr
    Gf = pd.Series(w * zr * u).groupby(clusters).sum().values
    sepi = np.sqrt(c * np.sum(Gf ** 2)) / np.sum(w * zr * zr)
    return dict(b=b, se=se, F=(pi / sepi) ** 2, pi=pi, se_pi=sepi)


def ar_analytic(yr, xr, zr, w, clusters, K, grid):
    acc = []
    ng = len(np.unique(clusters)); N = len(yr)
    c = ng / (ng - 1) * (N - 1) / (N - K)
    zz = np.sum(w * zr * zr)
    for b0 in grid:
        u = yr - b0 * xr
        g = np.sum(w * zr * u) / zz
        e = u - g * zr
        G = pd.Series(w * zr * e).groupby(clusters).sum().values
        se = np.sqrt(c * np.sum(G ** 2)) / zz
        acc.append(abs(g / se) <= 1.959964)
    return interval(grid, np.array(acc))


def interval(grid, acc):
    if not acc.any():
        return [np.nan, np.nan]
    lo, hi = grid[acc].min(), grid[acc].max()
    lo = -np.inf if acc[0] else lo
    hi = np.inf if acc[-1] else hi
    gaps = (np.diff(acc.astype(int)) != 0).sum() > 2
    return [float(lo), float(hi)] + (['non-convex'] if gaps else [])


def ar_wcr(yr, xr, zr, w, clusters, K, grid, B=9999, seed=1):
    """Wild cluster restricted bootstrap AR test with Webb six-point weights."""
    rng = np.random.default_rng(seed)
    cl = pd.factorize(clusters)[0]; ng = cl.max() + 1; N = len(yr)
    webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])
    V = webb[rng.integers(0, 6, size=(B, ng))]
    c = ng / (ng - 1) * (N - 1) / (N - K)
    zz = np.sum(w * zr * zr)
    bg = np.bincount(cl, weights=w * zr * zr, minlength=ng)
    acc = []
    for b0 in grid:
        u = yr - b0 * xr                                # null-restricted residual (controls partialled out)
        ag = np.bincount(cl, weights=w * zr * u, minlength=ng)
        g = ag.sum() / zz
        Gt = ag - g * bg
        t0 = g / (np.sqrt(c * np.sum(Gt ** 2)) / zz)
        Nst = V @ ag
        gst = Nst / zz
        Gst = V * ag[None, :] - gst[:, None] * bg[None, :]
        tst = gst / (np.sqrt(c * np.sum(Gst ** 2, axis=1)) / zz)
        p = np.mean(np.abs(tst) >= abs(t0))
        acc.append(p > 0.05)
    return interval(grid, np.array(acc))


def perm_instruments(S, G, strata, n_perm=2000, seed=7):
    """Instruments under permutations of origin growth paths within strata.
    G: N x O centred growth (leave-out). Returns (z_obs, mu, Zperm [n_perm x N])."""
    rng = np.random.default_rng(seed)
    O = S.shape[1]
    z = (S * G).sum(axis=1)
    groups = {}
    for o, st in enumerate(strata):
        groups.setdefault(st, []).append(o)
    Zp = np.empty((n_perm, S.shape[0]))
    for b in range(n_perm):
        pi = np.arange(O)
        for st, idx in groups.items():
            pi[idx] = rng.permutation(idx)
        Zp[b] = (S * G[:, pi]).sum(axis=1)
    mu = Zp.mean(axis=0)
    return z, mu, Zp


def ri_ar(yr, xr, w, z_r, Zp_r, grid):
    """Randomisation-inference AR set: statistic sum w * z~ (y - b0 x) with residualised recentred
    instruments; z_r: observed recentred residualised instrument; Zp_r: permuted (n_perm x N)."""
    a_obs, b_obs = np.sum(w * z_r * yr), np.sum(w * z_r * xr)
    a_p, b_p = Zp_r @ (w * yr), Zp_r @ (w * xr)
    acc, pv = [], []
    for b0 in grid:
        t0 = abs(a_obs - b0 * b_obs)
        tp = np.abs(a_p - b0 * b_p)
        p = np.mean(tp >= t0)
        pv.append(p); acc.append(p > 0.05)
    return interval(grid, np.array(acc)), dict(zip([float(g) for g in grid], pv))


def akm0(yr, xr, w, Sexp_r, g_hat, shock_cluster, grid):
    """AKM0-type exposure-robust test for the national-shock instrument.
    Sexp_r: N x Nshocks residualised exposures; g_hat: shocks demeaned by year (shock-level control);
    shock_cluster: cluster id of each shock (origin)."""
    acc, tvals = [], []
    sc = pd.factorize(np.asarray(shock_cluster))[0]
    for b0 in grid:
        e = yr - b0 * xr
        Rn = Sexp_r.T @ (w * e)                        # sum_i w s~_in e_i
        num = np.sum(g_hat * Rn)
        var = np.sum(np.bincount(sc, weights=g_hat * Rn) ** 2)
        t = num / np.sqrt(var)
        tvals.append(t); acc.append(abs(t) <= 1.959964)
    return interval(grid, np.array(acc))


def ri_ar_full(yr, xr, w, z_r, Zp_r, clusters, grid):
    """Randomisation-inference AR sets with three statistics:
    'sum'  : sum w z~ (y - b0 x)                 (unnormalised, as in the original manuscript)
    'coef' : reduced-form coefficient of (y - b0 x) on z~  (scale-invariant)
    't'    : cluster-robust t-statistic of that coefficient (studentised).
    Also returns first-stage randomisation p-values for 'coef' and 't'."""
    cl = pd.factorize(clusters)[0]; ng = cl.max() + 1
    Zall = np.vstack([z_r[None, :], Zp_r])                       # (1+P) x N
    zz = (Zall ** 2) @ w
    Ay = Zall @ (w * yr); Ax = Zall @ (w * xr)
    # cluster sums: (1+P) x G
    def csum(v):
        M = np.zeros((Zall.shape[0], ng))
        for g in range(ng):
            idx = cl == g
            M[:, g] = Zall[:, idx] @ v[idx]
        return M
    Cy = csum(w * yr); Cx = csum(w * xr); Cz = csum_z = None
    Bz = np.zeros((Zall.shape[0], ng))
    for g in range(ng):
        idx = cl == g
        Bz[:, g] = (Zall[:, idx] ** 2) @ w[idx]
    out = {}
    def tstat(A, C):
        coef = A / zz
        Gc = C - coef[:, None] * Bz
        return coef, coef / np.sqrt((Gc ** 2).sum(axis=1)) * 1.0
    # first stage
    cf, tf = tstat(Ax, Cx)
    out['fs_p_coef'] = float(np.mean(np.abs(cf[1:]) >= abs(cf[0])))
    out['fs_p_t'] = float(np.mean(np.abs(tf[1:]) >= abs(tf[0])))
    acc = {'sum': [], 'coef': [], 't': []}; p0 = {}
    for b0 in grid:
        A = Ay - b0 * Ax; C = Cy - b0 * Cx
        c, t = tstat(A, C)
        for k, stat in [('sum', A), ('coef', c), ('t', t)]:
            p = np.mean(np.abs(stat[1:]) >= abs(stat[0]))
            acc[k].append(p > 0.05)
            if abs(b0) < 1e-9:
                p0[k] = float(p)
    for k in acc:
        out[f'ci_{k}'] = interval(grid, np.array(acc[k]))
    out['p0'] = p0
    return out


def iv_multi(d, y, xs, zs, ctrls, w='w', fe=('cy',), cluster='cpro'):
    """2SLS with several endogenous regressors on FWL-residualised data, CRV1 covariance."""
    Rm = Resid(d, list(fe), list(ctrls), w); W_ = Rm.w
    Y = Rm(d[y].values)
    X = np.column_stack([Rm(d[x].values) for x in xs]); Z = np.column_stack([Rm(d[z].values) for z in zs])
    ZWZ = (Z * W_[:, None]).T @ Z
    Xh = Z @ np.linalg.solve(ZWZ, (Z * W_[:, None]).T @ X)
    A = (Xh * W_[:, None]).T @ X
    b = np.linalg.solve(A, (Xh * W_[:, None]).T @ Y)
    e = Y - X @ b
    cl = d[cluster].values
    sc_ = pd.DataFrame(Xh * (W_ * e)[:, None]).groupby(cl).sum().values
    ng = sc_.shape[0]; N = len(Y); K = Rm.rank + len(xs)
    c = ng / (ng - 1) * (N - 1) / (N - K)
    Ainv = np.linalg.inv(A)
    V = c * Ainv @ (sc_.T @ sc_) @ Ainv.T
    out = {x: dict(b=float(b[j]), se=float(np.sqrt(V[j, j]))) for j, x in enumerate(xs)}
    out['_V'] = V.tolist(); out['_n'] = int(N)
    return out

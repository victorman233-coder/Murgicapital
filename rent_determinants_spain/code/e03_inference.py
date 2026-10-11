"""Entry-gap paper: shift-share inference and origin placebo for the long-difference design of e01.
The long-difference instrument is a sum over origins, Z_i = sum_o s_io (P_i03/P_i15) g_io, with g_io the cumulative
leave-own-province-out change in the stock born in origin o (2015-2024) over its 2003 national stock.
1. Rotemberg weights by origin (Goldsmith-Pinkham, Sorkin and Swift 2020).
2. Randomisation inference with the recentred instrument, permuting origin shock paths across origins and within
   continents (Borusyak and Hull 2023); Anderson-Rubin sets with the cluster-robust t statistic.
3. Exposure-robust AKM0-type confidence sets with national shocks clustered by origin (Adao, Kolesar and Morales 2019).
4. Effective first-stage F: with one instrument the Montiel Olea-Pflueger effective F equals the cluster-robust F.
5. Placebo by origin income: inflows from high-income European origins vs the rest, each with its own instrument."""
import numpy as np, pandas as pd
from rd_common import *
from rev_common import GROUPS, REGION
from rev_design import Resid, tsls, ar_analytic, perm_instruments, ri_ar_full, akm0, iv_multi
from ld_shiftshare import components, flows_cum

X = pd.read_parquet(f'{CL}/e01_X.parquet')
CEN = PRED + ECON


res = {}
OUTS = {'G_vr': 2024, 'entry': 2024, 'dlnR': 2024, 'AE': 2024, 'd_uc': 2023, 'd_hhsize': 2023}
grid = np.round(np.arange(-4, 6.0001, 0.01), 3)
for y, T in OUTS.items():
    x, z = f'x{T}', f'Z{T}'
    d = X.dropna(subset=[y, x, z] + CEN).reset_index(drop=True)
    S, Gl, gn = components(d, T)
    zchk = (S * Gl).sum(axis=1)
    R = Resid(d, ['cpro'], CEN, 'P15'); wt = R.w; K = R.rank + 1
    yr, xr = R(d[y].values), R(d[x].values)
    zr = R(d[z].values)
    base = tsls(yr, xr, zr, wt, d.cpro.values, K)
    o = dict(n=len(d), b=float(base['b']), se=float(base['se']), F_eff=float(base['F']),
             check_corr=float(np.corrcoef(zchk, d[z].values)[0, 1]), check_maxdiff=float(np.max(np.abs(zchk - d[z].values))))
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values, K, grid)
    # Rotemberg weights
    Zo_r = R(S * Gl)
    den = (wt[:, None] * Zo_r * xr[:, None]).sum(0); num = (wt[:, None] * Zo_r * yr[:, None]).sum(0)
    alpha = den / den.sum(); beta_o = np.where(np.abs(den) > 0, num / den, np.nan)
    rot = pd.DataFrame({'origin': GROUPS, 'region': [REGION[g] for g in GROUPS], 'alpha': alpha, 'beta': beta_o,
                        'g_nat': gn}).sort_values('alpha', ascending=False)
    o['rotemberg'] = dict(top5=rot.head(5)[['origin', 'alpha', 'beta']].round(4).to_dict('records'),
                          sum_neg_alpha=float(alpha[alpha < 0].sum()), top5_alpha=float(rot.alpha.head(5).sum()),
                          beta_check=float(np.nansum(alpha * beta_o)),
                          share_pos_beta_weighted=float(rot.loc[rot.alpha > 0, 'alpha'][rot.beta[rot.alpha > 0] > 0].sum() / rot.alpha[rot.alpha > 0].sum()))
    if y == 'G_vr':
        rot.to_csv(os.path.join(OUT, 'e03_rotemberg_Gvr.csv'), index=False)
    # randomisation inference: recentred instrument
    o['ri'] = {}
    for sname, strata in [('all', ['all'] * len(GROUPS)), ('continent', [REGION[g] for g in GROUPS])]:
        zo, mu, Zp = perm_instruments(S, Gl, strata, n_perm=2000, seed=11)
        zt_r = R(zo - mu); Zp_r = R((Zp - mu[None, :]).T).T
        rr = tsls(yr, xr, zt_r, wt, d.cpro.values, K)
        ri = ri_ar_full(yr, xr, wt, zt_r, Zp_r, d.cpro.values, grid)
        o['ri'][sname] = dict(b=float(rr['b']), se=float(rr['se']), F=float(rr['F']), ci_t=ri['ci_t'], ci_coef=ri['ci_coef'],
                              p0_t=ri['p0'].get('t'), fs_p_t=ri['fs_p_t'])
    # AKM0 with national shocks (demeaned), one cluster per origin
    gh = gn - np.average(gn, weights=(S * wt[:, None]).sum(0))
    Sr = R(S)
    o['akm0'] = akm0(yr, xr, wt, Sr, gh, np.array(GROUPS), grid)
    res[y] = o
    print(y, {k: v for k, v in o.items() if k not in ('rotemberg',)}, o['rotemberg']['top5'][:3])

# ------------------------------------------------------------------ placebo by origin income
RICH = ['Alemania', 'Francia', 'Italia', 'Reino Unido', 'Portugal']
OTHER = [g for g in GROUPS if g not in RICH]
cum = flows_cum(2015, 2024)
plc = {}
for y in ['G_vr', 'entry', 'dlnR']:
    d = X.dropna(subset=[y, 'x2024', 'Z2024'] + CEN).reset_index(drop=True)
    S, Gl, gn = components(d, 2024)
    ir = [GROUPS.index(g) for g in RICH]; io = [GROUPS.index(g) for g in OTHER]
    d['Z_rich'] = (S[:, ir] * Gl[:, ir]).sum(1); d['Z_oth'] = (S[:, io] * Gl[:, io]).sum(1)
    c = cum.reindex(d.cmun)
    d['x_rich'] = c[RICH].sum(1).values / d.P15.values; d['x_oth'] = c[OTHER].sum(1).values / d.P15.values
    two = iv_multi(d, y, ['x_rich', 'x_oth'], ['Z_rich', 'Z_oth'], CEN, w='P15', fe=('cpro',), cluster='cpro')
    # first stages and separate just-identified IVs
    R = Resid(d, ['cpro'], CEN, 'P15'); wt = R.w; K = R.rank + 1
    sep = {}
    for g in ['rich', 'oth']:
        other = 'oth' if g == 'rich' else 'rich'
        R2 = Resid(d, ['cpro'], CEN + [f'Z_{other}'], 'P15')
        rr = tsls(R2(d[y].values), R2(d[f'x_{g}'].values), R2(d[f'Z_{g}'].values), R2.w, d.cpro.values, R2.rank + 1)
        rr['ar'] = ar_analytic(R2(d[y].values), R2(d[f'x_{g}'].values), R2(d[f'Z_{g}'].values), R2.w, d.cpro.values, R2.rank + 1, grid)
        sep[g] = {k: (float(v) if not isinstance(v, list) else v) for k, v in rr.items()}
    V = np.array(two['_V'])
    diff = two['x_oth']['b'] - two['x_rich']['b']; sed = np.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1])
    plc[y] = dict(joint={k: two[k] for k in ['x_rich', 'x_oth']}, diff=float(diff), se_diff=float(sed), n=two['_n'],
                  separate=sep, share_rich_inflow=float(np.average(d.x_rich, weights=d.P15) / np.average(d.x_rich + d.x_oth, weights=d.P15)))
    print('placebo', y, plc[y]['joint'], 'diff', round(diff, 3), round(sed, 3), {g: (round(sep[g]['b'], 3), round(sep[g]['F'], 1), sep[g]['ar']) for g in sep})
res['placebo_rich'] = plc
res['rich_origins'] = RICH
save('e03_inference.json', res)

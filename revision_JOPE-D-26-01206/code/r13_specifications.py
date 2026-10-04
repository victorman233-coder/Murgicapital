"""Stage 1C: specification battery for the rent elasticity: controls (predetermined, economic structure),
fixed effects (province x size, FUA), weights, exclusions (forest plot), placebo shares.
Central specification of the revision: province x year FE; 2003 exposure and predetermined 2011
covariates interacted with every year; weights 2003 population (paper) and renters 2011 / unweighted.
Output: out/r13_specs.json, out/r13_forest.csv"""
import numpy as np, pandas as pd
from rev_common import *
from rev_design import *

d = load_revision_panel()
grid = np.round(np.arange(-3, 4.0001, 0.01), 3)
S_all, Gl_all, Gn_all = obs_matrices(d)


def run(dd, ctrl_vars, fe=('cy',), w='w', z='Zc', x='xc', y='dlnR', extra_ctrl=()):
    dd = dd.dropna(subset=[y, x, z] + list(ctrl_vars) + ([w] if w else [])).copy().reset_index(drop=True)
    fecol = fe[0]
    dd = dd[dd.groupby(fecol).cmun.transform('size') > 1].reset_index(drop=True)
    c = year_ctrls(dd, ['forsh_base'] + list(ctrl_vars)) + list(extra_ctrl)
    Rm = Resid(dd, list(fe), c, w)
    yr, xr, zr = Rm(dd[y]), Rm(dd[x]), Rm(dd[z])
    r = tsls(yr, xr, zr, Rm.w, dd['cpro'].values, Rm.rank + 1)
    r['ar'] = ar_analytic(yr, xr, zr, Rm.w, dd['cpro'].values, Rm.rank + 1, grid)
    r['rf'] = float(np.sum(Rm.w * zr * yr) / np.sum(Rm.w * zr * zr))
    r['n'] = len(dd); r['munis'] = int(dd.cmun.nunique())
    return r

AUTH = ['lninc15', 'lnpop11', 'rent11', 'vac11']
res = {}
specs = {
    'S1_minimal': dict(ctrl_vars=[]),
    'S2_author_covariates': dict(ctrl_vars=AUTH),
    'S3_predetermined': dict(ctrl_vars=PRED),
    'S4_predetermined_econ': dict(ctrl_vars=PRED + ECON),
    'S5_pred_econ_sizeFE': dict(ctrl_vars=PRED + ECON, fe=('cy_size',)),
    'S6_pred_econ_FUAFE': dict(ctrl_vars=PRED + ECON, fe=('fuay',)),
    'S7_author_cov_sizeFE': dict(ctrl_vars=AUTH, fe=('cy_size',)),
}
for name, sp in specs.items():
    for w in ['w', 'w_rent', None]:
        r = run(d, sp['ctrl_vars'], fe=sp.get('fe', ('cy',)), w=w)
        res[f'{name}|{w or "unw"}'] = r
        print(f'{name:28s} {str(w):7s} b={r["b"]:.3f} se={r["se"]:.3f} F={r["F"]:.1f} AR={r["ar"]} n={r["n"]}')

# ------------------------------------------------------------------ exclusions and leave-one-out (forest), central spec S3, weights w
rows = []
CEN = PRED + ECON
def add(label, group, dd, **kw):
    try:
        r = run(dd, CEN, **kw)
        rows.append(dict(label=label, group=group, b=r['b'], se=r['se'], F=r['F'], ar_lo=r['ar'][0], ar_hi=r['ar'][1], n=r['n']))
    except Exception as e:
        rows.append(dict(label=label, group=group, b=np.nan, se=np.nan, F=np.nan, ar_lo=np.nan, ar_hi=np.nan, n=0))
add('Central specification', 'baseline', d)
for pr in sorted(d.cpro.unique()):
    add(f'without province {pr}', 'leave-one-province-out', d[d.cpro != pr])
for ca in sorted(d.ccaa.dropna().unique()):
    add(f'without {ca}', 'leave-one-region-out', d[d.ccaa != ca])
add('without Madrid and Barcelona provinces', 'territory', d[~d.cpro.isin(['28', '08'])])
add('without Balearic and Canary Islands', 'territory', d[~d.cpro.isin(['07', '35', '38'])])
add('without coastal municipalities', 'territory', d[d.coastal != 1])
add('without FUA core cities', 'territory', d[d.city_core != 1])
add('without largest municipality of each province', 'territory', d[d.groupby('cpro').pop11.transform('max') != d.pop11])
add('without Almería, Murcia, Huelva (agricultural SE)', 'territory', d[~d.cpro.isin(['04', '30', '21'])])
add('without Catalan rent-control municipalities', 'policy', d[(d.cat_rc2020 != 1) & (d.cat_zmrt1 != 1)])
add('without 2020-2021', 'period', d[~d.year.isin([2020, 2021])])
add('without 2024', 'period', d[d.year != 2024])
add('2015-2024 only (inflow years)', 'period', d[d.year >= 2015])
add('2012-2019 only', 'period', d[d.year <= 2019])
add('2020-2024 only', 'period', d[d.year >= 2020])
# leave-one-origin-out and leave-one-continent-out: drop origin from instrument and from total exposure
s, lam, P0 = shares(2003)
for o in GROUPS + ['cont:' + c for c in ['Europa', 'Africa', 'America', 'Asia']]:
    drop = [g for g in GROUPS if (REGION[g] == o[5:] if o.startswith('cont:') else g == o)]
    keep = [j for j, g in enumerate(GROUPS) if g not in drop]
    dd = d.copy()
    dd['Zc_lo'] = (S_all[:, keep] * Gl_all[:, keep]).sum(axis=1)
    dd['S_lo'] = S_all[:, keep].sum(axis=1)
    try:
        r = run(dd.drop(columns=['forsh_base']).rename(columns={'S_lo': 'forsh_base'}), CEN, z='Zc_lo')
        rows.append(dict(label=f'instrument without {o}', group='leave-one-origin-out' if not o.startswith('cont:') else 'leave-one-continent-out',
                         b=r['b'], se=r['se'], F=r['F'], ar_lo=r['ar'][0], ar_hi=r['ar'][1], n=r['n']))
    except Exception as e:
        print('fail', o, e)
F = pd.DataFrame(rows)
F.to_csv(os.path.join(OUT, 'r13_forest.csv'), index=False)
print(F.groupby('group')[['b', 'F']].describe().round(3).to_string())
print(F[F.group.isin(['territory', 'policy', 'period', 'leave-one-continent-out', 'baseline'])].round(3).to_string())
print(F[F.group == 'leave-one-origin-out'].sort_values('b').round(3).head(8).to_string())
print(F[F.group == 'leave-one-origin-out'].sort_values('b').round(3).tail(5).to_string())

# ------------------------------------------------------------------ placebo shares: (a) permuted share vectors within province x size; (b) pseudo-shares from observables
rng = np.random.default_rng(11)
base_r = run(d, CEN)
munis = d.drop_duplicates('cmun')[['cmun', 'cpro', 'size_cl']].reset_index(drop=True)
cells = munis.groupby(['cpro', 'size_cl']).indices
rf_perm = []
Sdf = pd.DataFrame(S_all, index=d.index)
mi = {m: i for i, m in enumerate(munis.cmun)}
row_of = d['cmun'].map(mi).values
Smuni = s.reindex(munis.cmun).fillna(0)[GROUPS].values
for b in range(300):
    perm = np.arange(len(munis))
    for k, idx in cells.items():
        perm[idx] = rng.permutation(idx)
    Sp = Smuni[perm][row_of]
    dd = d.copy(); dd['Zp'] = (Sp * Gl_all).sum(axis=1); dd['Sp'] = Sp.sum(axis=1)
    r = run(dd.drop(columns=['forsh_base']).rename(columns={'Sp': 'forsh_base'}), CEN, z='Zp')
    rf_perm.append(r['rf'])
rf_perm = np.array(rf_perm)
res['placebo_permuted_shares'] = dict(rf_obs=base_r['rf'], p=float(np.mean(np.abs(rf_perm) >= abs(base_r['rf']))),
                                      q05=float(np.percentile(rf_perm, 5)), q95=float(np.percentile(rf_perm, 95)), n=len(rf_perm))
# (b) pseudo-shares: fitted values of each origin share on predetermined characteristics + province FE (all municipalities in sample)
import pyfixest as pf
M = munis.merge(d.drop_duplicates('cmun')[['cmun'] + PRED + ECON], on='cmun')
M = M.join(pd.DataFrame(Smuni, columns=[f's{j}' for j in range(len(GROUPS))]))
Shat = np.zeros_like(Smuni)
for j in range(len(GROUPS)):
    mm = pf.feols(f's{j} ~ {" + ".join(PRED + ECON)} | cpro', data=M.fillna(M.median(numeric_only=True)))
    Shat[:, j] = np.clip(mm.predict(), 0, None)
dd = d.copy(); dd['Zps'] = (Shat[row_of] * Gl_all).sum(axis=1); dd['Sps'] = Shat[row_of].sum(axis=1)
rps = run(dd.drop(columns=['forsh_base']).rename(columns={'Sps': 'forsh_base'}), CEN, z='Zps')
res['placebo_pseudo_shares'] = dict(b=rps['b'], se=rps['se'], F=rps['F'], ar=rps['ar'], rf=rps['rf'], rf_obs=base_r['rf'])
print('placebos', res['placebo_permuted_shares'], res['placebo_pseudo_shares'])
save('r13_specs.json', res)

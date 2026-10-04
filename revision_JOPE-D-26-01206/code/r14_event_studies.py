"""Stage 1D: origin-specific event studies around push episodes, comparing municipalities exposed
to the affected origins with municipalities exposed to other origins of the SAME continent.
Episodes: Colombia + Peru (Schengen visa waivers Dec 2015 / Mar 2016) -> event 2016;
          Venezuela (crisis; national inflows accelerate) -> event 2017;
          Ukraine (war, temporary protection) -> event 2022.
Outcomes: ln R_it - ln R_i,t_X-1 (rent) and (F_it - F_i,t_X-1)/P_i,2003 (foreign-born stock).
Output: out/r14_events.csv, out/r14_events.json"""
import numpy as np, pandas as pd, pyfixest as pf
from rev_common import *
from rev_design import *

d = load_revision_panel()
s, lam, P0 = shares(2003)
lev = levels(['FOR', 'P'])
pg = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
# national series of the episode origins (for documentation)
nat = pg[pg.cmun == '00000'].sort_values(['src', 'year'])
docs = nat[['src', 'year', 'Colombia', 'Perú', 'Venezuela', 'Ucrania']].to_dict('records')

# panel of lnR and FOR stock for 2011-2024 (sample municipalities)
pan = pd.read_parquet(f'{REP}/data/clean/panel_muni_nacim.parquet')[['cmun', 'year', 'lnR']]
munis = d.cmun.unique()
pan = pan[pan.cmun.isin(munis)]
F = lev.reset_index()
F = F[F.cmun.isin(munis)][['cmun', 'year', 'FOR']]
E = pan.merge(F, on=['cmun', 'year'], how='left')
base = d.drop_duplicates('cmun').set_index('cmun')
E['cpro'] = E.cmun.str[:2]; E['cy'] = E.cpro + '_' + E.year.astype(str)
for v in ['w', 'w_rent', 'forsh_base'] + PRED + ECON:
    E[v] = E.cmun.map(base[v])
E['P03'] = E.cmun.map(P0)
EPIS = {'ColPer_2016': (['Colombia', 'Perú'], 'America', 2016),
        'Venezuela_2017': (['Venezuela'], 'America', 2017),
        'Ucrania_2022': (['Ucrania'], 'Europa', 2022)}
rows = []; summ = {}
for name, (orig, cont, tX) in EPIS.items():
    others = [g for g in GROUPS if REGION[g] == cont and g not in orig]
    e = E.copy()
    e['EX'] = e.cmun.map(s[orig].sum(axis=1)) * 100            # pp of 2003 population
    e['EO'] = e.cmun.map(s[others].sum(axis=1)) * 100
    bR = e[e.year == tX - 1].set_index('cmun')['lnR']; bF = e[e.year == tX - 1].set_index('cmun')['FOR']
    e['yR'] = e.lnR - e.cmun.map(bR)
    e['yF'] = (e.FOR - e.cmun.map(bF)) / e.P03 * 100           # pp of 2003 population
    e = e.dropna(subset=['yR', 'yF', 'EX', 'EO'] + PRED + ECON)
    yrs = sorted(e.year.unique()); ks = [y - tX for y in yrs if y != tX - 1]
    reg = []
    for y in yrs:
        if y == tX - 1:
            continue
        k = y - tX
        kn = ('m' if k < 0 else 'p') + str(abs(k)); e[f'ex_{kn}'] = e.EX * (e.year == y); e[f'eo_{kn}'] = e.EO * (e.year == y); reg += [f'ex_{kn}', f'eo_{kn}']
    ctrl = year_ctrls(e, ['forsh_base'] + PRED + ECON, 'ev')
    out = {}
    for yv in ['yR', 'yF']:
        for w in ['w', None]:
            m = pf.feols(f'{yv} ~ {" + ".join(reg + ctrl)} | cy', data=e, vcov={'CRV1': 'cpro'}, weights=w)
            t = m.tidy()
            for k in ks:
                r = t.loc['ex_' + ('m' if k < 0 else 'p') + str(abs(k))]
                rows.append(dict(episode=name, outcome=yv, w=w or 'unw', k=k, b=float(r['Estimate']), se=float(r['Std. Error'])))
            # pooled pre and post averages with Wald
            kname = lambda k: 'ex_' + ('m' if k < 0 else 'p') + str(abs(k))
            pre = [kname(k) for k in ks if k < -1]; post = [kname(k) for k in ks if k >= 0]
            V = pd.DataFrame(m._vcov, index=m.coef().index, columns=m.coef().index); b = m.coef()
            def avg(names):
                a = np.zeros(len(b)); idx = [list(b.index).index(n) for n in names]; a[idx] = 1 / len(names)
                return float(a @ b.values), float(np.sqrt(a @ V.values @ a))
            out[f'{yv}_{w or "unw"}'] = dict(pre_avg=avg(pre), post_avg=avg(post), n=int(m._N))
    # implied IV: post-average rent effect per post-average stock effect (delta-method SE ignored; report both)
    for w in ['w', 'unw']:
        r_ = out[f'yR_{w}']['post_avg']; f_ = out[f'yF_{w}']['post_avg']
        out[f'iv_ratio_{w}'] = r_[0] / f_[0] if f_[0] != 0 else None
    summ[name] = out
    print(name, json.dumps(out, default=float))
pd.DataFrame(rows).to_csv(os.path.join(OUT, 'r14_events.csv'), index=False)
save('r14_events.json', dict(summary=summ, national_series=docs))

# ------------------------------------------------------------------ DiD-IV for the Colombia+Peru episode (weak-IV robust AR set)
orig, cont, tX = EPIS['ColPer_2016']
others = [g for g in GROUPS if REGION[g] == cont and g not in orig]
e = E.copy()
e['EX'] = e.cmun.map(s[orig].sum(axis=1)) * 100
e['EO'] = e.cmun.map(s[others].sum(axis=1)) * 100
bR = e[e.year == tX - 1].set_index('cmun')['lnR']; bF = e[e.year == tX - 1].set_index('cmun')['FOR']
e['yR'] = (e.lnR - e.cmun.map(bR)) * 100                       # percent
e['yF'] = (e.FOR - e.cmun.map(bF)) / e.P03 * 100                # pp of 2003 population
e = e.dropna(subset=['yR', 'yF', 'EX', 'EO'] + PRED + ECON).reset_index(drop=True)
e['post'] = (e.year >= tX).astype(float)
e['zX'] = e.EX * e.post
grid = np.round(np.arange(-3, 5.0001, 0.01), 3)
did = {}
for w in ['w', 'w_rent', None]:
    c = year_ctrls(e, ['forsh_base', 'EO', 'EX'] + PRED + ECON, 'dd')   # EX x year absorbs nothing post? -> use EX x pre-years only
    # keep EX x year only for pre-event years (allows differential pre-trends), identification from post-period break
    c = [x for x in c if not (x.startswith('dd_EX_') and int(x.split('_')[-1]) >= tX)]
    Rm = Resid(e, ['cy'], c, w)
    yr, xr, zr = Rm(e.yR), Rm(e.yF), Rm(e.zX)
    r = tsls(yr, xr, zr, Rm.w, e.cpro.values, Rm.rank + 1)
    r['ar'] = ar_analytic(yr, xr, zr, Rm.w, e.cpro.values, Rm.rank + 1, grid)
    r['ar_wcr'] = ar_wcr(yr, xr, zr, Rm.w, e.cpro.values, Rm.rank + 1, grid, B=4999)
    did[w or 'unw'] = r
    print('ColPer DiD-IV', w, r)
summ_all = json.load(open(os.path.join(OUT, 'r14_events.json')))
summ_all['did_iv_colper'] = did
save('r14_events.json', summ_all)

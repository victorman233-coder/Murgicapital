"""Figures for 'What drives rents in Spain?' (vector PDF, same style as the companion paper)."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from rd_common import *
import rev_style
from rev_style import K, G1, G2, G3, G4, interval
FIGDIR = FIG
save_fig = lambda fig, name: (fig.savefig(os.path.join(FIGDIR, name + '.pdf')), plt.close(fig))
EN_DASH = '–'

N = pd.read_parquet(f'{CL}/national.parquet')
F = load('a01_facts.json'); T = load('a03_tourism.json'); Rg = load('a04_regulation.json')

# ------------------------------------------------------------- Fig. 1: stock vs new leases vs inflation
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.8), gridspec_kw={'wspace': 0.32})
a = ax[0]; yrs = range(2011, 2025)
a.plot(list(yrs), [100 * N.ipva[y] / N.ipva[2015] for y in yrs], color=K, lw=1.4, marker='o', ms=2.6, label='Rent index, all leases (IPVA)')
a.plot(list(yrs), [100 * N.cpi[y] / N.cpi[2015] for y in yrs], color=G2, lw=1.4, ls=(0, (3, 1.5)), label='Consumer prices')
ny = [2021, 2022, 2023, 2024]
a.plot(ny, [100 * N.ipva[2021] / N.ipva[2015] * N.ipva_new[y] / N.ipva_new[2021] for y in ny], color=K, lw=1.4, ls=':', marker='s', ms=2.6,
       label='New leases only (from 2021)')
a.set_title('(a) Spain, 2015 = 100'); a.legend(loc='upper left', handlelength=2.2); a.set_xticks([2011, 2014, 2017, 2020, 2023])
# Catalonia: new-lease deposits vs IPVA, same municipalities
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = L[L['Període'] == 'gener-desembre'].assign(cmun=lambda d: d['Codi territorial'].astype(int).astype(str).str.zfill(5))
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
cat_ip = M[M.cpro.isin(['08', '17', '25', '43'])].pivot_table(index='cmun', columns='year', values='R')
nw = La.pivot_table(index='cmun', columns='Any', values='Renda'); cnt = La.pivot_table(index='cmun', columns='Any', values='Habitatges')
both = cat_ip.index.intersection(nw.index)
yy = list(range(2013, 2025))
both = [c for c in both if nw.loc[c, yy].notna().all() and cat_ip.loc[c, yy].notna().all()]   # balanced set
w = M[M.year == 2015].set_index('cmun').P.reindex(both)
yy = list(range(2013, 2025))
new_idx = [np.average(nw.loc[both, y] / nw.loc[both, 2015], weights=w) * 100 for y in yy]
st_idx = [np.average(cat_ip.loc[both, y] / cat_ip.loc[both, 2015], weights=w) * 100 for y in yy]
a = ax[1]
a.plot(yy, new_idx, color=K, lw=1.4, ls=':', marker='s', ms=2.6, label='New leases (deposit register)')
a.plot(yy, st_idx, color=K, lw=1.4, marker='o', ms=2.6, label='All leases (IPVA)')
a.plot(yy, [100 * N.cpi[y] / N.cpi[2015] for y in yy], color=G2, lw=1.4, ls=(0, (3, 1.5)), label='Consumer prices')
a.set_title(f'(b) Catalonia, {len(both)} municipalities, 2015 = 100'); a.legend(loc='upper left', handlelength=2.2)
a.set_xticks([2013, 2016, 2019, 2022])
save_fig(fig, 'fig1_index')

# ------------------------------------------------------------- Fig. 2: tourist dwellings and rents
fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.6), gridspec_kw={'wspace': 0.38})
e = T['ipva_event']; ys = [y for y in range(2012, 2025)]
b = [0 if y == 2019 else 100 * e[f'E_{y}']['b'] for y in ys]; s = [0 if y == 2019 else 100 * e[f'E_{y}']['se'] for y in ys]
a = ax[0]
a.fill_between(ys, np.array(b) - 1.96 * np.array(s), np.array(b) + 1.96 * np.array(s), color=G4, lw=0)
a.axhline(0, color=G2, lw=0.6); a.axvspan(2019.5, 2021.5, color=G4, alpha=0.5, lw=0)
a.plot(ys, b, color=K, lw=1.1); a.plot([y for y in ys if y != 2019], [v for y, v in zip(ys, b) if y != 2019], 'o', color=K, ms=3)
a.plot([2019], [0], 'o', color=K, mfc='white', ms=3.4, mew=0.9)
a.set_title('(a) All leases (IPVA), Spain'); a.set_ylabel('% per pp of dwellings in tourist use'); a.set_xticks([2012, 2016, 2020, 2024])
for j, (y, ttl) in enumerate([('lnrent', '(b) New-lease rents, Catalonia'), ('lnn', '(c) New leases signed, Catalonia')]):
    ev = T[f'cat_event_{y}']
    qs = [f'{yr}q{q}' for yr in range(2019, 2026) for q in (1, 2, 3, 4)]
    xs, bb, ss = [], [], []
    for i, q in enumerate(qs):
        k = f'E_{q}'
        xs.append(2019 + i / 4)
        if q.startswith('2019'):
            bb.append(0); ss.append(0)
        else:
            bb.append(100 * ev[k]['b']); ss.append(100 * ev[k]['se'])
    a = ax[j + 1]; xs = np.array(xs); bb = np.array(bb); ss = np.array(ss)
    a.fill_between(xs, bb - 1.96 * ss, bb + 1.96 * ss, color=G4, lw=0)
    a.axhline(0, color=G2, lw=0.6); a.axvspan(2020.25, 2021.5, color=G4, alpha=0.5, lw=0)
    a.plot(xs, bb, color=K, lw=1.0, marker='o', ms=2.2)
    a.set_title(ttl); a.set_xticks([2019, 2021, 2023, 2025])
fig.text(0.5, -0.04, 'Shaded band: tourism collapse (2020' + EN_DASH + '21). Reference: 2019. Bands: 95% intervals.', ha='center', fontsize=7, color=G1)
save_fig(fig, 'fig2_tourism')

# ------------------------------------------------------------- Fig. 3: tensioned-zone cap (Catalonia)
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.7), gridspec_kw={'wspace': 0.3})
for a, (y, ttl) in zip(ax, [('lnrent', '(a) New-lease rents (log points)'), ('lnn', '(b) New leases signed (log points)')]):
    for lab, key, mk, col, off in [('Wave 1 (March 2024) vs never designated', 'zmrt1_vs_never', 'o', K, -0.12),
                                   ('Wave 2 (October 2024) vs never designated', 'zmrt2_vs_never', 's', G1, 0.12)]:
        ev = Rg[key][y]['event']
        ks, bb, ss = [-1], [0.0], [0.0]
        for n, v in ev.items():
            if not isinstance(v, dict):
                continue
            k = -int(n[3:]) if n.startswith('r_m') else int(n[3:])
            if k < -8:
                continue
            ks.append(k); bb.append(v['b']); ss.append(v['se'])
        o = np.argsort(ks); ks = np.array(ks)[o] + off; bb = np.array(bb)[o]; ss = np.array(ss)[o]
        a.errorbar(ks, bb, yerr=1.96 * ss, fmt=mk, color=col, ms=3, elinewidth=0.7, capsize=0, mfc=col if mk == 'o' else 'white', label=lab)
    a.axhline(0, color=G2, lw=0.6); a.axvline(-0.5, color=G2, lw=0.6, ls=(0, (1, 1.5)))
    a.set_title(ttl); a.set_xlabel('Quarters relative to the first full quarter of the cap')
ax[0].legend(loc='lower left', fontsize=6.6)
save_fig(fig, 'fig3_cap')
print('figures written')

# ------------------------------------------------------------- Fig. 4: ranking of contributions (log points, 2015-2024)
Kr = load('a06_ranking.json'); A = Kr['A_national_stock']
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.5), gridspec_kw={'width_ratios': [1, 1.25], 'wspace': 0.9})
acc = [('Index for all leases', 100 * A['total'], None), ('Consumer prices', 100 * A['cpi'], None),
       ('Cap on updates, 2022' + EN_DASH + '23', 100 * A['update_cap']['contrib'], None)]
a = ax[0]
for i, (lab, v, _) in enumerate(acc):
    a.barh(-i, v, color=K if i == 0 else G2, height=0.55, edgecolor='white')
    a.text(v + (0.6 if v >= 0 else -0.6), -i, f'{v:.1f}'.replace('-', '\u2212'), va='center', ha='left' if v >= 0 else 'right', fontsize=7)
a.set_yticks([-i for i in range(len(acc))]); a.set_yticklabels([r[0] for r in acc]); a.tick_params(axis='y', length=0)
a.axvline(0, color=G2, lw=0.6); a.set_xlim(-10, 27); a.spines['left'].set_visible(False)
a.set_title('(a) Accounting, Spain'); a.set_xlabel('Log points, 2015' + EN_DASH + '2024')
loc = [('Population (immigration), IV', 100 * A['population']['contrib'], (100 * A['population']['lo'], 100 * A['population']['hi']), True),
       ('Real income, OLS', 100 * A['income_ols']['contrib'], (100 * A['income_ols']['lo'], 100 * A['income_ols']['hi']), False),
       ('Tourist dwellings, 2015' + EN_DASH + '19', 100 * A['tourism']['contrib_2015_2019'], None, True),
       ('Tourist dwellings, 2019' + EN_DASH + '24', 100 * A['tourism']['contrib_2019_2024'], None, True)]
a = ax[1]
for i, (lab, v, ci, ident) in enumerate(loc):
    if ci:
        a.plot(ci, [-i, -i], color=G1, lw=1.0)
    a.plot(v, -i, 'o', color=K, ms=4, mfc=K if ident else 'white', mew=0.9)
a.set_yticks([-i for i in range(len(loc))]); a.set_yticklabels([r[0] for r in loc]); a.tick_params(axis='y', length=0)
a.axvline(0, color=G2, lw=0.6); a.spines['left'].set_visible(False); a.set_ylim(-len(loc) + 0.5, 0.5)
a.set_title('(b) Local channels, aggregated'); a.set_xlabel('Log points, 2015' + EN_DASH + '2024')
save_fig(fig, 'fig4_ranking')

# ------------------------------------------------------------- Fig. 5: by municipality size
D = Kr['D_by_size']; labs = SIZE_LABELS
fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.4), gridspec_kw={'wspace': 0.45})
xs = np.arange(len(labs)); nice = [l.replace('k', ',000').replace('-', EN_DASH).replace('>', '>') for l in ['10-20k', '20-50k', '50-100k', '100-500k', '>500k']]
nice = ['10' + EN_DASH + '20k', '20' + EN_DASH + '50k', '50' + EN_DASH + '100k', '100' + EN_DASH + '500k', '>500k']
ax[0].bar(xs, [100 * D[k]['dlnR'] for k in labs], color=K, width=0.6, edgecolor='white'); ax[0].set_title('(a) Rent index growth')
ax[1].bar(xs, [100 * D[k]['inflow'] for k in labs], color=G1, width=0.6, edgecolor='white'); ax[1].set_title('(b) Foreign-born inflow, % of pop.')
ax[2].bar(xs, [D[k]['vut20'] for k in labs], color=G2, width=0.6, edgecolor='white', label='Mean')
ax[2].plot(xs, [D[k]['vut20_p90'] for k in labs], 'v', color=K, ms=4, label='90th percentile'); ax[2].set_title('(c) Tourist dwellings, % (2020)')
ax[2].set_ylim(0, 6.2); ax[2].legend(loc='upper right', fontsize=6.5)
for a in ax:
    a.set_xticks(xs); a.set_xticklabels(nice, rotation=35, ha='right', fontsize=6.8); a.tick_params(axis='x', length=0)
ax[0].set_ylabel('Log points, 2015' + EN_DASH + '2024')
save_fig(fig, 'fig5_size')
print('ranking figures written')

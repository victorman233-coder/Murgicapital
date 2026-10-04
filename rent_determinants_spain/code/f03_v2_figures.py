"""Figures for 'Insiders and Outsiders in the Rental Market' (vector PDF, greyscale, companion-paper style)."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from rd_common import *
import rev_style
from rev_style import K, G1, G2, G3, G4
D = '–'; MINUS = '−'
FV = os.path.join(HERE, '..', 'paper_v2', 'fig'); os.makedirs(FV, exist_ok=True)
sv = lambda fig, n: (fig.savefig(os.path.join(FV, n + '.pdf')), plt.close(fig))
E1 = load('e01_main.json'); E2 = load('e02_panels_regulation.json')
M = pd.read_parquet(f'{CL}/muni_panel.parquet'); A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
uc = A[A.indicator == 'Mediana de la renta por unidad de consumo'].pivot_table(index='cmun', columns='year', values='value')
pr = M.pivot_table(index='cmun', columns='year', values='lnR'); P = M[M.year == 2015].set_index('cmun').P

# ------------------------------------------------------------- Fig 1: insiders vs entrants
X = pd.DataFrame({'dR': 100 * (pr[2023] - pr[2015]), 'dY': 100 * np.log(uc[2023] / uc[2015]), 'P': P}).dropna()
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = L[L['Període'] == 'gener-desembre'].assign(cmun=lambda d: d['Codi territorial'].astype(int).astype(str).str.zfill(5))
nw = La.pivot_table(index='cmun', columns='Any', values='Renda'); nn = La.pivot_table(index='cmun', columns='Any', values='Habitatges')
Cc = pd.DataFrame({'dN': 100 * np.log(nw[2023] / nw[2015]), 'dY': 100 * np.log(uc[2023] / uc[2015]).reindex(nw.index), 'n15': nn[2015]})
Cc = Cc[Cc.n15 >= 30].dropna()
Em = pd.read_parquet(f'{CL}/emal_muni.parquet'); pm = Em.pivot_table(index='cmun', columns='year', values='rent_m2_new')
Bq = pd.DataFrame({'dN': 100 * np.log(pm[2023] / pm[2016]), 'dY': 100 * np.log(uc[2023] / uc[2016]).reindex(pm.index)}).dropna()
fig, ax = plt.subplots(1, 2, figsize=(6.9, 3.2), gridspec_kw={'wspace': 0.3})
a = ax[0]
a.scatter(X.dY, X.dR, s=4 + 50 * np.sqrt(X.P / X.P.max()), facecolors='none', edgecolors=G3, lw=0.5, label=f'All leases (IPVA), 2015{D}23')
a.scatter(Cc.dY, Cc.dN, s=9, color=K, marker='^', lw=0, label=f'New leases, Catalonia, 2015{D}23')
a.scatter(Bq.dY, Bq.dN, s=12, facecolors='white', edgecolors=G1, marker='s', lw=0.8, label=f'New leases per m², Basque C., 2016{D}23')
a.plot([0, 75], [0, 75], color=G1, lw=0.8, ls=(0, (3, 1.5))); a.text(64, 67, '45°', fontsize=7, color=G1)
a.set_xlim(0, 75); a.set_ylim(-5, 75)
a.set_xlabel('Income growth per consumption unit (log points)'); a.set_ylabel('Rent growth (log points)')
a.set_title('(a) Rent vs income growth, by municipality'); a.legend(loc='upper left', fontsize=6.4)
b = ax[1]
labs = ['10' + D + '20k', '20' + D + '50k', '50' + D + '100k', '100' + D + '500k', '>500k']
X['size'] = pd.cut(X.P, SIZE_EDGES, labels=SIZE_LABELS)
Cc['P'] = P.reindex(Cc.index); Cc = Cc.dropna(subset=['P']); Cc['size'] = pd.cut(Cc.P, SIZE_EDGES, labels=SIZE_LABELS)
ins = [wmean((X.dR - X.dY)[X['size'] == k].values, X.P[X['size'] == k].values) for k in SIZE_LABELS]
ent = [wmean((Cc.dN - Cc.dY)[Cc['size'] == k].values, Cc.P[Cc['size'] == k].values) if (Cc['size'] == k).any() else np.nan for k in SIZE_LABELS]
xs = np.arange(5); w = 0.36
b.bar(xs - w / 2, ins, w, color=G3, edgecolor='white', label='Insiders: all leases, Spain')
b.bar(xs + w / 2, ent, w, color=K, edgecolor='white', label='Entrants: new leases, Catalonia')
b.axhline(0, color=G1, lw=0.6); b.set_ylim(-24, 30)
b.set_xticks(xs); b.set_xticklabels(labs, rotation=30, ha='right', fontsize=7); b.tick_params(axis='x', length=0)
b.set_ylabel(f'Rent minus income growth, 2015{D}23 (log pts)'); b.set_title('(b) Change in rent-to-income, by size')
b.legend(loc='upper left', fontsize=6.4)
sv(fig, 'fig1_insiders_entrants')

# ------------------------------------------------------------- Fig 2: entry gap over time (INE) and in levels (AEAT 2024)
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.typ == 'Índice')].pivot_table(index=['prov', 'year'], columns='age', values='val').reset_index()
pa['gap'] = 100 * np.log(pa['Nuevo contrato'] / pa['Contrato existente'])
nat = pa[pa.prov == '00'].set_index('year').gap
pv = pa[pa.prov != '00'].pivot_table(index='prov', columns='year', values='gap')
AE = pd.read_parquet(f'{CL}/aeat_entry_gap_2024.parquet').set_index('cmun')
AE['P'] = P.reindex(AE.index); AE = AE.dropna(subset=['P'])
AE['size'] = pd.cut(AE.P, SIZE_EDGES, labels=SIZE_LABELS)
fig, ax = plt.subplots(1, 2, figsize=(6.9, 2.9), gridspec_kw={'wspace': 0.32})
a = ax[0]
for p in pv.index:
    a.plot(pv.columns, pv.loc[p].values, color=G4, lw=0.6)
a.plot(nat.index, nat.values, color=K, lw=1.6, marker='o', ms=3, label='Spain')
a.set_xticks([2021, 2022, 2023, 2024]); a.set_ylabel('log(new) − log(existing), ×100')
a.set_title('(a) Entry gap since 2015, INE indices'); a.text(2021.05, nat.max() * 0.95, 'grey: 48 provinces', fontsize=6.6, color=G1)
b = ax[1]
vals = [100 * AE.G_vr[AE['size'] == k].values for k in SIZE_LABELS]
bp = b.boxplot(vals, widths=0.5, patch_artist=True, showfliers=False, medianprops=dict(color=K, lw=1.2), whiskerprops=dict(color=G1, lw=0.7),
               capprops=dict(color=G1, lw=0.7), boxprops=dict(facecolor=G4, edgecolor=G1, lw=0.7))
b.axhline(0, color=G1, lw=0.6)
b.set_xticks(range(1, 6)); b.set_xticklabels(labs, rotation=30, ha='right', fontsize=7); b.tick_params(axis='x', length=0)
b.set_ylabel('Quality-adjusted entry gap, 2024 (log pts)'); b.set_title('(b) Entry gap in levels, AEAT 2024')
sv(fig, 'fig2_entry_gap')

# ------------------------------------------------------------- Fig 3: where the demand shock goes (2SLS)
m = E1['main']
rows = [('Rent, all leases (2015' + D + '24)', 'dlnR'), ('Entry gap, quality-adjusted (2024)', 'G_vr'), ('Implied entry rent', 'entry'),
        ('Income per consumption unit', 'd_uc'), ('Income per person', 'd_pp'), ('Income per household', 'd_hh'), ('Household size', 'd_hhsize'),
        ('Population', 'dP2024'), ('Dwelling stock (cadastre)', 'dlnviv'),
        ('Affordability, insiders', 'AI'), ('Affordability, entrants', 'AE')]
fig, a = plt.subplots(figsize=(5.6, 3.6))
for i, (lab, k) in enumerate(rows):
    q = m[k]; lo, hi = q['ar'][0], q['ar'][1]
    y = -i - (0.5 if i >= 3 else 0) - (0.5 if i >= 7 else 0) - (0.5 if i >= 9 else 0)
    a.plot([max(lo, -1.5), min(hi, 2.6)], [y, y], color=G1, lw=1.0)
    if hi > 2.6:
        a.plot(2.6, y, '>', color=G1, ms=3, clip_on=False)
    a.plot(q['b'], y, 'o', color=K, ms=4)
    a.text(-1.62, y, lab, ha='right', va='center', fontsize=7)
a.axvline(0, color=G3, lw=0.7); a.set_xlim(-1.5, 2.6); a.set_yticks([]); a.spines['left'].set_visible(False)
a.set_xlabel('2SLS effect of a cumulative inflow of 1% of the population (log points ×100 per pp)')
sv(fig, 'fig3_where_shock_goes')

# ------------------------------------------------------------- Fig 4: supply rigidity and the entry gap (marginal effect)
X1 = pd.read_parquet(f'{CL}/e01_X.parquet')
r = E1['rigidity']['G_vr|undev10']; rr = E1['rigidity']['dlnR|undev10']
u = X1.undev10.dropna(); mu = np.average(u, weights=X1.loc[u.index, 'P15']); sd = u.std()
grid = np.linspace(np.percentile(u, 5), np.percentile(u, 95), 40); zs = (grid - mu) / sd
fig, a = plt.subplots(figsize=(4.4, 3.0))
for rr_, lab, col, ls in [(r, 'Entry gap (quality-adjusted)', K, '-'), (rr, 'Rent, all leases', G2, (0, (3, 1.5)))]:
    me = rr_['b_x'] + rr_['b_xR'] * zs
    se = np.sqrt(rr_['se_x'] ** 2 + zs ** 2 * rr_['se_xR'] ** 2 + 2 * zs * rr_['cov'])
    if col == K:
        a.fill_between(100 * grid, me - 1.96 * se, me + 1.96 * se, color=G4, lw=0)
    a.plot(100 * grid, me, color=col, lw=1.4, ls=ls, label=lab)
a.axhline(0, color=G3, lw=0.7)
a.set_ylim(-2.2, 2.6)
a.set_xlabel('Undevelopable land within 10 km (% of area: sea or slope >15%)'); a.set_ylabel('Effect of a 1 pp inflow')
a.legend(loc='upper left', fontsize=6.8); a.set_title('Demand shock × geographic constraint', fontsize=8)
sv(fig, 'fig4_rigidity')

# ------------------------------------------------------------- Fig 5: tourism thresholds (Catalan new leases)
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.7), gridspec_kw={'wspace': 0.32})
bins = ['b1', 'b2', 'b3']; bl = ['1' + D + '3%', '3' + D + '8%', '>8%']
for a, (y, ttl) in zip(ax, [('lnrent', '(a) New-lease rents'), ('lnn', '(b) New leases signed')]):
    t = E2[f'tour_bins_{y}']
    for j, (p, lab, col, mk) in enumerate([('covid', f'Collapse 2020Q2' + D + '21Q2', K, 'o'), ('recov', 'Recovery 2022' + D + '23', G2, 's')]):
        b_ = [100 * t[f'{b}_{p}']['b'] for b in bins]; s_ = [100 * t[f'{b}_{p}']['se'] for b in bins]
        xs = np.arange(3) + (j - 0.5) * 0.22
        a.errorbar(xs, b_, yerr=1.96 * np.array(s_), fmt=mk, color=col, ms=4, elinewidth=0.8, capsize=0, label=lab, mfc=col if mk == 'o' else 'white')
    a.axhline(0, color=G3, lw=0.7); a.set_xticks(range(3)); a.set_xticklabels(bl); a.set_xlabel('Dwellings in tourist use, 2020')
    a.set_title(ttl); a.set_ylabel('% vs municipalities below 1%')
ax[0].legend(loc='lower left', fontsize=6.6)
sv(fig, 'fig5_tourism_threshold')

# ------------------------------------------------------------- Fig 6: regulation and substitution towards seasonal leases
ev = E2['zmrt_seasonal']['sh_seas_event1']
ks, bb, ss = [-1], [0.0], [0.0]
for n, v in ev.items():
    if isinstance(v, dict):
        ks.append(-int(n[2:]) if n.startswith('em') else int(n[2:])); bb.append(100 * v['b']); ss.append(100 * v['se'])
o = np.argsort(ks); ks = np.array(ks)[o]; bb = np.array(bb)[o]; ss = np.array(ss)[o]
fig, a = plt.subplots(figsize=(4.4, 2.8))
a.fill_between(ks, bb - 1.96 * ss, bb + 1.96 * ss, color=G4, lw=0); a.plot(ks, bb, color=K, lw=1.1, marker='o', ms=3)
a.axhline(0, color=G3, lw=0.7); a.axvline(-0.5, color=G2, lw=0.6, ls=(0, (1, 1.5)))
a.set_xlabel('Quarters relative to the cap (wave 1, 2024Q2)'); a.set_ylabel('Seasonal share of new leases (pp)')
a.set_title('Tensioned-zone cap and seasonal leases, Catalonia', fontsize=8)
sv(fig, 'fig6_cap_seasonal')
print('v2 figures written')

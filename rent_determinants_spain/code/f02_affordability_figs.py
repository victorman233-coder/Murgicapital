"""Figures for the redesign proposal: rent growth vs income growth (insiders vs entrants)."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from rd_common import *
import rev_style
from rev_style import K, G1, G2, G3, G4
D = '–'
M = pd.read_parquet(f'{CL}/muni_panel.parquet'); A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
inc = A[A.indicator == 'Mediana de la renta por unidad de consumo'].pivot_table(index='cmun', columns='year', values='value')
pr = M.pivot_table(index='cmun', columns='year', values='lnR'); P = M[M.year == 2015].set_index('cmun').P
X = pd.DataFrame({'dR': 100 * (pr[2023] - pr[2015]), 'dY': 100 * np.log(inc[2023] / inc[2015]), 'P': P}).dropna()
C = pd.read_parquet(f'{CL}/b01_catalonia_ld.parquet')
C['dYuc'] = 100 * np.log(inc[2023] / inc[2015]).reindex(C.index)
C = C.dropna(subset=['dYuc'])
fig, ax = plt.subplots(1, 2, figsize=(6.8, 3.1), gridspec_kw={'wspace': 0.32})
a = ax[0]
s = 4 + 60 * np.sqrt(X.P / X.P.max())
a.scatter(X.dY, X.dR, s=s, facecolors='none', edgecolors=G2, lw=0.5, label='All leases (IPVA), 703 municipalities')
a.scatter(C.dYuc, 100 * C.d_new, s=10, color=K, marker='^', lw=0, label='New leases, Catalonia (123)')
lim = [0, 75]; a.plot(lim, lim, color=G1, lw=0.8, ls=(0, (3, 1.5)))
a.text(62, 66, '45°', fontsize=7, color=G1)
a.set_xlim(*lim); a.set_ylim(-5, 75)
a.set_xlabel(f'Income growth 2015{D}2023 (log points)'); a.set_ylabel(f'Rent growth 2015{D}2023 (log points)')
a.set_title('(a) Rent vs income growth, by municipality'); a.legend(loc='upper left', fontsize=6.6)
b = ax[1]
labs = ['10' + D + '20k', '20' + D + '50k', '50' + D + '100k', '100' + D + '500k', '>500k']
C['size'] = pd.cut(C.P, SIZE_EDGES, labels=SIZE_LABELS)
X['size'] = pd.cut(X.P, SIZE_EDGES, labels=SIZE_LABELS)
ent = [wmean((100 * C.d_new - C.dYuc)[C['size'] == k].values, C.P[C['size'] == k].values) for k in SIZE_LABELS]
ins = [wmean((X.dR - X.dY)[X['size'] == k].values, X.P[X['size'] == k].values) for k in SIZE_LABELS]
xs = np.arange(5); w = 0.36
b.bar(xs - w / 2, ins, w, color=G3, edgecolor='white', label='Incumbents: all leases, Spain')
b.bar(xs + w / 2, ent, w, color=K, edgecolor='white', label='Entrants: new leases, Catalonia')
b.axhline(0, color=G1, lw=0.6)
b.set_xticks(xs); b.set_xticklabels(labs, rotation=30, ha='right', fontsize=7); b.tick_params(axis='x', length=0)
b.set_ylabel('Rent minus income growth (log points)'); b.set_title('(b) Change in rent-to-income, by size')
b.legend(loc='upper left', fontsize=6.6); b.set_ylim(-24, 30)
fig.savefig(os.path.join(FIG, 'figP1_rent_vs_income.pdf')); plt.close(fig)
print('ok', len(X), len(C), [round(v, 1) for v in ins], [round(v, 1) for v in ent])

# entry gap by province, 2021-2024 (INE new vs existing leases) against foreign-born inflow
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.typ == 'Índice') & (pa.prov != '00')].pivot_table(index=['prov', 'year'], columns='age', values='val').unstack('year')
gap = 100 * (np.log(pa[('Nuevo contrato', 2024)] / pa[('Nuevo contrato', 2021)]) - np.log(pa[('Contrato existente', 2024)] / pa[('Contrato existente', 2021)]))
lev = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
pp = lev[(lev.cmun.str.len() == 5) & (lev.cmun != '00000')].assign(prov=lambda d: d.cmun.str[:2])
c21 = pp[(pp.src == 'censo') & (pp.year == 2021)].groupby('prov')[['P', 'FOR']].sum(); c24 = pp[(pp.src == 'censo') & (pp.year == 2024)].groupby('prov')[['P', 'FOR']].sum()
G = pd.DataFrame({'gap': gap, 'inflow': 100 * (c24.FOR - c21.FOR) / c21.P, 'P': c21.P}).dropna()
fig, a = plt.subplots(figsize=(4.2, 3.0))
a.scatter(G.inflow, G.gap, s=6 + 80 * np.sqrt(G.P / G.P.max()), facecolors='none', edgecolors=K, lw=0.7)
for p, nm in [('28', 'Madrid'), ('08', 'Barcelona'), ('46', 'Valencia'), ('29', 'Málaga'), ('07', 'Balearic Is.')]:
    if p in G.index:
        a.annotate(nm, (G.loc[p, 'inflow'], G.loc[p, 'gap']), xytext=(4, 2), textcoords='offset points', fontsize=6.6)
bfit = np.polyfit(G.inflow, G.gap, 1, w=np.sqrt(G.P)); xx = np.linspace(G.inflow.min(), G.inflow.max(), 10)
a.plot(xx, np.polyval(bfit, xx), color=G2, lw=0.8)
a.set_xlabel(f'Foreign-born net inflow 2021{D}2024 (% of 2021 population)'); a.set_ylabel('Entry gap opened (log points)')
a.set_title(f'Entry gap, new vs existing leases, 2021{D}2024', fontsize=8)
fig.savefig(os.path.join(FIG, 'figP2_entry_gap_prov.pdf')); plt.close(fig)
print('prov', len(G), round(G.gap.mean(), 1), round(G.gap.min(), 1), round(G.gap.max(), 1))

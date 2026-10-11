"""Context figure (Fig. 1) and maps, rebuilt from the raw INE, Eurostat and IGN files.
Fig. 1: foreign-born share (register and census), national IPVA, EU-SILC overcrowding and tenure.
Maps: net foreign-born inflow and IPVA change, 2015-2024, with explicit categories for net decreases and missing data."""
import json, os
import numpy as np, pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle
from rev_style import K, G1, G2, G3, G4, save
from rev_common import WORK, OUT

RAW = f'{WORK}/raw'


def ine_csv(t):
    d = pd.read_csv(f'{RAW}/ine_{t}.csv', sep=';', encoding='utf-8-sig', dtype=str)
    d['v'] = pd.to_numeric(d['Total'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    return d


def eurostat(f):
    """Decode a JSON-stat 2.0 file into a long DataFrame."""
    d = json.load(open(f'{RAW}/eurostat/{f}'))
    dims, size = d['id'], d['size']
    lab = {k: {i: c for c, i in d['dimension'][k]['category']['index'].items()} for k in dims}
    rows = []
    for pos, v in d['value'].items():
        pos = int(pos); r = {}
        for k, s in zip(reversed(dims), reversed(size)):
            r[k] = lab[k][pos % s]; pos //= s
        r['value'] = v; rows.append(r)
    out = pd.DataFrame(rows); out['year'] = out['time'].astype(int)
    return out


# ============================================================== Fig. 1: national context
lev = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
nat = lev[lev.cmun == '00000'].assign(sh=lambda d: 100 * d.FOR / d.P)
pad = nat[nat.src == 'padron'].sort_values('year'); cen = nat[nat.src == 'censo'].sort_values('year')
ip = ine_csv(59060)
ip = ip[(ip.Municipio == 'Total Nacional') & (ip['Tipo de dato'] == 'Índice')].assign(year=lambda d: d.Periodo.astype(int)).sort_values('year')
oc = eurostat('ilc_lvho15_ES.json'); te = eurostat('ilc_lvps15_ES.json')
oc = oc[(oc.sex == 'T') & (oc.age == 'Y_GE18')]
te = te[(te.tenure == 'RENT') & (te.sex == 'T') & (te.age == 'Y_GE18')]
years = np.arange(2011, 2026)

fig, axs = plt.subplots(2, 2, figsize=(6.2, 4.7))
a = axs[0, 0]
a.plot(pad.year, pad.sh, color=K, lw=1.3, label='Municipal register (2003\u20132022)')
a.plot(cen.year, cen.sh, color=K, lw=1.3, ls=(0, (3, 1.5)), label='Annual census (2021\u20132025)')
a.set_title('(a) Foreign-born population'); a.set_ylabel('% of population')
a.set_xticks([2003, 2008, 2013, 2018, 2023]); a.set_xlim(2002.3, 2025.7); a.legend(loc='upper left')
a = axs[0, 1]
a.axhline(100, color=G3, lw=0.6)
a.plot(ip.year, ip.v, color=K, lw=1.3, marker='o', ms=2.6)
a.set_title('(b) Rental housing price index (IPVA)'); a.set_ylabel('Index, 2015 = 100')
a.set_xticks([2011, 2014, 2017, 2020, 2023]); a.set_xlim(2010.3, 2024.7)
for a, df, ttl in [(axs[1, 0], oc, '(c) Overcrowding rate'), (axs[1, 1], te, '(d) Adults living in rented housing')]:
    for cit, col, lab in [('FOR', K, 'Foreign citizens'), ('NAT', G2, 'Spanish citizens')]:
        s = df[df.citizen == cit].set_index('year')['value'].reindex(years)   # missing years stay NaN: the line breaks
        a.plot(years, s.values, color=col, lw=1.3, marker='o', ms=2.6, label=lab)
    a.set_title(ttl); a.set_ylim(0, None); a.set_ylabel('% of adults')
    a.set_xticks([2011, 2015, 2019, 2023]); a.set_xlim(2010.3, 2025.7)
axs[1, 0].legend(loc='upper left', bbox_to_anchor=(0.0, 0.93))
miss = [y for y in years if not np.isfinite(te[te.citizen == 'FOR'].set_index('year')['value'].reindex([y]).iloc[0])]
for y in miss:   # Eurostat did not publish the tenure split for these years
    axs[1, 1].text(y, 42, f'{y}\nnot\npublished', ha='center', va='center', fontsize=6.3, color=G1, linespacing=0.95)
fig.tight_layout(h_pad=1.2, w_pad=1.6); save(fig, 'fig1_contexto')

# ============================================================== Maps
T = json.load(open(f'{RAW}/geo/municipalities.json'))
sc, tr = T['transform']['scale'], T['transform']['translate']
arcs = []
for arc in T['arcs']:
    x = y = 0; pts = []
    for dx, dy in arc:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)


def ring(idx):
    pts = []
    for i in idx:
        seg = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(seg if not pts else seg[1:])
    return np.array(pts)


CAN = np.array([5.0, 7.0])                 # Canary Islands moved to an inset
polys = {}
for g in T['objects']['municipalities']['geometries']:
    if g['id'][:2] == '54':                # Gibraltar is not part of the INE municipal register
        continue
    P = [g['arcs']] if g['type'] == 'Polygon' else g['arcs'] if g['type'] == 'MultiPolygon' else []
    polys[g['id']] = [ring(p[0]) + (CAN if g['id'][:2] in ('35', '38') else 0) for p in P]
prov = []
for g in T['objects']['provinces']['geometries']:
    P = [g['arcs']] if g['type'] == 'Polygon' else g['arcs']
    prov += [ring(p[0]) + (CAN if g.get('id', '')[:2] in ('35', '38') else 0) for p in P]

# net foreign-born inflow 2015-2024: register 2015->2021 plus census 2021->2024 (differences within source)
p15 = lev[(lev.src == 'padron') & (lev.year == 2015)].set_index('cmun'); p21 = lev[(lev.src == 'padron') & (lev.year == 2021)].set_index('cmun')
c21 = lev[(lev.src == 'censo') & (lev.year == 2021)].set_index('cmun'); c24 = lev[(lev.src == 'censo') & (lev.year == 2024)].set_index('cmun')
inflow = (100 * ((p21.FOR - p15.FOR) + (c24.FOR - c21.FOR)) / p15.P).replace([np.inf, -np.inf], np.nan).dropna().drop('00000', errors='ignore')
# municipal IPVA (base 2015 = 100)
im = ine_csv(59060)
im = im[(im['Tipo de dato'] == 'Índice') & im.Municipio.str[:5].str.isdigit()].assign(cmun=lambda d: d.Municipio.str[:5])
im = im.pivot_table(index='cmun', columns='Periodo', values='v')
rent = (100 * (im['2024'] / im['2015'] - 1)).dropna()

BLUES = ['#dbe7f3', '#b0cbe4', '#7ea9d0', '#4f86ba', '#2b649d', '#123f6e']
ORANGES = ['#d98b3f', '#f3cc9f']           # strong and mild net decrease
NODATA = '#e3e3e3'


def classify(v, edges, colors):
    return colors[int(np.searchsorted(edges, v, side='right'))]


def draw(ax, values, edges, colors):
    verts, fc = [], []
    for cm, rings in polys.items():
        v = values.get(cm, np.nan)
        c = classify(v, edges, colors) if np.isfinite(v) else NODATA
        for r in rings:
            verts.append(r); fc.append(c)
    # edges in the fill colour close the hairline seams between neighbouring polygons
    ax.add_collection(PolyCollection(verts, facecolors=fc, edgecolors=fc, linewidths=0.15))
    ax.add_collection(PolyCollection(prov, facecolors='none', edgecolors='#505050', linewidths=0.22))
    ax.plot([-13.9, -8.1, -8.1], [36.8, 36.8, 34.2], color=G1, lw=0.5)
    ax.set_xlim(-13.9, 4.6); ax.set_ylim(34.2, 44.0); ax.set_aspect(1 / np.cos(np.radians(39.5))); ax.axis('off')


def key(ax, colors, ticks, nodata_label, low_label=None):
    """Binned legend: equal boxes, boundary values between boxes, a separate box for missing data."""
    n = len(colors)
    for i, c in enumerate(colors):
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=c, edgecolor='white', lw=0.8))
    for i, t in enumerate(ticks, start=1):
        ax.text(i, -0.35, t, ha='center', va='top', fontsize=6.6)
    if low_label:
        ax.text(0, 1.3, low_label, ha='left', va='bottom', fontsize=6.6, color=G1)
    ax.add_patch(Rectangle((n + 0.7, 0), 1, 1, facecolor=NODATA, edgecolor='white', lw=0.8))
    ax.text(n + 1.85, 0.5, nodata_label, ha='left', va='center', fontsize=6.6)
    ax.set_xlim(-0.05, n + 6.2); ax.set_ylim(-1.6, 2.4); ax.axis('off')


fig = plt.figure(figsize=(7.0, 3.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.12], hspace=0.0, wspace=0.04, left=0.0, right=1.0, top=0.89, bottom=0.02)
e1 = [-2, 0, 2, 4, 6, 8, 12]; c1 = ORANGES + BLUES
ax = fig.add_subplot(gs[0, 0]); draw(ax, inflow, e1, c1)
ax.set_title('(a) Net foreign-born inflow, 2015\u20132024\n(% of 2015 population)')
key(fig.add_subplot(gs[1, 0]), c1, ['−2', '0', '2', '4', '6', '8', '12'], 'No data', 'Net decrease')
e2 = [10, 15, 20, 25, 30]
ax = fig.add_subplot(gs[0, 1]); draw(ax, rent, e2, BLUES)
ax.set_title('(b) Change in the rental price index (IPVA),\n2015\u20132024 (%)')
key(fig.add_subplot(gs[1, 1]), BLUES, ['10', '15', '20', '25', '30'], 'No municipal index')
save(fig, 'fig7_mapas')

inf_r = inflow.reindex(rent.index).dropna()
json.dump(dict(n_inflow=int(len(inflow)), n_decrease=int((inflow < 0).sum()), inflow_median=float(inflow.median()),
               inflow_p90=float(inflow.quantile(.9)), n_rent=int(len(rent)), rent_median=float(rent.median()),
               n_polygons=len(polys), n_polygons_nodata_inflow=int(sum(c not in inflow.index for c in polys)),
               corr_inflow_rent=float(np.corrcoef(inf_r, rent.reindex(inf_r.index))[0, 1]),
               silc_tenure_missing_years=[int(y) for y in miss]),
          open(os.path.join(OUT, 'r22_context.json'), 'w'), indent=1)
print('context figure and maps written')

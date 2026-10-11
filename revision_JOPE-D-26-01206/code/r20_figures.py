"""Figures for the revised manuscript (vector PDF, Helvetica-type lettering, greyscale)."""
import json, os, re
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from rev_style import K, G1, G2, G3, G4, FIG, save, spread, interval
from rev_common import OUT

J = lambda f: json.load(open(os.path.join(OUT, f)))
EN = {'Rumanía': 'Romania', 'Reino Unido': 'United Kingdom', 'Perú': 'Peru', 'Alemania': 'Germany', 'Marruecos': 'Morocco',
      'Ucrania': 'Ukraine', 'Europa': 'Europe', 'America': 'Americas'}
tr = lambda s: EN.get(s, s)


def rows_axis(ax, rows, xlim, ref=None):
    """Forest panel. rows: list of ('h', label) headers or ('r', label, b, lo, hi[, marker, filled]) estimates."""
    y, ticks, labels, heads = 0.0, [], [], []
    for r in rows:
        if r[0] == 'h':
            if ticks:
                y -= 0.35
            ticks.append(y); labels.append(r[1]); heads.append(len(labels) - 1); y -= 1
            continue
        _, lab, b, lo, hi, *mk = r
        mk = mk or ['o', True]
        interval(ax, lo, hi, y, *xlim)
        ax.plot(b, y, mk[0], color=K, ms=4, mfc=K if mk[1] else 'white', mew=0.9, zorder=3)
        ticks.append(y); labels.append(lab); y -= 1
    ax.axvline(0, color=G3, lw=0.7, zorder=0)
    if ref is not None:
        ax.axvline(ref, color=G2, lw=0.7, ls=(0, (1, 1.5)), zorder=0)
    ax.set_yticks(ticks); ax.set_yticklabels([re.sub(r'(\d{4})-(\d{4})', '\\1\u2013\\2', l) for l in labels])
    for i in heads:
        ax.get_yticklabels()[i].set_fontweight('bold')
    ax.tick_params(axis='y', length=0)
    ax.spines['left'].set_visible(False)
    ax.set_xlim(*xlim); ax.set_ylim(y + 0.4, 0.6)


# ---------------------------------------------------------------- Fig. 3: shock diagnostics
gn = pd.read_csv(os.path.join(OUT, 'r10_shocks.csv'), index_col=0)
rot = pd.read_csv(os.path.join(OUT, 'r10_rotemberg.csv'))
yrs = [c for c in gn.columns if c.isdigit()]
fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.9), gridspec_kw={'width_ratios': [1, 1.05], 'wspace': 0.62})
sel = ['Rumanía', 'Colombia', 'Reino Unido', 'Perú', 'Alemania', 'Venezuela', 'Marruecos']
end = {}
for o in sel:
    v = gn.loc[o, yrs].astype(float).cumsum()
    key = o in ('Rumanía', 'Colombia')          # the two largest Rotemberg weights
    ax[0].plot([int(y) for y in yrs], v.values, color=K if key else G2, lw=1.4 if key else 1.0, zorder=3 if key else 2)
    end[o] = v.values[-1]
ly = spread(list(end.values()), 0.62)
for (o, v), l in zip(end.items(), ly):
    ax[0].annotate(tr(o).replace('United Kingdom', 'UK'), (int(yrs[-1]), v), xytext=(int(yrs[-1]) + 0.6, l), textcoords='data', va='center', fontsize=7,
                   annotation_clip=False, arrowprops=dict(arrowstyle='-', color=G3, lw=0.5, shrinkA=0, shrinkB=1))
ax[0].axhline(0, color=G3, lw=0.7, zorder=0)
ax[0].set_xlim(2011.6, int(yrs[-1]) + 0.2); ax[0].set_xticks([2012, 2015, 2018, 2021, 2024])
ax[0].set_title('(a) Cumulative national growth since 2012,\nrelative to the 2003 stock of each origin')
ax[0].set_xlabel('Calendar year')
r = rot.copy(); lim = 3.0
inr = r.beta.abs() <= lim
sizes = 380 * r.share2003 / r.share2003.max() + 8
ax[1].scatter(r.beta[inr], r.alpha[inr], s=sizes[inr], facecolors='none', edgecolors=K, lw=0.7)
for sgn, m in [(-1, '<'), (1, '>')]:                    # estimates beyond the axis limits, drawn at the edge
    q = r[(~inr) & (np.sign(r.beta) == sgn)]
    ax[1].scatter(np.full(len(q), sgn * (lim + 0.18)), q.alpha, marker=m, s=16, color=G1, clip_on=False)
offs = {'Rumanía': (6, 0), 'Colombia': (8, 0), 'Reino Unido': (-9, 0), 'Perú': (7, 0), 'Alemania': (-10, -1), 'Venezuela': (7, 0)}
for o, (dx, dy) in offs.items():
    q = r[r.origin == o].iloc[0]
    ax[1].annotate(tr(o).replace('United Kingdom', 'UK'), (q.beta, q.alpha), xytext=(dx, dy), textcoords='offset points', fontsize=7,
                   ha='left' if dx > 0 else 'right', va='center')
ax[1].axhline(0, color=G3, lw=0.7, zorder=0); ax[1].axvline(0, color=G3, lw=0.7, zorder=0)
ax[1].set_xlim(-lim - 0.3, lim + 0.3); ax[1].set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax[1].set_xlabel(r'Origin-specific estimate $\hat\beta_o$ (arrows: beyond $\pm$3)'); ax[1].set_ylabel(r'Rotemberg weight $\hat\alpha_o$')
ax[1].set_title('(b) Rotemberg weights and origin-specific estimates')
save(fig, 'fig3_shocks')

# ---------------------------------------------------------------- Fig. 4: specification forest
m = J('r19_main.json')['main']
F = pd.read_csv(os.path.join(OUT, 'r13_forest.csv'))
XL = (-0.8, 1.0)
specs = [('minimal', 'Minimal controls'), ('original (author covariates)', 'Original covariates'),
         ('central (predetermined + structure)', 'Central: predetermined + structure'),
         ('central + province x size FE', 'Central + province × size × year FE')]
ra = []
for key, head in specs:
    ra.append(('h', head))
    for w, mk, fill, wl in [('w', 'o', True, 'Population 2003 weights'), ('w_rent', 's', True, 'Renter 2011 weights'),
                            ('unw', '^', False, 'Unweighted')]:
        q = m[f'{key}|{w}']; ra.append(('r', wl, q['b'], q['ar'][0], q['ar'][1], mk, fill))
g = lambda lab: F[F.label == lab].iloc[0]
short = [('h', 'Central specification', None),
         ('r', 'All municipalities, 2012-2024', 'Central specification'),
         ('h', 'Excluding territories', None),
         ('r', 'Madrid and Barcelona provinces', 'without Madrid and Barcelona provinces'),
         ('r', 'Balearic and Canary Islands', 'without Balearic and Canary Islands'),
         ('r', 'Coastal municipalities', 'without coastal municipalities'),
         ('r', 'FUA core cities', 'without FUA core cities'),
         ('r', 'Largest municipality of each province', 'without largest municipality of each province'),
         ('r', 'Almería, Murcia, Huelva', 'without Almería, Murcia, Huelva (agricultural SE)'),
         ('r', 'Catalan rent-control municipalities', 'without Catalan rent-control municipalities'),
         ('h', 'Restricting years', None),
         ('r', 'Without 2020-2021', 'without 2020-2021'), ('r', 'Without 2024', 'without 2024'),
         ('r', '2015-2024 only', '2015-2024 only (inflow years)'), ('r', '2012-2019 only', '2012-2019 only'),
         ('r', '2020-2024 only', '2020-2024 only'),
         ('h', 'Instrument without', None)]
lo_ = F[F.group == 'leave-one-origin-out'].sort_values('b')
extra = [('r', None, f'instrument without cont:{c}') for c in ['Europa', 'Africa', 'America', 'Asia']]
extra += [('r', None, x) for x in lo_.label.iloc[[0, 1, -2, -1]]]
rb = []
for t, lab, src in short + extra:
    if t == 'h':
        rb.append(('h', lab)); continue
    q = g(src)
    if lab is None:
        lab = tr(src.replace('instrument without ', '').replace('cont:', ''))
        if not (np.isfinite(q.ar_lo) and np.isfinite(q.ar_hi)):
            lab += ' (set unbounded)'
    rb.append(('r', lab, q.b, q.ar_lo, q.ar_hi))
fig, ax = plt.subplots(1, 2, figsize=(6.5, 5.0), gridspec_kw={'wspace': 1.15})
rows_axis(ax[0], ra, XL); rows_axis(ax[1], rb, XL, ref=g('Central specification').b)
for a, t in zip(ax, ['(a) Controls, fixed effects and weights', '(b) Central specification: exclusions']):
    a.set_title(t, loc='left', x=-0.9 if a is ax[0] else -1.05); a.set_xlabel('Elasticity and AR 95% set')
save(fig, 'fig4_forest')

# ---------------------------------------------------------------- Fig. 5: Colombia + Peru visa-waiver event study
ev = pd.read_csv(os.path.join(OUT, 'r14_events.csv'))
e = ev[(ev.episode == 'ColPer_2016') & (ev.w == 'w')]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.7), gridspec_kw={'wspace': 0.3})
for a, (yv, ttl, sc) in zip(ax, [('yF', '(a) Foreign-born stock (pp of 2003 population)', 1),
                                ('yR', '(b) Rent index (log points × 100)', 100)]):
    q = e[e.outcome == yv].sort_values('k')
    k = np.append(q.k.values, -1); b = np.append(q.b.values * sc, 0); s_ = np.append(q.se.values * sc, 0)
    o = np.argsort(k); k, b, s_ = k[o], b[o], s_[o]
    a.fill_between(k, b - 1.96 * s_, b + 1.96 * s_, color=G4, lw=0)
    a.axhline(0, color=G2, lw=0.6); a.axvline(-0.5, color=G2, lw=0.6, ls=(0, (1, 1.5)))
    a.plot(k, b, '-', color=K, lw=1.1)
    a.plot(k[k != -1], b[k != -1], 'o', color=K, ms=3.4)
    a.plot([-1], [0], 'o', color=K, mfc='white', ms=3.6, mew=0.9, zorder=4)    # reference year, normalised to zero
    a.set_title(ttl); a.set_xlabel('Years relative to 2016'); a.set_xticks(range(-5, 9))
ax[0].set_ylabel('Coefficient per pp of 2003 exposure')
save(fig, 'fig5_event_colper')

# ---------------------------------------------------------------- Fig. 6: margins of adjustment (census 2011-2021)
mg = J('r16_margins.json')
rows = [('y_pop', 'Net\nresidents'), ('y_nat', 'Spain-\nborn'), ('y_new', 'New\ndwellings'), ('y_vac', 'Non-primary\ndwellings'),
        ('y_crowd', 'Higher\noccupancy'), ('y_rent', 'Moved into\nrenting')]
fig, ax = plt.subplots(figsize=(6.0, 2.8))
xs = np.arange(len(rows)); wd = 0.24
for j, (key, lab_, col) in enumerate([('census_author_w', 'Original covariates, weighted', G2), ('census_central_w', 'Central, weighted', K),
                                     ('census_central_unw', 'Central, unweighted', G3)]):
    b = np.array([mg[key][r_[0]]['b'] for r_ in rows]); s_ = np.array([mg[key][r_[0]]['se'] for r_ in rows])
    ax.bar(xs + (j - 1) * wd, b, wd, color=col, label=lab_, edgecolor='white', lw=0.8)
    ax.errorbar(xs + (j - 1) * wd, b, yerr=1.96 * s_, fmt='none', ecolor=K, elinewidth=0.7, capsize=0)
lo = min(min(mg[k][r_[0]]['b'] - 1.96 * mg[k][r_[0]]['se'] for r_ in rows) for k in ['census_author_w', 'census_central_w', 'census_central_unw'])
hi = max(max(mg[k][r_[0]]['b'] + 1.96 * mg[k][r_[0]]['se'] for r_ in rows) for k in ['census_author_w', 'census_central_w', 'census_central_unw'])
ax.axhline(0, color=K, lw=0.6)
ax.set_xticks(xs); ax.set_xticklabels([r_[1] for r_ in rows]); ax.tick_params(axis='x', length=0)
ax.set_ylabel('Persons per immigrant'); ax.set_ylim(np.floor(lo * 2) / 2 - 0.2, np.ceil(hi * 2) / 2 + 0.2)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, handlelength=1.2, columnspacing=1.6)
save(fig, 'fig6_margins')

# ---------------------------------------------------------------- Fig. 7: implied share of national IPVA growth
M, G = 0.065, 0.206
fac = 100 * M / G
m15 = J('r19_main_2015.json')['main']; ep = J('r14_events.json')['did_iv_colper']['w']
cen = 'central (predetermined + structure)'
D = '\u2013'
mk = [(f'Central specification, 2012{D}2024', m[f'{cen}|w']), (f'Central specification, arrival period 2015{D}2024', m15[f'{cen}|w']),
      (f'Central, renter weights, 2015{D}2024', m15[f'{cen}|w_rent']),
      (f'Central + province \u00d7 size FE, 2015{D}2024', m15['central + province x size FE|w']),
      (f'Original covariates, 2012{D}2024', m['original (author covariates)|w']),
      (f'Colombia{D}Peru episode (DiD-IV)', dict(b=ep['b'], ar=ep['ar_wcr']))]           # rows and order of table 7
fig, ax = plt.subplots(figsize=(5.4, 2.5))
XS = (-2, 60)
# as in table 7, the share interval truncates negative values of the robust set at zero
rows_axis(ax, [('r', f"{l}   $\\beta$ = {q['b']:.2f}", fac * q['b'], max(fac * q['ar'][0], 0), fac * q['ar'][1]) for l, q in mk], XS)
ax.set_xlabel(f'Implied share of national IPVA growth 2015{D}2024 (%)')
ax.set_xticks(range(0, 61, 10))
save(fig, 'fig7_magnitude')

# ---------------------------------------------------------------- Fig. A1: local projections, balanced sample
lp = pd.read_csv(os.path.join(OUT, 'r12_lp.csv'))
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.6), gridspec_kw={'wspace': 0.27})
for a, sp, ttl in [(ax[0], 'min_w_L3', '(a) Minimal controls'), (ax[1], 'cov_w_L3', '(b) Original covariates')]:
    q = lp[lp.spec == sp].sort_values('h')
    a.fill_between(q.h, q.b - 1.96 * q.se, q.b + 1.96 * q.se, color=G4, lw=0)
    a.axhline(0, color=G2, lw=0.6)
    a.plot(q.h, q.b, '-', color=K, lw=1.1)
    nz = q.h != -1
    a.plot(q.h[nz], q.b[nz], 'o', color=K, ms=3.4)
    a.plot(q.h[~nz], q.b[~nz], 'o', color=K, mfc='white', ms=3.6, mew=0.9, zorder=4)
    Fv = q.F.dropna().iloc[0]
    a.set_title(f'{ttl}, first-stage F = {Fv:.1f}'); a.set_xlabel('Horizon h (years)')
ax[0].set_ylabel(r'$\beta_h$')
save(fig, 'figA1_lp')
print('figures written to', FIG)

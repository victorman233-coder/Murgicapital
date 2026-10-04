"""Figures for the revised manuscript (PDF, sans-serif, greyscale-friendly)."""
import json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rev_common import *

FIG = os.path.join(HERE, '..', 'paper', 'fig'); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 9.5, 'axes.titleweight': 'normal', 'legend.frameon': False})
DARK, MID, LIGHT = '#1f1f1f', '#6e6e6e', '#b5b5b5'
J = lambda f: json.load(open(os.path.join(OUT, f)))

# ---------------------------------------------------------------- Fig. 3: shock diagnostics
gn = pd.read_csv(os.path.join(OUT, 'r10_shocks.csv'), index_col=0)
rot = pd.read_csv(os.path.join(OUT, 'r10_rotemberg.csv'))
yrs = [c for c in gn.columns if c.isdigit()]
fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.1))
sel = ['Rumanía', 'Colombia', 'Reino Unido', 'Perú', 'Alemania', 'Venezuela', 'Marruecos']
lab = {'Rumanía': 'Romania', 'Colombia': 'Colombia', 'Reino Unido': 'United Kingdom', 'Perú': 'Peru', 'Alemania': 'Germany',
       'Venezuela': 'Venezuela', 'Marruecos': 'Morocco'}
styles = ['-', '--', ':', '-.', (0, (5, 1)), (0, (1, 1)), (0, (3, 1, 1, 1))]
for k, o in enumerate(sel):
    v = gn.loc[o, yrs].astype(float).cumsum()
    ax[0].plot([int(y) for y in yrs], v.values, linestyle=styles[k], color=DARK if k < 3 else MID, lw=1.2, label=lab[o])
ax[0].axhline(0, color=LIGHT, lw=0.8)
ax[0].set_title('(a) Cumulative national growth since 2012\n(relative to the 2003 stock of each origin)')
ax[0].set_xlabel('Calendar year'); ax[0].legend(fontsize=7, ncol=2, loc='upper left')
r = rot.copy()
sizes = 400 * r.share2003 / r.share2003.max() + 8
ax[1].scatter(r.beta.clip(-3, 3), r.alpha, s=sizes, facecolors='none', edgecolors=DARK, lw=0.8)
offs = {'Rumanía': (4, 2), 'Colombia': (4, 2), 'Reino Unido': (-18, 4), 'Perú': (5, -3), 'Alemania': (-34, -8), 'Ucrania': (4, -7), 'Venezuela': (4, 2)}
for _, q in r.head(7).iterrows():
    ax[1].annotate({'Rumanía': 'Romania', 'Reino Unido': 'UK', 'Perú': 'Peru', 'Alemania': 'Germany', 'Ucrania': 'Ukraine'}.get(q.origin, q.origin),
                   (np.clip(q.beta, -3, 3), q.alpha), xytext=offs.get(q.origin, (4, 2)), textcoords='offset points', fontsize=7)
ax[1].axhline(0, color=LIGHT, lw=0.8); ax[1].axvline(0, color=LIGHT, lw=0.8)
ax[1].set_xlabel(r'Origin-specific estimate $\beta_o$ (clipped at $\pm$3)'); ax[1].set_ylabel(r'Rotemberg weight $\alpha_o$')
ax[1].set_title('(b) Rotemberg decomposition, original specification')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig3_shocks.pdf')); plt.close(fig)

# ---------------------------------------------------------------- Fig. 4: specification forest
m = J('r19_main.json')['main']
order = [('minimal', 'Minimal controls'), ('original (author covariates)', 'Original covariates'),
         ('central (predetermined + structure)', 'Central: predetermined + structure'),
         ('central + province x size FE', 'Central + province x size x year FE')]
F = pd.read_csv(os.path.join(OUT, 'r13_forest.csv'))
fig, ax = plt.subplots(1, 2, figsize=(8.2, 4.6), gridspec_kw={'width_ratios': [1, 1.15]})
yy = 0; ticks = []; labels = []
for key, lab_ in order:
    for w, mk, wl in [('w', 'o', 'population 2003'), ('w_rent', 's', 'renters 2011'), ('unw', '^', 'unweighted')]:
        q = m[f'{key}|{w}']
        lo, hi = q['ar'][0], q['ar'][1]
        ax[0].plot([max(lo, -1), min(hi, 1.5)], [yy, yy], color=MID, lw=1)
        ax[0].plot(q['b'], yy, mk, color=DARK, ms=4.5, mfc='white' if w == 'unw' else DARK)
        ticks.append(yy); labels.append(f'{lab_} ({wl})'); yy -= 1
    yy -= 0.6
ax[0].axvline(0, color=LIGHT, lw=0.8)
ax[0].set_yticks(ticks); ax[0].set_yticklabels(labels, fontsize=6.6); ax[0].set_xlim(-1, 1.5)
ax[0].set_xlabel('Elasticity and AR 95% set'); ax[0].set_title('(a) Controls, fixed effects, weights')
sel = F[F.group.isin(['baseline', 'territory', 'policy', 'period', 'leave-one-continent-out'])].copy()
sel = pd.concat([sel, F[F.group == 'leave-one-origin-out'].sort_values('b').iloc[[0, 1, -2, -1]]])
yy = 0; ticks = []; labels = []
for _, q in sel.iterrows():
    lo, hi = q.ar_lo, q.ar_hi
    ax[1].plot([max(lo, -1), min(hi, 1.5)], [yy, yy], color=MID, lw=1)
    ax[1].plot(q.b, yy, 'o', color=DARK, ms=4)
    ticks.append(yy); labels.append(q.label.replace('instrument without cont:', 'instrument without ').replace('Rumanía', 'Romania')
                                   .replace('Marruecos', 'Morocco').replace('Reino Unido', 'UK').replace('Europa', 'Europe').replace('America', 'Americas')); yy -= 1
ax[1].axvline(0, color=LIGHT, lw=0.8)
ax[1].set_yticks(ticks); ax[1].set_yticklabels(labels, fontsize=6.6); ax[1].set_xlim(-1, 1.5)
ax[1].set_xlabel('Elasticity and AR 95% set'); ax[1].set_title('(b) Exclusions, central spec.')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig4_forest.pdf')); plt.close(fig)

# ---------------------------------------------------------------- Fig. 5: Colombia + Peru visa-waiver event study
ev = pd.read_csv(os.path.join(OUT, 'r14_events.csv'))
e = ev[(ev.episode == 'ColPer_2016') & (ev.w == 'w')]
fig, ax = plt.subplots(1, 2, figsize=(7.6, 2.9))
for a, (yv, ttl, sc) in zip(ax, [('yF', '(a) Foreign-born stock (pp of 2003 population)', 1), ('yR', '(b) Rent index (log points x 100)', 100)]):
    q = e[e.outcome == yv].sort_values('k')
    k = np.append(q.k.values, -1); b = np.append(q.b.values * sc, 0); s_ = np.append(q.se.values * sc, 0)
    o = np.argsort(k); k, b, s_ = k[o], b[o], s_[o]
    a.fill_between(k, b - 1.96 * s_, b + 1.96 * s_, color=LIGHT, alpha=0.6, lw=0)
    a.plot(k, b, 'o-', color=DARK, ms=3.5, lw=1)
    a.axhline(0, color=MID, lw=0.7); a.axvline(-0.5, color=MID, lw=0.7, ls=':')
    a.set_title(ttl); a.set_xlabel('Years relative to 2016')
ax[0].set_ylabel('Effect of 1 pp of 2003 exposure')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig5_event_colper.pdf')); plt.close(fig)

# ---------------------------------------------------------------- Fig. 6: margins of adjustment (census 2011-2021)
mg = J('r16_margins.json')
rows = [('y_pop', 'Net\nresidents'), ('y_nat', 'Spain-\nborn'), ('y_new', 'New\ndwellings'), ('y_vac', 'Non-primary\ndwellings'),
        ('y_crowd', 'Higher\noccupancy'), ('y_rent', 'Moved into\nrenting')]
fig, ax = plt.subplots(figsize=(7.2, 3.0))
xs = np.arange(len(rows)); wd = 0.2
for j, (key, lab_, col) in enumerate([('census_author_w', 'Original covariates, weighted', MID), ('census_central_w', 'Central, weighted', DARK),
                                     ('census_central_unw', 'Central, unweighted', LIGHT)]):
    b = [mg[key][r_[0]]['b'] for r_ in rows]; s_ = [mg[key][r_[0]]['se'] for r_ in rows]
    ax.bar(xs + (j - 1) * wd, b, wd, color=col, label=lab_, edgecolor=DARK, lw=0.4)
    ax.errorbar(xs + (j - 1) * wd, b, yerr=1.96 * np.array(s_), fmt='none', ecolor=DARK, lw=0.7, capsize=0)
ax.axhline(0, color=DARK, lw=0.6)
ax.set_xticks(xs); ax.set_xticklabels([r_[1] for r_ in rows], fontsize=8); ax.set_ylabel('Persons per immigrant')
ax.set_ylim(-3.2, 4.2); ax.legend(fontsize=7, loc='upper left')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig6_margins.pdf')); plt.close(fig)

# ---------------------------------------------------------------- Fig. 7: aggregate share as a function of the elasticity
fac = 0.065 / 0.206
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 4.2), sharex=True, gridspec_kw={'height_ratios': [1.3, 1]})
bb = np.linspace(-0.5, 2.0, 100); ax.plot(bb, 100 * fac * bb, color=DARK, lw=1)
m15 = J('r19_main_2015.json')['main']
mk = [('Central, 2012-2024', m['central (predetermined + structure)|w']['b'], m['central (predetermined + structure)|w']['ar']),
      ('Central, 2015-2024', m15['central (predetermined + structure)|w']['b'], m15['central (predetermined + structure)|w']['ar']),
      ('Central, 2015-2024, renter weights', m15['central (predetermined + structure)|w_rent']['b'], m15['central (predetermined + structure)|w_rent']['ar']),
      ('Original covariates, 2012-2024', m['original (author covariates)|w']['b'], m['original (author covariates)|w']['ar']),
      ('Colombia-Peru episode (WCR)', J('r14_events.json')['did_iv_colper']['w']['b'], J('r14_events.json')['did_iv_colper']['w']['ar_wcr'])]
for i, (l, b, ci) in enumerate(mk):
    yv = -i
    ax2.plot([max(ci[0], -0.5), min(ci[1], 2.0)], [yv, yv], color=MID, lw=1.2); ax2.plot(b, yv, 'o', color=DARK, ms=4)
    ax2.text(-0.48, yv + 0.25, l, va='bottom', fontsize=6.8)
ax.axhline(0, color=LIGHT, lw=0.7); ax.axvline(0, color=LIGHT, lw=0.7); ax2.axvline(0, color=LIGHT, lw=0.7)
ax2.set_yticks([]); ax2.set_ylim(-len(mk) + 0.4, 0.9)
ax.set_title('(a) Implied share of IPVA growth 2015-2024 (%), under assumptions A1-A4')
ax2.set_title('(b) Estimates and robust 95% sets', fontsize=8.5)
ax2.set_xlabel(r'Elasticity $\beta$'); ax.set_xlim(-0.5, 2.0)
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig7_magnitude.pdf')); plt.close(fig)

# ---------------------------------------------------------------- Fig. A1: local projections, balanced sample
lp = pd.read_csv(os.path.join(OUT, 'r12_lp.csv'))
fig, ax = plt.subplots(1, 2, figsize=(7.4, 2.8))
for a, sp, ttl in [(ax[0], 'min_w_L3', '(a) Minimal controls'), (ax[1], 'cov_w_L3', '(b) Original covariates')]:
    q = lp[lp.spec == sp].sort_values('h')
    a.fill_between(q.h, q.b - 1.96 * q.se, q.b + 1.96 * q.se, color=LIGHT, alpha=0.6, lw=0)
    a.plot(q.h, q.b, 'o-', color=DARK, ms=3.5, lw=1); a.axhline(0, color=MID, lw=0.7)
    Fv = q.F.dropna().iloc[0]
    a.set_title(f'{ttl} (first-stage F = {Fv:.1f})'); a.set_xlabel('Horizon h (years)')
ax[0].set_ylabel(r'$\beta_h$')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'figA1_lp.pdf')); plt.close(fig)
print('figures written to', FIG)

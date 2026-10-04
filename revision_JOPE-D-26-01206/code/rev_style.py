"""Shared figure style: Helvetica-type lettering (TeX Gyre Heros), greyscale marks, recessive axes."""
import glob, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

for f in glob.glob('/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-*.otf'):
    fm.fontManager.addfont(f)
_fam = 'TeX Gyre Heros' if any('Heros' in f.name for f in fm.fontManager.ttflist) else 'DejaVu Sans'
mpl.rcParams.update({
    'font.family': _fam, 'mathtext.fontset': 'custom', 'mathtext.rm': _fam, 'mathtext.it': f'{_fam}:italic',
    'font.size': 8.5, 'axes.titlesize': 8.5, 'axes.labelsize': 8.5, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5, 'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.titleweight': 'normal', 'axes.titlelocation': 'left',
    'legend.frameon': False, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03, 'pdf.fonttype': 42,
    'axes.edgecolor': '#4d4d4d', 'xtick.color': '#4d4d4d', 'ytick.color': '#4d4d4d', 'axes.labelcolor': '#1f1f1f'})
K, G1, G2, G3, G4 = '#1a1a1a', '#5f5f5f', '#9a9a9a', '#c8c8c8', '#e6e6e6'
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', 'paper', 'fig'); os.makedirs(FIG, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.pdf')); plt.close(fig)


def spread(y, gap):
    """Shift label positions apart so that consecutive labels are at least `gap` apart (keeps order)."""
    y = np.asarray(y, float); o = np.argsort(y); z = y[o].copy()
    for _ in range(200):
        moved = False
        for i in range(1, len(z)):
            if z[i] - z[i - 1] < gap:
                d = (gap - (z[i] - z[i - 1])) / 2; z[i - 1] -= d; z[i] += d; moved = True
        if not moved:
            break
    out = np.empty_like(z); out[o] = z
    return out


def interval(ax, lo, hi, y, xmin, xmax, color=G1, lw=1.0, ms=3.2):
    """Horizontal interval clipped to [xmin, xmax]; arrowheads mark ends that are truncated or unbounded."""
    a, b = max(lo, xmin), min(hi, xmax)
    unb = not (np.isfinite(lo) and np.isfinite(hi))
    ax.plot([a, b], [y, y], color=color, lw=lw, ls=(0, (3, 1.5)) if unb else '-', solid_capstyle='butt')
    if lo < xmin:
        ax.plot(xmin, y, marker='<', color=color, ms=ms, clip_on=False)
    if hi > xmax:
        ax.plot(xmax, y, marker='>', color=color, ms=ms, clip_on=False)

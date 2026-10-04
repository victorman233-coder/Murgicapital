"""Shared paths and helpers for the rent-determinants analysis."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
REVCODE = os.path.join(HERE, '..', '..', 'revision_JOPE-D-26-01206', 'code')
sys.path.insert(0, REVCODE)
WORK = os.environ.get('WORK', '/home/user/work'); RAW = f'{WORK}/rent/raw'; CL = f'{WORK}/rent/clean'
OUT = os.path.join(HERE, '..', 'out'); os.makedirs(OUT, exist_ok=True)
FIG = os.path.join(HERE, '..', 'paper', 'fig'); os.makedirs(FIG, exist_ok=True)
TAB = os.path.join(HERE, '..', 'paper', 'tab'); os.makedirs(TAB, exist_ok=True)
SIZE_EDGES = [0, 20000, 50000, 100000, 500000, 1e9]
SIZE_LABELS = ['10-20k', '20-50k', '50-100k', '100-500k', '>500k']
PRED = ['lnpop11', 'rent11', 'vac11', 'tert11', 'sh65_11']                  # predetermined (census 2011)
ECON = ['sh_constr12', 'sh_ind12', 'sh_trade_hosp12', 'firms12_pc', 'coastal', 'city_core']


def save(name, obj):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    json.dump(obj, open(os.path.join(OUT, name), 'w'), indent=1, default=conv)


def load(name):
    return json.load(open(os.path.join(OUT, name)))


def wmean(x, w):
    m = np.isfinite(x) & np.isfinite(w)
    return float(np.sum(x[m] * w[m]) / np.sum(w[m]))


def coefs(m, names):
    """pyfixest model -> dict of b, se, p, ci for selected names."""
    t = m.tidy()
    out = {}
    for n in names:
        if n in t.index:
            r = t.loc[n]
            out[n] = dict(b=float(r['Estimate']), se=float(r['Std. Error']), p=float(r['Pr(>|t|)']),
                          lo=float(r['2.5%']), hi=float(r['97.5%']))
    out['n'] = int(m._N)
    return out

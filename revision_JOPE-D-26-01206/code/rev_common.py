"""Common utilities for the revision analyses.

Builds on the author's replication package (REP, code/ and data/clean/) and on the
re-downloaded INE stocks by origin (WORK/clean/pop_groups_nacim.parquet).
"""
import os, sys, json
import numpy as np, pandas as pd, pyfixest as pf
import warnings; warnings.filterwarnings('ignore')

WORK = os.environ.get('WORK', '/home/user/work')
REP = os.environ.get('REP', f'{WORK}/replication_package')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out'); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, f'{REP}/code')

COUNTRIES = ['Alemania', 'Bulgaria', 'Francia', 'Italia', 'Polonia', 'Portugal', 'Rumanía',
             'Reino Unido', 'Rusia', 'Ucrania', 'Argelia', 'Marruecos', 'Nigeria', 'Senegal',
             'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Cuba', 'Ecuador', 'Paraguay',
             'Perú', 'República Dominicana', 'Uruguay', 'Venezuela', 'China', 'Pakistán']
GROUPS = COUNTRIES + ['Resto_Europa', 'Resto_Africa', 'Resto_America', 'Resto_Asia', 'Oceania_otros']
REGION = {**{c: 'Europa' for c in COUNTRIES[:10]}, **{c: 'Africa' for c in COUNTRIES[10:14]},
          **{c: 'America' for c in COUNTRIES[14:26]}, **{c: 'Asia' for c in COUNTRIES[26:]},
          'Resto_Europa': 'Europa', 'Resto_Africa': 'Africa', 'Resto_America': 'America',
          'Resto_Asia': 'Asia', 'Oceania_otros': 'Otros'}
VC = {'CRV1': 'cpro'}
COVS = ['lninc15', 'lnpop11', 'rent11', 'vac11']


def save(name, obj):
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump(obj, f, indent=1, default=float)


def coef(m, var):
    t = m.tidy().loc[var]
    return dict(b=float(t['Estimate']), se=float(t['Std. Error']), p=float(t['Pr(>|t|)']), n=int(m._N))


# ----------------------------------------------------------------------------- population by origin
def pop_groups():
    p = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
    pad = p[p.src == 'padron'].set_index(['cmun', 'year']).sort_index()
    cen = p[p.src == 'censo'].set_index(['cmun', 'year']).sort_index()
    return pad, cen


def flows_by_origin(cols=GROUPS + ['P', 'NAT', 'FOR']):
    """Calendar-year changes (stock Jan t+1 - stock Jan t) within a single source:
    Padrón for t<=2021, annual census for t>=2022 (as in build_panel.flows)."""
    pad, cen = pop_groups()
    dp = (pad[cols].groupby(level=0).shift(-1) - pad[cols])
    dc = (cen[cols].groupby(level=0).shift(-1) - cen[cols])
    dp = dp[dp.index.get_level_values(1) <= 2021]
    dc = dc[dc.index.get_level_values(1) >= 2022]
    return pd.concat([dp, dc]).dropna(how='all').sort_index()


def levels(cols=GROUPS + ['P', 'NAT', 'FOR']):
    pad, cen = pop_groups()
    return pd.concat([pad[pad.index.get_level_values(1) <= 2021][cols],
                      cen[cen.index.get_level_values(1) >= 2022][cols]]).sort_index()


def shares(base=2003):
    """s_io = F_io,base / P_i,base (municipal exposure) and lambda_io = F_io,base / F_o,base."""
    pad, _ = pop_groups()
    b = pad.xs(base, level=1)
    b = b[b.index != '00000']
    s = b[GROUPS].div(b['P'], axis=0)
    lam = b[GROUPS] / b[GROUPS].sum()
    return s, lam, b['P']


def shocks_counts(dF, munis_all=None):
    """National and province-level changes by origin and calendar year (counts)."""
    d = dF[dF.index.get_level_values(0) != '00000'][GROUPS].reset_index()
    d['cpro'] = d['cmun'].str[:2]
    nat = d.groupby('year')[GROUPS].sum()
    prv = d.groupby(['cpro', 'year'])[GROUPS].sum()
    return nat, prv


def instrument(munis_years, base=2003, groups=GROUPS, shock_override=None):
    """Author's instrument: Z_it = sum_o lambda_io * (dF_ot^nat - dF_ot^prov) / P_i,base,
    for calendar year t. munis_years: DataFrame with cmun, year. Returns Series aligned."""
    dF = flows_by_origin()
    s, lam, P0 = shares(base)
    nat, prv = shocks_counts(dF)
    out = np.full(len(munis_years), np.nan)
    my = munis_years.reset_index(drop=True)
    cpro = my['cmun'].str[:2]
    for (pro, yr), idx in my.groupby([cpro, my['year']]).groups.items():
        if yr not in nat.index:
            continue
        if shock_override is not None:
            sh = shock_override.loc[yr, groups]
        else:
            sh = nat.loc[yr, groups] - (prv.loc[(pro, yr), groups] if (pro, yr) in prv.index else 0)
        L = lam.reindex(my.loc[idx, 'cmun'])[groups].fillna(0).values
        out[idx] = L @ sh.values / my.loc[idx, 'cmun'].map(P0).values
    return pd.Series(out, index=munis_years.index)


# ----------------------------------------------------------------------------- analysis panel
def load_panel(extra=True):
    """Author's analysis sample (9,060 obs) with Zc, xc, minimal and covariate controls."""
    import analysis_main as am
    cwd = os.getcwd(); os.chdir(REP)
    try:
        p = am.load('nacim')
        s, fsx = am.sample(p)
        sc, cvx = am.add_cov(s)
    finally:
        os.chdir(cwd)
    return sc, fsx, cvx


def year_interact(d, var, prefix=None, years=None):
    prefix = prefix or f'yi_{var}'
    years = years if years is not None else sorted(d.year.unique())[1:]
    names = []
    for y in years:
        n = f'{prefix}_{y}'
        d[n] = (d.year == y) * d[var]
        names.append(n)
    return ' + '.join(names)


# ----------------------------------------------------------------------------- revision specification helpers
PRED = ['lnpop11', 'rent11', 'vac11', 'tert11', 'sh65_11']                     # predetermined (census 2011)
ECON = ['sh_constr12', 'sh_ind12', 'sh_trade_hosp12', 'firms12_pc', 'coastal', 'city_core']


def load_revision_panel():
    """Analysis sample (author's 9,060 obs) + extended predetermined characteristics, renter weights,
    size classes, FUA and policy indicators."""
    sc, fsx, cvx = load_panel()
    d = sc.reset_index(drop=True)
    d = d[[c for c in d.columns if not c.startswith(('fs_', 'cv_'))]]
    ext = pd.read_parquet(f'{WORK}/clean/muni_extended.parquet')
    d = d.merge(ext, left_on='cmun', right_index=True, how='left', suffixes=('', '_x'))
    d['tert11'] = d['tert11'].replace([np.inf, -np.inf], np.nan)
    d['w_rent'] = d['renters11']
    d['size_cl'] = pd.cut(d['pop11'], [0, 20000, 50000, 100000, 1e9], labels=['10-20k', '20-50k', '50-100k', '>100k']).astype(str)
    d['cy_size'] = d['cy'] + '_' + d['size_cl']
    d['fuay'] = np.where(d['fua'].notna(), 'F' + d['fua'].astype(str) + '_' + d['year'].astype(str), d['cy'])
    d['ccaa'] = d['cmun'].str[:2].map(CCAA_OF)
    return d


def year_ctrls(d, vars_, prefix='yc'):
    """Complete set of variable x year interactions (no omitted base year)."""
    names = []
    for v in vars_:
        for y in sorted(d.year.unique()):
            n = f'{prefix}_{v}_{y}'
            d[n] = d[v].astype(float) * (d.year == y)
            names.append(n)
    return names


CCAA_OF = {**{p: 'AND' for p in ['04', '11', '14', '18', '21', '23', '29', '41']}, **{p: 'ARA' for p in ['22', '44', '50']},
           '33': 'AST', '07': 'BAL', **{p: 'CAN' for p in ['35', '38']}, '39': 'CANT',
           **{p: 'CYL' for p in ['05', '09', '24', '34', '37', '40', '42', '47', '49']},
           **{p: 'CLM' for p in ['02', '13', '16', '19', '45']}, **{p: 'CAT' for p in ['08', '17', '25', '43']},
           **{p: 'VAL' for p in ['03', '12', '46']}, **{p: 'EXT' for p in ['06', '10']}, **{p: 'GAL' for p in ['15', '27', '32', '36']},
           '28': 'MAD', '30': 'MUR', '31': 'NAV', **{p: 'PV' for p in ['01', '20', '48']}, '26': 'RIO', '51': 'CEU', '52': 'MEL'}

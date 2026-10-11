"""Large owners and credit (P4, P5): what public data allow, without causal claims.
(a) Provinces: foreclosures on dwellings owned by legal persons, 2014-2016 (stock later sold by banks, often to funds),
    and provincial rent growth 2015-2024, conditional on population growth.
(b) Catalonia: share of registered tourist dwellings held by companies and new-lease rent growth 2019-2025.
(c) National series: 12-month Euribor, average rate on new mortgages, and rents (time series only)."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *

res = {}
# ---------------------------------------------------------------- (a) provinces
f = pd.read_csv(f'{RAW}/ine_10745.csv', sep=';', encoding='utf-8-sig', dtype=str)
f = f[f.Provincias.notna()].assign(prov=lambda d: d.Provincias.str[:2], year=lambda d: d.Periodo.astype(int),
                                    v=lambda d: pd.to_numeric(d.Total.str.replace('.', '', regex=False), errors='coerce'))
fj = f[(f['Titular de la vivienda'] == 'Persona jurídica') & f.year.between(2014, 2016)].groupby('prov').v.sum()
ft = f[(f['Titular de la vivienda'] == 'Total') & f.year.between(2014, 2016)].groupby('prov').v.sum()
cat = pd.read_parquet(f'{WORK}/replication_package/data/clean/catastro_muni.parquet')
viv = cat[cat.year == 2015].assign(prov=lambda d: d.cmun.str[:2]).groupby('prov').viv.sum()
ip = pd.read_csv(f'{RAW}/ine_59058.csv', sep=';', encoding='utf-8-sig', dtype=str)
ip = ip[ip.Provincias.notna() & (ip['Tipo de edificación'] == 'Total') & (ip['Tipo de dato'] == 'Índice')]
ip = ip.assign(prov=ip.Provincias.str[:2], year=ip.Periodo.astype(int), v=pd.to_numeric(ip.Total.str.replace(',', '.'), errors='coerce'))
ipv = ip.pivot_table(index='prov', columns='year', values='v')
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
lev = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
pp = lev[lev.cmun.str.len() == 5].assign(prov=lambda d: d.cmun.str[:2])
p15 = pp[(pp.src == 'padron') & (pp.year == 2015)].groupby('prov').P.sum()
p21p = pp[(pp.src == 'padron') & (pp.year == 2021)].groupby('prov').P.sum()
p21c = pp[(pp.src == 'censo') & (pp.year == 2021)].groupby('prov').P.sum(); p24c = pp[(pp.src == 'censo') & (pp.year == 2024)].groupby('prov').P.sum()
P = pd.DataFrame({'dlnR': np.log(ipv[2024] / ipv[2015]), 'fj': 1000 * fj / viv, 'ft': 1000 * ft / viv,
                  'dlnP': np.log(p21p / p15) + np.log(p24c / p21c), 'P15': p15}).dropna()
P['ccaa'] = P.index.map(lambda p: {**{q: 'AND' for q in ['04', '11', '14', '18', '21', '23', '29', '41']}, **{q: 'CAT' for q in ['08', '17', '25', '43']},
                                    **{q: 'VAL' for q in ['03', '12', '46']}}.get(p, p))
for c in ['fj', 'ft']:
    P[c + '_s'] = (P[c] - P[c].mean()) / P[c].std()
m = pf.feols('dlnR ~ fj_s + dlnP', data=P.reset_index(), weights='P15', vcov='hetero')
res['prov_foreclosure_legal'] = coefs(m, ['fj_s', 'dlnP'])
m = pf.feols('dlnR ~ fj_s + ft_s + dlnP', data=P.reset_index(), weights='P15', vcov='hetero')
res['prov_foreclosure_legal_vs_total'] = coefs(m, ['fj_s', 'ft_s', 'dlnP'])
res['prov_n'] = len(P); res['prov_fj_mean'] = float(P.fj.mean()); res['prov_fj_sd'] = float(P.fj.std())
res['nat_foreclosures_legal_share_2014_16'] = float(fj.sum() / ft.sum())

# ---------------------------------------------------------------- (b) Catalonia: corporate tourist-dwelling owners
C = pd.read_parquet(f'{CL}/cat_q.parquet')
ann = C[C.year.isin([2019, 2025])].groupby(['cmun', 'year']).apply(lambda q: np.average(q.rent, weights=q.n), include_groups=False).unstack()
X = pd.DataFrame({'g_new': np.log(ann[2025] / ann[2019])}).join(C.drop_duplicates('cmun').set_index('cmun')[['hut', 'hut_corp', 'P', 'vutpct_2020M08', 'zmrt']])
X = X.dropna(subset=['g_new', 'P']); X['hut'] = X.hut.fillna(0); X['hut_corp'] = X.hut_corp.fillna(0)
X = X[X.P >= 5000].copy()
X['hut_pc'] = 100 * X.hut / X.P; X['corp_sh'] = np.where(X.hut > 0, X.hut_corp / X.hut, np.nan)
X['lnP'] = np.log(X.P)
Xs = X.dropna(subset=['corp_sh']).reset_index()
m = pf.feols('g_new ~ corp_sh + hut_pc + lnP + C(zmrt)', data=Xs, weights='P', vcov='hetero')
res['cat_corp_hut'] = coefs(m, ['corp_sh', 'hut_pc'])
res['cat_corp_share_mean'] = float(np.average(Xs.corp_sh, weights=Xs.hut)); res['cat_munis'] = len(Xs)
res['cat_hut_total'] = float(C.drop_duplicates('cmun').hut.sum()); res['cat_hut_corp_total'] = float(C.drop_duplicates('cmun').hut_corp.sum())

# ---------------------------------------------------------------- (c) national series
N = pd.read_parquet(f'{CL}/national.parquet')
r = pd.read_csv(f'{RAW}/ine_24457.csv', sep=';', encoding='utf-8-sig', dtype=str)
r = r[(r['Tipo de interés'] == 'Total') & (r['Naturaleza de la finca'].str.contains('Viviendas', na=False))]
r = r.assign(year=r.Periodo.str[:4].astype(int), v=pd.to_numeric(r.Total.str.replace(',', '.'), errors='coerce'))
N['mortgage_rate'] = r.groupby('year').v.mean()
N.to_parquet(f'{CL}/national.parquet')
res['national_rates'] = N[['euribor12m', 'mortgage_rate']].loc[2015:2025].round(3).to_dict()
save('a05_investors_credit.json', res)
print({k: v for k, v in res.items() if k != 'national_rates'})

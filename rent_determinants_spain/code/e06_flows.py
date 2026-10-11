"""Entry-gap paper: residential flows (INE, Estadística de Migraciones y Cambios de Residencia, 2021-2024).
Tables 69743 (intermunicipal in-migration by municipality of destination and nationality) and 69745 (intermunicipal
out-migration by municipality of origin and nationality), calendar years 2021-2024.
(a) Displacement: does a local foreign-born inflow (2021-2024, shift-share IV) raise the out-migration of Spanish nationals
    to other municipalities, or lower their in-migration?
(b) Spillovers within functional urban areas: does the core city's predicted inflow raise the in-migration of Spanish
    nationals into its periphery (reduced form, controlling for the periphery's own predicted inflow)?"""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *
from rev_common import flows_by_origin, instrument, pop_groups
from rev_design import Resid, tsls, ar_analytic

res = {}


def read_emcr(tid):
    d = pd.read_csv(f'{RAW}/emcr_{tid}.csv', sep=';', dtype=str, encoding='utf-8-sig')
    d = d[d.Municipios.notna() & (d.Sexo == 'Ambos sexos')].copy()
    d['cmun'] = d.Municipios.str[:5]
    d['v'] = pd.to_numeric(d.Total.str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    return d.pivot_table(index='cmun', columns=['Nacionalidad', 'Periodo'], values='v', aggfunc='sum')


IN, OUTm = read_emcr(69743), read_emcr(69745)
yrs = ['2021', '2022', '2023', '2024']
pad, cen = pop_groups()
P21 = pd.concat([pad, cen]).xs(2021, level=1).P.groupby(level=0).first()
F = pd.DataFrame({'in_sp': IN['Española'][yrs].sum(1), 'out_sp': OUTm['Española'][yrs].sum(1),
                  'in_fx': IN['Extranjero'][yrs].sum(1), 'out_fx': OUTm['Extranjero'][yrs].sum(1)})
F = F.div(P21.reindex(F.index), axis=0) * 100                          # per 100 residents in 2021
F['net_sp'] = F.in_sp - F.out_sp
# treatment and instrument over the same window: foreign-born net inflow 2021-2024 and the shift-share prediction
dF = flows_by_origin().reset_index()
fl = dF[dF.year.between(2021, 2024)].groupby('cmun').FOR.sum()
munis = sorted(set(F.index) & set(P21.index))
my = pd.DataFrame([(m, y) for m in munis for y in range(2021, 2025)], columns=['cmun', 'year'])
my['Z'] = instrument(my).values
from rev_common import shares
s, lam, P0 = shares(2003)
Zc = my.groupby('cmun').Z.sum() * P0.reindex(munis).values / P21.reindex(munis).values
X = pd.read_parquet(f'{CL}/e01_X.parquet').set_index('cmun')
D = F.join(pd.DataFrame({'x21': fl.reindex(munis) / P21.reindex(munis), 'Z21': Zc, 'P21': P21.reindex(munis)}), how='inner')
D = D.join(X[PRED + ECON + ['cpro', 'fua']], how='inner').reset_index().rename(columns={'index': 'cmun'})
D = D.replace([np.inf, -np.inf], np.nan).dropna(subset=['x21', 'Z21'] + PRED + ECON)
CEN = PRED + ECON
grid = np.linspace(-20, 20, 4001)
disp = {}
for y in ['out_sp', 'in_sp', 'net_sp', 'out_fx', 'in_fx']:
    d = D.dropna(subset=[y]).copy()
    R = Resid(d, ['cpro'], CEN, 'P21')
    yr, xr, zr = R(d[y].values), R(d.x21.values * 100), R(d.Z21.values * 100)     # per pp of inflow
    o = {k: float(v) for k, v in tsls(yr, xr, zr, R.w, d.cpro.values, R.rank + 1).items()}
    o['ar'] = ar_analytic(yr, xr, zr, R.w, d.cpro.values, R.rank + 1, grid); o['n'] = len(d); o['ymean'] = wmean(d[y].values, d.P21.values)
    disp[y] = o
    print('displacement', y, round(o['b'], 3), round(o['se'], 3), 'F', round(o['F'], 1), o['ar'], 'mean', round(o['ymean'], 2))
res['displacement'] = disp
# spillovers: periphery in-migration on the core's predicted inflow
Fq = D.dropna(subset=['fua']).copy()
core = X[X.city_core == 1].reset_index().merge(D[['cmun', 'Z21', 'x21']], on='cmun').sort_values('P15', ascending=False).drop_duplicates('fua').set_index('fua')
Fq['Z_core'] = Fq.fua.map(core.Z21)
per = Fq[~Fq.cmun.isin(core.cmun) & Fq.Z_core.notna()].copy()
per['Z21p'] = per.Z21 * 100; per['Z_corep'] = per.Z_core * 100
sp = {}
for y in ['in_sp', 'out_sp', 'net_sp', 'in_fx']:
    q = per.dropna(subset=[y])
    m = pf.feols(f'{y} ~ Z21p + Z_corep + ' + ' + '.join(CEN) + ' | cpro', data=q, weights='P21', vcov={'CRV1': 'fua'})
    sp[y] = coefs(m, ['Z21p', 'Z_corep'])
    print('spill', y, sp[y])
res['spillovers'] = sp; res['n_periphery'] = int(len(per)); res['n_fua'] = int(per.fua.nunique()); res['n'] = int(len(D))
save('e06_flows.json', res)

"""Entry-gap paper: panels of new leases and regulation.
(a) Entry rents vs incomes in the deposit registers: Catalonia (mean rent, 2015-2023) and the Basque Country (rent per m2, 2016-2023),
    and the response of entry rents to the long-difference demand shock (all municipalities with data).
(b) Tourism reversal on new leases (Catalonia, quarterly): non-linear exposure bins x collapse / recovery.
(c) Regulation: Catalan tensioned-zone cap and substitution towards seasonal leases (2023Q1-2025Q4);
    the 2022-23 cap on updates and the entry gap (INE, provinces, 2021-2024)."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *
from rev_design import Resid, tsls, ar_analytic

res = {}
LD = pd.read_parquet(f'{CL}/ld_instrument_all.parquet').set_index('cmun')
A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
uc = A[A.indicator == 'Mediana de la renta por unidad de consumo'].pivot_table(index='cmun', columns='year', values='value')
# controls available for all municipalities: census 2011 (log pop, renting, vacancy) built from tract indicators
import glob
fs = []
for f in sorted(glob.glob(f'{WORK}/raw/c2011/C2011_ccaa*_Indicadores.csv')):
    e = pd.read_csv(f, dtype={'cpro': str, 'cmun': str}, usecols=['cpro', 'cmun', 't1_1', 't17_1', 't17_2', 't17_3', 't18_4'])
    fs.append(e)
E = pd.concat(fs); E['cm'] = E.cpro.str.zfill(2) + E.cmun.str.zfill(3)
E = E.groupby('cm')[['t1_1', 't17_1', 't17_2', 't17_3', 't18_4']].sum()
C11 = pd.DataFrame({'lnpop11': np.log(E.t1_1), 'rent11': E.t18_4 / E.t17_1.replace(0, np.nan), 'vac11': E.t17_3 / (E.t17_1 + E.t17_2 + E.t17_3)})
CT = ['lnpop11', 'rent11', 'vac11']


def iv(d, y, x='x2024', z='Z2024', w='P15', ctrls=CT, fe='cpro'):
    d = d.dropna(subset=[y, x, z] + ctrls).copy()
    R = Resid(d, [fe] if fe else [], ctrls, w=w)
    yr, xr, zr = R(d[y].values), R(d[x].values), R(d[z].values); wt = d[w].values.astype(float)
    o = tsls(yr, xr, zr, wt, d.cpro.values if d.cpro.nunique() > 3 else d.cmun.values, R.rank + 1)
    o['ar'] = ar_analytic(yr, xr, zr, wt, d.cpro.values if d.cpro.nunique() > 3 else d.cmun.values, R.rank + 1, np.linspace(-6, 6, 2401))
    o['n'] = len(d); o['ymean'] = wmean(d[y].values, wt)
    return o


# ---------------------------------------------------------------- (a) Catalonia: new leases (annual mean rent), all municipalities with data
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = L[L['Període'] == 'gener-desembre'].assign(cmun=lambda d: d['Codi territorial'].astype(int).astype(str).str.zfill(5))
nw = La.pivot_table(index='cmun', columns='Any', values='Renda'); nn = La.pivot_table(index='cmun', columns='Any', values='Habitatges')
Cc = pd.DataFrame({'d_new': np.log(nw[2024] / nw[2015]), 'd_new23': np.log(nw[2023] / nw[2015]), 'd_uc': np.log(uc[2023] / uc[2015]).reindex(nw.index),
                   'n15': nn[2015]}).join(LD).join(C11)
Cc = Cc[(Cc.n15 >= 30)].copy(); Cc['cpro'] = Cc.index.str[:2]; Cc['cmun'] = Cc.index
Cc['AE'] = Cc.d_new23 - Cc.d_uc
res['cat_desc'] = dict(n=len(Cc), d_new=wmean(Cc.d_new23.values, Cc.P15.values), d_uc=wmean(Cc.d_uc.dropna().values, Cc.dropna(subset=['d_uc']).P15.values),
                       share_AE_pos=float((Cc.AE.dropna() > 0).mean()))
res['cat_iv'] = {y: iv(Cc, y, x='x2023' if y != 'd_new' else 'x2024', z='Z2023' if y != 'd_new' else 'Z2024') for y in ['d_new', 'd_new23', 'AE', 'd_uc']}
# ---------------------------------------------------------------- Basque Country: new leases per m2 (EMAL)
Em = pd.read_parquet(f'{CL}/emal_muni.parquet')
pm = Em.pivot_table(index='cmun', columns='year', values='rent_m2_new'); pr = Em.pivot_table(index='cmun', columns='year', values='rent_new')
Bq = pd.DataFrame({'d_new_m2': np.log(pm[2024] / pm[2016]), 'd_new_m2_23': np.log(pm[2023] / pm[2016]), 'd_new': np.log(pr[2024] / pr[2016]),
                   'd_uc': np.log(uc[2023] / uc[2016]).reindex(pm.index)}).join(LD).join(C11)
Bq['cpro'] = Bq.index.str[:2]; Bq['cmun'] = Bq.index; Bq['AE'] = Bq.d_new_m2_23 - Bq.d_uc
Bq = Bq.dropna(subset=['d_new_m2', 'P15'])
res['bas_desc'] = dict(n=len(Bq), d_new_m2=wmean(Bq.d_new_m2_23.values, Bq.P15.values), d_uc=wmean(Bq.d_uc.values, Bq.P15.values),
                       share_AE_pos=float((Bq.AE > 0).mean()))
res['bas_iv'] = {y: iv(Bq, y, x='x2023', z='Z2023') for y in ['d_new_m2_23', 'AE']}
# ---------------------------------------------------------------- Comunitat Valenciana: deposits (proxy, robustness)
G = pd.read_parquet(f'{CL}/gva_muni.parquet')
gm = G.pivot_table(index='cmun', columns='year', values='dep_med'); gn = G.pivot_table(index='cmun', columns='year', values='n')
Vq = pd.DataFrame({'d_dep': np.log(gm[2023] / gm[2020]), 'd_uc': np.log(uc[2023] / uc[2020]).reindex(gm.index), 'n20': gn[2020]}).join(LD).join(C11)
Vq = Vq[Vq.n20 >= 30].dropna(subset=['d_dep', 'P15']); Vq['cpro'] = Vq.index.str[:2]; Vq['cmun'] = Vq.index
res['val_desc'] = dict(n=len(Vq), d_dep=wmean(Vq.d_dep.values, Vq.P15.values), d_uc=wmean(Vq.d_uc.dropna().values, Vq.dropna(subset=['d_uc']).P15.values))

# ---------------------------------------------------------------- (b) tourism reversal on Catalan new leases: exposure bins
Cq = pd.read_parquet(f'{CL}/cat_q.parquet'); Cq = Cq[Cq.year <= 2025].copy()
b19 = Cq[Cq.year == 2019].groupby('cmun').n.agg(['count', 'sum'])
Cq = Cq[Cq.cmun.isin(b19[(b19['count'] == 4) & (b19['sum'] >= 40)].index)].copy()
Cq['E'] = Cq.vutpct_2020M08.fillna(0); Cq['lnn'] = np.log(Cq.n); Cq['lnrent'] = np.log(Cq.rent)
Cq['t'] = (Cq.year - 2019) * 4 + Cq.q - 1; Cq['P19'] = Cq.cmun.map(Cq[Cq.year == 2019].groupby('cmun').P.first())
Cq['bin'] = pd.cut(Cq.E, [-0.01, 1, 3, 8, 100], labels=['b0', 'b1', 'b2', 'b3'])
per = {'covid': Cq.t.between(5, 9), 'recov': Cq.t.between(12, 19), 'late': Cq.t.between(20, 27)}
terms = []
for b in ['b1', 'b2', 'b3']:
    for k in (2, 3, 4):
        Cq[f'{b}q{k}'] = ((Cq.bin == b) & (Cq.q == k)).astype(float); terms.append(f'{b}q{k}')
    for p, msk in per.items():
        Cq[f'{b}_{p}'] = ((Cq.bin == b) & msk).astype(float)
names = [f'{b}_{p}' for b in ['b1', 'b2', 'b3'] for p in per]
for y in ['lnrent', 'lnn']:
    m = pf.feols(f'{y} ~ ' + ' + '.join(names + terms) + ' | cmun + t', data=Cq, weights='P19', vcov={'CRV1': 'cmun'})
    res[f'tour_bins_{y}'] = coefs(m, names)
res['tour_bin_munis'] = Cq.drop_duplicates('cmun').bin.value_counts().to_dict()

# ---------------------------------------------------------------- (c) regulation: tensioned-zone cap and seasonal leases
S = pd.read_parquet(f'{CL}/cat_seasonal.parquet')
Q = Cq[['cmun', 'year', 'q', 'n', 'zmrt', 'P19', 'E']].merge(S, on=['cmun', 'year', 'q'], how='left')
Q = Q[(Q.year >= 2023)].copy(); Q['n_seasonal'] = Q.n_seasonal.fillna(0)
Q['t'] = (Q.year - 2023) * 4 + Q.q - 1                              # 0 = 2023Q1; wave 1 from t=5 (2024Q2), wave 2 from t=7 (2024Q4)
Q['sh_seas'] = Q.n_seasonal / (Q.n_seasonal + Q.n); Q['ln_seas'] = np.log1p(Q.n_seasonal); Q['ln_n'] = np.log(Q.n)
Q['post1'] = ((Q.zmrt == 1) & (Q.t >= 5)).astype(float); Q['post2'] = ((Q.zmrt == 2) & (Q.t >= 7)).astype(float)
for k in (2, 3, 4):
    Q[f'Eq{k}'] = Q.E * (Q.q == k)
reg = {}
for y in ['sh_seas', 'ln_seas', 'ln_n']:
    m = pf.feols(f'{y} ~ post1 + post2 + Eq2 + Eq3 + Eq4 | cmun + t', data=Q, vcov={'CRV1': 'cmun'})
    reg[y] = coefs(m, ['post1', 'post2'])
    # event study for wave 1 against never designated (2023Q1-2025Q4)
    q1 = Q[Q.zmrt.isin([0, 1])].copy(); nm = []
    for k in range(-5, 7):
        if k == -1:
            continue
        n_ = f'e{"m" if k < 0 else "p"}{abs(k)}'; q1[n_] = ((q1.zmrt == 1) & (q1.t - 5 == k)).astype(float); nm.append(n_)
    m = pf.feols(f'{y} ~ ' + ' + '.join(nm) + ' + Eq2 + Eq3 + Eq4 | cmun + t', data=q1, vcov={'CRV1': 'cmun'})
    reg[y + '_event1'] = coefs(m, nm)
res['zmrt_seasonal'] = reg; res['seas_share_2023'] = float(Q[Q.year == 2023].n_seasonal.sum() / (Q[Q.year == 2023].n_seasonal.sum() + Q[Q.year == 2023].n.sum()))
res['seas_share_2025'] = float(Q[Q.year == 2025].n_seasonal.sum() / (Q[Q.year == 2025].n_seasonal.sum() + Q[Q.year == 2025].n.sum()))
# ---------------------------------------------------------------- the cap on updates and the entry gap, provinces 2021-2024
pa = pd.read_parquet(f'{CL}/prov_age.parquet')
pa = pa[(pa.typ == 'Índice')].pivot_table(index=['prov', 'year'], columns='age', values='val').reset_index()
pa['gap'] = np.log(pa['Nuevo contrato'] / pa['Contrato existente'])          # both indices are 100 in 2015? (relative change since 2015 base)
g = pa.pivot_table(index='prov', columns='year', values='gap')
res['prov_gap_change'] = {f'{a}_{b}': dict(mean=float((g[b] - g[a]).mean()), sd=float((g[b] - g[a]).std())) for a, b in [(2021, 2022), (2022, 2023), (2023, 2024)]}
res['national_gap_path'] = {int(y): float(v) for y, v in g.loc['00'].items()} if '00' in g.index else None
save('e02_panels_regulation.json', res)
import json
for k in ['cat_desc', 'bas_desc', 'val_desc']:
    print(k, res[k])
for k in ['cat_iv', 'bas_iv']:
    for y, v in res[k].items():
        print(k, y, round(v['b'], 3), round(v['se'], 3), 'F', round(v['F'], 1), [round(a, 2) for a in v['ar'][:2]], v['n'])
for y in ['lnrent', 'lnn']:
    print('tour', y, {k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res[f'tour_bins_{y}'].items() if isinstance(v, dict)})
print(res['tour_bin_munis'])
for y in ['sh_seas', 'ln_seas', 'ln_n']:
    print('zmrt', y, {k: (round(v['b'], 4), round(v['se'], 4)) for k, v in res['zmrt_seasonal'][y].items() if isinstance(v, dict)})
    print('   event', {k: round(v['b'], 3) for k, v in res['zmrt_seasonal'][y + '_event1'].items() if isinstance(v, dict)})
print(res['seas_share_2023'], res['seas_share_2025'], res['prov_gap_change'], res['national_gap_path'])

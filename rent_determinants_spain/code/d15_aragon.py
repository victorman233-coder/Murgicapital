"""Aragón lease-deposit register (Gobierno de Aragón open data, resource 100, CC BY 4.0): one row per deposit with year,
province, street, municipality, use, monthly rent and amount returned (missing while the deposit has not been returned).
Outputs:
  aragon_muni.parquet      municipality x year: number of new residential leases, median and mean rent, and a
                           composition-adjusted entry-rent index from a regression of log rent on year effects and street
                           fixed effects within each municipality (log points relative to 2015)
  aragon_survival.parquet  share of deposits of each cohort not returned at the time of download (lease survival)"""
import json
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *

d = pd.read_csv(f'{RAW}/aragon/fianzas_100.csv', low_memory=False)
v = d[(d.tipo == 'Vivienda') & d.total_rentas.between(100, 5000) & d.anyo.between(1996, 2025)].copy()
T = json.load(open(f'{WORK}/raw/geo/municipalities.json'))
names = pd.DataFrame([(g['id'], g['properties']['name']) for g in list(T['objects'].values())[0]['geometries']], columns=['cmun', 'name'])
names = names[names.cmun.str[:2].isin(['22', '44', '50'])]
names['key'] = names.cmun.str[:2] + names.name.map(norm)
v['key'] = v.codigo_provincia.astype(int).astype(str).str.zfill(2) + v.nombre_municipio.map(norm)
v = v.merge(names[['key', 'cmun']], on='key', how='left')
ALIAS = {'PUEBLA DE ALFINDEN': '50219', 'PINA': '50208', 'QUINTO DE EBRO': '50222', 'BREA': '50057', 'OSERA': '50199',
         'MEDIANA': '50164', 'GELSA DE EBRO': '50119', 'TORLA': '22230'}     # register names that differ from INE names
v['cmun'] = v.cmun.fillna(v.nombre_municipio.map(ALIAS))
match = float(v.cmun.notna().mean())
print('matched deposits', round(match, 4), v[v.cmun.isna()].nombre_municipio.value_counts().head(10).to_dict())
v = v.dropna(subset=['cmun'])
v['lr'] = np.log(v.total_rentas)
v['street'] = v.cmun + '_' + v.clave_calle.astype(str)
A = v.groupby(['cmun', 'year' if 'year' in v else 'anyo']).agg(n=('lr', 'size'), rent_med=('total_rentas', 'median'),
                                                               rent_mean=('total_rentas', 'mean')).reset_index().rename(columns={'anyo': 'year'})
# composition-adjusted index: municipalities with at least 30 deposits per year on average in 2012-2024
big = A[A.year.between(2012, 2024)].groupby('cmun').n.mean()
big = big[big >= 30].index
rows = []
for c in big:
    s = v[(v.cmun == c) & v.anyo.between(2010, 2025)]
    m = pf.feols('lr ~ i(anyo, ref=2015) | street', data=s, vcov='hetero')
    t = m.tidy()
    for k, r in t.iterrows():
        yr = int(str(k).split('::')[1].split(']')[0].split('.')[0])
        rows.append(dict(cmun=c, year=yr, idx_street=float(r['Estimate'])))
    rows.append(dict(cmun=c, year=2015, idx_street=0.0))
I = pd.DataFrame(rows)
A = A.merge(I, on=['cmun', 'year'], how='left')
A.to_parquet(f'{CL}/aragon_muni.parquet')
print('Aragón', A.shape, 'munis with street index', len(big))
print(A[A.cmun == '50297'].tail(12).round(3).to_string())
# lease survival by cohort: share of deposits not returned (snapshot at download)
v['open'] = v.total_devolucion.isna()
Sv = v.groupby('anyo').agg(n=('open', 'size'), open_share=('open', 'mean')).reset_index().rename(columns={'anyo': 'cohort'})
Sz = v[v.cmun == '50297'].groupby('anyo').open.mean().rename('open_share_zgz').reset_index().rename(columns={'anyo': 'cohort'})
Sv = Sv.merge(Sz, on='cohort', how='left')
Sv.to_parquet(f'{CL}/aragon_survival.parquet')
print(Sv.tail(14).round(3).to_string())
save('d15_aragon.json', dict(match_rate=match, n_deposits=int(len(v)), munis_index=int(len(big))))

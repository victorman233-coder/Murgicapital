"""Extended municipal characteristics for the revision (all predetermined unless noted).

Sources (all downloaded from official open-data endpoints, see DATA_SOURCES.md):
  - INE Census 2011 section indicators (raw/c2011): education, age, rooms, surface, tenure
  - INE Census 2021 section indicators (raw/c2021): households, dwellings, tenure (2021)
  - INE DIRCE table 4721 (firms by municipality and activity), 2012: sector structure
  - Eurostat LAU-2021 correspondence (DEGURBA, coastal flag, city and FUA codes)
  - Generalitat de Catalunya open data: tensioned residential market zones (ZMRT 1/2),
    PTSH demand areas (used to approximate the 2020-22 rent-containment perimeter)
Output: WORK/clean/muni_extended.parquet indexed by 5-digit INE code.
"""
import os, glob
import numpy as np, pandas as pd
WORK = os.environ.get('WORK', '/home/user/work')
R = f'{WORK}/raw'

# ---------------------------------------------------------------- census 2011 indicators
fs = sorted(glob.glob(f'{R}/c2011/C2011_ccaa*_Indicadores.csv'))
c = pd.concat([pd.read_csv(f, dtype={'ccaa': str, 'cpro': str, 'cmun': str, 'dist': str, 'secc': str}) for f in fs])
c['cmun5'] = c['cpro'] + c['cmun']
rooms_k = np.arange(1, 10)
c['rooms_tot'] = sum(c[f't20_{k}'] * k for k in rooms_k)          # 9 = '9 or more' (lower bound)
c['dw_rooms'] = c[[f't20_{k}' for k in rooms_k]].sum(axis=1, min_count=9)
mids = [25, 37.5, 53, 68, 83, 98, 113, 135.5, 165.5, 200]           # interval midpoints, m2
c['m2_tot'] = sum(c[f't19_{k}'] * m for k, m in zip(range(1, 11), mids))
c['dw_m2'] = c[[f't19_{k}' for k in range(1, 11)]].sum(axis=1, min_count=10)
c['edu_ad'] = c[['t12_1', 't12_2', 't12_3', 't12_4', 't12_5']].sum(axis=1, min_count=5)
agg = c.groupby('cmun5').agg(pop11=('t1_1', 'sum'), age65=('t3_3', 'sum'), age16=('t3_1', 'sum'),
                             tert=('t12_5', 'sum'), edu_ad=('edu_ad', 'sum'), rooms_tot=('rooms_tot', 'sum'),
                             dw_rooms=('dw_rooms', 'sum'), m2_tot=('m2_tot', 'sum'), dw_m2=('dw_m2', 'sum'),
                             hh11=('t21_1', 'sum'), rentdw11=('t18_4', 'sum'), dwmain11=('t17_1', 'sum'))
X = pd.DataFrame(index=agg.index)
X['sh65_11'] = agg.age65 / agg.pop11
X['tert11'] = agg.tert / agg.edu_ad
X['rooms_per_dw11'] = agg.rooms_tot / agg.dw_rooms
X['m2_per_dw11'] = agg.m2_tot / agg.dw_m2
X['persons_per_room11'] = (agg.pop11 / agg.dwmain11) / X['rooms_per_dw11']     # pop / (main dwellings x rooms per dwelling)
X['m2_per_person11'] = X['m2_per_dw11'] * agg.dwmain11 / agg.pop11
X['renters11'] = agg.rentdw11                                               # rented main dwellings (weight)
X['hh11'] = agg.hh11
X['pop11c'] = agg.pop11

# ---------------------------------------------------------------- census 2021 indicators (registers-based)
c21 = pd.read_csv(f'{R}/c2021/C2021_Indicadores.csv', dtype={'ccaa': str, 'cpro': str, 'cmun': str, 'dist': str, 'secc': str})
c21['cmun5'] = c21['cpro'] + c21['cmun']
a21 = c21.groupby('cmun5').agg(pop21=('t1_1', 'sum'), dwmain21=('t19_1', 'sum'), hh21=('t21_1', 'sum'))
X = X.join(a21, how='outer')

# ---------------------------------------------------------------- DIRCE 2012 sector structure (non-agricultural firms)
d = pd.read_csv(f'{R}/ine_4721.csv', sep=';', dtype=str, encoding='utf-8-sig')
d = d[d['Municipios'].notna() & (d['Periodo'] == '2012')]
d['cmun5'] = d['Municipios'].str[:5]
d['v'] = pd.to_numeric(d['Total'].str.replace('.', '', regex=False), errors='coerce')
F = d.pivot_table(index='cmun5', columns='Grupos CNAE', values='v', aggfunc='first')
X['firms12_pc'] = F['Total'] / X['pop11c']
X['sh_constr12'] = F['F Construcción'] / F['Total']
X['sh_ind12'] = F['Industria'] / F['Total']
X['sh_trade_hosp12'] = F['Comercio, transporte y hostelería'] / F['Total']
X['sh_realestate12'] = F['L Actividades inmobiliarias'] / F['Total']

# ---------------------------------------------------------------- Eurostat LAU 2021: DEGURBA, coast, city, FUA
L = pd.read_excel(f'{R}/gisco/EU-27-LAU-2021-NUTS-2021.xlsx', 'ES', dtype={'LAU CODE': str})
L['cmun5'] = L['LAU CODE'].str.zfill(5)
L = L.set_index('cmun5')
X['degurba'] = L['DEGURBA']
X['coastal'] = (L['COASTAL AREA (yes/no)'].str.lower() == 'yes').astype(float)
X['fua'] = L['FUA_ID']
X['city_core'] = L['CITY_ID'].notna().astype(float)
X['area_km2'] = L['TOTAL AREA (m2)'] / 1e6

# ---------------------------------------------------------------- Catalan housing-policy zones
A = pd.read_csv(f'{R}/cat/arees_referencia_habitatge.csv', dtype={'Codi INE': str})
A['cmun5'] = A['Codi INE'].str.zfill(5)
A = A.set_index('cmun5')
X['cat_zmrt1'] = (A['Zona de mercat residencial tensat'] == 'ZMRT 1').astype(float).reindex(X.index).fillna(0)
X['cat_zmrt2'] = (A['Zona de mercat residencial tensat'] == 'ZMRT 2').astype(float).reindex(X.index).fillna(0)
adfa = A['Municipis segons àrea del PTSH'].isin(['ADFA 1', 'ADFA 2']).astype(float).reindex(X.index).fillna(0)
# approximation of the 2020-22 rent-containment perimeter (Catalan Law 11/2020): strong-demand areas, >20,000 inh.
X['cat_rc2020'] = ((adfa == 1) & (X['pop11c'] > 20000)).astype(float)
X.index.name = 'cmun'
X.to_parquet(f'{WORK}/clean/muni_extended.parquet')
print(X.describe().T[['count', 'mean', 'min', 'max']].to_string())
print('Catalan RC-2020 proxy municipalities:', int(X.cat_zmrt1.sum()), int(X.cat_rc2020.sum()))

"""Build the analysis files.
  muni_panel.parquet  municipality x year (2011-2024): IPVA, population, shift-share inflow and instrument (2012-2024 sample of
                      the companion paper), tourist dwellings (INE, 2020-2026), cadastral dwellings, household income (ADRH)
  cat_q.parquet       Catalan municipality x quarter (2019Q1-2025Q4): new-lease rents and counts, tensioned-zone designation,
                      tourist-dwelling exposure (INE 2020, Catalan tourism register), tourist-tax revenue from tourist dwellings
  national.parquet    national annual series; prov_age.parquet: provincial IPVA by contract age (2021-2024)
"""
import os, sys, re, unicodedata
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'revision_JOPE-D-26-01206', 'code'))
from rev_common import load_revision_panel, WORK, REP
RAW = f'{WORK}/rent/raw'; CL = f'{WORK}/rent/clean'; os.makedirs(CL, exist_ok=True)
num = lambda s: pd.to_numeric(s.astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')


def ine(t):
    return pd.read_csv(f'{RAW}/ine_{t}.csv', sep=';', encoding='utf-8-sig', dtype=str)


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"\(.*?\)", '', s)
    m = re.match(r"^(.*), (l'|el|la|els|les|lo|los|las)$", s.strip())          # 'Escala, l'' -> 'l'escala'
    if m:
        s = (m.group(2) + ('' if m.group(2).endswith("'") else ' ') + m.group(1))
    return re.sub(r"[^a-z]", '', s)


# ------------------------------------------------------------------ municipal IPVA, 2011-2024 (all published municipalities)
ip = ine(59060); ip = ip[(ip['Tipo de dato'] == 'Índice') & ip.Municipio.str[:5].str.isdigit()]
ip = ip.assign(cmun=ip.Municipio.str[:5], year=ip.Periodo.astype(int), R=num(ip.Total))[['cmun', 'year', 'R']].dropna()
ip['lnR'] = np.log(ip.R)

# ------------------------------------------------------------------ population (register to 2021, census from 2021; growth within source)
lev = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
pad = lev[lev.src == 'padron'].set_index(['cmun', 'year'])[['P', 'FOR']]
cen = lev[lev.src == 'censo'].set_index(['cmun', 'year'])[['P', 'FOR']]
pop = pad.copy()
for y in range(2022, 2026):                         # chain census growth onto the 2021 register level
    g = (cen.xs(y, level='year') / cen.xs(2021, level='year'))
    base = pad.xs(2021, level='year')
    add = (base * g).dropna(); add['year'] = y
    pop = pd.concat([pop[pop.index.get_level_values('year') != y], add.reset_index().set_index(['cmun', 'year'])])
pop = pop.sort_index().reset_index()

# ------------------------------------------------------------------ tourist dwellings (INE experimental statistic)
v = ine(39363); v = v[v.Municipios.notna() & v.Municipios.str[:5].str.isdigit()]
v = v.assign(cmun=v.Municipios.str[:5], per=v.Periodo, val=num(v.Total))
vut = v[v['Viviendas y plazas'] == 'Viviendas turísticas'].pivot_table(index='cmun', columns='per', values='val')
vut.columns = [f'vut_{c}' for c in vut.columns]
vp = ine(39366); vp = vp[vp.Municipios.notna() & vp.Municipios.str[:5].str.isdigit()]
vp = vp.assign(cmun=vp.Municipios.str[:5], val=num(vp.Total)).pivot_table(index='cmun', columns='Periodo', values='val')
vp.columns = [f'vutpct_{c}' for c in vp.columns]
VUT = vut.join(vp, how='outer')
VUT.to_parquet(f'{CL}/vut_muni.parquet')

# ------------------------------------------------------------------ cadastral dwellings and household income
cat = pd.read_parquet(f'{REP}/data/clean/catastro_muni.parquet')[['cmun', 'year', 'viv']]
inc = None
if os.path.exists(f'{CL}/adrh_muni.parquet'):
    A = pd.read_parquet(f'{CL}/adrh_muni.parquet')
    inc = A[A.indicator == 'Renta neta media por persona'].rename(columns={'value': 'inc_pp'})[['cmun', 'year', 'inc_pp']]
    inc = inc.drop_duplicates(['cmun', 'year'])

# ------------------------------------------------------------------ municipal panel
M = ip.merge(pop, on=['cmun', 'year'], how='left').merge(cat, on=['cmun', 'year'], how='left')
if inc is not None:
    M = M.merge(inc, on=['cmun', 'year'], how='left')
rp = load_revision_panel()
keep = ['cmun', 'year', 'xc', 'Zc', 'w', 'w_rent', 'cy', 'cpro', 'ccaa', 'size_cl', 'pop11', 'lnpop11', 'rent11', 'vac11', 'tert11', 'sh65_11',
        'lninc15', 'sh_constr12', 'sh_ind12', 'sh_trade_hosp12', 'firms12_pc', 'coastal', 'city_core', 'fua', 'area_km2', 'degurba',
        'cat_zmrt1', 'cat_zmrt2', 'renters11', 'hh11', 'dwmain21']
M = M.merge(rp[keep], on=['cmun', 'year'], how='left')
static = rp.drop_duplicates('cmun').set_index('cmun')[[c for c in keep if c not in ('cmun', 'year', 'xc', 'Zc', 'w', 'w_rent', 'cy')]]
for c in static.columns:
    M[c] = M[c].fillna(M.cmun.map(static[c]))
M['cpro'] = M.cmun.str[:2]
M = M.merge(VUT[[c for c in VUT.columns if c in ('vut_2020M08', 'vut_2024M08', 'vutpct_2020M08', 'vutpct_2024M08', 'vut_2026M05', 'vutpct_2026M05')]],
            left_on='cmun', right_index=True, how='left')
M['in_sample'] = M.cmun.isin(rp.cmun.unique())
M.to_parquet(f'{CL}/muni_panel.parquet')
print('municipal panel', M.shape, M.cmun.nunique(), 'sample munis', M[M.in_sample].cmun.nunique())

# ------------------------------------------------------------------ Catalonia: new leases by quarter
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
Q = {'gener-març': 1, 'abril-juny': 2, 'juliol-setembre': 3, 'octubre-desembre': 4}
L = L[L['Període'].isin(Q)].assign(q=lambda d: d['Període'].map(Q))
L['cmun'] = L['Codi territorial'].astype(int).astype(str).str.zfill(5)
L = L.rename(columns={'Any': 'year', 'Habitatges': 'n', 'Renda': 'rent'})[['cmun', 'year', 'q', 'n', 'rent']]
L['n'] = pd.to_numeric(L.n, errors='coerce'); L['rent'] = pd.to_numeric(L.rent, errors='coerce')
L['t'] = L.year * 4 + L.q - 1
Aa = pd.read_csv(f'{RAW}/cat/arees_referencia_habitatge.csv')
Aa['cmun'] = Aa['Codi INE'].astype(int).astype(str).str.zfill(5)
Aa['zmrt'] = Aa['Zona de mercat residencial tensat'].map({'ZMRT 1': 1, 'ZMRT 2': 2}).fillna(0).astype(int)
L = L.merge(Aa[['cmun', 'zmrt', 'Comarca']], on='cmun', how='left')
p = pop.copy(); p['year'] = p.year.clip(upper=2025)
L = L.merge(pop[['cmun', 'year', 'P']], on=['cmun', 'year'], how='left')
L['P'] = L.groupby('cmun').P.transform(lambda s: s.ffill().bfill())
# tourist-dwelling exposure: INE share of dwellings (Aug 2020) and the Catalan tourism register (current stock, owner type)
L = L.merge(VUT[['vutpct_2020M08', 'vut_2020M08']], left_on='cmun', right_index=True, how='left')
T = pd.read_csv(f'{RAW}/cat/registre_turisme.csv', dtype=str)
T = T[(T['Tipus establiment'] == "Habitatges d'ús turístic") & (T['Estat'] == 'Alta')]
T['cmun'] = T['Codi Municipi (IDESCAT)'].str.zfill(6).str[:5]
T['corp'] = T['Raó Social del titular'].fillna('No aplica').ne('No aplica')
H = T.groupby('cmun').agg(hut=('corp', 'size'), hut_corp=('corp', 'sum'))
L = L.merge(H, left_on='cmun', right_index=True, how='left')
# tourist-stay tax (IEET) paid by tourist dwellings, by municipality and semester (name match)
I = pd.read_csv(f'{RAW}/cat/ieet_municipi.csv', dtype=str)
I['sem'] = I['Període autoliquidació']; I['key'] = I.Municipi.map(norm)
I['ht_quota'] = num(I['HT - quota IEET'])
names = Aa.assign(key=Aa.Municipi.map(norm)).drop_duplicates('key').set_index('key').cmun
I['cmun'] = I.key.map(names)
print('IEET municipalities matched:', I.cmun.notna().mean().round(3), I[I.cmun.isna()].Municipi.unique()[:10])
IE = I.dropna(subset=['cmun']).pivot_table(index='cmun', columns='sem', values='ht_quota', aggfunc='sum')
IE.columns = [f'ht_{c}' for c in IE.columns]
IE.to_parquet(f'{CL}/ieet_ht.parquet')
L.to_parquet(f'{CL}/cat_q.parquet')
print('Catalan quarterly', L.shape, L.cmun.nunique(), L.t.min() // 4, L.t.max() // 4)

# ------------------------------------------------------------------ provincial IPVA by contract age and national series
pa = ine(59005)
pa = pa.assign(prov=pa.Provincias.fillna('00 Total Nacional').str[:2], age=pa['Antigüedad del contrato de arrendamiento'], typ=pa['Tipo de dato'],
               year=pa.Periodo.astype(int), val=num(pa.Total))[['prov', 'age', 'typ', 'year', 'val']]
pa.to_parquet(f'{CL}/prov_age.parquet')
c = ine(50902); c = c[(c['Grupos ECOICOP'] == 'Índice general') & (c['Tipo de dato'] == 'Índice')]
cpi = c.assign(year=c.Periodo.str[:4].astype(int), v=num(c.Total)).groupby('year').v.mean().rename('cpi')
nat = ine(59060); nat = nat[(nat.Municipio == 'Total Nacional') & (nat['Tipo de dato'] == 'Índice')]
nat = nat.assign(year=nat.Periodo.astype(int), ipva=num(nat.Total)).set_index('year').ipva
e = pd.read_csv(f'{RAW}/ecb/euribor12m.csv'); e['year'] = e.TIME_PERIOD.str[:4].astype(int)
eur = e.groupby('year').OBS_VALUE.mean().rename('euribor12m')
ag = ine(59004); ag = ag[ag.iloc[:, 1].isna() & (ag['Tipo de dato'] == 'Índice')]
ag = ag.assign(year=ag.Periodo.astype(int), val=num(ag.Total)).pivot_table(index='year', columns='Antigüedad del contrato de arrendamiento', values='val')
ag.columns = ['ipva_' + {'Total': 'total', 'Nuevo contrato': 'new', 'Contrato existente': 'existing'}[c] for c in ag.columns]
wt = ine(59008); wt = wt.assign(year=wt.Periodo.astype(int), val=num(wt.Total)).pivot_table(index='year', columns='Antigüedad del contrato de arrendamiento', values='val')
wt = (wt['Nuevo contrato'] / 1000).rename('w_new')
pn = pop[pop.cmun == '00000'].set_index('year')[['P', 'FOR']] if (pop.cmun == '00000').any() else None
N = pd.concat([nat, cpi, eur, ag, wt] + ([pn] if pn is not None else []), axis=1).sort_index()
N.to_parquet(f'{CL}/national.parquet'); print(N.loc[2011:2025].round(3).to_string())

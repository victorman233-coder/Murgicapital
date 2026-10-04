"""Build the additional analysis files for the entry-gap paper.
  emal_muni.parquet      Basque Country: new leases (deposits by contract start year), mean rent and rent per m2, 2016-2025
  gva_muni.parquet       Comunitat Valenciana: deposits by municipality and year (count, median and mean deposit), 2020-2026
  cat_seasonal.parquet   Catalonia: seasonal leases by municipality and quarter, 2023-2026
  aeat_cp_2024.parquet   AEAT 2024 by postal code (new vs all leases) within large cities
  mivau_vt.parquet       MIVAU appraised value of free-market housing (EUR/m2), municipalities >25k, Q4 of each year"""
import io, os, re, unicodedata
import numpy as np, pandas as pd
WORK = os.environ.get('WORK', '/home/user/work'); RAW = f'{WORK}/rent/raw'; CL = f'{WORK}/rent/clean'


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower().strip()
    m = re.match(r'^(.*?)\s*\((el|la|los|las|l\'|els|les|o|a|os|as)\)$', s) or re.match(r'^(.*?),\s*(el|la|los|las|l\'|els|les|o|a|os|as)$', s)
    if m:
        s = m.group(2) + ' ' + m.group(1)
    s = {'palma de mallorca': 'palma', 'mahon': 'mao', 'san cristobal laguna': 'san cristobal de la laguna',
         'santa coloma gramanet': 'santa coloma de gramenet', 'santa eulalia del rio': 'santa eularia des riu'}.get(s, s)
    s = s.split('/')[0]
    return re.sub(r'[^a-z]', '', s)


# ------------------------------------------------------------------ Basque Country (EMAL), annual tables by municipality (>5k)
x = pd.ExcelFile(f'{RAW}/emal/EMAL_barrios_municipios_2016_2025.xlsx')
out = {}
for sh, var in [('T2.1', 'n_new'), ('T2.2', 'rent_new'), ('T2.3', 'rent_m2_new')]:
    d = pd.read_excel(x, sh, header=None)
    isyr = lambda v: pd.notna(pd.to_numeric(v, errors='coerce')) and 2000 < float(pd.to_numeric(v, errors='coerce')) < 2100
    yrow = [i for i in range(8) if sum(isyr(v) for v in d.iloc[i].values) >= 5][0]
    years = {j: int(float(v)) for j, v in enumerate(d.iloc[yrow].values) if isyr(v)}
    for i in range(yrow + 1, len(d)):
        code = str(d.iat[i, 0]).strip()
        if re.fullmatch(r'\d{5}', code):
            for j, y in years.items():
                v = pd.to_numeric(d.iat[i, j], errors='coerce')
                out.setdefault((code, y), {})[var] = v
E = pd.DataFrame([dict(cmun=k[0], year=k[1], **v) for k, v in out.items()])
E.to_parquet(f'{CL}/emal_muni.parquet'); print('EMAL', E.shape, E.cmun.nunique(), E.year.min(), E.year.max())

# ------------------------------------------------------------------ Comunitat Valenciana deposits (microdata -> municipality x year)
g = []
for f in sorted(os.listdir(f'{RAW}/gva')):
    d = pd.read_csv(f'{RAW}/gva/{f}', sep=';', dtype=str)
    d['cmun'] = d.cod_provincia.str.zfill(2) + d.cod_municipio.str.zfill(3)
    d['dep'] = pd.to_numeric(d.importe_fianza, errors='coerce')
    d = d[(d.dep >= 100) & (d.dep <= 10000)]                                  # implausible deposits dropped
    g.append(d.groupby(['cmun', 'anyo_datos']).dep.agg(n='size', dep_med='median', dep_mean='mean').reset_index())
G = pd.concat(g).rename(columns={'anyo_datos': 'year'}); G['year'] = G.year.astype(int)
G.to_parquet(f'{CL}/gva_muni.parquet'); print('GVA', G.shape, G.groupby('year').n.sum().to_dict())

# ------------------------------------------------------------------ Catalonia seasonal leases (quarterly counts by municipality)
c = pd.ExcelFile(f'{RAW}/cat2/lloguer_temporada_mun.xlsx'); rows = []
for sh in c.sheet_names:
    d = pd.read_excel(c, sh, header=None)
    hdr = [i for i in range(10) if str(d.iat[i, 0]).strip() == 'Codi'][0]
    qcols = {j: q for j, q in zip(range(4, 8), [1, 2, 3, 4])}
    for i in range(hdr + 1, len(d)):
        code = str(d.iat[i, 0]).strip()
        if re.fullmatch(r'\d{5}', code):
            for j, q in qcols.items():
                v = pd.to_numeric(d.iat[i, j], errors='coerce')
                if pd.notna(v):
                    rows.append((code, int(sh), q, v))
S = pd.DataFrame(rows, columns=['cmun', 'year', 'q', 'n_seasonal'])
S.to_parquet(f'{CL}/cat_seasonal.parquet'); print('Seasonal', S.shape, S.groupby('year').n_seasonal.sum().to_dict())

# ------------------------------------------------------------------ AEAT 2024 by postal code
h = open(f'{RAW}/aeat/aeat_newcontracts_cp_2024.html', encoding='utf-8', errors='replace').read()
t = pd.read_html(io.StringIO(h), decimal=',', thousands='.')[0]
t.columns = ['loc', 'rent', 'rent_new', 'm2', 'm2_new', 'vr', 'vr_new', 'yld', 'yld_new']
cur = None; rows = []
for _, r in t.iterrows():
    m = re.search(r'-(\d{5})\s*$', str(r['loc'])); p = re.match(r'^(\d{5})-', str(r['loc']))
    if m and not p:
        cur = m.group(1)
    elif p and cur:
        rows.append(dict(cmun=cur, cp=p.group(1), **{k: pd.to_numeric(r[k], errors='coerce') for k in t.columns[1:]}))
CP = pd.DataFrame(rows)
CP['G'] = np.log(CP.rent_new / CP.rent); CP['G_m2'] = np.log((CP.rent_new / CP.m2_new) / (CP.rent / CP.m2))
CP['G_vr'] = np.log((CP.rent_new / CP.vr_new) / (CP.rent / CP.vr))
CP.to_parquet(f'{CL}/aeat_cp_2024.parquet'); print('AEAT CP', CP.shape, CP.cmun.nunique())

# ------------------------------------------------------------------ MIVAU appraised value (EUR/m2), municipalities >25k, Q4
ip = pd.read_csv(f'{RAW}/ine_59060.csv', sep=';', encoding='utf-8-sig', dtype=str)
nm = ip[ip.Municipio.str[:5].str.isdigit()].Municipio.drop_duplicates()
names = pd.DataFrame({'cmun': nm.str[:5], 'key': nm.str[6:].map(norm)})
prov_names = {}
x = pd.ExcelFile(f'{RAW}/mivau/valor_tasado_muni.xls'); rows = []
for y in range(2015, 2026):
    sh = [s for s in x.sheet_names if s.strip() == f'T4A{y}']
    if not sh:
        continue
    d = pd.read_excel(x, sh[0], header=None)
    prov = None
    for i in range(16, len(d)):
        if pd.notna(d.iat[i, 1]) and str(d.iat[i, 1]).strip() not in ('', 'nan'):
            prov = str(d.iat[i, 1]).strip()
        mun = d.iat[i, 2]
        if pd.isna(mun) or prov is None:
            continue
        v = pd.to_numeric(d.iat[i, 5], errors='coerce')
        rows.append(dict(year=y, prov=prov, mun=str(mun).strip(), vt=v, key=norm(mun)))
V = pd.DataFrame(rows).merge(names, on='key', how='left')
print('MIVAU match rate', round(V.cmun.notna().mean(), 3), V[V.cmun.isna()].mun.unique()[:15])
V.dropna(subset=['cmun']).to_parquet(f'{CL}/mivau_vt.parquet')

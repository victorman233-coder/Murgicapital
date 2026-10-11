"""INE Atlas de Distribucion de Renta de los Hogares (ADRH): download the 54 provincial tables
'Indicadores de renta media y mediana' and keep municipal rows only (no district / census-tract rows).
Output: $WORK/rent/clean/adrh_muni.parquet with cmun, year, indicator, value."""
import io, json, os, subprocess, sys, urllib.request
import pandas as pd
WORK = os.environ.get('WORK', '/home/user/work'); RAW = f'{WORK}/rent/raw'; CL = f'{WORK}/rent/clean'; os.makedirs(CL, exist_ok=True)
ids = json.load(urllib.request.urlopen('https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/353', timeout=120))
ids = [t['Id'] for t in ids if t['Nombre'].strip() == 'Indicadores de renta media y mediana']
out = []
for t in ids:
    f = f'{RAW}/adrh/{t}.parquet'; os.makedirs(f'{RAW}/adrh', exist_ok=True)
    if not os.path.exists(f):
        tmp = f'{RAW}/adrh/{t}.csv'
        subprocess.run(['curl', '-sS', '--retry', '4', '--max-time', '1800', '-o', tmp, f'https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv'], check=True)
        d = pd.read_csv(tmp, sep=';', dtype=str, encoding='utf-8-sig')
        os.remove(tmp)
        if not {'Municipios', 'Distritos', 'Secciones'} <= set(d.columns):     # table with another layout: not used
            print('skipped', t, list(d.columns)); os.path.exists(tmp) and os.remove(tmp); continue
        d = d[d['Distritos'].isna() & d['Secciones'].isna() & d['Municipios'].notna()]
        d.to_parquet(f)
    d = pd.read_parquet(f)
    d = d.rename(columns={d.columns[3]: 'indicator'})
    d['cmun'] = d['Municipios'].str[:5]; d['year'] = d['Periodo'].astype(int)
    d['value'] = pd.to_numeric(d['Total'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    out.append(d[['cmun', 'year', 'indicator', 'value']]); print(t, len(d), flush=True)
A = pd.concat(out, ignore_index=True)
A.to_parquet(f'{CL}/adrh_muni.parquet'); print(A.indicator.unique(), A.year.min(), A.year.max(), A.cmun.nunique())

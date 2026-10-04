"""INE ADRH extra indicators at municipal level: demographic indicators (30832: household size, % Spanish nationals, age)
and income by source (30825: wage share). National tables, municipal rows kept."""
import os, subprocess
import pandas as pd
WORK = os.environ.get('WORK', '/home/user/work'); RAW = f'{WORK}/rent/raw/adrh'; CL = f'{WORK}/rent/clean'
for t in [30832, 30825]:
    out = f'{CL}/adrh_{t}_muni.parquet'
    if os.path.exists(out):
        continue
    tmp = f'{RAW}/{t}.csv'
    subprocess.run(['curl', '-sS', '--retry', '4', '--max-time', '3600', '-o', tmp, f'https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv'], check=True)
    rows = []
    for ch in pd.read_csv(tmp, sep=';', dtype=str, encoding='utf-8-sig', chunksize=500000):
        rows.append(ch[ch['Distritos'].isna() & ch['Secciones'].isna() & ch['Municipios'].notna()])
    d = pd.concat(rows); d = d.rename(columns={d.columns[3]: 'indicator'})
    d['cmun'] = d.Municipios.str[:5]; d['year'] = d.Periodo.astype(int)
    d['value'] = pd.to_numeric(d.Total.str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    d[['cmun', 'year', 'indicator', 'value']].to_parquet(out); os.remove(tmp)
    print(t, len(d), d.indicator.unique())

"""Parse INE jaxiT3 long CSV files (semicolon, UTF-8 with BOM) into compact parquet.

Usage: python r00_parse_ine_long.py <table_id> <municipality_column> <category_column>
Keeps Sexo == 'Total' (when present) and municipality rows with a 5-digit INE code.
Output: <WORK>/clean/ine_<table>.parquet with columns cmun, cat, year, v.
"""
import sys, os, re
import numpy as np, pandas as pd

WORK = os.environ.get('WORK', '/home/user/work')
tab, mcol, ccol = sys.argv[1], sys.argv[2], sys.argv[3]
src = f'{WORK}/raw/ine_{tab}.csv'
out = []
for ch in pd.read_csv(src, sep=';', dtype=str, encoding='utf-8-sig', chunksize=2_000_000):
    ch.columns = [c.replace('﻿', '').replace('ï»¿', '') for c in ch.columns]
    if 'Sexo' in ch.columns:
        ch = ch[ch['Sexo'] == 'Total']
    m = ch[mcol].astype(str)
    is_nat = m.str.startswith('Total Nacional')
    code = m.str.extract(r'^(\d{5})\s')[0]
    code = code.where(~is_nat, '00000')
    ch = ch.assign(cmun=code).dropna(subset=['cmun'])
    yr = ch['Periodo'].astype(str).str.extract(r'(\d{4})')[0].astype(int)
    v = pd.to_numeric(ch['Total'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
    out.append(pd.DataFrame({'cmun': ch['cmun'].values, 'cat': ch[ccol].values, 'year': yr.values, 'v': v.values}))
d = pd.concat(out, ignore_index=True)
d['cat'] = d['cat'].astype('category')
d.to_parquet(f'{WORK}/clean/ine_{tab}.parquet')
print(tab, d.shape, d.cmun.nunique(), sorted(d.year.unique()))
print(d['cat'].cat.categories.tolist()[:300])

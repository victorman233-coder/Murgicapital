"""Rebuild municipality x year x origin-group stocks (33 groups) from the INE downloads.

Inputs (downloaded by r00):  raw/ine_33573.csv (Padrón 2003-2022, country of birth)
                             raw/ine_66322.csv (Estadística continua de población 2021-2025)
Output: clean/pop_groups_nacim.parquet with the same layout as the author's build_data.py
(cmun, year, P, NAT, 33 groups, FOR, src), including the national row cmun='00000'.
The grouping replicates build_data.py exactly (28 countries + 5 continental residuals).
"""
import os, sys
import numpy as np, pandas as pd
WORK = os.environ.get('WORK', '/home/user/work')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'revision_JOPE-D-26-01206', 'code'))
COUNTRIES = ['Alemania', 'Bulgaria', 'Francia', 'Italia', 'Polonia', 'Portugal', 'Rumanía',
             'Reino Unido', 'Rusia', 'Ucrania', 'Argelia', 'Marruecos', 'Nigeria', 'Senegal',
             'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Cuba', 'Ecuador', 'Paraguay',
             'Perú', 'República Dominicana', 'Uruguay', 'Venezuela', 'China', 'Pakistán']
CONT = {'Europa': COUNTRIES[:10], 'Africa': COUNTRIES[10:14], 'America': COUNTRIES[14:26], 'Asia': COUNTRIES[26:]}
GROUPS = COUNTRIES + ['Resto_Europa', 'Resto_Africa', 'Resto_America', 'Resto_Asia', 'Oceania_otros']


def padron():
    d = pd.read_parquet(f'{WORK}/clean/ine_33573.parquet')
    W = d.pivot_table(index=['cmun', 'year'], columns='cat', values='v', aggfunc='first', observed=True)
    out = pd.DataFrame(index=W.index)
    out['P'] = W['Total']; out['NAT'] = W['España']
    for c in COUNTRIES:
        out[c] = W[c].fillna(0)
    out['Resto_Europa'] = W['Europa (sin España)'] - out[CONT['Europa']].sum(axis=1)
    out['Resto_Africa'] = W['África'] - out[CONT['Africa']].sum(axis=1)
    out['Resto_America'] = W['América'] - out[CONT['America']].sum(axis=1)
    out['Resto_Asia'] = W['Asia'] - out[CONT['Asia']].sum(axis=1)
    out['Oceania_otros'] = W['Oceanía']
    out['FOR'] = out[GROUPS].sum(axis=1)
    out['src'] = 'padron'
    return out.reset_index()


def censo():
    rows = []
    for ch in pd.read_csv(f'{WORK}/raw/ine_66322.csv', sep=';', dtype=str, encoding='utf-8-sig', chunksize=2_000_000):
        ch = ch[ch['Sexo'] == 'Total']
        nat = ch['Provincias'].isna() & ch['Municipios'].isna()
        code = ch['Municipios'].str.extract(r'^(\d{5})\s')[0]
        code = code.where(~nat, '00000')
        ch = ch.assign(cmun=code).dropna(subset=['cmun'])
        v = pd.to_numeric(ch['Total'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce')
        rows.append(pd.DataFrame({'cmun': ch['cmun'].values, 'cat': ch['Lugar de nacimiento (principales países)'].values,
                                  'year': ch['Periodo'].astype(int).values, 'v': v.values}))
    d = pd.concat(rows, ignore_index=True)
    W = d.pivot_table(index=['cmun', 'year'], columns='cat', values='v', aggfunc='first').fillna(0)
    cols = list(W.columns)
    eu_other = [c for c in cols if c.startswith('Otros países de la Unión') or c.startswith('Otros países de Europa')]
    europe_all = ['Bélgica', 'Bulgaria', 'Dinamarca', 'Finlandia', 'Francia', 'Irlanda', 'Italia', 'Países Bajos', 'Polonia',
                  'Portugal', 'Alemania', 'Rumanía', 'Suecia', 'Lituania', 'Noruega', 'Reino Unido', 'Suiza', 'Ucrania',
                  'Moldavia', 'Rusia'] + eu_other
    africa_all = ['Argelia', 'Gambia', 'Ghana', 'Guinea', 'Guinea Ecuatorial', 'Mali', 'Marruecos', 'Mauritania', 'Nigeria',
                  'Senegal'] + [c for c in cols if c.startswith('Otros países de África')]
    america_all = ['Canadá', 'Estados Unidos de América', 'México', 'Cuba', 'Honduras', 'Nicaragua', 'República Dominicana',
                   'Argentina', 'Bolivia', 'Brasil', 'Colombia', 'Chile', 'Ecuador', 'Paraguay', 'Perú', 'Uruguay', 'Venezuela'] + \
                  [c for c in cols if c.startswith('Otro país de Centro') or c.startswith('Otros países de Sudam')]
    asia_all = ['Bangladesh', 'China', 'Filipinas', 'India', 'Pakistán'] + [c for c in cols if c.startswith('Otros países de Asia')]
    other = [c for c in cols if c in ('Oceanía', 'Apátridas')]
    for grp in (europe_all, africa_all, america_all, asia_all):
        miss = [c for c in grp if c not in cols]
        assert not miss, miss
    out = pd.DataFrame(index=W.index)
    out['P'] = W['Total']; out['NAT'] = W['España']
    for c in COUNTRIES:
        out[c] = W[c]
    out['Resto_Europa'] = W[europe_all].sum(axis=1) - out[CONT['Europa']].sum(axis=1)
    out['Resto_Africa'] = W[africa_all].sum(axis=1) - out[CONT['Africa']].sum(axis=1)
    out['Resto_America'] = W[america_all].sum(axis=1) - out[CONT['America']].sum(axis=1)
    out['Resto_Asia'] = W[asia_all].sum(axis=1) - out[CONT['Asia']].sum(axis=1)
    out['Oceania_otros'] = W[other].sum(axis=1)
    out['FOR'] = out[GROUPS].sum(axis=1)
    print('censo accounting gap (max abs):', float((out['P'] - out['NAT'] - out['FOR']).abs().max()))
    # extra origins used in the push-shock event studies (not part of the 33 groups)
    for c in ['Honduras', 'Nicaragua', 'México', 'Estados Unidos de América']:
        out['x_' + c] = W[c]
    out['src'] = 'censo'
    return out.reset_index()


if __name__ == '__main__':
    pad = padron(); cen = censo()
    allp = pd.concat([pad, cen], ignore_index=True)
    allp.to_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
    nat = allp[allp.cmun == '00000'].sort_values(['src', 'year'])
    print(nat[['src', 'year', 'P', 'NAT', 'FOR', 'Marruecos', 'Colombia', 'Venezuela', 'Rumanía', 'Reino Unido']].to_string())
    print('municipalities:', allp.cmun.nunique())

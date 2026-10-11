"""INE Encuesta de Presupuestos Familiares (household budget survey), public-use microdata 2016-2024.
Households renting at market price (REGTEN = 3): annual rent paid for the main residence (ECOICOP 04110; GASTO is grossed up
by the household weight, so the household amount is GASTO / FACTOR), monthly net household income (IMPEXAC, exact amount;
from 2024 mostly reported in intervals, so an interval-midpoint measure INTERIN is built for every year), equivalence scale
(UC2), floor area (SUPERF), age and nationality of the reference person, region and municipality size.
Output: epf_renters.parquet (one row per renting household and year) and out/d16_epf.json with weighted summaries by group
(the interval-midpoint income is the comparable measure across years, because exact income is missing for most of 2024):
young (reference person under 35), foreign nationality, and the rest, which are likelier to be recent entrants."""
import io, zipfile
import numpy as np, pandas as pd
from rd_common import *

MID = {'01': 250, '02': 750, '03': 1250, '04': 1750, '05': 2250, '06': 2750, '07': 4000, '08': 6000, '09': 8000, '10': 11000}
H = ['ANOENC', 'NUMERO', 'CCAA', 'TAMAMU', 'FACTOR', 'NMIEMB', 'UC2', 'EDADSP', 'NACIONASP', 'REGTEN', 'SUPERF', 'IMPEXAC', 'INTERIN']


def member(oz, kind):
    names = oz.namelist()
    inner = [n for n in names if kind in n.lower() and n.lower().endswith('.zip') and 'mhogar' not in n.lower()][0]
    iz = zipfile.ZipFile(io.BytesIO(oz.read(inner)))
    pq = [n for n in iz.namelist() if n.endswith('.parquet')][0]
    return pd.read_parquet(io.BytesIO(iz.read(pq)))


DEC = {'GASTO': 2, 'FACTOR': 6, 'UC2': 1}                 # implied decimals of fixed-width fields (record layout)


def num(v, dec=0):
    """Numeric value of a field stored either as a number or as fixed-width text with implied decimals (2016-2021 files)."""
    t = v.astype(str).str.strip()
    x = pd.to_numeric(t.str.replace(',', '.', regex=False), errors='coerce')
    if v.dtype == object and dec and not t.str.contains(r'[.,]', regex=True).any():
        x = x / 10 ** dec
    return x


rows = []
for y in range(2016, 2025):
    oz = zipfile.ZipFile(f'{RAW}/epf/datos_{y}.zip')
    h = member(oz, 'hogar')[H].copy()
    g = member(oz, 'gastos')
    g = g[g.CODIGO.astype(str) == '04110']
    rent = (num(g.GASTO, 2) / num(g.FACTOR, 6)).groupby(g.NUMERO.astype(int)).sum()
    h['NUMERO'] = h.NUMERO.astype(int)
    for c in ['FACTOR', 'NMIEMB', 'UC2', 'EDADSP', 'SUPERF', 'IMPEXAC', 'ANOENC']:
        h[c] = num(h[c], DEC.get(c, 0))
    for c in ['CCAA', 'TAMAMU', 'REGTEN', 'NACIONASP', 'INTERIN']:
        h[c] = h[c].astype(str)
    h['rent_m'] = h.NUMERO.map(rent) / 12
    rows.append(h)
    print(y, len(h), int((h.REGTEN.astype(str) == '3').sum()))
D = pd.concat(rows, ignore_index=True)
D['REGTEN'] = D.REGTEN.astype(str).str.strip(); D['NACIONASP'] = D.NACIONASP.astype(str).str.strip()
D['INTERIN'] = D.INTERIN.astype(str).str.strip().str.zfill(2)
D['inc_mid'] = D.INTERIN.map(MID)
D['inc_exact'] = D.IMPEXAC.where(D.IMPEXAC > 0)
R = D[(D.REGTEN == '3') & (D.rent_m > 50)].copy()
R['young'] = R.EDADSP < 35
R['foreign'] = R.NACIONASP == '2'
R['group'] = np.select([R.foreign, R.young], ['foreign', 'young_native'], 'other')
R['burden'] = R.rent_m / R.inc_exact
R['burden_mid'] = R.rent_m / R.inc_mid
R['rent_m2'] = R.rent_m / R.SUPERF.where(R.SUPERF > 0)
R['inc_uc'] = R.inc_exact / R.UC2
R.to_parquet(f'{CL}/epf_renters.parquet')


def wq(x, w, q=0.5):
    m = np.isfinite(x) & np.isfinite(w); x, w = x[m], w[m]
    o = np.argsort(x); c = np.cumsum(w[o]) / w[o].sum()
    return float(x[o][np.searchsorted(c, q)])


res = {'n_renters': R.groupby('ANOENC').size().to_dict(), 'share_exact_income': R.groupby('ANOENC').inc_exact.apply(lambda s: s.notna().mean()).round(3).to_dict()}
tab = []
for (y, gname), q in list(R.groupby(['ANOENC', 'group'])) + [((y, 'all'), q) for y, q in R.groupby('ANOENC')]:
    w = q.FACTOR.values
    tab.append(dict(year=int(y), group=gname, n=len(q), rent=wq(q.rent_m.values, w), rent_m2=wq(q.rent_m2.values, w),
                    inc=wq(q.inc_exact.values, w), inc_uc=wq(q.inc_uc.values, w), size=float(np.average(q.NMIEMB, weights=w)),
                    burden=wq(q.burden.values, w), burden_mid=wq(q.burden_mid.values, w),
                    over40=float(np.average((q.burden > 0.4)[q.burden.notna()], weights=w[q.burden.notna()])) if q.burden.notna().any() else np.nan,
                    over40_mid=float(np.average((q.burden_mid > 0.4)[q.burden_mid.notna()], weights=w[q.burden_mid.notna()])),
                    n_mid=int(q.burden_mid.notna().sum())))
T = pd.DataFrame(tab).sort_values(['group', 'year'])
res['table'] = T.round(4).to_dict('records')
print(T[T.year.isin([2016, 2019, 2023, 2024])].round(3).to_string())
save('d16_epf.json', res)

# premium per m2 of foreign-national and young renters by year, conditional on region, municipality size and floor area
import pyfixest as pf
Q = R[np.isfinite(np.log(R.rent_m2)) & R.SUPERF.between(20, 300)].copy()
Q['lrm2'] = np.log(Q.rent_m2); Q['lsup'] = np.log(Q.SUPERF); Q['yr'] = Q.ANOENC.astype(int)
Q['fy'] = Q.foreign.astype(int); Q['yy'] = (Q.young & ~Q.foreign).astype(int)
mm = pf.feols('lrm2 ~ i(yr, fy) + i(yr, yy) + lsup | yr + CCAA + TAMAMU', data=Q, weights='FACTOR', vcov='hetero')
t = mm.tidy()
prem = {}
for k, r in t.iterrows():
    if 'fy' in k or 'yy' in k:
        prem[k] = dict(b=float(r['Estimate']), se=float(r['Std. Error']))
res['premium_m2'] = prem
fo = {int(k.split('::')[1].split(':')[0]): v for k, v in prem.items() if k.endswith(':fy')}
yo = {int(k.split('::')[1].split(':')[0]): v for k, v in prem.items() if k.endswith(':yy')}
res['premium_foreign'] = fo; res['premium_young'] = yo
# change 2016 -> 2023/24 in the foreign premium, with a pooled test
Q['late'] = (Q.yr >= 2022).astype(int); Q['early'] = (Q.yr <= 2018).astype(int)
m2 = pf.feols('lrm2 ~ fy + fy:late + yy + yy:late + lsup | yr + CCAA + TAMAMU', data=Q[(Q.late == 1) | (Q.early == 1)], weights='FACTOR', vcov='hetero')
res['premium_change'] = coefs(m2, ['fy', 'fy:late', 'yy', 'yy:late'])
print({y: round(v['b'], 3) for y, v in sorted(fo.items())}, {y: round(v['b'], 3) for y, v in sorted(yo.items())})
print(res['premium_change'])
save('d16_epf.json', res)

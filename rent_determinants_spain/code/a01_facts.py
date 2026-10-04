"""Stylised facts: (i) national stock index vs inflation and vs new contracts (index identity, eq. 5);
(ii) rent growth 2015-2024 by municipality size, coast and tourist intensity; (iii) how much of municipal rent growth
is common (year / province-year) and how much is local; (iv) new-contract vs stock rents in Catalonia."""
import numpy as np, pandas as pd
import pyfixest as pf
from rd_common import *

N = pd.read_parquet(f'{CL}/national.parquet')
res = {}
# (i) national: real stock rents and the contribution of new vs existing leases, 2022-2024
r = N.loc[[2011, 2015, 2019, 2021, 2024]]
res['national'] = dict(ipva_2015_2024=N.ipva[2024] / N.ipva[2015] - 1, cpi_2015_2024=N.cpi[2024] / N.cpi[2015] - 1,
                       real_ipva_2015_2024=(N.ipva[2024] / N.ipva[2015]) / (N.cpi[2024] / N.cpi[2015]) - 1,
                       ipva_2019_2024=N.ipva[2024] / N.ipva[2019] - 1, cpi_2019_2024=N.cpi[2024] / N.cpi[2019] - 1,
                       new_2021_2024=N.ipva_new[2024] / N.ipva_new[2021] - 1, existing_2021_2024=N.ipva_existing[2024] / N.ipva_existing[2021] - 1,
                       cpi_2021_2024=N.cpi[2024] / N.cpi[2021] - 1)
dec = []
for y in [2022, 2023, 2024]:
    gn = N.ipva_new[y] / N.ipva_new[y - 1] - 1; ge = N.ipva_existing[y] / N.ipva_existing[y - 1] - 1; gt = N.ipva[y] / N.ipva[y - 1] - 1
    wn = N.w_new[y]
    dec.append(dict(year=y, total=gt, new=gn, existing=ge, w_new=wn, contrib_new=wn * gn, contrib_existing=(1 - wn) * ge,
                    cpi=N.cpi[y] / N.cpi[y - 1] - 1))
res['index_identity'] = dec

# (ii) municipal growth 2015-2024 by group
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
w15 = M[M.year == 2015].set_index('cmun')
g = M[M.year.isin([2015, 2024])].pivot_table(index='cmun', columns='year', values='lnR')
G = pd.DataFrame({'dlnR': g[2024] - g[2015]}).join(w15[['P', 'coastal', 'city_core', 'cpro', 'ccaa', 'vutpct_2020M08']]).dropna(subset=['dlnR', 'P'])
G['size'] = pd.cut(G.P, SIZE_EDGES, labels=SIZE_LABELS)
G['vut_t'] = pd.qcut(G.vutpct_2020M08.rank(method='first'), 3, labels=['low', 'mid', 'high'])
G['g'] = np.exp(G.dlnR) - 1
tab = {}
for col in ['size', 'coastal', 'vut_t']:
    tab[col] = {str(k): dict(n=len(q), g_w=wmean(q.g.values, q.P.values), g_med=float(q.g.median()),
                             p10=float(q.g.quantile(.1)), p90=float(q.g.quantile(.9)))
                for k, q in G.groupby(col, observed=True)}
tab['all'] = dict(n=len(G), g_w=wmean(G.g.values, G.P.values), g_med=float(G.g.median()), p10=float(G.g.quantile(.1)), p90=float(G.g.quantile(.9)))
res['growth_2015_2024'] = tab
G.to_parquet(f'{CL}/ld_2015_2024_basic.parquet')

# (iii) common vs local components of annual rent growth, 2016-2024 (sample of IPVA municipalities)
D = M.sort_values(['cmun', 'year']).copy()
D['dlnR'] = D.groupby('cmun').lnR.diff()
D = D[(D.year >= 2016) & D.dlnR.notna() & D.P.notna()].copy()
D['wt'] = D.groupby('cmun').P.transform('first')
D['py'] = D.cpro + '_' + D.year.astype(str); D['ay'] = D.ccaa.fillna('NA') + '_' + D.year.astype(str)
r2 = {}


def wr2(m, y, w):
    e = np.asarray(m.resid()).ravel(); yy = y[np.isfinite(y)] if len(e) != len(y) else y
    return float(1 - np.sum(w * e ** 2) / np.sum(w * (y - np.average(y, weights=w)) ** 2))


for k, f in [('year', 'dlnR ~ 1 | year'), ('ccaa_year', 'dlnR ~ 1 | ay'), ('province_year', 'dlnR ~ 1 | py'),
             ('province_year_muni', 'dlnR ~ 1 | py + cmun')]:
    m = pf.feols(f, data=D, weights='wt', fixef_rm='none')
    r2[k] = wr2(m, D.dlnR.values, D.wt.values)
res['variance_shares_annual'] = r2
# long difference: share of cross-municipal variance of 2015-2024 growth explained by province
Gr = G.reset_index()
m = pf.feols('dlnR ~ 1 | cpro', data=Gr, weights='P', fixef_rm='none')
res['variance_share_ld_province'] = wr2(m, Gr.dlnR.values, Gr.P.values)

# (iv) Catalonia: new-contract rents (deposits register) vs stock index (IPVA), same municipalities
L = pd.read_csv(f'{RAW}/cat/lloguer_municipi.csv')
La = L[L['Període'] == 'gener-desembre'].assign(cmun=lambda d: d['Codi territorial'].astype(int).astype(str).str.zfill(5))
La = La.pivot_table(index='cmun', columns='Any', values='Renda')
cat_ip = M[M.cpro.isin(['08', '17', '25', '43'])].pivot_table(index='cmun', columns='year', values='R')
both = La.index.intersection(cat_ip.index)
wts = w15.P.reindex(both)
comp = {}
for a, b in [(2015, 2024), (2019, 2024)]:
    gn = (La.loc[both, b] / La.loc[both, a] - 1); gs = (cat_ip.loc[both, b] / cat_ip.loc[both, a] - 1)
    ok = gn.notna() & gs.notna()
    comp[f'{a}_{b}'] = dict(n=int(ok.sum()), new_w=wmean(gn[ok].values, wts[ok].values), stock_w=wmean(gs[ok].values, wts[ok].values),
                            corr=float(np.corrcoef(gn[ok], gs[ok])[0, 1]))
res['catalonia_new_vs_stock'] = comp
save('a01_facts.json', res)
import json; print(json.dumps(res, indent=1, default=float)[:4000])

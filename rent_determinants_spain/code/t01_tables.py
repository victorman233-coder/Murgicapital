"""LaTeX tables and number macros (paper/tab)."""
import numpy as np
from rd_common import *

F = load('a01_facts.json'); L2 = load('a02_local.json'); T = load('a03_tourism.json'); R = load('a04_regulation.json')
I = load('a05_investors_credit.json'); K = load('a06_ranking.json')
f = lambda x, d=2: ('$-$' if x < 0 else '') + f'{abs(x):.{d}f}' if x is not None and np.isfinite(x) else '--'
pc = lambda x, d=1: f(100 * x, d)
ar = lambda a: '[' + ', '.join('$-\\infty$' if v == -np.inf else '$\\infty$' if v == np.inf else f(v) for v in a[:2]) + ']'
star = lambda p: '' if p is None else '***' if p < .01 else '**' if p < .05 else '*' if p < .1 else ''
W = lambda name, s: open(os.path.join(TAB, name), 'w').write(s)
mac = []
DIG = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
m = lambda k, v: mac.append(f'\\newcommand{{\\{"".join(DIG.get(c, c) for c in k)}}}{{{v}}}')

# ------------------------------------------------------------------ Table 1: what rose
g = F['growth_2015_2024']
rows = [('All IPVA municipalities', g['all'])] + [(f'{k} inhabitants', g['size'][k]) for k in SIZE_LABELS] + \
       [('Inland', g['coastal']['0.0']), ('Coastal', g['coastal']['1.0'])] + \
       [(f'Tourist-dwelling share 2020: {k} tercile', g['vut_t'][k]) for k in ['low', 'mid', 'high']]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Growth of the rent index for all leases, 2015--2024, by type of municipality}\label{tab:facts}',
     r'\begin{tabular}{lcccc}\toprule', r' & Municipalities & Weighted mean (\%) & p10 (\%) & p90 (\%)\\\midrule']
for lab, q in rows:
    s.append(f"{lab.replace('k', ',000').replace('>', '$>$').replace('-', '--')} & {q['n']} & {pc(q['g_w'])} & {pc(q['p10'])} & {pc(q['p90'])}\\\\")
    if lab.startswith('All') or lab.startswith('>') or lab == 'Coastal':
        s.append(r'\addlinespace')
s += [r'\bottomrule\end{tabular}', r'\begin{minipage}{0.92\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: growth of the INE IPVA (all leases in force declared in income-tax returns) between 2015 and 2024; means weighted by 2015 population. '
      r'Size classes by 2015 population. Tourist-dwelling share: INE experimental statistic, August 2020, as a percentage of dwellings. Over the same period consumer prices rose by '
      + pc(F['national']['cpi_2015_2024']) + r'\,\%.', r'\end{minipage}\end{table}']
W('t1_facts.tex', '\n'.join(s))
n = F['national']
m('ipvaGrowth', pc(n['ipva_2015_2024'])); m('cpiGrowth', pc(n['cpi_2015_2024'])); m('realIpva', pc(n['real_ipva_2015_2024']))
m('newGrowth', pc(n['new_2021_2024'])); m('existGrowth', pc(n['existing_2021_2024'])); m('cpiTwoOne', pc(n['cpi_2021_2024']))
for d in F['index_identity']:
    y = str(d['year'])[2:]
    m(f'wNew{y}', pc(d['w_new'])); m(f'gNew{y}', pc(d['new'])); m(f'gExist{y}', pc(d['existing'])); m(f'cNew{y}', pc(d['contrib_new'], 2))
    m(f'cExist{y}', pc(d['contrib_existing'], 2)); m(f'gTot{y}', pc(d['total'])); m(f'cpiY{y}', pc(d['cpi']))
cn = F['catalonia_new_vs_stock']['2015_2024']
m('catNew', pc(cn['new_w'], 0)); m('catStock', pc(cn['stock_w'], 0)); m('catN', cn['n'])
vs = F['variance_shares_annual']
m('vsYear', pc(vs['year'], 0)); m('vsCcaa', pc(vs['ccaa_year'], 0)); m('vsProv', pc(vs['province_year'], 0)); m('vsLdProv', pc(F['variance_share_ld_province'], 0))
m('gSmall', pc(g['size']['10-20k']['g_w'])); m('gBig', pc(g['size']['>500k']['g_w']))

# ------------------------------------------------------------------ Table 2: population, supply, income (long differences)
def ivrow(lab, k):
    q = L2[k]
    return f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {q['n']}\\\\"
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Local demand and supply: long differences 2015--2024 within provinces}\label{tab:local}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccccc}\toprule',
     r'Outcome (2015--2024) on foreign-born inflow 2016--2024 & 2SLS & SE & AR 95\% set & First-stage $F$ & $N$\\\midrule',
     r'\multicolumn{6}{l}{\textit{A. Population weights}}\\',
     ivrow('Log rent index (all leases)', 'rent_inflow_w'), ivrow('Log population', 'dlnP_inflow_w'),
     ivrow('Log rent index per log point of population', 'rent_dlnP_w'), ivrow('Log dwellings (cadastre)', 'viv_inflow_w'),
     ivrow('Falsification: log rent index 2012--2015', 'pre_inflow_w'), r'\addlinespace',
     r'\multicolumn{6}{l}{\textit{B. Unweighted}}\\', ivrow('Log rent index (all leases)', 'rent_inflow_unw'), ivrow('Log dwellings (cadastre)', 'viv_inflow_unw'),
     r'\addlinespace', r'\multicolumn{6}{l}{\textit{C. Log rent index by size and location (population weights)}}\\',
     ivrow('Municipalities below 50,000 inhabitants', 'rent_inflow_big0'), ivrow('Municipalities of 50,000 or more', 'rent_inflow_big1'),
     ivrow('Inland', 'rent_inflow_coast0'), ivrow('Coastal', 'rent_inflow_coast1'), r'\midrule',
     r'\multicolumn{6}{l}{\textit{D. Descriptive horse race, OLS (coefficient per standard deviation of each regressor)}}\\']
o = L2['ols_horse_race']
for k, lab in [('xc_s', 'Foreign-born inflow 2016--2024'), ('dlninc_s', 'Log net income per person 2015--2023'),
               ('vut20_s', 'Tourist-dwelling share 2020'), ('dlnviv_s', 'Log dwellings 2015--2024')]:
    if k in o:
        s.append(f"{lab} & {f(o[k]['b'], 4)}{star(o[k]['p'])} & ({f(o[k]['se'], 4)}) & & & {o['n']}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: one observation per municipality. The inflow is the sum over 2016--2024 of the annual net change in the foreign-born population relative '
      r'to population (centred timing), instrumented with the corresponding sum of shift-share predictions (33 origins, 2003 settlement, national growth excluding the own province). '
      r'All regressions include province fixed effects and the central controls of the companion paper (2011 census: log population, renting, vacancy, tertiary education, '
      r'share aged 65+; 2012: construction, industry and trade-hospitality shares of firms, firms per capita; coastal and FUA-core indicators). Standard errors clustered by province; '
      r'AR: Anderson-Rubin set. Panel D: OLS with the same fixed effects and controls; none of these regressors is instrumented. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.',
      r'\end{minipage}\end{table}']
W('t2_local.tex', '\n'.join(s))
q = L2['rent_inflow_w']; m('bPop', f(q['b'])); m('bPopSe', f(q['se'])); m('bPopAR', ar(q['ar'])); m('bPopF', f(q['F'], 1))
m('bPopP', f(L2['dlnP_inflow_w']['b'])); m('bPopPAR', ar(L2['dlnP_inflow_w']['ar'])); m('bViv', f(L2['viv_inflow_w']['b'])); m('bVivAR', ar(L2['viv_inflow_w']['ar']))
m('bPre', f(L2['pre_inflow_w']['b'])); m('bPreAR', ar(L2['pre_inflow_w']['ar'])); m('bPopUnwF', f(L2['rent_inflow_unw']['F'], 1))
m('bBig', f(L2['rent_inflow_big1']['b'])); m('bBigAR', ar(L2['rent_inflow_big1']['ar'])); m('bSmall', f(L2['rent_inflow_big0']['b'])); m('bSmallAR', ar(L2['rent_inflow_big0']['ar']))
m('bRentP', f(L2['rent_dlnP_w']['b'])); m('bRentPAR', ar(L2['rent_dlnP_w']['ar']))
if 'dlninc_s' in o:
    m('bInc', f(o['dlninc_s']['b'] * 100, 2)); m('bIncP', f(o['dlninc_s']['p'], 2))

# ------------------------------------------------------------------ Table 3: tourism
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Tourist dwellings and long-term rents: the 2020--21 collapse of tourism and the recovery}\label{tab:tourism}',
     r'\begin{tabular}{lcccc}\toprule', r' & \multicolumn{2}{c}{New-lease rents (log)} & \multicolumn{2}{c}{New leases signed (log)}\\\cmidrule(lr){2-3}\cmidrule(lr){4-5}',
     r'Exposure (pp of dwellings in tourist use) $\times$ & Coef.$\times$100 & SE & Coef.$\times$100 & SE\\\midrule']
for k, lab in [('E_q120', '2020Q1 (placebo)'), ('E_covid', 'Collapse: 2020Q2--2021Q2'), ('E_recov', 'Recovery: 2022--2023'), ('E_late', '2024--2025')]:
    a, b = T['cat_pooled_lnrent'][k], T['cat_pooled_lnn'][k]
    s.append(f"{lab} & {f(100 * a['b'])}{star(a['p'])} & ({f(100 * a['se'])}) & {f(100 * b['b'])}{star(b['p'])} & ({f(100 * b['se'])})\\\\")
s += [f"Municipalities / observations & \\multicolumn{{2}}{{c}}{{{T['cat_n_munis']} / {T['cat_pooled_lnrent']['n']}}} & \\multicolumn{{2}}{{c}}{{{T['cat_n_munis']} / {T['cat_pooled_lnn']['n']}}}\\\\",
      r'\bottomrule\end{tabular}', r'\begin{minipage}{0.92\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: Catalan municipalities with new leases in every quarter of 2019 and at least 40 in that year; quarters 2019Q1--2025Q4. Exposure: tourist dwellings as a percentage of all dwellings in August 2020 (INE). '
      r'Regressions include municipality and quarter fixed effects, exposure $\times$ calendar-quarter terms (seasonality of tourist letting) and log 2019 population $\times$ quarter; reference period 2019Q1--2019Q4. '
      r'Population weights; standard errors clustered by municipality. In 2020 the tourist-stay tax paid by tourist dwellings in Catalonia fell to '
      + pc(T['ieet_ratio_2020_2019'], 0) + r'\,\% of its 2019 level and in 2021 it was ' + pc(T['ieet_ratio_2021_2019'], 0) + r'\,\%. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.',
      r'\end{minipage}\end{table}']
W('t3_tourism.tex', '\n'.join(s))
for k, nm in [('E_covid', 'Covid'), ('E_recov', 'Recov'), ('E_late', 'Late'), ('E_q120', 'Placebo')]:
    m(f'tR{nm}', f(100 * T['cat_pooled_lnrent'][k]['b'])); m(f'tN{nm}', f(100 * T['cat_pooled_lnn'][k]['b']))
    m(f'tR{nm}P', f(T['cat_pooled_lnrent'][k]['p'], 3)); m(f'tN{nm}P', f(T['cat_pooled_lnn'][k]['p'], 3))
m('ieetTwenty', pc(T['ieet_ratio_2020_2019'], 0)); m('ieetTwentyOne', pc(T['ieet_ratio_2021_2019'], 0))
ev = T['ipva_event']
m('ipvaEvTwelve', f(100 * ev['E_2012']['b'])); m('ipvaEvTwenty', f(100 * ev['E_2020']['b'])); m('ipvaEvTwentyFour', f(100 * ev['E_2024']['b']))
m('expMean', f(T['ipva_event_meanE'], 1)); m('expSd', f(T['ipva_event_sdE'], 1)); m('catExpMean', f(T['cat_meanE'], 1)); m('catMunis', T['cat_n_munis'])
m('vutTwenty', f'{T["vut_national"]["2020M08"]:,.0f}'); m('vutTwentyFour', f'{T["vut_national"]["2024M08"]:,.0f}'); m('vutTwentySix', f'{T["vut_national"]["2026M05"]:,.0f}')

# ------------------------------------------------------------------ Table 4: regulation
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Caps on rents: the Catalan tensioned-zone cap (2024) and the cap on annual updates (2022--2023)}\label{tab:regulation}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccccc}\toprule',
     r' & Treated & Controls & \multicolumn{2}{c}{New-lease rents (log)} & \multicolumn{2}{c}{New leases signed (log)}\\\cmidrule(lr){4-5}\cmidrule(lr){6-7}',
     r' & & & Post & Pre-trend adj. & Post & Pre-trend adj.\\\midrule',
     r'\multicolumn{7}{l}{\textit{A. Tensioned-zone cap on new contracts, Catalonia (stacked comparisons, unweighted)}}\\']
for k, lab in [('zmrt1_vs_notyet', 'Wave 1 vs not yet designated, to 2024Q3'), ('zmrt1_vs_never', 'Wave 1 vs never designated, to 2025Q4'),
               ('zmrt2_vs_never', 'Wave 2 vs never designated, to 2025Q4')]:
    q = R[k]; a = q['lnrent']; b = q['lnn']
    s.append(f"{lab} & {q['n_treat']} & {q['n_ctrl']} & {f(a['pooled']['post']['b'], 3)} ({f(a['pooled']['post']['se'], 3)}) & {f(a['detrended']['post']['b'], 3)} & "
             f"{f(b['pooled']['post']['b'], 3)} ({f(b['pooled']['post']['se'], 3)}) & {f(b['detrended']['post']['b'], 3)}\\\\")
s.append(r'\multicolumn{7}{l}{\textit{Population-weighted}}\\')
for k, lab in [('zmrt1_vs_notyet_w', 'Wave 1 vs not yet designated, to 2024Q3'), ('zmrt2_vs_never_w', 'Wave 2 vs never designated, to 2025Q4')]:
    q = R[k]; a = q['lnrent']; b = q['lnn']
    s.append(f"{lab} & {q['n_treat']} & {q['n_ctrl']} & {f(a['pooled']['post']['b'], 3)} ({f(a['pooled']['post']['se'], 3)}) & {f(a['detrended']['post']['b'], 3)} & "
             f"{f(b['pooled']['post']['b'], 3)} ({f(b['pooled']['post']['se'], 3)}) & {f(b['detrended']['post']['b'], 3)}\\\\")
pn = R['prov_new_contracts_new']['cat24']; pe = R['prov_new_contracts_existing']['cat24']
s += [r'\addlinespace', r'\multicolumn{7}{l}{\textit{B. Provinces: growth of the IPVA in 2024, Catalan provinces vs the rest (2022--2024)}}\\',
      f"New contracts & 4 & 44 & {f(pn['b'], 4)} ({f(pn['se'], 4)}) & & & \\\\", f"Existing contracts & 4 & 44 & {f(pe['b'], 4)} ({f(pe['se'], 4)}) & & & \\\\",
      r'\addlinespace', r'\multicolumn{7}{l}{\textit{C. Cap on annual updates of existing leases (2\,\%), Spain}}\\']
u = R['update_cap']['by_year']
for y in ['2022', '2023']:
    s.append(f"{y}: growth of existing leases {pc(u[y]['existing'])}\\,\\%, CPI {pc(u[y]['cpi'])}\\,\\% & \\multicolumn{{6}}{{l}}{{gap in the index for all leases: {f(u[y]['gap_pp'], 1)} pp}}\\\\")
s += [f"Cumulative 2022--2023 & \\multicolumn{{6}}{{l}}{{index for all leases {pc(R['update_cap']['cumulative_gap'])}\\,\\% higher if existing leases had followed the CPI}}\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, Catalan municipalities with new leases in every quarter of 2019 (at least 40 in the year); wave 1: 140 municipalities designated on 16 March 2024 '
      r'(first full quarter 2024Q2); wave 2: 131 designated in October 2024 (first full quarter 2024Q4). Regressions include municipality and quarter fixed effects, '
      r'tourist-dwelling exposure $\times$ calendar quarter and $\times$ the 2020--21 and 2022--23 periods. Post: average post-treatment coefficient, standard error clustered by municipality in parentheses. '
      r'Pre-trend adjusted: outcome net of a treated-group linear trend estimated on pre-treatment quarters. Panel B: province and year fixed effects, standard errors clustered by province. '
      r'Panel C: accounting with INE weights of new and existing leases; it is an upper bound because not all leases are indexed to the CPI and annual averages are used.',
      r'\end{minipage}\end{table}']
W('t4_regulation.tex', '\n'.join(s))
for k, nm in [('zmrt1_vs_notyet', 'One'), ('zmrt1_vs_never', 'OneNever'), ('zmrt2_vs_never', 'Two')]:
    m(f'capR{nm}', pc(R[k]['lnrent']['pooled']['post']['b'])); m(f'capN{nm}', pc(R[k]['lnn']['pooled']['post']['b'], 0))
    m(f'capRd{nm}', pc(R[k]['lnrent']['detrended']['post']['b'])); m(f'capNd{nm}', pc(R[k]['lnn']['detrended']['post']['b'], 0))
m('capGap', pc(R['update_cap']['cumulative_gap'])); m('provNew', f(100 * pn['b'], 2)); m('provExist', f(100 * pe['b'], 2))
agg = R['cat_leases_by_year_q']
m('catLeasesTwentyThree', f'{sum(agg["2023"].values()):,.0f}'); m('catLeasesTwentyFive', f'{sum(agg["2025"].values()):,.0f}')

# ------------------------------------------------------------------ Table 5: ranking
A = K['A_national_stock']
rows = [('General inflation (CPI), via indexation and new contracts', 'Accounting', f(100 * A['cpi'], 1), '', 'Common'),
        ('Cap on updates of existing leases, 2022--2023', 'Accounting (upper bound)', f(100 * A['update_cap']['contrib'], 1), '', 'Common'),
        ('Population growth driven by immigration', 'Shift-share IV', f(100 * A['population']['contrib'], 1),
         f"[{f(100 * A['population']['lo'], 1)}, {f(100 * A['population']['hi'], 1)}]", 'Larger in big cities'),
        ('Household income (real)', 'OLS, not identified', f(100 * A['income_ols']['contrib'], 1) if 'income_ols' in A else '--',
         f"[{f(100 * A['income_ols']['lo'], 1)}, {f(100 * A['income_ols']['hi'], 1)}]" if 'income_ols' in A else '', 'Uniform'),
        ('Tourist dwellings, 2015--2019', 'Event study (exposure)', f(100 * A['tourism']['contrib_2015_2019'], 2), '', 'Tourist municipalities'),
        ('Tourist dwellings, 2019--2024', 'Event study (exposure)', f(100 * A['tourism']['contrib_2019_2024'], 2), '', 'Tourist municipalities'),
        ('Supply response of the dwelling stock', 'Shift-share IV', '$\\approx$ 0', '', 'Absent everywhere'),
        ('Tensioned-zone cap (Catalonia, 2024--)', 'Stacked DiD (new leases)', '--', '', 'Catalonia: ' + pc(R['zmrt1_vs_never']['lnrent']['pooled']['post']['b']) + '\\,\\% on new leases'),
        ('Large owners and investment funds', 'Not identified', '--', '', 'No association found'),
        ('Interest rates and credit standards', 'Not identified', '--', '', 'Common')]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Contributions to the growth of the rent index for all leases, Spain, 2015--2024 (log points)}\label{tab:ranking}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{llcll}\toprule', r'Determinant & Evidence & Contribution & 95\% range & Where it matters\\\midrule',
     f"Total growth of the index & & {f(100 * A['total'], 1)} & & \\\\", r'\addlinespace']
for r_ in rows:
    s.append(' & '.join(r_) + r'\\')
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: contributions to the change in the log of the national IPVA between 2015 and 2024. Inflation: change in the log CPI. Update cap: section~\ref{sec:regulation}. '
      r'Population: within-province long-difference 2SLS elasticity times the population-weighted mean cumulative foreign-born inflow (' + pc(A['population']['M']) + r'\,\% of population), '
      r'range from the Anderson-Rubin set. Income: within-province OLS elasticity times mean real income growth 2015--2023. Tourist dwellings: event-study coefficients times the mean exposure. '
      r'Aggregation of local elasticities assumes no spillovers across municipalities and a national elasticity equal to the local one; the contributions are not additive and do not sum to the total.',
      r'\end{minipage}\end{table}']
W('t5_ranking.tex', '\n'.join(s))
m('cTotal', f(100 * A['total'], 1)); m('cCpi', f(100 * A['cpi'], 1)); m('cReal', f(100 * A['real'], 1)); m('cCap', f(100 * A['update_cap']['contrib'], 1))
m('cPop', f(100 * A['population']['contrib'], 1)); m('cPopLo', f(100 * A['population']['lo'], 1)); m('cPopHi', f(100 * A['population']['hi'], 1)); m('cPopM', pc(A['population']['M']))
m('cPopTot', f(100 * A['population_total']['contrib'], 1)); m('cPopTotM', pc(A['population_total']['M']))
if 'income_ols' in A:
    m('cInc', f(100 * A['income_ols']['contrib'], 1)); m('cIncLo', f(100 * A['income_ols']['lo'], 1)); m('cIncHi', f(100 * A['income_ols']['hi'], 1))
    m('incEl', f(A['income_ols']['elasticity'], 2)); m('incReal', pc(A['income_ols']['mean_real']))
m('cTourA', f(100 * A['tourism']['contrib_2015_2019'], 2)); m('cTourB', f(100 * A['tourism']['contrib_2019_2024'], 2)); m('tourPerPpA', f(100 * A['tourism']['per_pp_2015_2019'], 2))
m('dlnviv', pc(A['supply']['dlnviv_mean']))
B = K['B_within_province_shares']; m('shPop', pc(B['population (2SLS)'], 0))
C = K['C_catalonia_new']; m('catNewTwoFive', pc(C['growth_2019_2025'])); m('capShare', pc(C['cap_share_pop'], 0))
D = K['D_by_size']
for k, nm in [('10-20k', 'A'), ('20-50k', 'B'), ('50-100k', 'C'), ('100-500k', 'D'), ('>500k', 'E')]:
    m(f'sz{nm}Infl', pc(D[k]['inflow'])); m(f'sz{nm}Vut', f(D[k]['vut20'], 1)); m(f'sz{nm}Pop', f(100 * D[k]['pop_contrib'], 1)); m(f'sz{nm}R', pc(D[k]['dlnR']))
    m(f'sz{nm}VutNinety', f(D[k]['vut20_p90'], 1))
# investors and credit
m('fjB', f(100 * I['prov_foreclosure_legal']['fj_s']['b'], 2)); m('fjLo', f(100 * I['prov_foreclosure_legal']['fj_s']['lo'], 1)); m('fjHi', f(100 * I['prov_foreclosure_legal']['fj_s']['hi'], 1))
m('provPopB', f(I['prov_foreclosure_legal']['dlnP']['b'])); m('fjShare', pc(I['nat_foreclosures_legal_share_2014_16'], 0))
m('corpB', f(I['cat_corp_hut']['corp_sh']['b'], 3)); m('corpLo', f(I['cat_corp_hut']['corp_sh']['lo'], 3)); m('corpHi', f(I['cat_corp_hut']['corp_sh']['hi'], 3))
m('corpShare', pc(I['cat_corp_share_mean'], 0)); m('hutTotal', f'{I["cat_hut_total"]:,.0f}'); m('hutPcB', f(100 * I['cat_corp_hut']['hut_pc']['b'], 2))
nr = I['national_rates']
m('eurTwentyOne', f(nr['euribor12m']['2021'], 2)); m('eurTwentyThree', f(nr['euribor12m']['2023'], 2))
m('mrTwentyOne', f(nr['mortgage_rate']['2021'], 2)); m('mrTwentyThree', f(nr['mortgage_rate']['2023'], 2))
W('numbers.tex', '\n'.join(mac) + '\n')
print('tables and', len(mac), 'macros written')

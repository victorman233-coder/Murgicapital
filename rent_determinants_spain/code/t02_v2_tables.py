"""Tables and number macros for 'Insiders and Outsiders in the Rental Market' (paper_v2/tab)."""
import numpy as np, pandas as pd
from rd_common import *

TV = os.path.join(HERE, '..', 'paper_v2', 'tab'); os.makedirs(TV, exist_ok=True)
E1 = load('e01_main.json'); E2 = load('e02_panels_regulation.json'); B1 = load('b01_affordability.json'); B3 = load('b03_aeat_entry_gap.json')
E7 = load('e07_review.json'); E3 = load('e03_inference.json'); E4 = load('e04_panel_entry.json'); E5 = load('e05_extensions.json'); E6 = load('e06_flows.json')
F = load('a01_facts.json'); T3 = load('a03_tourism.json'); R4 = load('a04_regulation.json'); GT = load('b02_gap_by_type.json')
f = lambda x, d=2: '--' if x is None or not np.isfinite(x) else ('$-$' if x < 0 else '') + f'{abs(x):.{d}f}'
pc = lambda x, d=1: f(100 * x, d)
def ar(a):
    v = [('$-\\infty$' if x == -np.inf else '$\\infty$' if x == np.inf else f(x)) for x in a[:2]]
    return '[' + ', '.join(v) + ']' if all(np.isfinite(x) or np.isinf(x) for x in a[:2]) and not any(pd.isna(x) for x in a[:2]) else '--'
star = lambda p: '' if p is None else '***' if p < .01 else '**' if p < .05 else '*' if p < .1 else ''
W = lambda n, s: open(os.path.join(TV, n), 'w').write(s)
DIG = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
mac = []
PCT = '\\,\\%'
m = lambda k, v: mac.append(f'\\newcommand{{\\{"".join(DIG.get(c, c) for c in k)}}}{{{v}}}')

# ------------------------------------------------------------------ Table 1: insiders vs entrants
N1 = B1['T1_national']; C2 = B1['T2_catalonia']
rows = [
    ('All leases (IPVA), Spain', '2015--2023', f"{GT['all']['n']} municipalities", GT['all']['dR'] / 100, GT['all']['inc_uc'] / 100, GT['all']['share_gap_pos'], GT['all']['gap_uc'] / 100),
    ('New leases (deposits), Catalonia', '2015--2023', f"{E2['cat_desc']['n']} municipalities", E2['cat_desc']['d_new'], E2['cat_desc']['d_uc'], E2['cat_desc']['share_AE_pos'], None),
    ('New leases per m$^2$ (deposits), Basque Country', '2016--2023', f"{E2['bas_desc']['n']} municipalities", E2['bas_desc']['d_new_m2'], E2['bas_desc']['d_uc'], E2['bas_desc']['share_AE_pos'], None),
    ('New leases, street-adjusted index (deposits), Aragón', '2015--2023', f"{E2['ara_desc']['n']} municipalities", E2['ara_desc']['d_new'], E2['ara_desc']['d_uc'], E2['ara_desc']['share_AE_pos'], None),
    ('Deposits on new leases, Comunitat Valenciana', '2020--2023', f"{E2['val_desc']['n']} municipalities", E2['val_desc']['d_dep'], E2['val_desc']['d_uc'], None, None),
]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Rents of insiders and entrants against incomes}\label{tab:facts}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lllcccc}\toprule',
     r'Rent measure & Period & Units & Rent growth & Income growth & Difference & Share with rent $>$ income\\', r' & & & \multicolumn{3}{c}{(log points, weighted)} & \\\midrule']
for lab, per, un, dr, dy, sh, df in rows:
    shs = '--' if sh is None else pc(sh, 0) + PCT
    df = dr - dy if df is None else df                        # difference of unrounded growth rates (IPVA: as in the macros)
    assert all(-1 < v < 1 for v in (dr, dy, df)), (lab, dr, dy, df)       # growth rates in log units, not log points
    s.append(f"{lab} & {per} & {un} & {pc(dr)} & {pc(dy)} & {pc(df)} & {shs}\\\\")
s += [r'\addlinespace', r'\multicolumn{7}{l}{\textit{Entry gap: new leases relative to leases in force}}\\',
      r' & & & New leases & Existing or all & Gap & Share with gap $>$ 0\\',
      f"INE index, new vs existing, Spain & 2021--2024 & national & {pc(N1['new_2021_2024'])} & {pc(N1['existing_2021_2024'])} & {pc(N1['new_2021_2024'] - N1['existing_2021_2024'])} & \\\\",
      f"AEAT, new vs all leases, per euro of cadastral value & 2024 & {B3['n_merged']} municipalities & & & {pc(B3['desc']['G_vr']['mean_w'])} & {pc(B3['desc']['G_vr']['share_pos'], 1)}\\,\\%$^a$\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: income is the median net income per consumption unit of the municipality (INE household income atlas). Means weighted by 2015 population. '
      r'IPVA: index of all leases in force (tax returns). Deposit registers record leases at signature: mean rent in Catalonia (contracts of more than one year), '
      r'rent per m$^2$ built in the Basque Country (free-market collective main residences), an index of rents per contract with street fixed effects in Aragón, deposit amount in the Comunitat Valenciana (one month of rent by law; partial coverage). '
      r'AEAT: tax statistics of dwellings declared in 2024, municipalities above 20,000 inhabitants; the entry gap is $\ln(\text{rent}_{new}/\text{value}_{new})-\ln(\text{rent}_{all}/\text{value}_{all})$. '
      r'$^a$ Share of municipalities with a positive gap.', r'\end{minipage}\end{table}']
W('t1_facts.tex', '\n'.join(s))
m('insN', GT['all']['n']); m('insR', pc(GT['all']['dR'] / 100)); m('insY', pc(GT['all']['inc_uc'] / 100)); m('insGap', pc(GT['all']['gap_uc'] / 100))
m('catR', pc(E2['cat_desc']['d_new'])); m('catY', pc(E2['cat_desc']['d_uc'])); m('catGap', pc(E2['cat_desc']['d_new'] - E2['cat_desc']['d_uc'])); m('catShare', pc(E2['cat_desc']['share_AE_pos'], 0))
m('basR', pc(E2['bas_desc']['d_new_m2'])); m('basY', pc(E2['bas_desc']['d_uc'])); m('basGap', pc(E2['bas_desc']['d_new_m2'] - E2['bas_desc']['d_uc'])); m('basShare', pc(E2['bas_desc']['share_AE_pos'], 0))
m('valR', pc(E2['val_desc']['d_dep'])); m('valY', pc(E2['val_desc']['d_uc']))
m('newNat', pc(N1['new_2021_2024'])); m('existNat', pc(N1['existing_2021_2024'])); m('cpiNat', pc(N1['cpi_2021_2024']))
m('gapVr', pc(B3['desc']['G_vr']['mean_w'])); m('gapVrShare', pc(B3['desc']['G_vr']['share_pos'], 1)); m('gapRaw', pc(B3['desc']['G']['mean_w']))
m('gapMtwo', pc(B3['desc']['G_m2']['mean_w'])); m('aeatN', B3['n_merged'])
nn = B3['national']; m('aeatRent', f"{nn['rent']:.0f}"); m('aeatRentNew', f"{nn['rent_new']:.0f}"); m('aeatYld', f(nn['yld'], 1)); m('aeatYldNew', f(nn['yld_new'], 1))
m('aeatVr', f"{nn['vr']:,.0f}"); m('aeatVrNew', f"{nn['vr_new']:,.0f}")
pg = E2['national_gap_path']; m('gapTwoOne', pc(pg['2021'])); m('gapTwoFour', pc(pg['2024']))
for k, nm in [('10-20k', 'A'), ('>500k', 'E')]:
    m(f'insGap{nm}', f(GT[f'size:{k}']['gap_uc'], 1))

# ------------------------------------------------------------------ Table 2: where the demand shock goes
from scipy.stats import t as tdist
XP = pd.read_parquet(f'{CL}/e01_X.parquet'); NG = XP.dropna(subset=['G_vr']).cpro.nunique()
pt = lambda b, se, g=NG: float(2 * tdist.sf(abs(b / se), g - 1))
mm = E1['main']; HH = E7['households']; WC = E7['ar_wcr']
SRC = dict(mm); SRC.update({k: HH[k] for k in ['hh_n', 'size_inc', 'AE23']})
rows = [('A. Rents', None), ('Rent, all leases, 2015--2024', 'dlnR'), ('Entry gap, value-adjusted, 2024 (level)', 'G_vr'), ('Entry gap, per m$^2$, 2024 (level)', 'G_m2'),
        ('Entry gap, raw, 2024 (level)', 'G'), ('Implied entry rent (rent of all leases + value-adjusted gap)$^a$', 'entry'),
        ('B. Incomes and households, 2015--2023', None), ('Income per consumption unit (median)', 'd_uc'), ('Income per person', 'd_pp'), ('Income per household', 'd_hh'),
        ('Household size (income atlas)', 'd_hhsize'), ('Household size implied by income per household and per person', 'size_inc'),
        ('Number of households (population minus household size)', 'hh_n'),
        ('C. Affordability', None), ('Insiders: rent of all leases minus income per consumption unit', 'AI'),
        ('Entrants: implied entry rent minus income per consumption unit', 'AE'), ('Entrants, rents and incomes both over 2015--2023', 'AE23'),
        ('D. Quantities and falsification', None), ('Population', 'dP2024'), ('Dwelling stock (cadastre)', 'dlnviv'), ('Rent of all leases, 2012--2015 (pre-period)', 'dlnR_pre')]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Where a local demand shock goes: rents, entry rents, incomes and households}\label{tab:main}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccccccc}\toprule', r'Outcome & 2SLS & SE & AR 95\,\% set & WCR-AR 95\,\% set & First-stage $F$ & $N$ & Mean\\\midrule']
for lab, k in rows:
    if k is None:
        s.append(f'\\multicolumn{{8}}{{l}}{{\\textit{{{lab}}}}}\\\\'); continue
    q = SRC[k]; wc = ar(WC[k]) if k in WC else '--'
    s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {wc} & {f(q['F'], 1)} & {q['n']} & {f(q.get('ymean'), 3)}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: one observation per municipality; coefficients in log points per percentage point of inflow. Treatment: cumulative net foreign-born inflow from 1 January 2015 to 1 January 2025 '
      r'(to 1 January 2024 for the outcomes measured to 2023: panel B, the insiders row and the last entrants row) relative to 2015 population, instrumented with the corresponding sum of leave-own-province-out shift-share predictions (33 origins, 2003 settlement). '
      r'All regressions include province fixed effects and predetermined controls (2011 census: log population, renting, vacancy, tertiary education, share aged 65+; '
      r'2012: construction, industry and trade-hospitality shares of firms, firms per capita; coastal and FUA-core indicators), 2015 population weights and standard errors clustered by province with the CRV1 small-sample correction. '
      r'Entry-gap outcomes are available for the municipalities above 20,000 inhabitants in the AEAT statistics. AR: Anderson-Rubin set; WCR-AR: wild cluster restricted bootstrap Anderson-Rubin set (Webb weights, 4,999 draws); $F$: cluster-robust first-stage $F$. '
      r'$^a$ The entry gap is observed only in 2024; the implied entry rent measures the growth of entry rents since 2015 only if the 2015 gap is unrelated to the instrument (section~\ref{sec:strategy}).', r'\end{minipage}\end{table}']
W('t2_main.tex', '\n'.join(s))
for k, nm in [('dlnR', 'Stock'), ('G_vr', 'Gap'), ('G_m2', 'GapM'), ('G', 'GapRaw'), ('entry', 'Entry'), ('d_uc', 'Uc'), ('d_pp', 'Pp'), ('d_hh', 'Hh'), ('d_hhsize', 'Hs'),
              ('AI', 'AI'), ('AE', 'AE'), ('dP2024', 'Pop'), ('dlnviv', 'Viv'), ('dlnR_pre', 'Pre'), ('hh_n', 'Hn'), ('size_inc', 'Si'), ('AE23', 'AEtt')]:
    q = SRC[k]; m(f'b{nm}', f(q['b'])); m(f'b{nm}AR', ar(q['ar'])); m(f'b{nm}F', f(q['F'], 1)); m(f'b{nm}Se', f(q['se']))
    if k in WC:
        m(f'b{nm}WCR', ar(WC[k]))
m('nMain', E1['n']); m('nAeat', E1['n_aeat']); m('nProv', NG)

# ------------------------------------------------------------------ Table 3: rigidity and coast
rg = E1['rigidity']; rn = E1['rigidity_net_tourism']; gc = E7['geo_coast']
cell = lambda q: f"{f(q['b'])}{star(pt(q['b'], q['se']))} ({f(q['se'])})"
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Demand shocks, geographic constraints and the coast}\label{tab:rigidity}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{llccccccc}\toprule',
     r'Outcome & Constraint & Inflow & Inflow $\times$ constraint & $F$ (inflow; & \multicolumn{2}{c}{Adding inflow $\times$ tourism} & \multicolumn{2}{c}{Adding inflow $\times$ coast}\\\cmidrule(lr){6-7}\cmidrule(lr){8-9}',
     r' & & (at mean) & & interaction) & $\times$ constraint & $\times$ tourism & $\times$ constraint & $\times$ coast\\\midrule']
for y, yl in [('G_vr', 'Entry gap (value-adjusted)'), ('entry', 'Implied entry rent'), ('AE', 'Entrants\' affordability'), ('dlnR', 'Rent, all leases'), ('dlnviv', 'Dwelling stock')]:
    for r_, rl in [('undev10', 'Undevelopable'), ('sea10', 'Sea'), ('steep10', 'Slope $>$15\\,\\%')]:
        q = rg[f'{y}|{r_}']; nt = rn.get(f'{y}|{r_}'); g_ = gc.get(f'{y}|{r_}')
        e1 = f" & {f(nt['xR']['b'])}{star(nt['xR']['p'])} ({f(nt['xR']['se'])}) & {f(nt['xT']['b'])}{star(nt['xT']['p'])} ({f(nt['xT']['se'])})" if nt else ' & & '
        e2 = f" & {cell(g_['xU'])} & {cell(g_['xC'])}" if g_ else ' & & '
        s.append(f"{yl if r_ == 'undev10' else ''} & {rl} & {f(q['b_x'])} ({f(q['se_x'])}) & {f(q['b_xR'])}{star(q['p_xR'])} ({f(q['se_xR'])}) & "
                 f"{f(q['F_part'][0], 1)}; {f(q['F_part'][1], 1)}{e1}{e2}\\\\")
    if f'{y}|coast_only' in gc:
        q = gc[f'{y}|coast_only']; s.append(f" & Coast (indicator) & {cell(q['x2024'])} & {cell(q['xC'])} & & & & & \\\\")
    s.append(r'\addlinespace')
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: 2SLS with two endogenous regressors, the inflow and its interaction with a constraint standardised with population weights, instrumented with the shift-share prediction and its interaction; '
      r'the inflow coefficient is the effect at the population-weighted mean of the constraint. '
      r'Constraints: share of land within 10 km of the municipality centroid that is sea or has slope above 15\,\% (Copernicus DEM GLO-90), and each component. '
      r'Same fixed effects, controls, weights and clustering as table~\ref{tab:main}. $F$: first-stage partial $F$ statistics. The columns on tourism add the inflow interacted with the share of dwellings in tourist use (2020) and its instrument; '
      r'the columns on the coast add the inflow interacted with the coastal indicator and its instrument (three endogenous regressors). The rows labelled Coast (indicator) interact the inflow with the coastal indicator alone. '
      r'*** $p<0.01$, ** $p<0.05$, * $p<0.1$.', r'\end{minipage}\end{table}']
W('t3_rigidity.tex', '\n'.join(s))
q = rg['G_vr|undev10']; m('rigB', f(q['b_xR'])); m('rigP', f(q['p_xR'], 3)); m('rigSe', f(q['se_xR'])); m('rigFi', f(q['F_part'][1], 1))
m('rigBx', f(q['b_x'])); m('rigBxSe', f(q['se_x']))
q = rn['G_vr|undev10']; m('rigBt', f(q['xR']['b'])); m('rigPt', f(q['xR']['p'], 3)); m('tourInt', f(q['xT']['b'])); m('tourIntP', f(q['xT']['p'], 3))
q = rg['entry|undev10']; m('rigEntry', f(q['b_xR'])); m('rigEntryP', f(q['p_xR'], 3))
q = rg['dlnR|undev10']; m('rigStock', f(q['b_xR'])); q = rg['dlnviv|undev10']; m('rigViv', f(q['b_xR']))
q = rg['G_vr|sea10']; m('rigSea', f(q['b_xR'])); m('rigSeaP', f(q['p_xR'], 3)); q = rg['G_vr|steep10']; m('rigSteep', f(q['b_xR'])); m('rigSteepP', f(q['p_xR'], 3))
q = rg['AE|undev10']; m('rigAE', f(q['b_xR'])); m('rigAEP', f(q['p_xR'], 3))
q = rg['G_vr|undev10']; Ug = np.linspace(-2, 4, 6001)
lb_ = q['b_x'] + q['b_xR'] * Ug - 1.96 * np.sqrt(q['se_x'] ** 2 + Ug ** 2 * q['se_xR'] ** 2 + 2 * Ug * q['cov'])
thr = q['mu'] + Ug[lb_ > 0].min() * q['sd']                    # undevelopable share above which the 95 % band of the effect on the gap excludes 0
dd = XP.dropna(subset=['G_vr', 'undev10'])
m('rigThr', pc(thr, 0)); m('rigThrPop', pc(dd.P15[dd.undev10 > thr].sum() / dd.P15.sum(), 0)); m('rigThrN', int((dd.undev10 > thr).sum()))
q = gc['G_vr|undev10']; m('gcU', f(q['xU']['b'])); m('gcUSe', f(q['xU']['se'])); m('gcUP', f(pt(q['xU']['b'], q['xU']['se']), 2)); m('gcC', f(q['xC']['b'])); m('gcCSe', f(q['xC']['se']))
q = gc['G_vr|coast_only']; m('coastOnly', f(q['xC']['b'])); m('coastOnlySe', f(q['xC']['se'])); m('coastOnlyX', f(q['x2024']['b']))
q = gc['entry|undev10']; m('gcUentry', f(q['xU']['b'])); m('gcUentrySe', f(q['xU']['se']))

# ------------------------------------------------------------------ Table 4: other channels
tb = E2['tour_bins_lnrent']; tn = E2['tour_bins_lnn']; z = E2['zmrt_seasonal']; sp = E1['spillovers_rf']; te = E1['tenure_event_ipva']; ta = E7['tourism_annual']
pp_ = lambda p: '$<$0.001' if p < 0.001 else f(p, 3)
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Tourism, regulation, tenure and spillovers}\label{tab:channels}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccccc}\toprule',
     r'\multicolumn{7}{l}{\textit{A. Tourist dwellings and new leases, Catalonia (\% relative to municipalities with $<$1\,\% of dwellings in tourist use); descriptive}}\\',
     r'Exposure in 2020 & \multicolumn{3}{c}{New-lease rents} & \multicolumn{3}{c}{New leases signed}\\\cmidrule(lr){2-4}\cmidrule(lr){5-7}',
     r' & Collapse & Recovery & 2024--25 & Collapse & Recovery & 2024--25\\']
for b, bl in [('b1', '1--3\\,\\%'), ('b2', '3--8\\,\\%'), ('b3', '$>$8\\,\\%')]:
    cells = [f"{f(100 * t[f'{b}_{p}']['b'], 1)}{star(t[f'{b}_{p}']['p'])}" for t in (tb, tn) for p in ('covid', 'recov', 'late')]
    s.append(f"{bl} & " + ' & '.join(cells) + r'\\')
s.append(r'Pre-trend test, annual register 2014--2018 ($p$) & \multicolumn{3}{c}{' + '; '.join(pp_(ta['lnrent'][b]['pre_p']) for b in ['b1', 'b2', 'b3']) +
         r'} & \multicolumn{3}{c}{' + '; '.join(pp_(ta['lnn'][b]['pre_p']) for b in ['b1', 'b2', 'b3']) + r'}\\')
s += [r'\midrule', r'\multicolumn{7}{l}{\textit{B. Rent cap in stressed (tensioned) market areas and seasonal leases, Catalonia, 2023Q1--2025Q4 (DiD)}}\\',
      r' & \multicolumn{2}{c}{Seasonal share (pp)} & \multicolumn{2}{c}{log seasonal leases} & \multicolumn{2}{c}{log regular leases}\\',
      f"Wave 1 (2024Q2) & \\multicolumn{{2}}{{c}}{{{f(100 * z['sh_seas']['post1']['b'], 2)}{star(z['sh_seas']['post1']['p'])} ({f(100 * z['sh_seas']['post1']['se'], 2)})}} & "
      f"\\multicolumn{{2}}{{c}}{{{f(z['ln_seas']['post1']['b'])}{star(z['ln_seas']['post1']['p'])} ({f(z['ln_seas']['post1']['se'])})}} & \\multicolumn{{2}}{{c}}{{{f(z['ln_n']['post1']['b'])}{star(z['ln_n']['post1']['p'])} ({f(z['ln_n']['post1']['se'])})}}\\\\",
      f"Wave 2 (2024Q4) & \\multicolumn{{2}}{{c}}{{{f(100 * z['sh_seas']['post2']['b'], 2)}{star(z['sh_seas']['post2']['p'])} ({f(100 * z['sh_seas']['post2']['se'], 2)})}} & "
      f"\\multicolumn{{2}}{{c}}{{{f(z['ln_seas']['post2']['b'])}{star(z['ln_seas']['post2']['p'])} ({f(z['ln_seas']['post2']['se'])})}} & \\multicolumn{{2}}{{c}}{{{f(z['ln_n']['post2']['b'])}{star(z['ln_n']['post2']['p'])} ({f(z['ln_n']['post2']['se'])})}}\\\\",
      r'\midrule', r'\multicolumn{7}{l}{\textit{C. Tenure: price-to-income in 2021 (s.d.) $\times$ year, rent of all leases (reference 2021)}}\\',
      ' & '.join(['', '2019', '2020', '2022', '2023', '2024', 'Entry gap 2024']) + r'\\',
      ' & '.join(['Coefficient'] + [f"{f(100 * te[f'pti_{y}']['b'], 2)}{star(te[f'pti_{y}']['p'])}" for y in (2019, 2020, 2022, 2023, 2024)] +
                 [f"{f(100 * E1['tenure_gap_pti']['pti_s']['b'], 2)}"]) + r'\\',
      r'\midrule', r'\multicolumn{7}{l}{\textit{D. Spillovers: shift-share shock of the core city on peripheral municipalities of the same FUA (reduced form)}}\\',
      r' & Rent, all leases & Entry gap & Population & Inflow & Dwellings & \\',
      'Own shock & ' + ' & '.join([f"{f(sp[y]['Z2024']['b'])}{star(sp[y]['Z2024']['p'])}" for y in ['dlnR', 'G_vr', 'dP2024', 'x2024', 'dlnviv']]) + r' & \\',
      'Core shock & ' + ' & '.join([f"{f(sp[y]['Z_core']['b'])}{star(sp[y]['Z_core']['p'])}" for y in ['dlnR', 'G_vr', 'dP2024', 'x2024', 'dlnviv']]) + r' & \\',
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, ' + f"{E2['tour_bin_munis']['b0'] + E2['tour_bin_munis']['b1'] + E2['tour_bin_munis']['b2'] + E2['tour_bin_munis']['b3']}" +
      r' Catalan municipalities with new leases in every quarter of 2019; municipality and quarter fixed effects and exposure-bin $\times$ calendar-quarter terms; '
      r'collapse 2020Q2--2021Q2, recovery 2022--2023; population weights; clusters by municipality. Exposure: dwellings in tourist use in August 2020 (INE experimental statistics, which start that month). '
      r'Pre-trend test: annual register, ' + f"{E7['tourism_annual_n']}" + r' municipalities, municipality and year fixed effects and exposure-bin $\times$ year terms (reference 2019), Wald test that the 2014--2018 terms of each bin are zero, clusters by municipality. '
      r'Panel B: municipality and quarter fixed effects and tourist exposure $\times$ calendar quarter; '
      r'clusters by municipality; the seasonal-lease register starts in 2023. Panel C: IPVA municipalities with an appraised value (MIVAU, municipalities above 25,000 inhabitants); '
      r'municipality and province $\times$ year fixed effects and predetermined characteristics $\times$ year; coefficients $\times$100. '
      r'Panel D: ' + f"{E1['spill_n_periphery']} peripheral municipalities in {E1['spill_n_fua']} functional urban areas; province fixed effects and controls; clusters by FUA. "
      r'*** $p<0.01$, ** $p<0.05$, * $p<0.1$.', r'\end{minipage}\end{table}']
W('t4_channels.tex', '\n'.join(s))
m('seasPostOne', f(100 * z['sh_seas']['post1']['b'], 1)); m('seasLnOne', pc(z['ln_seas']['post1']['b'], 0)); m('seasShareTwoThree', pc(E2['seas_share_2023']))
m('seasShareTwoFive', pc(E2['seas_share_2025'])); m('regLnOne', f(z['ln_n']['post1']['b'])); m('regLnOneSe', f(z['ln_n']['post1']['se']))
for b in ['b1', 'b2', 'b3']:
    for p_ in ['covid', 'recov', 'late']:
        m(f'tR{b}{p_}', f(100 * tb[f'{b}_{p_}']['b'], 1)); m(f'tN{b}{p_}', f(100 * tn[f'{b}_{p_}']['b'], 1))
    m(f'preR{b}', pp_(ta['lnrent'][b]['pre_p'])); m(f'preN{b}', pp_(ta['lnn'][b]['pre_p']))
m('tourAnnN', E7['tourism_annual_n'])
m('spCoreViv', f(sp['dlnviv']['Z_core']['b'])); m('spCoreVivP', f(sp['dlnviv']['Z_core']['p'], 3)); m('spCoreR', f(sp['dlnR']['Z_core']['b'])); m('spCoreG', f(sp['G_vr']['Z_core']['b']))
m('spN', E1['spill_n_periphery']); m('spF', E1['spill_n_fua']); m('ptiN', E1['pti_n'])
for y in (2019, 2020):
    m(f'pti{DIG[str(y)[-1]]}', f(100 * te[f'pti_{y}']['b'], 2)); m(f'pti{DIG[str(y)[-1]]}P', f(te[f'pti_{y}']['p'], 3))
# companion analysis of the Catalan cap on new leases (a04, stacked DiD, first wave)
z1 = R4['zmrt1_vs_notyet']; z1n = R4['zmrt1_vs_never']
m('capRent', pc(z1['lnrent']['pooled']['post']['b'])); m('capRentNever', pc(z1n['lnrent']['pooled']['post']['b']))
m('capN', pc(z1['lnn']['pooled']['post']['b'], 0)); m('capNnever', pc(z1n['lnn']['pooled']['post']['b'], 0)); m('capNdet', pc(z1['lnn']['detrended']['post']['b'], 0))
m('capPreLead', f(z1['lnn']['event']['r_m12']['b'])); m('capPreLeadSe', f(z1['lnn']['event']['r_m12']['se']))

# ------------------------------------------------------------------ Table 5: robustness of the long-difference estimates
ss = E4['ld_sumshares']; lo = E4['leave_one_origin_out']; rb = E7['robust']; ov = E7['overid_origin']
YS = ['G_vr', 'entry', 'dlnR']
TOP5 = ['Colombia', 'Perú', 'Rumanía', 'Ecuador', 'Resto_America']
def two(lab, qs, F=None, sub=None):
    out = [f"{lab} & " + ' & '.join(f"{f(q['b'])} ({f(q['se'])})" if q else '' for q in qs) + f" & {F if F else ''}\\\\"]
    sub = sub if sub is not None else [ar(q['ar']) if q else '' for q in qs]
    out.append(r' & ' + ' & '.join(f'{{\\footnotesize {x}}}' for x in sub) + r' & \\')
    return out
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Robustness of the long-difference estimates: identification, inference, weights and provinces}\label{tab:robust}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccc}\toprule',
     r' & Entry gap & Implied & Rent, & First-stage\\', r' & (value-adjusted) & entry rent & all leases & $F$ (gap)\\\midrule',
     r'\multicolumn{5}{l}{\textit{A. Baseline (table~\ref{tab:main})}}\\']
s += two('2SLS; AR set', [mm[y] for y in YS], f(mm['G_vr']['F'], 1))
s.append(r'{\footnotesize WCR-AR set} & ' + ' & '.join(f'{{\\footnotesize {ar(WC[y])}}}' for y in YS) + r' & \\')
s.append(r'\multicolumn{5}{l}{\textit{B. Identification}}\\')
s += two('Control: 2003 foreign-born share (sum of exposure shares)', [ss[y] for y in YS], f(ss['G_vr']['F'], 1))
s += two('Control: foreign-born inflow 2003--2014', [rb[f'{y}|x0314'] for y in YS], f(rb['G_vr|x0314']['F'], 1))
gm = [dict(b=ov[y]['b_gmm'], se=ov[y]['se_gmm']) for y in YS]
s += two('Four instruments: Colombia, Peru, Romania, rest (two-step GMM)', gm, '', [f"Hansen $J$ $p$ = {f(ov[y]['J_p'], 2)}" for y in YS])
for o_, en in [('Colombia', 'Colombia'), ('Perú', 'Peru'), ('Rumanía', 'Romania')]:
    qs = [ov[y]['single'][f'Z_{o_}'] for y in YS]
    s.append(f"Single instrument: {en} & " + ' & '.join(f"{f(q['b'])} ({f(q['se'])})" for q in qs) + f" & {f(qs[0]['F'], 1)}\\\\")
rng = lambda y: [lo[f'{y}|{o}']['b'] for o in TOP5]
s.append(r'Dropping one of the five origins with largest Rotemberg weights (range) & ' + ' & '.join(f"{f(min(rng(y)))} to {f(max(rng(y)))}" for y in YS) + r' & \\')
s.append(r'\multicolumn{5}{l}{\textit{C. Weights and influential provinces}}\\')
s += two('Square-root population weights', [rb[f'{y}|sqrtP'] for y in YS], f(rb['G_vr|sqrtP']['F'], 1))
s += two('Without the provinces of Madrid and Barcelona', [rb[f'{y}|no28_08'] for y in YS], f(rb['G_vr|no28_08']['F'], 1))
s += two('Without the province of Málaga', [rb[f'{y}|no29'] for y in YS], f(rb['G_vr|no29']['F'], 1))
lp = rb['lopo_G_vr']
s.append(f"Leaving out one province at a time (range) & {f(lp['b_min'])} to {f(lp['b_max'])} & & & \\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: 2SLS coefficients (cluster-robust standard errors) and, below, Anderson-Rubin 95\,\% sets, for the specification of table~\ref{tab:main}; $F$ refers to the entry-gap sample (' + f"{mm['G_vr']['n']}" +
      r' municipalities; the rent of all leases uses ' + f"{mm['dlnR']['n']}" + r'). Panel B: the 2003 foreign-born share scaled as the instrument \citep{borusyak2022}; the 2003--2014 foreign-born inflow relative to 2003 population \citep{jaeger2018}; '
      r'two-step efficient GMM with the components of the instrument for the three origins with the largest Rotemberg weights and the sum of the other 30 as separate instruments, with the Hansen test of over-identifying restrictions; '
      r'the just-identified estimates with each origin component alone (the $F$ column reports the first stage in the gap sample); and the range of estimates when one of the five origins with the largest Rotemberg weights is dropped from the instrument. '
      r'Panel C: the range across the ' + f"{NG}" + r' leave-one-province-out estimates of the entry gap; its Anderson-Rubin set includes zero only when Málaga is excluded.',
      r'\end{minipage}\end{table}']
W('t5_robust.tex', '\n'.join(s))
m('ssGap', f(ss['G_vr']['b'])); m('ssGapAR', ar(ss['G_vr']['ar'])); m('ssGapF', f(ss['G_vr']['F'], 1)); m('ssEntry', f(ss['entry']['b'])); m('ssEntryAR', ar(ss['entry']['ar']))
m('ssHs', f(ss['d_hhsize']['b'])); m('ssStock', f(ss['dlnR']['b'])); m('ssStockAR', ar(ss['dlnR']['ar']))
for y, nm in [('G_vr', 'Gap'), ('entry', 'Entry'), ('dlnR', 'Stock'), ('d_hhsize', 'Hs')]:
    for sp_, sn in [('x0314', 'Jr'), ('sqrtP', 'Sq'), ('no28_08', 'Mb'), ('no29', 'Ma')]:
        q = rb[f'{y}|{sp_}']; m(f'r{sn}{nm}', f(q['b'])); m(f'r{sn}{nm}AR', ar(q['ar']))
    if y in ov:
        m(f'gmm{nm}', f(ov[y]['b_gmm'])); m(f'gmm{nm}Se', f(ov[y]['se_gmm'])); m(f'gmm{nm}J', f(ov[y]['J'], 2)); m(f'gmm{nm}Jp', f(ov[y]['J_p'], 2))
        for o_, on in [('Colombia', 'Col'), ('Perú', 'Per'), ('Rumanía', 'Rom'), ('rest', 'Rest')]:
            q = ov[y]['single'][f'Z_{o_}']; m(f'one{on}{nm}', f(q['b'])); m(f'one{on}{nm}Se', f(q['se']))
            if y == 'G_vr':
                m(f'one{on}F', f(q['F'], 1))
m('lopoMin', f(lp['b_min'])); m('lopoMax', f(lp['b_max']))
lv = rng('G_vr'); m('looMin', f(min(lv))); m('looMax', f(max(lv))); m('looEntryMin', f(min(rng('entry')))); m('looEntryMax', f(max(rng('entry'))))
m('looStockMin', f(min(rng('dlnR')))); m('looStockMax', f(max(rng('dlnR'))))

# ------------------------------------------------------------------ Table 6: timing, annual panel, instrument and registers
pv = E7['provincial_changes']; wn = E7['windows']; pn = E4['panel']
ci = E1['companion_instrument']; uw = E1['main_unw']; bi = E2['bas_iv']; cv = E2['cat_iv']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{The entry gap in changes, timing, annual panel and other registers}\label{tab:timing}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccc}\toprule',
     r'\multicolumn{5}{l}{\textit{A. Provinces: INE indices of new and existing leases (base 2015 = 100), 2SLS on the provincial inflow}}\\',
     r' & Population weights & Adding log population & Unweighted & First-stage $F$\\']
for y, lab in [('G24', r'$\ln(\text{new}/\text{existing})$ in 2024 = change since 2015'), ('dG', r'Change in $\ln(\text{new}/\text{existing})$, 2021--2024')]:
    s.append(f"{lab} & " + ' & '.join(f"{f(pv[f'{y}|{k}']['b'])}{star(pv[f'{y}|{k}']['p'])} ({f(pv[f'{y}|{k}']['se'])})" for k in ['w', 'w_lnP', 'unw']) + f" & {f(pv[f'{y}|w']['F'], 1)}\\\\")
s += [r'\midrule', r'\multicolumn{5}{l}{\textit{B. Earlier and recent inflows (two endogenous regressors)}}\\',
      r' & Inflow 2015--2019 & Inflow 2020--2024 & Correlation of instruments & $N$\\']
for y, lab in [('G_vr', 'Entry gap (value-adjusted), 2024'), ('entry', 'Implied entry rent'), ('dlnR', 'Rent, all leases, 2015--2024')]:
    q = wn[y]; s.append(f"{lab} & {f(q['x_old']['b'])} ({f(q['x_old']['se'])}) & {f(q['x_new']['b'])} ({f(q['x_new']['se'])}) & {f(q['corr_Z'])} & {q['n']}\\\\")
s += [r'\midrule', r'\multicolumn{5}{l}{\textit{C. Annual panel with year-varying shocks: Catalonia, Aragón and Comunitat Valenciana, 2012--2024}}\\',
      r' & 2SLS (SE) & AR 95\,\% set & Randomisation set$^r$ & $F$; $N$\\']
for k, lab in [('dln_new', 'New-lease rent, annual growth'), ('dlnR', 'Rent of all leases, annual growth'), ('dG', 'Change in the entry gap')]:
    q = pn[k]; s.append(f"{lab} & {f(q['b'])} ({f(q['se'])}) & {ar(q['ar'])} & {ar(q['ri']['all']['ci_t'])} & {f(q['F'], 1)}; {q['n']:,}\\\\")
s += [r'\midrule', r'\multicolumn{5}{l}{\textit{D. Instrument, weights and registers}}\\', r' & 2SLS (SE) & AR 95\,\% set & $F$ & $N$\\']
for lab, q in [('Companion-paper instrument (annual, centred timing), rent of all leases', ci['stock']), ('Companion-paper instrument, entry gap (value-adjusted)', ci['G_vr']),
               ('Companion-paper instrument, entry gap (raw)', ci['G']), ('Unweighted, rent of all leases', uw['dlnR']), ('Unweighted, entry gap (value-adjusted)', uw['G_vr']),
               ('Basque Country, new-lease rent per m$^2$, 2016--2023', bi['d_new_m2_23']), ('Basque Country, entrants\' affordability (per m$^2$)', bi['AE']),
               ('Catalonia, mean new-lease rent (not adjusted for size or value), 2015--2023', cv['d_new23']), ('Catalonia, income per consumption unit, 2015--2023', cv['d_uc'])]:
    s.append(f"{lab} & {f(q['b'])} ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {q['n']}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, ' + f"{pv['G24|w']['n']}" + r' provinces (INE table 59005, both indices with base 2015 = 100); treatment and instrument are the population-weighted provincial means of the municipal inflow and instrument of table~\ref{tab:main}; heteroskedasticity-robust standard errors. '
      r'Panel B: inflows and instruments summed over 2015--2019 and 2020--2024, specification of table~\ref{tab:main}. '
      r'Panel C: the panel of IPVA municipalities of the companion paper (annual inflow and instrument with centred timing, province $\times$ year fixed effects, 2003 foreign share and predetermined covariates $\times$ year, population weights) merged with annual new-lease rents '
      r'(Catalonia: mean rent; Aragón: street-adjusted index; Comunitat Valenciana: median deposit; municipalities with at least 30 leases in the year); clusters by municipality; no trimming. '
      r'$^r$ Randomisation-inference set: origin shock paths permuted across origins (2,000 draws), recentred instrument, cluster-robust $t$ statistic. '
      r'Panel D: companion-paper instrument, sum of annual centred shift-share predictions over 2016--2024 for its 699 IPVA municipalities \citep{fernandez2026}. '
      r'Basque Country and Catalonia: long-difference instrument of this paper; controls are the 2011 log population, renting and vacancy shares; province fixed effects '
      r'(Basque Country: three provinces, clusters by municipality). *** $p<0.01$, ** $p<0.05$, * $p<0.1$.',
      r'\end{minipage}\end{table}']
W('t6_timing.tex', '\n'.join(s))
for y, nm in [('G24', 'Lev'), ('dG', 'Chg')]:
    for k, kn in [('w', ''), ('w_lnP', 'L'), ('unw', 'U')]:
        q = pv[f'{y}|{k}']; m(f'pv{nm}{kn}', f(q['b'])); m(f'pv{nm}{kn}Se', f(q['se'])); m(f'pv{nm}{kn}P', f(q['p'], 3))
m('pvF', f(pv['G24|w']['F'], 1)); m('pvN', pv['G24|w']['n'])
for y, nm in [('G_vr', 'Gap'), ('entry', 'Entry'), ('dlnR', 'Stock')]:
    q = wn[y]; m(f'wOld{nm}', f(q['x_old']['b'])); m(f'wOld{nm}Se', f(q['x_old']['se'])); m(f'wNew{nm}', f(q['x_new']['b'])); m(f'wNew{nm}Se', f(q['x_new']['se']))
m('wCorr', f(wn['G_vr']['corr_Z']))
m('ciStock', f(ci['stock']['b'])); m('ciGap', f(ci['G_vr']['b'])); m('ciGapAR', ar(ci['G_vr']['ar'])); m('ciGapRaw', f(ci['G']['b'])); m('ciGapRawAR', ar(ci['G']['ar']))
m('basIv', f(bi['d_new_m2_23']['b'])); m('basIvAR', ar(bi['d_new_m2_23']['ar'])); m('basAE', f(bi['AE']['b'])); m('basAEAR', ar(bi['AE']['ar']))
m('catIv', f(cv['d_new23']['b'])); m('catIvAR', ar(cv['d_new23']['ar']))
m('unwGapF', f(uw['G_vr']['F'], 1))
m('pnNew', f(pn['dln_new']['b'])); m('pnNewSe', f(pn['dln_new']['se'])); m('pnNewAR', ar(pn['dln_new']['ar'])); m('pnStock', f(pn['dlnR']['b'])); m('pnGap', f(pn['dG']['b'])); m('pnGapSe', f(pn['dG']['se']))
m('pnF', f(pn['dln_new']['F'], 1))
m('pnRInew', ar(pn['dln_new']['ri']['all']['ci_t'])); m('pnRIpNew', f(pn['dln_new']['ri']['all']['p0_t'], 2)); m('pnRIpGap', f(pn['dG']['ri']['all']['p0_t'], 2))
m('pnN', f"{E4['sample']['n']:,}"); m('pnMunis', E4['sample']['munis'])
ld_ = E4['lead_rf']['dln_new']; m('pnLead', f(ld_['b'])); m('pnLeadSe', f(ld_['se']))

# ------------------------------------------------------------------ inference, origins, Aragón, turnover, regulation, threshold, flows, EPF: macros
rt = E3['G_vr']['rotemberg']; m('rotTop', pc(sum(r['alpha'] for r in rt['top5'][:3]), 0)); m('rotCol', f(rt['top5'][0]['alpha'])); m('rotNeg', f(rt['sum_neg_alpha']))
m('rotTopContr', f(sum(r['alpha'] * r['beta'] for r in rt['top5'][:3])))
m('riFall', f(E3['G_vr']['ri']['all']['F'], 2)); m('riFcont', f(E3['G_vr']['ri']['continent']['F'], 1))
pl = E3['placebo_rich']['G_vr']; m('plRich', f(pl['joint']['x_rich']['b'])); m('plRichSe', f(pl['joint']['x_rich']['se'])); m('plOth', f(pl['joint']['x_oth']['b']))
m('plOthSe', f(pl['joint']['x_oth']['se'])); m('plDiff', f(pl['diff'])); m('plDiffSe', f(pl['se_diff'])); m('plRichF', f(pl['separate']['rich']['F'], 1))
bal = E4['rotemberg_balance']; m('balRomPre', f(bal['Rumanía|dlnR_pre']['t'], 1)); m('balColPre', f(bal['Colombia|dlnR_pre']['t'], 1)); m('balPerPre', f(bal['Perú|dlnR_pre']['t'], 1))
nbal = sum(abs(v['t']) > 1.96 for v in bal.values()); m('balNsig', nbal); m('balN', len(bal))
ad = E2['ara_desc']; m('araR', pc(ad['d_new'])); m('araY', pc(ad['d_uc'])); m('araS', pc(ad['d_stock'])); m('araShare', pc(ad['share_AE_pos'], 0)); m('araN', ad['n'])
m('araGap', pc(ad['d_new'] - ad['d_uc'])); m('araNs', ad['n_stock']); m('zgzR', pc(ad['zgz']['d_new'])); m('zgzS', pc(ad['zgz']['d_stock'])); m('zgzY', pc(ad['zgz']['d_uc']))
DA = load('d15_aragon.json'); m('araDep', f"{DA['n_deposits']:,}"); m('araMatch', pc(DA['match_rate'], 2))
tv = E5['turnover']; sa = tv['sens_age']
m('lamAll', pc(tv['open_share']['annual_exit'])); m('lamZgz', pc(tv['open_share_zgz']['annual_exit'])); m('medDur', f(tv['open_share']['median_duration'], 1))
m('lamLo', pc(min(sa.values()))); m('lamHi', pc(max(sa.values()))); m('lamPre', pc(tv['cohorts_pre2019']['annual_exit'])); m('lamPost', pc(tv['cohorts_post2019']['annual_exit']))
m('pNever', pc(tv['open_share']['p_never'])); m('snapYear', f"{tv['snapshot']:.2f}")
m('wNewOne', pc(tv['ine_w_new']['2021'])); m('wNewFour', pc(tv['ine_w_new']['2024']))
MC = load('e08_model_checks.json'); lam_ = MC['lambda']
m('lamRangeLo', f(lam_['lo'])); m('lamRangeHi', f(lam_['hi']))
for k, nm in [('ratio_ss', 'Rss'), ('G_ss_2pp', 'Gss'), ('absorb_1', 'Aone'), ('absorb_4', 'Afour'), ('w_G2015', 'Wg'), ('kbar', 'Kbar'), ('ratio_index_entry', 'Rie')]:
    a_, b_ = MC['hi'][k], MC['lo'][k]; lo_, hi_ = min(a_, b_), max(a_, b_)
    if k in ('absorb_1', 'absorb_4', 'w_G2015', 'ratio_index_entry'):
        m(f'mc{nm}Lo', pc(lo_, 0)); m(f'mc{nm}Hi', pc(hi_, 0))
    else:
        m(f'mc{nm}Lo', f(lo_, 1)); m(f'mc{nm}Hi', f(hi_, 1))
m('mcRieObs', pc(MC['observed_ratio_index_entry'], 0)); m('mcRieGmm', pc(ov['dlnR']['b_gmm'] / ov['entry']['b_gmm'], 0))
gve = MC['gap_vs_existing']; m('gapExist', pc(gve['G_exist'])); m('gapScale', f(gve['scale']))
uc = E5['update_cap_national']; m('capWedge', pc(uc['wedge']['2022'])); m('capWedgeB', pc(uc['wedge']['2023'])); m('capGcf', pc(uc['G_2024_no_cap'])); m('capShare', pc(uc['share_widening_cap'], 0))
m('exTwoTwo', pc(uc['existing']['2022'])); m('piTwoTwo', pc(uc['pi']['2022'])); m('piTwoFour', pc(uc['pi']['2024']))
m('newTwoFour', pc(uc['new']['2024'])); m('exTwoFour', pc(uc['existing']['2024']))
up = E5['update_cap_provinces']; m('corrExOne', f(up['2021']['corr'])); m('corrExTwo', f(up['2022']['corr'])); m('sdExOne', f(up['2021']['sd_exist'])); m('sdExTwo', f(up['2022']['sd_exist']))
th = E5['tourism_threshold']; m('tauHat', f(th['lnn']['tau_hat'], 1))
m('tauPn', '$<$0.002' if th['lnn']['p_boot'] == 0 else f(th['lnn']['p_boot'], 3)); m('tauPr', f(th['lnrent']['p_boot'], 3)); m('tauAbove', th['lnn']['munis_above']); m('tauMunis', th['lnn']['munis'])
ht = E5['heterogeneity']; m('hetCoast', f(ht['coast|G_vr']['b_int'])); m('hetCoastSe', f(ht['coast|G_vr']['se_int'])); m('hetBigS', f(ht['big|dlnR']['b_int'])); m('hetCoreS', f(ht['core|dlnR']['b_int']))
m('hetBigSse', f(ht['big|dlnR']['se_int'])); m('hetCoreSse', f(ht['core|dlnR']['se_int']))
cp = E5['aeat_cp']; m('cpN', cp['n_cp']); m('cpCities', cp['n_cities']); m('cpMean', pc(cp['mean'])); m('cpShare', pc(cp['share_pos'], 1)); m('cpWithin', pc(cp['share_within'], 0))
m('cpGrad', f(cp['grad_rent']['lrent']['b'], 3)); m('cpGradSe', f(cp['grad_rent']['lrent']['se'], 3))
dp = E6['displacement']
for k, nm in [('out_sp', 'OutSp'), ('in_sp', 'InSp'), ('net_sp', 'NetSp'), ('out_fx', 'OutFx'), ('in_fx', 'InFx')]:
    m(f'fl{nm}', f(dp[k]['b'])); m(f'fl{nm}AR', ar(dp[k]['ar'])); m(f'fl{nm}M', f(dp[k]['ymean'], 1)); m(f'fl{nm}Se', f(dp[k]['se']))
m('flF', f(dp['in_sp']['F'], 1)); m('flN', E6['n'])
spf = E6['spillovers']; m('spInSpCore', f(spf['in_sp']['Z_corep']['b'])); m('spInSpCoreSe', f(spf['in_sp']['Z_corep']['se'])); m('spInFxCore', f(spf['in_fx']['Z_corep']['b']))
m('spInFxCoreP', f(spf['in_fx']['Z_corep']['p'], 3))
EP = load('d16_epf.json'); et = pd.DataFrame(EP['table']); g_ = lambda yr, gr, v: et[(et.year == yr) & (et.group == gr)][v].iloc[0]
m('epfBurdOne', pc(g_(2016, 'all', 'burden_mid'))); m('epfBurdNine', pc(g_(2024, 'all', 'burden_mid'))); m('epfOverOne', pc(g_(2016, 'all', 'over40_mid'), 0)); m('epfOverNine', pc(g_(2024, 'all', 'over40_mid'), 0))
m('epfBurdExOne', pc(g_(2016, 'all', 'burden'))); m('epfBurdExNine', pc(g_(2024, 'all', 'burden')))
m('epfExactNine', pc(EP['share_exact_income'][str(2024)] if str(2024) in EP['share_exact_income'] else EP['share_exact_income'][2024], 0))
m('epfRentG', pc(np.log(g_(2024, 'all', 'rent') / g_(2016, 'all', 'rent')))); m('epfIncG', pc(np.log(g_(2024, 'all', 'inc_uc') / g_(2016, 'all', 'inc_uc'))))
m('epfN', f"{sum(EP['n_renters'].values()):,}")
pcg = EP['premium_change']; m('epfFprem', pc(pcg['fy']['b'])); m('epfFchg', pc(pcg['fy:late']['b'])); m('epfFchgSe', pc(pcg['fy:late']['se'])); m('epfFchgP', f(pcg['fy:late']['p'], 2))
m('epfYchg', pc(pcg['yy:late']['b'])); m('epfYchgSe', pc(pcg['yy:late']['se']))
bw = E7['basque_within']; m('basW', f(bw['b'])); m('basWSe', f(bw['se'])); m('basWn', bw['n'])
by = E7['base_years']
for reg in ['CAT', 'ARA']:
    for b in [2015, 2016, 2018]:
        m(f'by{reg.title()}{DIG[str(b)[-1]]}', f(by[f'{reg}|{b}']['gap'], 1))
CH = load('b04_cat_history.json'); m('catPreDrop', pc(CH['d_2008_2015'])); m('catPostRise', pc(CH['d_2015_2023'])); m('catLongRise', pc(CH['d_2008_2023']))
va = E7['value_adjustment']; mg = va['mean_G_theta']
m('vaZero', f(va['theta_0']['b'])); m('vaHalf', f(va['theta_5']['b'])); m('vaSeven', f(va['theta_7']['b'])); m('vaCompV', f(va['comp_value']['b'])); m('vaCompVAR', ar(va['comp_value']['ar']))
m('vaCompM', f(va['comp_m2']['b'])); m('vaCompMAR', ar(va['comp_m2']['ar'])); m('vaMeanZero', f(mg['0.0'], 1)); m('vaMeanHalf', f(mg['0.5'], 1))

# ------------------------------------------------------------------ Table 7: margins of adjustment
P = r'\,\%'; EP_N = f"{sum(EP['n_renters'].values()):,}"
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Margins of adjustment: residential flows, heterogeneity, turnover and renters}\label{tab:margins}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccccc}\toprule',
     r'\multicolumn{6}{l}{\textit{A. Moves between municipalities per 100 residents, 2021--2024, per point of foreign-born inflow (2SLS)}}\\',
     r' & 2SLS & SE & AR 95\,\% set & $F$ & Mean\\']
for k, lab in [('out_sp', 'Out-migration of Spanish nationals'), ('in_sp', 'In-migration of Spanish nationals'), ('net_sp', 'Net migration of Spanish nationals'),
               ('out_fx', 'Out-migration of foreign nationals'), ('in_fx', 'In-migration of foreign nationals')]:
    q = dp[k]; s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {f(q['ymean'], 2)}\\\\")
s += [r'\midrule', r'\multicolumn{6}{l}{\textit{B. Heterogeneity: inflow and inflow $\times$ indicator (2SLS)}}\\',
      r' & \multicolumn{2}{c}{Entry gap} & \multicolumn{2}{c}{Rent, all leases} & Share\\\cmidrule(lr){2-3}\cmidrule(lr){4-5}', r' & Inflow & $\times$ indicator & Inflow & $\times$ indicator & \\']
for D, lab in [('coast', 'Coastal municipality'), ('big', 'More than 100,000 inhabitants'), ('core', 'Core city of a FUA'), ('rent_hi', 'Renting share in 2011 above mean')]:
    a, b_ = ht[f'{D}|G_vr'], ht[f'{D}|dlnR']
    s.append(f"{lab} & {f(a['b'])} ({f(a['se'])}) & {f(a['b_int'])} ({f(a['se_int'])}) & {f(b_['b'])} ({f(b_['se'])}) & {f(b_['b_int'])} ({f(b_['se_int'])}) & {pc(a['share'], 0)}{P}\\\\")
s += [r'\midrule', r'\multicolumn{6}{l}{\textit{C. Turnover, updates and renters}}\\',
      f"Annual exit rate of leases, Aragón register: baseline (range); Zaragoza & \\multicolumn{{2}}{{c}}{{{pc(tv['open_share']['annual_exit'])}{P} ({pc(min(sa.values()))}--{pc(max(sa.values()))}); {pc(tv['open_share_zgz']['annual_exit'])}{P}}} & "
      f"\\multicolumn{{3}}{{l}}{{cohorts 2012--18: {pc(tv['cohorts_pre2019']['annual_exit'])}{P}; 2019--25: {pc(tv['cohorts_post2019']['annual_exit'])}{P}}}\\\\",
      f"Weight of new leases in the INE index: 2021; 2024 & \\multicolumn{{2}}{{c}}{{{pc(tv['ine_w_new']['2021'])}{P}; {pc(tv['ine_w_new']['2024'])}{P}}} & \\multicolumn{{3}}{{l}}{{median lease duration, Aragón: {f(tv['open_share']['median_duration'], 1)} years}}\\\\",
      f"Entry gap (INE): 2021; 2024; 2024 without update caps & \\multicolumn{{2}}{{c}}{{{pc(uc['G_2021'])}; {pc(uc['G_2024'])}; {pc(uc['G_2024_no_cap'])}}} & \\multicolumn{{3}}{{l}}{{mechanical share of widening due to caps $\\le$ {pc(uc['share_widening_cap'], 0)}{P}}}\\\\",
      f"Renters' median rent-to-income ratio (EPF): 2016; 2024 & \\multicolumn{{2}}{{c}}{{{pc(g_(2016, 'all', 'burden_mid'))}{P}; {pc(g_(2024, 'all', 'burden_mid'))}{P}}} & \\multicolumn{{3}}{{l}}{{share above 40\\,\\%: {pc(g_(2016, 'all', 'over40_mid'), 0)}{P}; {pc(g_(2024, 'all', 'over40_mid'), 0)}{P}}}\\\\",
      f"Rent per m$^2$ premium of foreign-national renters: 2016--18; change to 2022--24 & \\multicolumn{{2}}{{c}}{{{pc(pcg['fy']['b'])}{P}; {pc(pcg['fy:late']['b'])} ({pc(pcg['fy:late']['se'])})}} & \\multicolumn{{3}}{{l}}{{young natives: change {pc(pcg['yy:late']['b'])} ({pc(pcg['yy:late']['se'])})}}\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, INE Estadística de Migraciones y Cambios de Residencia (tables 69743 and 69745), moves between Spanish municipalities in 2021--2024 per 100 residents in 2021, by nationality (naturalised residents count as Spanish nationals); '
      r'treatment: foreign-born net inflow over the same years relative to 2021 population (points), instrumented with the shift-share prediction for 2021--2024; controls, fixed effects, weights and clusters as table~\ref{tab:main}. '
      r'Panel B: 2SLS with the inflow and its interaction with the indicator, instrumented with the prediction and its interaction; same specification. '
      r'Panel C: exit rate from $S(a)=p+(1-p)e^{-ha}$ fitted to the share of each deposit cohort (2012--2025) not yet returned at the date of download; the age of each cohort is measured from mid-year (range: from the start of the year, or to the start of 2026); cohort rates fix $p$ at its pooled value. '
      r'The update-cap accounting adds back to existing-lease growth the difference between average CPI inflation and the cap for the share of each year in which the cap applied, an upper bound on its mechanical effect because not all leases are indexed to the CPI. '
      r'EPF: INE household budget survey, households renting at market price (' + EP_N + r' household-years, 2016--2024); income is the midpoint of the reported monthly income interval, available in every year; '
      r'premium from a weighted regression of log rent per m$^2$ on nationality and age of the reference person by period, log floor area and year, region and municipality-size fixed effects; robust standard errors in parentheses.',
      r'\end{minipage}\end{table}']
W('t7_margins.tex', '\n'.join(s))

# ------------------------------------------------------------------ Appendix table A1: shift-share diagnostics
TOPN = {'Colombia': 'Colombia', 'Perú': 'Peru', 'Rumanía': 'Romania', 'Ecuador': 'Ecuador', 'Resto_America': 'Rest of America'}
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Shift-share diagnostics: Rotemberg weights, origin-specific estimates and balance}\label{tab:A1}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccccc}\toprule',
     r'\multicolumn{7}{l}{\textit{A. Rotemberg decomposition of the entry-gap estimate and just-identified estimates by origin}}\\',
     r'Origin & Weight $\alpha_o$ & $\hat\beta_o$ (gap) & Entry gap & Implied entry rent & Rent, all leases & First-stage $F$\\\midrule']
for r in rt['top5']:
    o_ = r['origin']; sg = ov['G_vr']['single'].get(f'Z_{o_}')
    cells = ' & '.join(f"{f(ov[y]['single'][f'Z_{o_}']['b'])} ({f(ov[y]['single'][f'Z_{o_}']['se'])})" for y in YS) if sg else ' & & '
    s.append(f"{TOPN[o_]} & {f(r['alpha'], 3)} & {f(r['beta'])} & {cells} & {f(sg['F'], 1) if sg else ''}\\\\")
s.append(f"Other 28 origins (net sum) & {f(1 - sum(r['alpha'] for r in rt['top5']), 3)} & & & & & \\\\")
s.append(f"All origins except Colombia, Peru and Romania (one instrument) & & & " + ' & '.join(f"{f(ov[y]['single']['Z_rest']['b'])} ({f(ov[y]['single']['Z_rest']['se'])})" for y in YS) + f" & {f(ov['G_vr']['single']['Z_rest']['F'], 1)}\\\\")
s.append(f"Sum of negative weights & {f(rt['sum_neg_alpha'], 3)} & & & & & \\\\")
s += [r'\midrule', r'\multicolumn{7}{l}{\textit{B. Balance: standardised coefficient ($t$ statistic) of the 2003 origin share on predetermined characteristics, conditional on controls}}\\',
      r' & Rent growth 2012--15 & Renting 2011 & Vacancy 2011 & Tertiary 2011 & Aged 65+ 2011 & Coastal\\']
for o_ in ['Colombia', 'Perú', 'Rumanía']:
    s.append(f"{TOPN[o_]} & " + ' & '.join(f"{f(bal[f'{o_}|{c}']['b_std'])} ({f(bal[f'{o_}|{c}']['t'], 1)})" for c in ['dlnR_pre', 'rent11', 'vac11', 'tert11', 'sh65_11', 'coastal']) + r'\\')
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, Rotemberg weights $\alpha_o$ and origin-specific estimates $\hat\beta_o$ of the entry-gap coefficient \citep{goldsmith2020}, $\hat\beta=\sum_o\alpha_o\hat\beta_o$; '
      r'just-identified 2SLS with the component of the instrument of each origin (2003 share $\times$ leave-out national growth) as the only instrument, specification of table~\ref{tab:main}; the $F$ column refers to the entry-gap sample. '
      r'Panel B: regression of each characteristic (standardised) on the 2003 share of the origin, with the controls other than the characteristic, province fixed effects and population weights; clusters by province.',
      r'\end{minipage}\end{table}']
W('tA1_shiftshare.tex', '\n'.join(s))

# ------------------------------------------------------------------ Appendix table A2: measurement
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Measurement: value adjustment, composition, base year and the Basque register}\label{tab:A2}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccc}\toprule',
     r'\multicolumn{5}{l}{\textit{A. Entry gap with value elasticity $\theta$: $G^\theta=\ln(\text{rent}_{new}/\text{rent}_{all})-\theta\ln(\text{value}_{new}/\text{value}_{all})$}}\\',
     r' & Mean gap (log points) & 2SLS (SE) & AR 95\,\% set & $N$\\']
for th_, k in [('0 (raw gap)', 'theta_0'), ('0.5', 'theta_5'), ('0.7', 'theta_7'), ('1 (baseline)', 'theta_1')]:
    q = va[k]; key = {'theta_0': '0.0', 'theta_5': '0.5', 'theta_7': '0.7', 'theta_1': '1.0'}[k]
    s.append(f"$\\theta$ = {th_} & {f(mg[key], 1)} & {f(q['b'])} ({f(q['se'])}) & {ar(q['ar'])} & {q['n']}\\\\")
s.append(f"Composition: $\\ln(\\text{{value}}_{{new}}/\\text{{value}}_{{all}})$ & & {f(va['comp_value']['b'])} ({f(va['comp_value']['se'])}) & {ar(va['comp_value']['ar'])} & {va['comp_value']['n']}\\\\")
s.append(f"Composition: $\\ln(\\text{{m}}^2_{{new}}/\\text{{m}}^2_{{all}})$ & & {f(va['comp_m2']['b'])} ({f(va['comp_m2']['se'])}) & {ar(va['comp_m2']['ar'])} & {va['comp_m2']['n']}\\\\")
s += [r'\midrule', r'\multicolumn{5}{l}{\textit{B. Base year of the entry facts: growth to 2023 (log points, population-weighted)}}\\',
      r' & New-lease rents & Income per consumption unit & Difference (share $>$ 0) & $N$\\']
for reg, rl in [('CAT', 'Catalonia'), ('ARA', 'Aragón')]:
    for b in [2015, 2016, 2018]:
        q = by[f'{reg}|{b}']; s.append(f"{rl}, from {b} & {f(q['d_new'], 1)} & {f(q['d_uc'], 1)} & {f(q['gap'], 1)} ({pc(q['share_pos'], 0)}{P}) & {q['n']}\\\\")
s.append(f"Catalonia, mean new-lease rent, 2008--2015; 2015--2023 & \\multicolumn{{2}}{{c}}{{{pc(CH['d_2008_2015'])}; {pc(CH['d_2015_2023'])}}} & & \\\\")
s += [r'\midrule', r'\multicolumn{5}{l}{\textit{C. Basque Country: entry rent per m$^2$ minus income, 2016--2023, on the inflow (OLS, within province)}}\\',
      f"Inflow 2015--2023 & & {f(bw['b'])} ({f(bw['se'])}) & & {bw['n']}\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, AEAT 2024; $\theta=1$ is the value-adjusted gap of the main text; composition rows regress the log ratio of the mean cadastral value (or floor area) of new to all leases on the inflow; specification of table~\ref{tab:main}. '
      r'Panel B: Catalonia, mean rent of new leases in municipalities with at least 30 leases in the base year; Aragón, street-adjusted index; income from the INE household income atlas. '
      r'The last row uses all municipalities in the Catalan register, weighted by leases, and is not adjusted for composition. '
      r'Panel C: municipalities with rents per m$^2$ in the Basque register, province fixed effects, population weights, robust standard errors.',
      r'\end{minipage}\end{table}']
W('tA2_measurement.tex', '\n'.join(s))
W('numbers.tex', '\n'.join(mac) + '\n')
print('v2 tables and', len(mac), 'macros')

# ------------------------------------------------------------------ absolute values for verbal statements ("fell by ...") and other text macros
A_ = lambda k, v: m(k, v.replace('$-$', ''))
A_('insGapAbs', pc(GT['all']['gap_uc'] / 100)); A_('insGapAAbs', f(GT['size:10-20k']['gap_uc'], 1)); A_('insGapEAbs', f(GT['size:>500k']['gap_uc'], 1))
A_('flInSpAbs', f(dp['in_sp']['b'])); A_('flNetSpAbs', f(dp['net_sp']['b']))
A_('capRentAbs', pc(z1['lnrent']['pooled']['post']['b'])); A_('capRentNeverAbs', pc(z1n['lnrent']['pooled']['post']['b']))
A_('capNAbs', pc(z1['lnn']['pooled']['post']['b'], 0)); A_('capNdetAbs', pc(z1['lnn']['detrended']['post']['b'], 0))
A_('regLnOneAbs', f(z['ln_n']['post1']['b'])); A_('catPreDropAbs', pc(CH['d_2008_2015'])); A_('epfFpremAbs', pc(pcg['fy']['b']))
m('vaMeanSeven', f(mg['0.7'], 1)); m('vaMeanOne', f(mg['1.0'], 1))
sz = XP.dropna(subset=['G_vr', 'P15']).copy(); sz['size'] = pd.cut(sz.P15, SIZE_EDGES, labels=SIZE_LABELS)
med = sz.groupby('size', observed=True).G_vr.median() * 100
m('gapMedLo', f(med.min(), 1)); m('gapMedHi', f(med.max(), 1))
W('numbers.tex', '\n'.join(mac) + '\n')
print('text macros', len(mac), med.round(1).to_dict())

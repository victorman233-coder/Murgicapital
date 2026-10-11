"""Tables and number macros for 'Insiders and Outsiders in the Rental Market' (paper_v2/tab)."""
import numpy as np, pandas as pd
from rd_common import *

TV = os.path.join(HERE, '..', 'paper_v2', 'tab'); os.makedirs(TV, exist_ok=True)
E1 = load('e01_main.json'); E2 = load('e02_panels_regulation.json'); B1 = load('b01_affordability.json'); B3 = load('b03_aeat_entry_gap.json')
E3 = load('e03_inference.json'); E4 = load('e04_panel_entry.json'); E5 = load('e05_extensions.json'); E6 = load('e06_flows.json')
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
    ('All leases (IPVA), Spain', '2015--2023', '703 municipalities', 100 * GT['all']['dR'] / 100, GT['all']['inc_uc'] / 100, GT['all']['share_gap_pos']),
    ('New leases (deposits), Catalonia', '2015--2023', f"{E2['cat_desc']['n']} municipalities", E2['cat_desc']['d_new'], E2['cat_desc']['d_uc'], E2['cat_desc']['share_AE_pos']),
    ('New leases per m$^2$ (deposits), Basque Country', '2016--2023', f"{E2['bas_desc']['n']} municipalities", E2['bas_desc']['d_new_m2'], E2['bas_desc']['d_uc'], E2['bas_desc']['share_AE_pos']),
    ('New leases, street-adjusted index (deposits), Aragón', '2015--2023', f"{E2['ara_desc']['n']} municipalities", E2['ara_desc']['d_new'], E2['ara_desc']['d_uc'], E2['ara_desc']['share_AE_pos']),
    ('Deposits on new leases, Comunitat Valenciana', '2020--2023', f"{E2['val_desc']['n']} municipalities", E2['val_desc']['d_dep'], E2['val_desc']['d_uc'], None),
]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Rents of insiders and entrants against incomes}\label{tab:facts}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lllcccc}\toprule',
     r'Rent measure & Period & Units & Rent growth & Income growth & Difference & Share with rent $>$ income\\', r' & & & \multicolumn{3}{c}{(log points, weighted)} & \\\midrule']
for lab, per, un, dr, dy, sh in rows:
    shs = '--' if sh is None else pc(sh, 0) + PCT
    s.append(f"{lab} & {per} & {un} & {pc(dr)} & {pc(dy)} & {pc(dr - dy)} & {shs}\\\\")
s += [r'\addlinespace', r'\multicolumn{7}{l}{\textit{Entry gap: new leases relative to leases in force}}\\',
      f"INE index, new vs existing, Spain & 2021--2024 & national & {pc(N1['new_2021_2024'])} & {pc(N1['existing_2021_2024'])} & {pc(N1['new_2021_2024'] - N1['existing_2021_2024'])} & \\\\",
      f"AEAT, new vs all leases, per euro of cadastral value & 2024 & {B3['n_merged']} municipalities & & & {pc(B3['desc']['G_vr']['mean_w'])} & {pc(B3['desc']['G_vr']['share_pos'], 1)}\\,\\%$^a$\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: income is the median net income per consumption unit of the municipality (INE household income atlas). Means weighted by 2015 population. '
      r'IPVA: index of all leases in force (tax returns). Deposit registers record leases at signature: mean rent in Catalonia (contracts of more than one year), '
      r'rent per m$^2$ built in the Basque Country (free-market collective main residences), an index of rents per contract with street fixed effects in Aragón, deposit amount in the Comunitat Valenciana (one month of rent by law; partial coverage). '
      r'AEAT: tax statistics of dwellings declared in 2024, municipalities above 20,000 inhabitants; the entry gap is $\ln(\text{rent}_{new}/\text{value}_{new})-\ln(\text{rent}_{all}/\text{value}_{all})$. '
      r'$^a$ Share of municipalities with a positive gap.', r'\end{minipage}\end{table}']
W('t1_facts.tex', '\n'.join(s))
m('insR', pc(GT['all']['dR'] / 100)); m('insY', pc(GT['all']['inc_uc'] / 100)); m('insGap', pc(GT['all']['gap_uc'] / 100))
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
mm = E1['main']
rows = [('A. Rents', None), ('Rent, all leases, 2015--2024', 'dlnR'), ('Entry gap, per euro of cadastral value, 2024', 'G_vr'), ('Entry gap, per m$^2$, 2024', 'G_m2'),
        ('Entry gap, raw, 2024', 'G'), ('Implied entry rent (all leases + quality-adjusted gap)', 'entry'),
        ('B. Incomes and households, 2015--2023', None), ('Income per consumption unit (median)', 'd_uc'), ('Income per person', 'd_pp'), ('Income per household', 'd_hh'),
        ('Household size', 'd_hhsize'),
        ('C. Affordability', None), ('Insiders: rent of all leases minus income per consumption unit', 'AI'), ('Entrants: implied entry rent minus income per consumption unit', 'AE'),
        ('D. Quantities and falsification', None), ('Population', 'dP2024'), ('Dwelling stock (cadastre)', 'dlnviv'), ('Rent of all leases, 2012--2015 (pre-period)', 'dlnR_pre')]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Where a local demand shock goes: rents, entry rents, incomes and households}\label{tab:main}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccccc}\toprule', r'Outcome & 2SLS & SE & AR 95\% set & First-stage $F$ & $N$ & Mean\\\midrule']
for lab, k in rows:
    if k is None:
        s.append(f'\\multicolumn{{7}}{{l}}{{\\textit{{{lab}}}}}\\\\'); continue
    q = mm[k]
    s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {q['n']} & {f(q['ymean'], 3)}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: one observation per municipality. Treatment: cumulative net foreign-born inflow between 1 January 2015 and 1 January 2025 (2024 for panels B and C, insiders) '
      r'relative to 2015 population, instrumented with the corresponding sum of leave-own-province-out shift-share predictions (33 origins, 2003 settlement). '
      r'All regressions include province fixed effects and predetermined controls (2011 census: log population, renting, vacancy, tertiary education, share aged 65+; '
      r'2012: construction, industry and trade-hospitality shares of firms, firms per capita; coastal and FUA-core indicators), population weights and standard errors clustered by province. '
      r'Entry-gap outcomes are available for the municipalities above 20,000 inhabitants in the AEAT statistics. AR: Anderson-Rubin set.', r'\end{minipage}\end{table}']
W('t2_main.tex', '\n'.join(s))
for k, nm in [('dlnR', 'Stock'), ('G_vr', 'Gap'), ('G_m2', 'GapM'), ('G', 'GapRaw'), ('entry', 'Entry'), ('d_uc', 'Uc'), ('d_pp', 'Pp'), ('d_hh', 'Hh'), ('d_hhsize', 'Hs'),
              ('AI', 'AI'), ('AE', 'AE'), ('dP2024', 'Pop'), ('dlnviv', 'Viv'), ('dlnR_pre', 'Pre')]:
    q = mm[k]; m(f'b{nm}', f(q['b'])); m(f'b{nm}AR', ar(q['ar'])); m(f'b{nm}F', f(q['F'], 1)); m(f'b{nm}Se', f(q['se']))
m('nMain', E1['n']); m('nAeat', E1['n_aeat'])

# ------------------------------------------------------------------ Table 3: rigidity
rg = E1['rigidity']; rn = E1['rigidity_net_tourism']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Demand shocks and geographic constraints on supply}\label{tab:rigidity}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{llcccccc}\toprule',
     r'Outcome & Constraint & Inflow & Inflow $\times$ constraint & $p$ & $F$ (inflow; interaction) & \multicolumn{2}{c}{Net of inflow $\times$ tourism}\\\cmidrule(lr){7-8}',
     r' & & & & & & Inflow $\times$ constraint & Inflow $\times$ tourism\\\midrule']
for y, yl in [('G_vr', 'Entry gap (quality-adjusted)'), ('entry', 'Implied entry rent'), ('AE', 'Entrants\' affordability'), ('dlnR', 'Rent, all leases'), ('dlnviv', 'Dwelling stock')]:
    for r_, rl in [('undev10', 'Undevelopable'), ('sea10', 'Sea'), ('steep10', 'Slope $>$15\\%')]:
        q = rg[f'{y}|{r_}']; nt = rn.get(f'{y}|{r_}')
        extra = f" & {f(nt['xR']['b'])}{star(nt['xR']['p'])} ({f(nt['xR']['se'])}) & {f(nt['xT']['b'])}{star(nt['xT']['p'])} ({f(nt['xT']['se'])})" if nt else ' & & '
        s.append(f"{yl if r_ == 'undev10' else ''} & {rl} & {f(q['b_x'])} ({f(q['se_x'])}) & {f(q['b_xR'])}{star(q['p_xR'])} ({f(q['se_xR'])}) & {f(q['p_xR'], 3)} & "
                 f"{f(q['F_part'][0], 1)}; {f(q['F_part'][1], 1)}{extra}\\\\")
    s.append(r'\addlinespace')
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: 2SLS with two endogenous regressors, the inflow and its interaction with a standardised constraint, instrumented with the shift-share prediction and its interaction. '
      r'Constraints: share of land within 10 km of the municipality centroid that is sea or has slope above 15\,\% (Copernicus DEM GLO-90), and each component. '
      r'Same fixed effects, controls, weights and clustering as table~\ref{tab:main}. $F$: first-stage partial $F$ statistics. The last two columns add the inflow interacted with the share of dwellings in tourist use (2020) and its instrument. '
      r'*** $p<0.01$, ** $p<0.05$, * $p<0.1$.', r'\end{minipage}\end{table}']
W('t3_rigidity.tex', '\n'.join(s))
q = rg['G_vr|undev10']; m('rigB', f(q['b_xR'])); m('rigP', f(q['p_xR'], 3)); m('rigSe', f(q['se_xR'])); m('rigFi', f(q['F_part'][1], 1))
q = rn['G_vr|undev10']; m('rigBt', f(q['xR']['b'])); m('rigPt', f(q['xR']['p'], 3)); m('tourInt', f(q['xT']['b'])); m('tourIntP', f(q['xT']['p'], 3))
q = rg['entry|undev10']; m('rigEntry', f(q['b_xR'])); m('rigEntryP', f(q['p_xR'], 3))
q = rg['dlnR|undev10']; m('rigStock', f(q['b_xR'])); q = rg['dlnviv|undev10']; m('rigViv', f(q['b_xR']))
q = rg['G_vr|sea10']; m('rigSea', f(q['b_xR'])); m('rigSeaP', f(q['p_xR'], 3)); q = rg['G_vr|steep10']; m('rigSteep', f(q['b_xR'])); m('rigSteepP', f(q['p_xR'], 3))
q = rg['AE|undev10']; m('rigAE', f(q['b_xR'])); m('rigAEP', f(q['p_xR'], 3))

# ------------------------------------------------------------------ Table 4: other channels
tb = E2['tour_bins_lnrent']; tn = E2['tour_bins_lnn']; z = E2['zmrt_seasonal']; sp = E1['spillovers_rf']; te = E1['tenure_event_ipva']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Tourism, regulation, tenure and spillovers}\label{tab:channels}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccccc}\toprule',
     r'\multicolumn{7}{l}{\textit{A. Tourist dwellings and new leases, Catalonia (\% relative to municipalities with $<$1\,\% of dwellings in tourist use)}}\\',
     r'Exposure in 2020 & \multicolumn{3}{c}{New-lease rents} & \multicolumn{3}{c}{New leases signed}\\\cmidrule(lr){2-4}\cmidrule(lr){5-7}',
     r' & Collapse & Recovery & 2024--25 & Collapse & Recovery & 2024--25\\']
for b, bl in [('b1', '1--3\\,\\%'), ('b2', '3--8\\,\\%'), ('b3', '$>$8\\,\\%')]:
    cells = [f"{f(100 * t[f'{b}_{p}']['b'], 1)}{star(t[f'{b}_{p}']['p'])}" for t in (tb, tn) for p in ('covid', 'recov', 'late')]
    s.append(f"{bl} & " + ' & '.join(cells) + r'\\')
s += [r'\midrule', r'\multicolumn{7}{l}{\textit{B. Tensioned-zone cap and seasonal leases, Catalonia, 2023Q1--2025Q4 (DiD)}}\\',
      r' & \multicolumn{2}{c}{Seasonal share (pp)} & \multicolumn{2}{c}{log seasonal leases} & \multicolumn{2}{c}{log regular leases}\\',
      f"Wave 1 (2024Q2) & \\multicolumn{{2}}{{c}}{{{f(100 * z['sh_seas']['post1']['b'], 2)}{star(z['sh_seas']['post1']['p'])} ({f(100 * z['sh_seas']['post1']['se'], 2)})}} & "
      f"\\multicolumn{{2}}{{c}}{{{f(z['ln_seas']['post1']['b'])}{star(z['ln_seas']['post1']['p'])} ({f(z['ln_seas']['post1']['se'])})}} & \\multicolumn{{2}}{{c}}{{{f(z['ln_n']['post1']['b'])}{star(z['ln_n']['post1']['p'])} ({f(z['ln_n']['post1']['se'])})}}\\\\",
      f"Wave 2 (2024Q4) & \\multicolumn{{2}}{{c}}{{{f(100 * z['sh_seas']['post2']['b'], 2)}{star(z['sh_seas']['post2']['p'])} ({f(100 * z['sh_seas']['post2']['se'], 2)})}} & "
      f"\\multicolumn{{2}}{{c}}{{{f(z['ln_seas']['post2']['b'])}{star(z['ln_seas']['post2']['p'])} ({f(z['ln_seas']['post2']['se'])})}} & \\multicolumn{{2}}{{c}}{{{f(z['ln_n']['post2']['b'])}{star(z['ln_n']['post2']['p'])} ({f(z['ln_n']['post2']['se'])})}}\\\\",
      r'\midrule', r'\multicolumn{7}{l}{\textit{C. Tenure: price-to-income in 2021 (s.d.) $\times$ year, rent of all leases (reference 2021)}}\\',
      ' & '.join(['2019', '2020', '2022', '2023', '2024', 'Entry gap 2024', '']) + r'\\',
      ' & '.join([f"{f(100 * te[f'pti_{y}']['b'], 2)}{star(te[f'pti_{y}']['p'])}" for y in (2019, 2020, 2022, 2023, 2024)] +
                 [f"{f(100 * E1['tenure_gap_pti']['pti_s']['b'], 2)}", '']) + r'\\',
      r'\midrule', r'\multicolumn{7}{l}{\textit{D. Spillovers: shift-share shock of the core city on peripheral municipalities of the same FUA (reduced form)}}\\',
      r' & Rent, all leases & Entry gap & Population & Inflow & Dwellings & \\',
      'Own shock & ' + ' & '.join([f"{f(sp[y]['Z2024']['b'])}{star(sp[y]['Z2024']['p'])}" for y in ['dlnR', 'G_vr', 'dP2024', 'x2024', 'dlnviv']]) + r' & \\',
      'Core shock & ' + ' & '.join([f"{f(sp[y]['Z_core']['b'])}{star(sp[y]['Z_core']['p'])}" for y in ['dlnR', 'G_vr', 'dP2024', 'x2024', 'dlnviv']]) + r' & \\',
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, Catalan municipalities with new leases in every quarter of 2019; municipality and quarter fixed effects and exposure-bin $\times$ calendar-quarter terms; '
      r'collapse 2020Q2--2021Q2, recovery 2022--2023; population weights; clusters by municipality. Panel B: municipality and quarter fixed effects and tourist exposure $\times$ calendar quarter; '
      r'clusters by municipality; the seasonal-lease register starts in 2023. Panel C: IPVA municipalities with an appraised value (MIVAU, municipalities above 25,000 inhabitants); '
      r'municipality and province $\times$ year fixed effects and predetermined characteristics $\times$ year; coefficients $\times$100. '
      r'Panel D: ' + f"{E1['spill_n_periphery']} peripheral municipalities in {E1['spill_n_fua']} functional urban areas; province fixed effects and controls; clusters by FUA. "
      r'*** $p<0.01$, ** $p<0.05$, * $p<0.1$.', r'\end{minipage}\end{table}']
W('t4_channels.tex', '\n'.join(s))
m('seasPostOne', f(100 * z['sh_seas']['post1']['b'], 1)); m('seasLnOne', pc(z['ln_seas']['post1']['b'], 0)); m('seasShareTwoThree', pc(E2['seas_share_2023']))
m('seasShareTwoFive', pc(E2['seas_share_2025'])); m('regLnOne', pc(z['ln_n']['post1']['b'], 0))
for b in ['b1', 'b2', 'b3']:
    for p_ in ['covid', 'recov']:
        m(f'tR{b}{p_}', f(100 * tb[f'{b}_{p_}']['b'], 1)); m(f'tN{b}{p_}', f(100 * tn[f'{b}_{p_}']['b'], 1))
m('spCoreViv', f(sp['dlnviv']['Z_core']['b'])); m('spCoreVivP', f(sp['dlnviv']['Z_core']['p'], 3)); m('spCoreR', f(sp['dlnR']['Z_core']['b'])); m('spCoreG', f(sp['G_vr']['Z_core']['b']))
m('spN', E1['spill_n_periphery']); m('spF', E1['spill_n_fua']); m('ptiN', E1['pti_n'])

# ------------------------------------------------------------------ Table 5: robustness
ci = E1['companion_instrument']; uw = E1['main_unw']; bi = E2['bas_iv']; cv = E2['cat_iv']
rows = [('Companion-paper instrument (annual, centred timing), rent of all leases', ci['stock']), ('Companion-paper instrument, entry gap (quality-adjusted)', ci['G_vr']),
        ('Companion-paper instrument, entry gap (raw)', ci['G']), ('Unweighted, rent of all leases', uw['dlnR']), ('Unweighted, entry gap (quality-adjusted)', uw['G_vr']),
        ('Basque Country, new-lease rent per m$^2$, 2016--2023', bi['d_new_m2_23']), ('Basque Country, entrants\' affordability (per m$^2$)', bi['AE']),
        ('Catalonia, mean new-lease rent (not quality-adjusted), 2015--2023', cv['d_new23']), ('Catalonia, income per consumption unit, 2015--2023', cv['d_uc'])]
ss = E4['ld_sumshares']; lo = E4['leave_one_origin_out']; pn = E4['panel']
rowsA = [('Entry gap (quality-adjusted), controlling for the 2003 foreign-born share', ss['G_vr']), ('Implied entry rent, same control', ss['entry']),
         ('Rent of all leases, same control', ss['dlnR']), ('Household size, same control', ss['d_hhsize'])]
rowsA += [(f'Entry gap, instrument without {en}', lo[f'G_vr|{o}']) for o, en in [('Colombia', 'Colombia'), ('Perú', 'Peru'), ('Rumanía', 'Romania')]]
rowsB = [('New-lease rent, annual growth', pn['dln_new']), ('Rent of all leases, annual growth', pn['dlnR']), ('Change in the entry gap', pn['dG'])]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Robustness: identification, instrument, weights, registers and quality adjustment}\label{tab:robust}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccccc}\toprule', r' & 2SLS & SE & AR 95\% set & $F$ & $N$\\\midrule',
     r'\multicolumn{6}{l}{\textit{A. Shift-share identification (long difference)}}\\']
for lab, q in rowsA:
    s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {q.get('n', ss['G_vr']['n'])}\\\\")
s.append(r'\multicolumn{6}{l}{\textit{B. Annual panel with year-varying shocks: Catalonia, Aragón and Comunitat Valenciana, 2012--2024}}\\')
for lab, q in rowsB:
    s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ri']['all']['ci_t'])}$^r$ & {f(q['F'], 1)} & {q['n']}\\\\")
s.append(r'\multicolumn{6}{l}{\textit{C. Instrument, weights and registers}}\\')
for lab, q in rows:
    s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {q['n']}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: companion-paper instrument: sum of annual centred shift-share predictions over 2016--2024 for the 699 IPVA municipalities (Fernández-Aguilera 2026). '
      r'Basque Country and Catalonia: long-difference instrument of this paper; controls are the 2011 log population, renting and vacancy shares; province fixed effects '
      r'(Basque Country: three provinces, clusters by municipality). The Catalan deposit register reports the mean rent per contract, which is not adjusted for the size or quality of the dwelling. '
      r'Panel A adds to the specification of table~\ref{tab:main} the 2003 foreign-born share scaled as the instrument, the sum of exposure shares (Borusyak, Hull and Jaravel 2022), or drops from the instrument one of the three origins with the largest Rotemberg weights. '
      r'Panel B: the panel of IPVA municipalities of the companion paper (annual inflow and instrument with centred timing, province $\times$ year fixed effects, 2003 foreign share and predetermined covariates $\times$ year, population weights) merged with annual new-lease rents '
      r'(Catalonia: mean rent; Aragón: street-adjusted index; Comunitat Valenciana: median deposit; municipalities with at least 30 leases in the year); clusters by municipality. '
      r'$^r$ Randomisation-inference set: origin shock paths permuted across origins (2,000 draws), recentred instrument, cluster-robust $t$ statistic.',
      r'\end{minipage}\end{table}']
W('t5_robust.tex', '\n'.join(s))
m('ciStock', f(ci['stock']['b'])); m('ciGap', f(ci['G_vr']['b'])); m('ciGapAR', ar(ci['G_vr']['ar'])); m('ciGapRaw', f(ci['G']['b'])); m('ciGapRawAR', ar(ci['G']['ar']))
m('basIv', f(bi['d_new_m2_23']['b'])); m('basIvAR', ar(bi['d_new_m2_23']['ar'])); m('basAE', f(bi['AE']['b'])); m('basAEAR', ar(bi['AE']['ar']))
m('catIv', f(cv['d_new23']['b'])); m('catIvAR', ar(cv['d_new23']['ar']))
m('unwGapF', f(uw['G_vr']['F'], 1))
# ------------------------------------------------------------------ identification, Aragón, turnover, regulation, threshold, flows, EPF: macros
m('ssGap', f(ss['G_vr']['b'])); m('ssGapAR', ar(ss['G_vr']['ar'])); m('ssGapF', f(ss['G_vr']['F'], 1)); m('ssEntry', f(ss['entry']['b'])); m('ssEntryAR', ar(ss['entry']['ar']))
m('ssHs', f(ss['d_hhsize']['b'])); m('ssStock', f(ss['dlnR']['b'])); m('ssStockAR', ar(ss['dlnR']['ar']))
lv = [lo[f'G_vr|{o}']['b'] for o in ['Colombia', 'Perú', 'Rumanía', 'Ecuador', 'Resto_America']]
m('looMin', f(min(lv))); m('looMax', f(max(lv)))
rt = E3['G_vr']['rotemberg']; m('rotTop', pc(sum(r['alpha'] for r in rt['top5'][:3]), 0)); m('rotCol', f(rt['top5'][0]['alpha'])); m('rotNeg', f(rt['sum_neg_alpha']))
m('riFall', f(E3['G_vr']['ri']['all']['F'], 2)); m('riFcont', f(E3['G_vr']['ri']['continent']['F'], 1))
m('pnNew', f(pn['dln_new']['b'])); m('pnStock', f(pn['dlnR']['b'])); m('pnGap', f(pn['dG']['b'])); m('pnF', f(pn['dln_new']['F'], 1))
m('pnRInew', ar(pn['dln_new']['ri']['all']['ci_t'])); m('pnRIpNew', f(pn['dln_new']['ri']['all']['p0_t'], 3)); m('pnRIpGap', f(pn['dG']['ri']['all']['p0_t'], 3))
m('pnN', f"{E4['sample']['n']:,}"); m('pnMunis', E4['sample']['munis'])
ld_ = E4['lead_rf']['dln_new']; m('pnLead', f(ld_['b'])); m('pnLeadSe', f(ld_['se']))
pl = E3['placebo_rich']['G_vr']; m('plRich', f(pl['joint']['x_rich']['b'])); m('plRichSe', f(pl['joint']['x_rich']['se'])); m('plOth', f(pl['joint']['x_oth']['b']))
m('plOthSe', f(pl['joint']['x_oth']['se'])); m('plDiff', f(pl['diff'])); m('plDiffSe', f(pl['se_diff'])); m('plRichF', f(pl['separate']['rich']['F'], 1))
bal = E4['rotemberg_balance']; m('balRomPre', f(bal['Rumanía|dlnR_pre']['t'], 1)); m('balColPre', f(bal['Colombia|dlnR_pre']['t'], 1)); m('balPerPre', f(bal['Perú|dlnR_pre']['t'], 1))
ad = E2['ara_desc']; m('araR', pc(ad['d_new'])); m('araY', pc(ad['d_uc'])); m('araS', pc(ad['d_stock'])); m('araShare', pc(ad['share_AE_pos'], 0)); m('araN', ad['n'])
m('araGap', pc(ad['d_new'] - ad['d_uc'])); m('araNs', ad['n_stock']); m('zgzR', pc(ad['zgz']['d_new'])); m('zgzS', pc(ad['zgz']['d_stock'])); m('zgzY', pc(ad['zgz']['d_uc']))
DA = load('d15_aragon.json'); m('araDep', f"{DA['n_deposits']:,}"); m('araMatch', pc(DA['match_rate'], 2))
tv = E5['turnover']; m('lamAll', pc(tv['open_share']['annual_exit'])); m('lamZgz', pc(tv['open_share_zgz']['annual_exit'])); m('medDur', f(tv['open_share']['median_duration'], 1))
m('wNewOne', pc(tv['ine_w_new']['2021'])); m('wNewFour', pc(tv['ine_w_new']['2024']))
uc = E5['update_cap_national']; m('capWedge', pc(uc['wedge']['2022'])); m('capWedgeB', pc(uc['wedge']['2023'])); m('capGcf', pc(uc['G_2024_no_cap'])); m('capShare', pc(uc['share_widening_cap'], 0))
m('exTwoTwo', pc(uc['existing']['2022'])); m('piTwoTwo', pc(uc['pi']['2022']))
up = E5['update_cap_provinces']; m('corrExOne', f(up['2021']['corr'])); m('corrExTwo', f(up['2022']['corr'])); m('sdExOne', f(up['2021']['sd_exist'])); m('sdExTwo', f(up['2022']['sd_exist']))
th = E5['tourism_threshold']; m('tauHat', f(th['lnn']['tau_hat'], 1)); m('tauRentLo', f(th['lnrent']['ci'][0], 1)); m('tauRentHi', f(th['lnrent']['ci'][1], 1))
m('tauPn', '$<$0.002' if th['lnn']['p_boot'] == 0 else f(th['lnn']['p_boot'], 3)); m('tauPr', f(th['lnrent']['p_boot'], 3)); m('tauAbove', th['lnn']['munis_above']); m('tauMunis', th['lnn']['munis'])
ht = E5['heterogeneity']; m('hetCoast', f(ht['coast|G_vr']['b_int'])); m('hetCoastSe', f(ht['coast|G_vr']['se_int'])); m('hetBigS', f(ht['big|dlnR']['b_int'])); m('hetCoreS', f(ht['core|dlnR']['b_int']))
m('hetBigSse', f(ht['big|dlnR']['se_int'])); m('hetCoreSse', f(ht['core|dlnR']['se_int']))
cp = E5['aeat_cp']; m('cpN', cp['n_cp']); m('cpCities', cp['n_cities']); m('cpMean', pc(cp['mean'])); m('cpShare', pc(cp['share_pos'], 1)); m('cpWithin', pc(cp['share_within'], 0))
m('cpGrad', f(cp['grad_rent']['lrent']['b'], 3)); m('cpGradSe', f(cp['grad_rent']['lrent']['se'], 3))
dp = E6['displacement']
for k, nm in [('out_sp', 'OutSp'), ('in_sp', 'InSp'), ('net_sp', 'NetSp'), ('out_fx', 'OutFx'), ('in_fx', 'InFx')]:
    m(f'fl{nm}', f(dp[k]['b'])); m(f'fl{nm}AR', ar(dp[k]['ar'])); m(f'fl{nm}M', f(dp[k]['ymean'], 1))
m('flF', f(dp['in_sp']['F'], 1)); m('flN', E6['n'])
spf = E6['spillovers']; m('spInSpCore', f(spf['in_sp']['Z_corep']['b'])); m('spInSpCoreSe', f(spf['in_sp']['Z_corep']['se'])); m('spInFxCore', f(spf['in_fx']['Z_corep']['b']))
m('spInFxCoreP', f(spf['in_fx']['Z_corep']['p'], 3))
EP = load('d16_epf.json'); et = pd.DataFrame(EP['table']); g_ = lambda yr, gr, v: et[(et.year == yr) & (et.group == gr)][v].iloc[0]
m('epfBurdOne', pc(g_(2016, 'all', 'burden'))); m('epfBurdNine', pc(g_(2024, 'all', 'burden'))); m('epfOverOne', pc(g_(2016, 'all', 'over40'), 0)); m('epfOverNine', pc(g_(2024, 'all', 'over40'), 0))
m('epfRentG', pc(np.log(g_(2024, 'all', 'rent') / g_(2016, 'all', 'rent')))); m('epfIncG', pc(np.log(g_(2024, 'all', 'inc_uc') / g_(2016, 'all', 'inc_uc'))))
m('epfN', f"{sum(EP['n_renters'].values()):,}")
pcg = EP['premium_change']; m('epfFprem', pc(pcg['fy']['b'])); m('epfFchg', pc(pcg['fy:late']['b'])); m('epfFchgSe', pc(pcg['fy:late']['se'])); m('epfFchgP', f(pcg['fy:late']['p'], 2))
m('epfYchg', pc(pcg['yy:late']['b'])); m('epfYchgSe', pc(pcg['yy:late']['se']))

# ------------------------------------------------------------------ Table 6: margins of adjustment
P = r'\,\%'; EP_N = f"{sum(EP['n_renters'].values()):,}"
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Margins of adjustment: residential flows, heterogeneity, turnover and renters}\label{tab:margins}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccccc}\toprule',
     r'\multicolumn{6}{l}{\textit{A. Moves between municipalities per 100 residents, 2021--2024, per point of foreign-born inflow (2SLS)}}\\',
     r' & 2SLS & SE & AR 95\% set & $F$ & Mean\\']
for k, lab in [('out_sp', 'Out-migration of Spanish nationals'), ('in_sp', 'In-migration of Spanish nationals'), ('net_sp', 'Net migration of Spanish nationals'),
               ('out_fx', 'Out-migration of foreign nationals'), ('in_fx', 'In-migration of foreign nationals')]:
    q = dp[k]; s.append(f"{lab} & {f(q['b'])} & ({f(q['se'])}) & {ar(q['ar'])} & {f(q['F'], 1)} & {f(q['ymean'], 2)}\\\\")
s += [r'\midrule', r'\multicolumn{6}{l}{\textit{B. Heterogeneity: inflow and inflow $\times$ indicator (2SLS)}}\\',
      r' & \multicolumn{2}{c}{Entry gap} & \multicolumn{2}{c}{Rent, all leases} & Share\\\cmidrule(lr){2-3}\cmidrule(lr){4-5}', r' & Inflow & $\times$ indicator & Inflow & $\times$ indicator & \\']
for D, lab in [('coast', 'Coastal municipality'), ('big', 'More than 100,000 inhabitants'), ('core', 'Core city of a FUA'), ('rent_hi', 'Renting share in 2011 above mean')]:
    a, b_ = ht[f'{D}|G_vr'], ht[f'{D}|dlnR']
    s.append(f"{lab} & {f(a['b'])} ({f(a['se'])}) & {f(a['b_int'])} ({f(a['se_int'])}) & {f(b_['b'])} ({f(b_['se'])}) & {f(b_['b_int'])} ({f(b_['se_int'])}) & {pc(a['share'], 0)}{P}\\\\")
s += [r'\midrule', r'\multicolumn{6}{l}{\textit{C. Turnover, updates and renters}}\\',
      f"Annual exit rate of leases, Aragón register: all; Zaragoza & \\multicolumn{{2}}{{c}}{{{pc(tv['open_share']['annual_exit'])}{P}; {pc(tv['open_share_zgz']['annual_exit'])}{P}}} & \\multicolumn{{3}}{{l}}{{median duration {f(tv['open_share']['median_duration'], 1)} years}}\\\\",
      f"Weight of new leases in the INE index: 2021; 2024 & \\multicolumn{{2}}{{c}}{{{pc(tv['ine_w_new']['2021'])}{P}; {pc(tv['ine_w_new']['2024'])}{P}}} & & & \\\\",
      f"Entry gap (INE): 2021; 2024; 2024 without update caps & \\multicolumn{{2}}{{c}}{{{pc(uc['G_2021'])}; {pc(uc['G_2024'])}; {pc(uc['G_2024_no_cap'])}}} & \\multicolumn{{3}}{{l}}{{share of widening due to caps $\\le$ {pc(uc['share_widening_cap'], 0)}{P}}}\\\\",
      f"Renters' median rent-to-income ratio (EPF): 2016; 2024 & \\multicolumn{{2}}{{c}}{{{pc(g_(2016, 'all', 'burden'))}{P}; {pc(g_(2024, 'all', 'burden'))}{P}}} & \\multicolumn{{3}}{{l}}{{share above 40\\,\\%: {pc(g_(2016, 'all', 'over40'), 0)}{P}; {pc(g_(2024, 'all', 'over40'), 0)}{P}}}\\\\",
      f"Rent per m$^2$ premium of foreign-national renters: 2016--18; change to 2022--24 & \\multicolumn{{2}}{{c}}{{{pc(pcg['fy']['b'])}{P}; {pc(pcg['fy:late']['b'])} ({pc(pcg['fy:late']['se'])})}} & \\multicolumn{{3}}{{l}}{{young natives: change {pc(pcg['yy:late']['b'])} ({pc(pcg['yy:late']['se'])})}}\\\\",
      r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A, INE Estadística de Migraciones y Cambios de Residencia (tables 69743 and 69745), moves between Spanish municipalities in 2021--2024 per 100 residents in 2021; '
      r'treatment: foreign-born net inflow over the same years relative to 2021 population (points), instrumented with the shift-share prediction for 2021--2024; controls, fixed effects, weights and clusters as table~\ref{tab:main}. '
      r'Panel B: 2SLS with the inflow and its interaction with the indicator, instrumented with the prediction and its interaction; same specification. '
      r'Panel C: exit rate from $S(a)=p+(1-p)e^{-ha}$ fitted to the share of each deposit cohort (2012--2025) not yet returned; the update-cap accounting adds back to existing-lease growth the difference between CPI inflation and the cap for the share of each year in which the cap applied, an upper bound because not all leases are indexed to the CPI. '
      r'EPF: INE household budget survey, households renting at market price (' + EP_N + r' household-years, 2016--2024); premium from a weighted regression of log rent per m$^2$ on nationality and age of the reference person by period, log floor area and year, region and municipality-size fixed effects; robust standard errors in parentheses.',
      r'\end{minipage}\end{table}']
W('t6_margins.tex', '\n'.join(s))
W('numbers.tex', '\n'.join(mac) + '\n')
print('v2 tables and', len(mac), 'macros')

"""Write LaTeX tables and number macros for the revised manuscript from the JSON/CSV results."""
import json, numpy as np, pandas as pd
from rev_common import *

TAB = os.path.join(HERE, '..', 'paper', 'tab'); os.makedirs(TAB, exist_ok=True)
J = lambda f: json.load(open(os.path.join(OUT, f)))
M12 = J('r19_main.json'); M15 = J('r19_main_2015.json'); D10 = J('r10_diagnostics.json'); R11 = J('r11_ri.json')
F12 = J('r12_falsification.json'); S13 = J('r13_specs.json'); E14 = J('r14_events.json'); A15 = J('r15_alt_shocks.json')
G16 = J('r16_margins.json'); H17 = J('r17_het.json'); C18 = J('r18_catalonia.json')
macros = {}

def f(x, d=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return '--'
    if isinstance(x, str):
        return x
    if np.isinf(x):
        return r'$\infty$' if x > 0 else r'$-\infty$'
    s = f'{x:.{d}f}'
    return s.replace('-', '$-$') if s.startswith('-') else s
def ci(c, d=2):
    if not isinstance(c, (list, tuple)) or len(c) < 2 or isinstance(c[0], str):
        return 'unbounded'
    lo, hi = c[0], c[1]
    if np.isinf(lo) and np.isinf(hi):
        return r'$(-\infty,\infty)$'
    return f'[{f(lo, d)}, {f(hi, d)}]'
DIG = dict(zip('0123456789', ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']))
def mac(name, val):
    macros[''.join(DIG.get(ch, ch) for ch in name)] = val
def write(name, s):
    open(os.path.join(TAB, name), 'w').write(s)

# ---------------------------------------------------------------- Table: main results (population weights)
SP = [('minimal', 'Minimal'), ('original (author covariates)', 'Original'), ('central (predetermined + structure)', 'Central'),
      ('central + province x size FE', r'Central + size FE')]
def main_panel(M, w):
    rows = []
    g = lambda k: M['main'][f'{k}|{w}']
    rows.append(('OLS', [f(g(k)['ols']) for k, _ in SP]))
    rows.append(('Reduced form', [f(g(k)['rf']) for k, _ in SP]))
    rows.append(('First-stage $F$', [f(g(k)['F'], 1) for k, _ in SP]))
    rows.append(('2SLS', [f(g(k)['b']) for k, _ in SP]))
    rows.append(('', [f"({f(g(k)['se'])})" for k, _ in SP]))
    rows.append(('AR 95\\% set, province clusters', [ci(g(k)['ar']) for k, _ in SP]))
    rows.append(('AR 95\\% set, wild bootstrap', [ci(g(k)['ar_wcr']) for k, _ in SP]))
    rows.append(('Randomisation, all origins', [ci(g(k)['ri_all']['ci_t']) for k, _ in SP]))
    rows.append(('Randomisation, size terciles', [ci(g(k)['ri_size']['ci_t']) for k, _ in SP]))
    rows.append(('Randomisation, within continents', [ci(g(k)['ri_continent']['ci_t']) for k, _ in SP]))
    rows.append(('2SLS with national shocks', [f(g(k)['national_shock_iv']['b']) for k, _ in SP]))
    rows.append(('AKM0 95\\% set, shocks clustered by origin', [ci(g(k)['national_shock_iv']['akm0']) for k, _ in SP]))
    rows.append(('Observations', [f"{g(k)['n']:,}" for k, _ in SP]))
    return rows
def main_table(w, label, caption, note):
    s = [r'\begin{table}[!htbp]\centering\small', f'\\caption{{{caption}}}\\label{{{label}}}',
         r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccc}\toprule',
         ' & ' + ' & '.join(f'({i+1}) {n}' for i, (_, n) in enumerate(SP)) + r' \\ \midrule']
    for lab, M in [('A. Full period, 2012--2024', M12), ('B. Arrival period, 2015--2024', M15)]:
        s.append(r'\multicolumn{5}{l}{\textit{' + lab + r'}}\\')
        for r_, vals in main_panel(M, w):
            s.append(f'{r_} & ' + ' & '.join(vals) + r' \\')
        s.append(r'\midrule' if lab.startswith('A') else r'\bottomrule')
    s += [r'\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}', note, r'\end{minipage}\end{table}']
    return '\n'.join(s)
NOTE_MAIN = (r'\textit{Notes}: dependent variable $\Delta\ln R_{it}$, annual growth of the municipal IPVA; treatment $m_{it}$, foreign-born inflow over population '
             r'(centred timing); instrument $z_{it}$, 2003 shares of 33 origins times national growth excluding the own province. All columns include province $\times$ year '
             r'fixed effects and the 2003 foreign-born share interacted with every year. Column 2 adds the original covariates (log income per person 2015, '
             r'log population 2011, 2011 shares of renting households and non-primary dwellings) $\times$ year; column 3 replaces them with the central set of '
             r'predetermined covariates (2011 census: log population, renting share, non-primary share, tertiary-education share, share aged 65+; 2012 firm directory: '
             r'shares of construction, industry and trade-transport-hospitality firms and firms per capita; coastal and FUA-core indicators) $\times$ year; column 4 '
             r'adds province $\times$ size class $\times$ year fixed effects. Anderson-Rubin (AR) sets invert the reduced-form test with province-clustered errors '
             r'(analytical) or with 4,999 restricted wild-bootstrap draws with Webb weights. Randomisation sets permute the growth paths of origins 2,000 times within the '
             r'indicated strata, recentre the instrument and invert the studentised reduced-form test. The last two rows use national (not leave-out) shocks; AKM0 is '
             r'the null-imposed exposure-robust test of \citet{adao2019} with origin-year shocks clustered by origin. $\infty$ denotes an unbounded set.')
write('t3_main_w.tex', main_table('w', 'tab:main', 'Effect of immigrant inflows on rent growth: estimates and inference (population weights)',
                                  NOTE_MAIN + ' Weights: 2003 population.'))
write('ta_main_rent.tex', main_table('w_rent', 'tab:main_rent', 'Estimates and inference with renter weights', NOTE_MAIN + ' Weights: rented main dwellings, 2011 census.'))
write('ta_main_unw.tex', main_table('unw', 'tab:main_unw', 'Estimates and inference, unweighted', NOTE_MAIN + ' Unweighted.'))
c12 = M12['main']; c15 = M15['main']
K = 'central (predetermined + structure)'; O = 'original (author covariates)'
for nm, M, tag in [('Full', c12, 'w'), ('Arr', c15, 'w'), ('FullR', c12, 'w_rent'), ('ArrR', c15, 'w_rent'), ('FullU', c12, 'unw'), ('ArrU', c15, 'unw')]:
    q = M[f'{K}|{tag}']
    mac(f'cen{nm}B', f(q['b'])); mac(f'cen{nm}Se', f(q['se'])); mac(f'cen{nm}F', f(q['F'], 1)); mac(f'cen{nm}AR', ci(q['ar']))
    mac(f'cen{nm}WCR', ci(q['ar_wcr'])); mac(f'cen{nm}RI', ci(q['ri_all']['ci_t'])); mac(f'cen{nm}RIcont', ci(q['ri_continent']['ci_t']))
    mac(f'cen{nm}AKM', ci(q['national_shock_iv']['akm0'])); mac(f'cen{nm}RIp', f(q['ri_all']['p0_t'], 3))
    o = M[f'{O}|{tag}']
    mac(f'orig{nm}B', f(o['b'])); mac(f'orig{nm}Se', f(o['se'])); mac(f'orig{nm}AR', ci(o['ar'])); mac(f'orig{nm}AKM', ci(o['national_shock_iv']['akm0']))
    mac(f'orig{nm}F', f(o['F'], 1)); mac(f'orig{nm}RI', ci(o['ri_all']['ci_t'])); mac(f'orig{nm}WCR', ci(o['ar_wcr']))
    sz = M[f'central + province x size FE|{tag}']
    mac(f'size{nm}B', f(sz['b'])); mac(f'size{nm}AR', ci(sz['ar']))
    mn = M[f'minimal|{tag}']
    mac(f'min{nm}B', f(mn['b'])); mac(f'min{nm}AR', ci(mn['ar']))

# ---------------------------------------------------------------- Table: design diagnostics
rot = pd.read_csv(os.path.join(OUT, 'r10_rotemberg.csv'))
EN = {'Rumanía': 'Romania', 'Reino Unido': 'United Kingdom', 'Perú': 'Peru', 'Alemania': 'Germany', 'Ucrania': 'Ukraine', 'Rusia': 'Russia',
      'Resto_America': 'Rest of Americas', 'República Dominicana': 'Dominican Republic', 'Marruecos': 'Morocco', 'Resto_Europa': 'Rest of Europe',
      'Francia': 'France', 'Italia': 'Italy', 'Pakistán': 'Pakistan', 'Resto_Asia': 'Rest of Asia', 'Resto_Africa': 'Rest of Africa',
      'Argelia': 'Algeria', 'Brasil': 'Brazil', 'Polonia': 'Poland', 'Oceania_otros': 'Oceania and other', 'Bélgica': 'Belgium'}
sh = D10['shocks']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Design diagnostics: shocks, Rotemberg weights and shock-level balance}\label{tab:design}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lrrrrrr}\toprule',
     r'\multicolumn{7}{l}{\textit{A. Origin shocks, 2012--2024 (national growth over the 2003 stock)}}\\',
     f"Effective number of origins (inverse HHI of exposure) & {f(sh['eff_n_origins'],1)} & \\multicolumn{{5}}{{l}}{{Largest exposure weight: {f(sh['largest_weight'])} ({EN.get(sh['largest_origin'], sh['largest_origin'])})}}\\\\",
     f"Mean first-order autocorrelation of shocks & {f(sh['mean_autocorr'])} & \\multicolumn{{5}}{{l}}{{Mean pairwise correlation, all origins: {f(sh['mean_corr_all'])}}}\\\\",
     "Mean correlation within continent & \\multicolumn{6}{l}{Europe " + f(sh['mean_corr_within_continent']['Europa']) + ", Africa " + f(sh['mean_corr_within_continent']['Africa']) +
     ", Americas " + f(sh['mean_corr_within_continent']['America']) + ", Asia " + f(sh['mean_corr_within_continent']['Asia']) + r"}\\",
     f"Overidentification with 33 instruments: Hansen $J$ (df) & {f(D10['overid']['J'],1)} ({D10['overid']['J_df']}) & \\multicolumn{{5}}{{l}}{{$p$-value {f(D10['overid']['J_p'],3)}; LIML {f(D10['overid']['liml_b'])} ({f(D10['overid']['liml_se'])})}}\\\\",
     r'\midrule\multicolumn{7}{l}{\textit{B. Largest Rotemberg weights (original specification, population weights)}}\\',
     r'Origin & $\hat\alpha_o$ & $\hat\beta_o$ & $F_o$ & Share 2003 & $g_{2012-14}$ & $g_{2015-24}$\\']
for _, q in rot.head(8).iterrows():
    s.append(f"{EN.get(q.origin, q.origin)} & {f(q.alpha,3)} & {f(q.beta)} & {f(q.F,1)} & {f(q.share2003,3)} & {f(q.g_2012_2014)} & {f(q.g_2015_2024)}\\\\")
s.append(f"Sum of negative weights & {f(D10['rotemberg']['sum_neg_alpha'],3)} & \\multicolumn{{5}}{{l}}{{Contribution of the eight largest weights: {f(rot.head(8).contrib.sum(),3)} of {f(D10['rotemberg']['beta_total'],3)}}}\\\\")
s += [r'\midrule\multicolumn{7}{l}{\textit{C. Shock-level balance: 2015--2024 origin growth on exposure-weighted characteristics (standardised)}}\\',
      r'Characteristic & \multicolumn{2}{c}{Coefficient (s.e.)} & $p$ & \multicolumn{2}{c}{Within continent (s.e.)} & $p$\\']
NAMES = {'lnpop11': 'Log population, 2011', 'rent11': 'Renting share, 2011', 'vac11': 'Non-primary share, 2011', 'tert11': 'Tertiary education, 2011',
         'sh65_11': 'Share aged 65+, 2011', 'coastal': 'Coastal', 'sh_constr12': 'Construction firms share, 2012', 'sh_trade_hosp12': 'Trade-transport-hospitality share, 2012',
         'rent_growth_12_14': 'Rent growth 2012--2014'}
for b in D10['shock_balance']:
    s.append(f"{NAMES[b['var']]} & \\multicolumn{{2}}{{c}}{{{f(b['coef']['b'])} ({f(b['coef']['se'])})}} & {f(b['coef']['p'],3)} & \\multicolumn{{2}}{{c}}{{{f(b['coef_within_continent']['b'])} ({f(b['coef_within_continent']['se'])})}} & {f(b['coef_within_continent']['p'],3)}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A uses calendar-year national growth rates $g_{ot}=\Delta F_{ot}/F_{o,2003}$ for 2012--2024 and exposure weights $\sum_i\omega_i s_{io}$; '
      r'the overidentification test uses the 33 origin components of the instrument as separate instruments (two-step GMM, province clusters). Panel B: '
      r'decomposition $\hat\beta=\sum_o\hat\alpha_o\hat\beta_o$ of \citet{goldsmith2020} for the leave-out instrument with the original covariates; $F_o$ is the first-stage '
      r'$F$ of each origin component; $g$ are cumulative growth rates over the 2003 stock. Panel C: 33 origins, weights equal to exposure; heteroskedasticity-robust '
      r'standard errors; ``within continent'' adds continent fixed effects.', r'\end{minipage}\end{table}']
write('t2_design.tex', '\n'.join(s))
mac('effN', f(sh['eff_n_origins'], 1)); mac('corrAll', f(sh['mean_corr_all'])); mac('autoc', f(sh['mean_autocorr']))
mac('corrAme', f(sh['mean_corr_within_continent']['America'])); mac('corrEur', f(sh['mean_corr_within_continent']['Europa']))
mac('Jstat', f(D10['overid']['J'], 1)); mac('limlB', f(D10['overid']['liml_b'])); mac('limlSe', f(D10['overid']['liml_se']))
mac('rotRom', f(rot.set_index('origin').loc['Rumanía', 'alpha'])); mac('rotCol', f(rot.set_index('origin').loc['Colombia', 'alpha']))
mac('gRom', f(rot.set_index('origin').loc['Rumanía', 'g_2012_2024'])); mac('rotNeg', f(D10['rotemberg']['sum_neg_alpha']))
cb = {b['var']: b for b in D10['shock_balance']}
mac('balConstr', f(cb['sh_constr12']['coef']['b'])); mac('balConstrP', f(cb['sh_constr12']['coef']['p'], 3))
mac('balConstrW', f(cb['sh_constr12']['coef_within_continent']['b'])); mac('balConstrWP', f(cb['sh_constr12']['coef_within_continent']['p'], 3))
mac('balRent', f(cb['rent11']['coef']['b'])); mac('balRentP', f(cb['rent11']['coef']['p'], 3)); mac('balTert', f(cb['tert11']['coef']['b'])); mac('balTertP', f(cb['tert11']['coef']['p'], 3))
ns = D10['national_shocks']
mac('natIV', f(ns['iv']['b'])); mac('bhjEq', f(ns['shock_level_equivalent'], 3)); mac('bhjYfe', f(ns['shock_level_year_fe']['b'], 3))
mac('akmOrig', ci(ns['akm0_ci'])); mac('akmOY', ci(ns['akm0_ci_cluster_origin_year']))

# ---------------------------------------------------------------- Table: falsification and dynamics
W = F12['F1_F2_longdiff']
lp = F12['lp_tests']
rows = [
 (r'\textit{A. Pre-period and placebo outcomes (cross-section of municipalities)}', None),
 ('Rent growth 2011--2014 on predicted 2015--2024 inflow (original controls)', (W['w']['placebo_11_14']['Zpost'], W['u']['placebo_11_14']['Zpost'])),
 ('Rent growth 2011--2014 on predicted 2015--2024 inflow (central controls)', (W['w_central']['placebo_11_14']['Zpost'], W['u_central']['placebo_11_14']['Zpost'])),
 (r'\quad Reference: rent growth 2015--2024 on the same instrument (central controls)', (W['w_central']['rf_15_24']['Zpost'], W['u_central']['rf_15_24']['Zpost'])),
 ('Spain-born growth 2003--2008 (original controls)', (W['w']['placebo_demog']['dNAT_03_08']['Zpost'], W['u']['placebo_demog']['dNAT_03_08']['Zpost'])),
 ('Spain-born growth 2003--2008 (central controls)', (W['w_central']['placebo_demog']['dNAT_03_08']['Zpost'], W['u_central']['placebo_demog']['dNAT_03_08']['Zpost'])),
 ('Spain-born growth 2008--2011 (central controls)', (W['w_central']['placebo_demog']['dNAT_08_11']['Zpost'], W['u_central']['placebo_demog']['dNAT_08_11']['Zpost'])),
]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Falsification, dynamics and stability}\label{tab:falsification}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcc}\toprule', r' & Population weights & Unweighted \\ \midrule']
for lab, v in rows:
    if v is None:
        s.append(r'\multicolumn{3}{l}{' + lab + r'}\\'); continue
    a, b = v
    s.append(f"{lab} & {f(a['b'],3)} ({f(a['se'],3)}) & {f(b['b'],3)} ({f(b['se'],3)})\\\\")
pp = S13['placebo_permuted_shares']; ps = S13['placebo_pseudo_shares']
s.append(f"Reduced form with permuted share vectors (province $\\times$ size cells): $p$-value of observed & {f(pp['p'],2)} & --\\\\")
s.append(f"Reduced form with pseudo-shares predicted from observables vs observed & {f(ps['rf'],3)} vs {f(ps['rf_obs'],3)} & --\\\\")
s.append(r'\midrule\multicolumn{3}{l}{\textit{B. Dynamics and persistence of the instrument (original covariates, population weights)}}\\')
cw = F12['F1_F2_longdiff']['corr']['w']
s.append(f"Correlation of predicted inflows: 2003--2008 with 2015--2024 & {f(cw['Zboom']['Zpost'])} & {f(F12['F1_F2_longdiff']['corr']['u']['Zboom']['Zpost'])}\\\\")
jb = F12['JRS_boom_control']
s.append(f"2SLS adding predicted 2003--08 and 2008--12 inflows $\\times$ year & {f(jb['b'])} ({f(jb['se'])}), $F$ {f(jb['F'],1)} & --\\\\")
lt = lp['cov_w_L3']; lm = lp['min_w_L3']
s.append(f"Local projections, balanced 2015--2020, first-stage $F$ (original / minimal) & {f(lp['cov_w_L3'].get('F', np.nan) if 'F' in lt else np.nan,1)} & --\\\\" if False else
         f"Local projections, balanced 2015--2020: joint test of leads, $p$ (original / minimal) & {f(lt['p'],2)} / {f(lm['p'],2)} & {f(lp['cov_u_L3']['p'],2)} / {f(lp['min_u_L3']['p'],2)}\\\\")
lpdf = pd.read_csv(os.path.join(OUT, 'r12_lp.csv'))
Fo_ = lpdf[lpdf.spec == 'cov_w_L3'].F.dropna().iloc[0]; Fm_ = lpdf[lpdf.spec == 'min_w_L3'].F.dropna().iloc[0]
Fou = lpdf[lpdf.spec == 'cov_u_L3'].F.dropna().iloc[0]; Fmu = lpdf[lpdf.spec == 'min_u_L3'].F.dropna().iloc[0]
s.append(f"\\quad First-stage $F$ of the instrument innovation (original / minimal) & {f(Fo_,1)} / {f(Fm_,1)} & {f(Fou,1)} / {f(Fmu,1)}\\\\")
j2 = F12['JRS_two_instruments']
s.append(f"Two-instrument model: current / previous calendar-year inflow & {f(j2['est']['x1']['b'])} / {f(j2['est']['x1_l1']['b'])} & --\\\\")
s.append(f"\\quad Sanderson-Windmeijer $F$ & {f(j2['SW_F']['x1'],1)} / {f(j2['SW_F']['x1_l1'],1)} & --\\\\")
rc = F12['reconciliation_same_sample']
s.append(f"Same sample 2013--2024: centred / calendar-year / calendar with lagged instrument & {f(rc['a_centred_level']['b'])} / {f(rc['c_calendar_level']['b'])} / {f(rc['d_calendar_control_lag']['b'])} & --\\\\")
s.append(f"\\quad with municipality fixed effects (centred) & {f(rc['b_centred_municipal_FE']['b'])} ($F$ {f(rc['b_centred_municipal_FE']['F'],1)}) & --\\\\")
s.append(r'\midrule\multicolumn{3}{l}{\textit{C. Stability and symmetry (original covariates, all year interactions, population weights)}}\\')
for a_, b_, lab in [(2012, 2014, '2012--2014 (net outflows)'), (2015, 2024, '2015--2024 (arrivals)'), (2012, 2019, '2012--2019'), (2020, 2024, '2020--2024')]:
    q = F12[f'window_{a_}_{b_}']
    s.append(f"Window {lab} & {f(q['b'])} ({f(q['se'])}), AR {ci(q['ar'])} & --\\\\")
q = F12['window_2020_2024_policy_controls']
s.append(f"2020--2024 omitting the first-year interaction (as in the original manuscript) & {f(q['b'])} ({f(q['se'])}) & --\\\\")
sy = F12['symmetry_sign']
s.append(f"Observations with positive / non-positive predicted inflow & {f(sy['xc_pos']['b'])} ({f(sy['xc_pos']['se'])}) / {f(sy['xc_neg']['b'])} ({f(sy['xc_neg']['se'])}) & --\\\\")
s.append(f"Controlling for Catalan rent-control and tensioned-zone municipalities $\\times$ year & {f(F12['policy_controls']['b'])} ({f(F12['policy_controls']['se'])}) & --\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A regresses the indicated outcome on the predicted 2015--2024 inflow (2003 shares, leave-province-out national growth), with '
      r'province fixed effects, the 2003 foreign-born share and the indicated controls; the 2011--2014 regressions also control for the predicted 2011--2014 inflow. '
      r'Permuted shares: 300 reassignments of the 2003 share vectors across municipalities within province $\times$ size cells (central specification). Pseudo-shares: '
      r'origin shares predicted from the central covariates with province fixed effects. Panel B: local projections of $\ln R_{t+h}-\ln R_{t-1}$ on the calendar-year '
      r'inflow instrumented with its prediction, controlling for three lags of the prediction, balanced sample $t\in[2015,2020]$, $h\in\{-4,\dots,4\}$; the joint test '
      r'covers $h\in\{-4,-3,-2\}$. Panel C: subsample estimates with every year interaction of the controls. Standard errors clustered by province.',
      r'\end{minipage}\end{table}']
write('t4_falsification.tex', '\n'.join(s))
mac('preW', f(W['w_central']['placebo_11_14']['Zpost']['b'], 3)); mac('preWse', f(W['w_central']['placebo_11_14']['Zpost']['se'], 3)); mac('preWp', f(W['w_central']['placebo_11_14']['Zpost']['p'], 3))
mac('rfLDW', f(W['w_central']['rf_15_24']['Zpost']['b'], 3)); mac('rfLDWse', f(W['w_central']['rf_15_24']['Zpost']['se'], 3))
mac('natPreOrig', f(W['w']['placebo_demog']['dNAT_03_08']['Zpost']['b'])); mac('natPreOrigP', f(W['w']['placebo_demog']['dNAT_03_08']['Zpost']['p'], 3))
mac('natPreCen', f(W['w_central']['placebo_demog']['dNAT_03_08']['Zpost']['b'], 3)); mac('natPreCenP', f(W['w_central']['placebo_demog']['dNAT_03_08']['Zpost']['p'], 2))
mac('permP', f(pp['p'])); mac('boomCorr', f(cw['Zboom']['Zpost'])); mac('lpFcov', f(Fo_, 1)); mac('lpFmin', f(Fm_, 1))
mac('wOut', f(F12['window_2012_2014']['b'])); mac('wOutSe', f(F12['window_2012_2014']['se'])); mac('wIn', f(F12['window_2015_2024']['b'])); mac('wInAR', ci(F12['window_2015_2024']['ar']))
mac('w2024', f(F12['window_2020_2024']['b'])); mac('w2024AR', ci(F12['window_2020_2024']['ar'])); mac('w2024old', f(F12['window_2020_2024_policy_controls']['b']))
mac('calB', f(rc['c_calendar_level']['b'])); mac('cenB', f(rc['a_centred_level']['b'])); mac('swF1', f(j2['SW_F']['x1'], 1))

# ---------------------------------------------------------------- Table: Colombia-Peru episode
dv = E14['did_iv_colper']; sm = E14['summary']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{A sharper episode: the 2016 Schengen visa waivers for Colombia and Peru}\label{tab:episode}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccc}\toprule', r' & Population weights & Renter weights & Unweighted\\\midrule',
     r'\multicolumn{4}{l}{\textit{A. Difference-in-differences IV, 2011--2024 (exposure: 2003 Colombian and Peruvian share, pp)}}\\']
for k, lab in [('pi', 'First stage: foreign-born stock (pp) on exposure $\\times$ post'), ('F', 'First-stage $F$'), ('b', 'Rent (\\%) per pp of inflow')]:
    s.append(f'{lab} & ' + ' & '.join(f(dv[w][k], 2 if k != 'F' else 1) + (f" ({f(dv[w]['se'])})" if k == 'b' else (f" ({f(dv[w]['se_pi'])})" if k == 'pi' else '')) for w in ['w', 'w_rent', 'unw']) + r'\\')
s.append('AR 95\\% set, province clusters & ' + ' & '.join(ci(dv[w]['ar']) for w in ['w', 'w_rent', 'unw']) + r'\\')
s.append('AR 95\\% set, wild bootstrap & ' + ' & '.join(ci(dv[w]['ar_wcr']) for w in ['w', 'w_rent', 'unw']) + r'\\')
s.append(r'\midrule\multicolumn{4}{l}{\textit{B. Event-study averages (coefficients per pp of exposure; pre: $k\le-2$, post: $k\ge0$)}}\\')
for ep, lab in [('ColPer_2016', 'Colombia and Peru, 2016'), ('Venezuela_2017', 'Venezuela, 2017'), ('Ucrania_2022', 'Ukraine, 2022')]:
    q = sm[ep]
    s.append(f"{lab}: inflow pre / post & {f(q['yF_w']['pre_avg'][0])} / {f(q['yF_w']['post_avg'][0])} & -- & {f(q['yF_unw']['pre_avg'][0])} / {f(q['yF_unw']['post_avg'][0])}\\\\")
    s.append(f"\\quad rent (log points) pre / post & {f(q['yR_w']['pre_avg'][0],4)} / {f(q['yR_w']['post_avg'][0],4)} & -- & {f(q['yR_unw']['pre_avg'][0],4)} / {f(q['yR_unw']['post_avg'][0],4)}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: the exposure is the 2003 share of the population born in the episode countries (pp); all regressions control for the 2003 share born in '
      r'other countries of the same continent interacted with every event year, so that identification compares municipalities with similar continental '
      r'exposure. All include province $\times$ year fixed effects and the central covariates $\times$ year. Panel A: outcome $100(\ln R_{it}-\ln R_{i,2015})$, '
      r'endogenous variable the change in the foreign-born stock since 2015 in pp of 2003 population, instrument exposure $\times$ 1[$t\ge2016$]; exposure is '
      r'interacted with pre-2016 years so that pre-trends are absorbed. Panel B: averages of event-time coefficients (base year $t_X-1$). Standard errors clustered by province.',
      r'\end{minipage}\end{table}']
write('t5_episode.tex', '\n'.join(s))
for w, t in [('w', 'W'), ('w_rent', 'R'), ('unw', 'U')]:
    mac(f'epB{t}', f(dv[w]['b'])); mac(f'epSe{t}', f(dv[w]['se'])); mac(f'epF{t}', f(dv[w]['F'], 1)); mac(f'epAR{t}', ci(dv[w]['ar'])); mac(f'epWCR{t}', ci(dv[w]['ar_wcr']))

# ---------------------------------------------------------------- Table: margins of adjustment
G = G16
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Where newcomers are housed: margins of adjustment}\label{tab:margins}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lcccc}\toprule',
     r' & \multicolumn{2}{c}{Original covariates} & \multicolumn{2}{c}{Central covariates}\\\cmidrule(lr){2-3}\cmidrule(lr){4-5}',
     r' & Weighted & Unweighted & Weighted & Unweighted\\\midrule',
     r'\multicolumn{5}{l}{\textit{A. Census long differences 2011--2021 (municipalities above 5,000 inhabitants; persons per immigrant)}}\\']
lab = [('y_pop', 'Net residents'), ('y_nat', 'Born in Spain'), ('y_new', 'New dwellings'), ('y_vac', 'Non-primary dwellings brought into use'),
       ('y_crowd', 'Higher persons per primary dwelling'), ('y_rent', 'Persons in dwellings switched to renting'), ('dln_s', r'$\Delta\ln$ persons per primary dwelling')]
keys = ['census_author_w', 'census_author_unw', 'census_central_w', 'census_central_unw']
for k, l in lab:
    s.append(f'{l} & ' + ' & '.join(f"{f(G[q][k]['b'])} ({f(G[q][k]['se'])})" for q in keys) + r'\\')
s.append('First-stage $F$ & ' + ' & '.join(f(G[q]['F'], 1) for q in keys) + r'\\')
s.append('Share of net residents absorbed by occupancy & ' + ' & '.join(f(G[q]['share_crowd']['est']) for q in keys) + r'\\')
s.append(r'\quad Fieller 95\% interval & ' + ' & '.join(ci(G[q]['share_crowd']['fieller']) for q in keys) + r'\\')
s.append(r'\quad Province bootstrap 95\% interval & ' + ' & '.join(ci(G[q]['share_crowd']['boot_pct']) for q in keys) + r'\\')
ck = ['composition_author_w', 'composition_author_unw', 'composition_central_w', 'composition_central_unw']
s.append(r'$\Delta\ln$ persons per dwelling predicted by continental composition & ' + ' & '.join(f"{f(G[q]['dln_s_comp']['b'])} ({f(G[q]['dln_s_comp']['se'])})" for q in ck) + r'\\')
s.append(r'Within-group change (observed minus composition) & ' + ' & '.join(f"{f(G[q]['dln_s_within']['b'])} ({f(G[q]['dln_s_within']['se'])})" for q in ck) + r'\\')
s.append(f"Census minus register-cadastre occupancy, 2021 & -- & -- & {f(G['discrepancy2021_w']['b'])} ({f(G['discrepancy2021_w']['se'])}) & {f(G['discrepancy2021_unw']['b'])} ({f(G['discrepancy2021_unw']['se'])})\\\\")
s.append(r'\midrule\multicolumn{5}{l}{\textit{B. Annual register and cadastre, 2015--2023 (central covariates; per unit of calendar-year inflow)}}\\')
P = G['annual_panel_central']
s.append(r' & Population weights & Renter weights & Unweighted & \\')
for k, l in [('gP', r'$\Delta\ln$ registered population'), ('dlnviv_f', r'$\Delta\ln$ cadastral dwellings'), ('gratio', r'$\Delta\ln$ population per cadastral dwelling')]:
    s.append(f'{l} & ' + ' & '.join(f"{f(P[f'{k}_{w}']['b'])} ({f(P[f'{k}_{w}']['se'])})" for w in ['w', 'w_rent', 'unw']) + r' & \\')
s.append('First-stage $F$ & ' + ' & '.join(f(P[f'gP_{w}']['F'], 1) for w in ['w', 'w_rent', 'unw']) + r' & \\')
s.append(r'\midrule\multicolumn{5}{l}{\textit{C. Spain-born intermunicipal migration, 2021--2024 (INE EMCR; per unit of calendar-year inflow)}}\\')
N_ = G['spain_born_migration_2021_2024']
s.append(r' & Population weights & Unweighted & & \\')
for k, l in [('out_es', 'Out-migration rate of the Spain-born'), ('in_es', 'In-migration rate of the Spain-born'), ('net_es', 'Net rate')]:
    s.append(f'{l} & ' + ' & '.join(f"{f(N_[f'{k}_{w}']['b'])} ({f(N_[f'{k}_{w}']['se'])})" for w in ['w', 'unw']) + r' & & \\')
s.append('First-stage $F$ & ' + ' & '.join(f(N_[f'out_es_{w}']['F'], 1) for w in ['w', 'unw']) + r' & & \\')
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: panel A: each row is a 2SLS regression, estimated jointly across rows (stacked influence functions, province clusters), of the indicated '
      r'component of identity \eqref{eq:identity} (persons per 2011 inhabitant) on the change in the foreign-born population 2011--2021 per 2011 inhabitant, '
      r'instrumented with the predicted 2012--2021 inflow; province fixed effects. Rows 1 and 3--5 add up to row 1 by construction. The share is the ratio of rows 5 '
      r'and 1 with a Fieller interval and a 999-draw province pairs bootstrap. The composition-predicted change holds group-specific dwellings per person fixed at the '
      r'2011 ecological estimates (census tracts with municipality fixed effects, table~\ref{tab:kappa}) for Spain-born, European, African, American, Asian and Oceanian '
      r'residents and applies the 2011 (register) and 2021 (annual census) population shares. Panel B: annual changes on the January-to-January foreign-born inflow '
      r'instrumented with its prediction, province $\times$ year fixed effects. Panel C: INE Statistics on Migrations and Changes of Residence, municipal tables 69744 '
      r'and 69746, rates over the Spain-born population on 1 January.', r'\end{minipage}\end{table}']
write('t6_margins.tex', '\n'.join(s))
cw_ = G['census_central_w']; ca_ = G['census_author_w']
mac('crowdC', f(cw_['y_crowd']['b'])); mac('crowdCse', f(cw_['y_crowd']['se'])); mac('popC', f(cw_['y_pop']['b'])); mac('popCse', f(cw_['y_pop']['se']))
mac('natC', f(cw_['y_nat']['b'])); mac('vacC', f(cw_['y_vac']['b'])); mac('vacCse', f(cw_['y_vac']['se'])); mac('newC', f(cw_['y_new']['b'])); mac('newCse', f(cw_['y_new']['se']))
mac('dlnsC', f(cw_['dln_s']['b'])); mac('dlnsCse', f(cw_['dln_s']['se'])); mac('shareC', f(cw_['share_crowd']['est'])); mac('shareCfi', ci(cw_['share_crowd']['fieller']))
mac('shareCbo', ci(cw_['share_crowd']['boot_pct'])); mac('shareA', f(ca_['share_crowd']['est'])); mac('shareAfi', ci(ca_['share_crowd']['fieller']))
mac('shareAU', f(G['census_author_unw']['share_crowd']['est'])); mac('shareCU', f(G['census_central_unw']['share_crowd']['est'])); mac('shareCUfi', ci(G['census_central_unw']['share_crowd']['fieller']))
mac('shareMin', f(G['census_minimal_w']['share_crowd']['est'])); mac('compC', f(G['composition_central_w']['dln_s_comp']['b'])); mac('withinC', f(G['composition_central_w']['dln_s_within']['b']))
mac('ratioP', f(P['gratio_w']['b'])); mac('ratioPse', f(P['gratio_w']['se'])); mac('stockP', f(P['dlnviv_f_w']['b'])); mac('stockPse', f(P['dlnviv_f_w']['se'])); mac('panelF', f(P['gP_w']['F'], 1))
mac('outES', f(N_['out_es_w']['b'])); mac('outESse', f(N_['out_es_w']['se'])); mac('outESF', f(N_['out_es_w']['F'], 1))
eh = G['ecological_h']['kappa']
for g_, t in [('Europe', 'Eur'), ('Africa', 'Afr'), ('America', 'Ame'), ('Asia', 'Asi')]:
    mac(f'kap{t}', f(eh[g_]))

# ---------------------------------------------------------------- Table: magnitudes
fac = 0.065 / 0.206
rowsM = [('Central specification, 2012--2024', c12[f'{K}|w']), ('Central specification, arrival period 2015--2024', c15[f'{K}|w']),
         ('Central, renter weights, 2015--2024', c15[f'{K}|w_rent']), ('Central + province $\\times$ size FE, 2015--2024', c15[f'central + province x size FE|w']),
         ('Original covariates, 2012--2024', c12[f'{O}|w']), ('Colombia--Peru episode (DiD-IV)', dict(b=dv['w']['b'], ar=dv['w']['ar_wcr']))]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Implied contribution of immigration to national rent-index growth, 2015--2024, under explicit assumptions}\label{tab:magnitude}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lccc}\toprule', r'Elasticity used & $\beta$ & Robust 95\% set for $\beta$ & Implied share of IPVA growth (\%)\\\midrule']
for l, q in rowsM:
    lo, hi = q['ar'][0], q['ar'][1]
    sl = 'unbounded' if (np.isinf(lo) or np.isinf(hi)) else f"[{f(max(lo,0)*fac*100,1) if lo > 0 else '0'}, {f(hi*fac*100,1)}]"
    s.append(f"{l} & {f(q['b'])} & {ci(q['ar'])} & {f(q['b']*fac*100,1)} \; {sl}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.97\linewidth}\footnotesize\vspace{4pt}',
      r'\textit{Notes}: implied share $=\beta\times M/G$, with $M=6.5$\,\% the cumulative net foreign-born inflow relative to population (2016--2024, centred timing) '
      r'and $G=20.6$ log points the growth of the national IPVA between 2015 and 2024. The bracket translates the robust set into shares, truncating negative values '
      r'at zero (the AR set with province clusters; wild-bootstrap set for the episode). The calculation assumes (A1) that the national elasticity equals the '
      r'within-province elasticity, (A2) that level effects are permanent, (A3) that the 2015--2024 origin mix has the same elasticity as the identifying variation '
      r'and (A4) no general-equilibrium effects; none of these is identified by the design (section~\ref{sec:magnitude}).', r'\end{minipage}\end{table}']
write('t7_magnitude.tex', '\n'.join(s))
q = c15[f'{K}|w']
mac('shareArr', f(q['b'] * fac * 100, 1)); mac('shareArrLo', f(max(q['ar'][0], 0) * fac * 100, 1)); mac('shareArrHi', f(q['ar'][1] * fac * 100, 1))
q = c12[f'{K}|w']; mac('shareFullHi', f(q['ar'][1] * fac * 100, 1)); mac('shareFull', f(q['b'] * fac * 100, 1))
mac('shareEp', f(dv['w']['b'] * fac * 100, 1)); mac('shareOrig', f(c12[f'{O}|w']['b'] * fac * 100, 1))

# ---------------------------------------------------------------- Appendix tables
# A1: sample flow
sf = D10['sample_flow']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Sample flow}\label{tab:flow}', r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lr}\toprule',
     f"Municipalities in the Padrón (2003--2022) & {sf['municipalities_padron']:,}\\\\",
     f"Municipalities with an IPVA (INE table 59060) & {sf['municipalities_with_ipva']:,}\\\\",
     f"Municipality-years with IPVA growth, 2012--2024 & {sf['muni_years_ipva_2012_2024']:,}\\\\",
     f"Analysis sample after dropping singleton province-years and missing covariates & {sf['analysis_obs']:,} ({sf['analysis_munis']} municipalities, {sf['analysis_provinces']} provinces)\\\\",
     f"Census long-difference sample (municipalities above 5,000 inhabitants) & {G16['census_central_w']['n']:,}\\\\",
     r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.9\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: the IPVA excludes the Basque Country and Navarre. '
     r'Province-years with a single sample municipality are dropped because the province $\times$ year fixed effect absorbs them.\end{minipage}\end{table}']
write('ta1_flow.tex', '\n'.join(s))
# A2: full Rotemberg
s = [r'\begin{table}[!htbp]\centering\scriptsize', r'\caption{Rotemberg decomposition by origin (original specification, population weights)}\label{tab:rotfull}',
     r'\begin{tabular}{llrrrrr}\toprule', r'Origin & Continent & $\hat\alpha_o$ & $\hat\beta_o$ & $F_o$ & $\hat\alpha_o\hat\beta_o$ & $g_{2012-24}$\\\midrule']
CONTEN = {'Europa': 'Europe', 'Africa': 'Africa', 'America': 'Americas', 'Asia': 'Asia', 'Otros': 'Other'}
for _, q in rot.iterrows():
    s.append(f"{EN.get(q.origin, q.origin)} & {CONTEN[q.region]} & {f(q.alpha,3)} & {f(q.beta)} & {f(q.F,1)} & {f(q.contrib,3)} & {f(q.g_2012_2024)}\\\\")
s += [r'\bottomrule\end{tabular}', r'\end{table}']
write('ta2_rotemberg.tex', '\n'.join(s))
# A3: heterogeneity
hh = H17['heterogeneity']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Pre-specified heterogeneity (central specification)}\label{tab:het}', r'\begin{tabular}{lcccc}\toprule',
     r'Dimension & Weights & Interaction (s.e.) & $p$ & BH $q$\\\midrule']
for k, v in hh.items():
    nm, w = k.split('|')
    if 'H3' in nm:
        s.append(f"{nm} & {w} & {f(v['ZR']['b'])} ({f(v['ZR']['se'])}) & {f(v['p_inter'],3)} & {f(v['q_BH'],2)}\\\\")
    else:
        s.append(f"{nm} & {w} & {f(v['xh']['b'])} ({f(v['xh']['se'])}) & {f(v['p_inter'],3)} & {f(v['q_BH'],2)}\\\\")
s += [r'\bottomrule\end{tabular}', r'\begin{minipage}{0.95\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: H1 and H2: 2SLS with the inflow and its interaction with the '
      r'standardised characteristic, instrumented with the instrument and its interaction; the characteristic $\times$ year is controlled for. H3: reduced form with the '
      r'instrument and an effective rental-demand instrument that weights each origin by its relative housing consumption $\kappa$ (table~\ref{tab:kappa}); the '
      r'coefficient reported is that of the effective-demand instrument. $q$: Benjamini-Hochberg adjusted over the eight tests.\end{minipage}\end{table}']
write('ta3_het.tex', '\n'.join(s))
# A4: Catalonia
cat = C18
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Stock index and new-contract rents in Catalonia (Incasòl deposit register)}\label{tab:catalonia}', r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lc}\toprule',
     f"Municipalities matched to the analysis sample & {cat['n_munis']}\\\\",
     f"Median annual new contracts per rented main dwelling (2011 census) & {f(cat['turnover_median'])}\\\\",
     f"Correlation of annual growth: IPVA vs mean new-contract rent & {f(cat['corr_dln_new_dlnR'])}\\\\",
     f"IPVA growth on new-contract rent growth, contemporaneous (municipality and year FE) & {f(cat['ols_stock_on_new']['b'],3)} ({f(cat['ols_stock_on_new']['se'],3)})\\\\",
     f"\\quad with two lags: $t$ / $t-1$ / $t-2$ & {f(cat['ols_stock_on_new_lags']['dln_new']['b'],3)} / {f(cat['ols_stock_on_new_lags']['dln_new_l1']['b'],3)} / {f(cat['ols_stock_on_new_lags']['dln_new_l2']['b'],3)}\\\\",
     f"2SLS within Catalonia, central covariates: first-stage $F$ & {f(cat['central|w|dlnR']['F'],1)}\\\\",
     f"\\quad IPVA / new-contract rent / log contracts per capita & {f(cat['central|w|dlnR']['b'])} / {f(cat['central|w|dln_new']['b'])} / {f(cat['central|w|dln_contracts']['b'])}\\\\",
     r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.95\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: annual (January--December) mean monthly rent and number of '
     r'new contracts with a deposit lodged at Incasòl, by municipality (Generalitat de Catalunya open data). Within-Catalonia 2SLS uses municipality clusters because only '
     r'four provinces are available; the instrument is weak in this subsample and the estimates are reported for completeness.\end{minipage}\end{table}']
write('ta4_catalonia.tex', '\n'.join(s))
mac('turnover', f(cat['turnover_median'])); mac('passT', f(cat['ols_stock_on_new_lags']['dln_new']['b'], 3)); mac('passL1', f(cat['ols_stock_on_new_lags']['dln_new_l1']['b'], 3))
mac('passL2', f(cat['ols_stock_on_new_lags']['dln_new_l2']['b'], 3)); mac('catF', f(cat['central|w|dlnR']['F'], 1)); mac('catN', str(cat['n_munis']))
# A5: alternative shocks + spatial
sp = M12['spatial']
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Alternative push shocks and spatial spillovers (central specification)}\label{tab:altspatial}', r'\begin{tabular}{lcc}\toprule',
     r' & Population weights & Unweighted\\\midrule', r'\multicolumn{3}{l}{\textit{A. Shifts from inflows of each origin into 12 other European countries (Eurostat)}}\\',
     f"First-stage $F$ & {f(A15['S4_central|w|Zalt']['F'],2)} & {f(A15['S4_central|unw|Zalt']['F'],2)}\\\\",
     f"2SLS (AR set) & {f(A15['S4_central|w|Zalt']['b'])} {ci(A15['S4_central|w|Zalt']['ar'])} & {f(A15['S4_central|unw|Zalt']['b'])} {ci(A15['S4_central|unw|Zalt']['ar'])}\\\\",
     r'\midrule\multicolumn{3}{l}{\textit{B. Own inflow and inflow into the surroundings (both instrumented)}}\\']
for ring, l in [('contig', 'Contiguous municipalities'), ('r0_15', 'Ring 0--15 km'), ('r15_40', 'Ring 15--40 km')]:
    a = sp[f'{ring}|w']; b = sp[f'{ring}|unw']; xr_ = f'xc_{ring}'
    s.append(f"{l}: own & {f(a['xc']['b'])} ({f(a['xc']['se'])}) & {f(b['xc']['b'])} ({f(b['xc']['se'])})\\\\")
    s.append(f"\\quad surroundings & {f(a[xr_]['b'])} ({f(a[xr_]['se'])}) & {f(b[xr_]['b'])} ({f(b[xr_]['se'])})\\\\")
s += [r'\bottomrule\end{tabular}', r'\begin{minipage}{0.95\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: panel A: destinations AT, BG, CZ, FI, HR, IT, LU, NL, '
      r'NO, SE, SI and SK (Eurostat migr\_imm3ctb, isolated gaps interpolated); the shift is the inflow of each of the 28 individual origins into these countries over '
      r'its 2003 stock in Spain. Panel B: surroundings defined as in the original manuscript (all municipalities, with or without an IPVA).\end{minipage}\end{table}']
write('ta5_alt_spatial.tex', '\n'.join(s))
mac('altF', f(A15['S4_central|w|Zalt']['F'], 2)); mac('spContig', f(sp['contig|w']['xc_contig']['b'])); mac('spContigSe', f(sp['contig|w']['xc_contig']['se']))
# A6: ecological kappa
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Relative housing consumption by region of birth, 2011 census tracts}\label{tab:kappa}', r'\begin{tabular}{lcc}\toprule',
     r'Region of birth & Dwellings per person & $\kappa$ (relative to the average resident)\\\midrule']
for g_ in ['Spain', 'Europe', 'Africa', 'America', 'Asia', 'Oceania']:
    s.append(f"{g_} & {f(G['ecological_h']['h'][g_],3)} & {f(G['ecological_h']['kappa'][g_])}\\\\")
s += [r'\bottomrule\end{tabular}', r'\begin{minipage}{0.9\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: ecological regression of primary dwellings per person on '
      f"population shares by region of birth across {G['ecological_h']['n_sections']:,} census tracts with at least 100 inhabitants, with municipality fixed effects and population weights.\\end{{minipage}}\\end{{table}}"]
write('ta6_kappa.tex', '\n'.join(s))
# A7: leave-one-out summary
Fr = pd.read_csv(os.path.join(OUT, 'r13_forest.csv'))
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Leave-one-out estimates (central specification, population weights, 2012--2024)}\label{tab:loo}', r'\begin{tabular}{lcccc}\toprule',
     r'Excluded unit & Number & Min & Median & Max\\\midrule']
for gname, l in [('leave-one-province-out', 'One province'), ('leave-one-region-out', 'One autonomous community'), ('leave-one-origin-out', 'One origin from the instrument'),
                 ('leave-one-continent-out', 'One continent from the instrument')]:
    q = Fr[Fr.group == gname]
    s.append(f"{l} & {len(q)} & {f(q.b.min())} & {f(q.b.median())} & {f(q.b.max())}\\\\")
s += [r'\bottomrule\end{tabular}', r'\end{table}']
write('ta7_loo.tex', '\n'.join(s))
# descriptive statistics with new covariates
d = load_revision_panel()
rowsD = [('dlnR', 'Annual rent growth (\\%)', 100), ('xc', 'Foreign-born inflow / population (\\%)', 100), ('Zc', 'Predicted inflow (\\%)', 100),
         ('forsh_base', 'Foreign-born share, 2003 (\\%)', 100), ('rent11', 'Renting households, 2011 (\\%)', 100), ('vac11', 'Non-primary dwellings, 2011 (\\%)', 100),
         ('tert11', 'Tertiary education, 2011 (\\%)', 100), ('sh65_11', 'Population aged 65+, 2011 (\\%)', 100), ('sh_constr12', 'Construction firms, 2012 (\\%)', 100),
         ('sh_trade_hosp12', 'Trade, transport and hospitality firms, 2012 (\\%)', 100), ('coastal', 'Coastal municipality (\\%)', 100), ('city_core', 'FUA core city (\\%)', 100),
         ('persons_per_room11', 'Persons per room, 2011', 1), ('pop11', 'Population, 2011', 1)]
s = [r'\begin{table}[!htbp]\centering\small', r'\caption{Descriptive statistics of the municipal sample, 2012--2024}\label{tab:desc}',
     r'\begin{adjustbox}{max width=\linewidth}\begin{tabular}{lrrrrr}\toprule', r' & Mean & Std. dev. & Weighted mean & P10 & P90 \\ \midrule']
for v, l, sc in rowsD:
    x = d[v].replace([np.inf, -np.inf], np.nan) * sc; ok = x.notna()
    wm = np.average(x[ok], weights=d.loc[ok, 'w'])
    fmt = (lambda z: f'{z:,.0f}') if v == 'pop11' else (lambda z: f(z, 2))
    s.append(f"{l} & {fmt(x.mean())} & {fmt(x.std())} & {fmt(wm)} & {fmt(x.quantile(.1))} & {fmt(x.quantile(.9))}\\\\")
s += [r'\bottomrule\end{tabular}\end{adjustbox}', r'\begin{minipage}{0.95\linewidth}\footnotesize\vspace{4pt}\textit{Notes}: 9,060 municipality-year observations for '
      r'699 municipalities in 42 provinces. Flows between consecutive mid-years over population on 1 January of the previous year. The weighted mean uses 2003 '
      r'population. Sources: INE (IPVA, Padrón, annual population census, 2011 census, firm directory), Eurostat (LAU 2021).\end{minipage}\end{table}']
write('t1_desc.tex', '\n'.join(s))
with open(os.path.join(TAB, 'numbers_rev.tex'), 'w') as fh:
    for k, v in macros.items():
        fh.write(f'\\newcommand{{\\{k}}}{{{v}}}\n')
print(len(macros), 'macros;', sorted(os.listdir(TAB)))

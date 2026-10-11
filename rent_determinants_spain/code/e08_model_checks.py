"""Calibration of the stock-flow model with the turnover estimates (all numbers quoted in section 4 of the paper).
lambda range: lowest and highest of the INE implied weight of new leases (2021-2024) and the Aragón exit rate under the three
age conventions (e05). For each end of the range: (1-lambda)/lambda, the steady-state gap for entry rents growing 2 points a
year faster than updates, the share of a permanent entry-rent shock absorbed by the index of all leases after 1 and 4 years,
the weight (1-lambda)^9 of the 2015 gap in the 2024 gap, the front-loading horizon rho(1-lambda)/[1-rho(1-lambda)] with
rho = 0.96, and the ratio of the response of the index of all leases to that of entry rents in 2024 implied by the actual
national timing of the foreign-born inflow over 2015-2024 (shock of calendar year t absorbed at 1-(1-lambda)^(2025-t)).
Also the entry gap relative to existing leases implied by the AEAT gap relative to all leases, with the share of new leases s
set to the INE weight of new leases in 2024: ln[e^G (1-s) / (1 - s e^G)].
Output: out/e08_model_checks.json"""
import numpy as np
from rd_common import *
from rev_common import flows_by_origin

E5 = load('e05_extensions.json'); B3 = load('b03_aeat_entry_gap.json'); E1 = load('e01_main.json')
tv = E5['turnover']
cands = list(tv['ine_w_new'].values()) + list(tv['sens_age'].values())
lam = {'lo': float(min(cands)), 'hi': float(max(cands)), 'base': float(tv['open_share']['annual_exit'])}
dF = flows_by_origin(['FOR']).reset_index()
nat = dF[dF.year.between(2015, 2024)].groupby('year').FOR.sum()
w = nat / nat.sum()
res = {'lambda': lam, 'inflow_weights': w.round(4).to_dict()}
for k, l in lam.items():
    res[k] = dict(ratio_ss=(1 - l) / l, G_ss_2pp=2 * (1 - l) / l, absorb_1=1 - (1 - l), absorb_4=1 - (1 - l) ** 4,
                  w_G2015=(1 - l) ** 9, kbar=0.96 * (1 - l) / (1 - 0.96 * (1 - l)),
                  ratio_index_entry=float(sum(w[t] * (1 - (1 - l) ** (2025 - t)) for t in w.index)))
s = tv['ine_w_new']['2024'] if '2024' in tv['ine_w_new'] else tv['ine_w_new'][2024]
G = B3['desc']['G_vr']['mean_w']
res['gap_vs_existing'] = dict(s=s, G_all=G, G_exist=float(np.log(np.exp(G) * (1 - s) / (1 - s * np.exp(G)))), scale=float(1 / (1 - s)))
mm = E1['main']
res['observed_ratio_index_entry'] = mm['dlnR']['b'] / mm['entry']['b']
print(res)
save('e08_model_checks.json', res)

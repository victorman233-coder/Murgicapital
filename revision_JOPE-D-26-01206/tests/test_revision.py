"""Automatic checks of the revision pipeline (run after the analyses)."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
import numpy as np, pandas as pd
from rev_common import *
from rev_design import obs_matrices

R = json.load(open(os.path.join(OUT, 'r10_diagnostics.json')))
# 1. rebuilt instrument equals the one in the earlier version
assert R['check_instrument_maxdiff'] < 1e-12, R['check_instrument_maxdiff']
# 2. BHJ: 2SLS with national shocks equals the exact shock-level representation
assert abs(R['national_shocks']['iv']['b'] - R['national_shocks']['shock_level_equivalent']) < 1e-10
# 3. Rotemberg decomposition adds up to the 2SLS estimate and the hand-coded 2SLS equals pyfixest
assert abs(R['rotemberg']['beta_total'] - R['pyfixest_check']['b']) < 1e-10
# 4. census decomposition identity: net residents = new + non-primary + occupancy (coefficients, jointly estimated)
G = json.load(open(os.path.join(OUT, 'r16_margins.json')))
for k in ['census_central_w', 'census_author_w', 'census_central_unw']:
    g = G[k]; assert abs(g['y_pop']['b'] - (g['y_new']['b'] + g['y_vac']['b'] + g['y_crowd']['b'])) < 1e-6, k
# 5. shares: total exposure equals the sum of origin shares
s, lam, P0 = shares(2003)
pg = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
b = pg[(pg.src == 'padron') & (pg.year == 2003) & (pg.cmun != '00000')].set_index('cmun')
assert np.allclose(s.sum(axis=1), (b.FOR / b.P).reindex(s.index), atol=1e-12)
print('all revision checks passed')

"""Origin-level components of the long-difference shift-share instrument (d14): Z_i = sum_o S_io g_io with
S_io = s_io P_i03 / P_i15 and g_io the cumulative 2015..T leave-own-province-out change of the origin-o stock over its
2003 national stock."""
from rd_common import *
from rev_common import GROUPS, flows_by_origin, shares, shocks_counts

_dF = flows_by_origin()
_nat, _prv = shocks_counts(_dF)
_s, _lam, _P0 = shares(2003)
_Fo = _s.multiply(_P0, axis=0).sum()[GROUPS]


def components(d, T):
    """N x O exposures, N x O leave-out shocks and the O national shocks for the municipalities in d (cmun, P15)."""
    S = _s.reindex(d.cmun)[GROUPS].fillna(0).values * (_P0.reindex(d.cmun).values / d.P15.values)[:, None]
    gnat = (_nat.loc[2015:T, GROUPS].sum() / _Fo).values
    pv = _prv.reset_index(); pv = pv[(pv.year >= 2015) & (pv.year <= T)].groupby('cpro')[GROUPS].sum() / _Fo
    gprv = pv.reindex(d.cmun.str[:2]).fillna(0).values
    return S, gnat[None, :] - gprv, gnat


def flows_cum(T0=2015, T1=2024):
    """Cumulative net change by origin group and municipality, calendar years T0..T1."""
    f = _dF.reset_index()
    return f[(f.year >= T0) & (f.year <= T1)].groupby('cmun')[GROUPS].sum()

"""Stage 1E/2: margins of adjustment (census 2011-2021 and annual register-cadastre), absorption shares with
Fieller and bootstrap intervals, composition vs within-group occupancy, register-census discrepancy,
and native (Spain-born) intermunicipal migration 2021-2024 (INE EMCR).
Output: out/r16_margins.json"""
import glob
import numpy as np, pandas as pd, pyfixest as pf
from rev_common import *
from rev_design import *

res = {}
A = pd.read_parquet(f'{REP}/data/clean/census_ld_muni.parquet')
A.index.name = 'cmun'; A = A.reset_index()
ext = pd.read_parquet(f'{WORK}/clean/muni_extended.parquet')
A = A.merge(ext[[c for c in ext.columns if c not in A.columns]], left_on='cmun', right_index=True, how='left')
A['lnpop11'] = np.log(A['pop_11'])
A['tert11'] = A['tert11'].replace([np.inf, -np.inf], np.nan)
A['w'] = A['pop_11']
OUTC = ['y_pop', 'y_nat', 'y_new', 'y_vac', 'y_crowd', 'y_rent', 'dln_s']
SPECS = {'minimal': ['forsh_base'], 'author': ['forsh_base', 'lninc15', 'lnpop11', 'rent11', 'vac11'],
         'central': ['forsh_base'] + PRED + ECON}


def fieller(a, b, Va, Vb, Cab, z=1.959964):
    A_ = b * b - z * z * Vb; B_ = -2 * (a * b - z * z * Cab); C_ = a * a - z * z * Va
    disc = B_ * B_ - 4 * A_ * C_
    if A_ > 0 and disc >= 0:
        r1, r2 = (-B_ - np.sqrt(disc)) / (2 * A_), (-B_ + np.sqrt(disc)) / (2 * A_)
        return [float(min(r1, r2)), float(max(r1, r2))]
    return [-np.inf, np.inf] if A_ < 0 and disc < 0 else ['unbounded/disjoint']


def stacked(D, ys, x, z, ctrls, w, fe='cpro', B=999, seed=3):
    D = D.dropna(subset=ys + [x, z] + ctrls).reset_index(drop=True)
    Rm = Resid(D, [fe], ctrls, w); W_ = Rm.w
    xr, zr = Rm(D[x]), Rm(D[z]); den = np.sum(W_ * zr * xr)
    cl = D['cpro'].values; out = {}; psi = {}
    for y in ys:
        yr = Rm(D[y]); b = np.sum(W_ * zr * yr) / den
        e = yr - b * xr
        psi[y] = pd.Series(W_ * zr * e / den).groupby(cl).sum()
        out[y] = dict(b=float(b))
    Pm = pd.concat([psi[y] for y in ys], axis=1)
    ng = Pm.shape[0]; N = len(D); c = ng / (ng - 1) * (N - 1) / (N - Rm.rank - 1)
    V = c * Pm.values.T @ Pm.values
    for j, y in enumerate(ys):
        out[y]['se'] = float(np.sqrt(V[j, j]))
    # first stage
    pi = np.sum(W_ * zr * xr) / np.sum(W_ * zr * zr); u = xr - pi * zr
    sp = np.sqrt(c * np.sum(pd.Series(W_ * zr * u).groupby(cl).sum().values ** 2)) / np.sum(W_ * zr * zr)
    out['F'] = float((pi / sp) ** 2); out['n'] = int(N)
    # absorption share of occupancy (crowding) in net population growth
    i, j = ys.index('y_crowd'), ys.index('y_pop')
    a, b_ = out['y_crowd']['b'], out['y_pop']['b']
    out['share_crowd'] = dict(est=a / b_, fieller=fieller(a, b_, V[i, i], V[j, j], V[i, j]))
    # province pairs bootstrap
    rng = np.random.default_rng(seed); provs = np.unique(cl); ratios = []
    for _ in range(B):
        pick = rng.choice(provs, len(provs), replace=True)
        Db = pd.concat([D[D.cpro == p_].assign(cpro=f'{p_}_{k}') for k, p_ in enumerate(pick)], ignore_index=True)
        try:
            Rb = Resid(Db, ['cpro'], ctrls, w); Wb = Rb.w
            xb, zb = Rb(Db[x]), Rb(Db[z]); dn = np.sum(Wb * zb * xb)
            ratios.append((np.sum(Wb * zb * Rb(Db['y_crowd'])) / dn) / (np.sum(Wb * zb * Rb(Db['y_pop'])) / dn))
        except Exception:
            pass
    ratios = np.array(ratios)
    out['share_crowd']['boot_pct'] = [float(np.percentile(ratios, 2.5)), float(np.percentile(ratios, 97.5))]
    out['share_crowd']['boot_median'] = float(np.median(ratios))
    return out

for sname, ctrls in SPECS.items():
    for w in ['w', None]:
        r = stacked(A, OUTC, 'x', 'Z', ctrls, w)
        res[f'census_{sname}_{w or "unw"}'] = r
        print(sname, w, 'F', round(r['F'], 1), {y: (round(r[y]['b'], 3), round(r[y]['se'], 3)) for y in OUTC}, r['share_crowd'])

# ------------------------------------------------------------------ composition vs within-group occupancy
fs = sorted(glob.glob(f'{WORK}/raw/c2011/C2011_ccaa*_Indicadores.csv'))
c = pd.concat([pd.read_csv(f, dtype={'cpro': str, 'cmun': str, 'dist': str, 'secc': str}) for f in fs])
c['cmun5'] = c.cpro + c.cmun
c = c[(c.t1_1 >= 100)].dropna(subset=['t17_1', 't4_1', 't4_2', 't4_3', 't4_4', 't4_5', 't4_6', 't4_7', 't4_8'])
c['hpp'] = c.t17_1 / c.t1_1
grp = {'Europe': ['t4_2', 't4_3'], 'Africa': ['t4_4'], 'America': ['t4_5', 't4_6'], 'Asia': ['t4_7'], 'Oceania': ['t4_8']}
for g, cols in grp.items():
    c['sh_' + g] = c[cols].sum(axis=1) / c.t1_1
m = pf.feols('hpp ~ ' + ' + '.join('sh_' + g for g in grp) + ' | cmun5', data=c, vcov={'CRV1': 'cmun5'}, weights='t1_1')
slope = m.coef()
Ptot = c.t1_1.sum(); Htot = c.t17_1.sum()
Pg = {g: c[cols].sum(axis=1).sum() for g, cols in grp.items()}
hN = (Htot - sum(slope['sh_' + g] * Pg[g] for g in grp)) / Ptot
h = {'Spain': hN, **{g: hN + slope['sh_' + g] for g in grp}}
res['ecological_h'] = dict(h={k: float(v) for k, v in h.items()}, se={g: float(m.se()['sh_' + g]) for g in grp},
                           kappa={k: float(v / (Htot / Ptot)) for k, v in h.items()}, n_sections=int(len(c)))
pg = pd.read_parquet(f'{WORK}/clean/pop_groups_nacim.parquet')
def comp_shares(src, yr):
    q = pg[(pg.src == src) & (pg.year == yr)].set_index('cmun')
    out = pd.DataFrame(index=q.index)
    out['Spain'] = q.NAT
    for g, reg in [('Europe', 'Europa'), ('Africa', 'Africa'), ('America', 'America'), ('Asia', 'Asia'), ('Oceania', 'Otros')]:
        out[g] = q[[o for o in GROUPS if REGION[o] == reg]].sum(axis=1)
    return out.div(out.sum(axis=1), axis=0)
pi11 = comp_shares('padron', 2011); pi21 = comp_shares('censo', 2021)
hv = pd.Series(h)
A['inv_s11_comp'] = A.cmun.map(pi11[hv.index] @ hv); A['inv_s21_comp'] = A.cmun.map(pi21[hv.index] @ hv)
A['dln_s_comp'] = np.log(A.inv_s11_comp) - np.log(A.inv_s21_comp)
A['dln_s_within'] = A.dln_s - A.dln_s_comp
for sname, ctrls in SPECS.items():
    for w in ['w', None]:
        D = A.dropna(subset=['dln_s', 'dln_s_comp', 'x', 'Z'] + ctrls).reset_index(drop=True)
        ys = ['dln_s', 'dln_s_comp', 'dln_s_within']
        Rm = Resid(D, ['cpro'], ctrls, w); W_ = Rm.w
        xr, zr = Rm(D.x), Rm(D.Z); den = np.sum(W_ * zr * xr); cl = D.cpro.values
        out = {}; psi = {}
        for y in ys:
            yr = Rm(D[y]); b = np.sum(W_ * zr * yr) / den; e = yr - b * xr
            psi[y] = pd.Series(W_ * zr * e / den).groupby(cl).sum(); out[y] = dict(b=float(b))
        Pm = pd.concat([psi[y] for y in ys], axis=1).values; ng = Pm.shape[0]; N = len(D)
        V = ng / (ng - 1) * (N - 1) / (N - Rm.rank - 1) * Pm.T @ Pm
        for j, y in enumerate(ys):
            out[y]['se'] = float(np.sqrt(V[j, j]))
        out['share_composition'] = dict(est=out['dln_s_comp']['b'] / out['dln_s']['b'],
                                        fieller=fieller(out['dln_s_comp']['b'], out['dln_s']['b'], V[1, 1], V[0, 0], V[0, 1]))
        res[f'composition_{sname}_{w or "unw"}'] = out
        print('composition', sname, w, out)

# ------------------------------------------------------------------ register/cadastre vs census occupancy in 2021
cat = pd.read_parquet(f'{REP}/data/clean/catastro_muni.parquet')
H21 = cat[cat.year == 2021].set_index('cmun').viv
P21 = pg[(pg.src == 'censo') & (pg.year == 2021)].set_index('cmun').P
A['ln_s21_census'] = np.log(A.s21)
A['ln_s21_regcad'] = np.log(A.cmun.map(P21) / A.cmun.map(H21))
A['disc21'] = A.ln_s21_census - A.ln_s21_regcad
for w in ['w', None]:
    D = A.dropna(subset=['disc21', 'x', 'Z'] + SPECS['central']).reset_index(drop=True)
    mm = pf.feols(f'disc21 ~ {" + ".join(SPECS["central"])} | cpro | x ~ Z', data=D, vcov={'CRV1': 'cpro'}, weights=w)
    res[f'discrepancy2021_{w or "unw"}'] = coef(mm, 'x')
    print('discrepancy', w, res[f'discrepancy2021_{w or "unw"}'])

# ------------------------------------------------------------------ annual register-cadastre panel (central spec)
d = load_revision_panel()
cat = cat.sort_values(['cmun', 'year'])
cat['lnviv'] = np.log(cat.viv.where(cat.viv > 0))
cat['dlnviv_f'] = cat.groupby('cmun').lnviv.shift(-1) - cat.lnviv
d = d.merge(cat[['cmun', 'year', 'dlnviv_f']], on=['cmun', 'year'], how='left')
d['x1'] = d.d_FOR / d.P; d['z1'] = d.Zcount / d.P; d['gP'] = d.d_P / d.P
d['gratio'] = d.gP - d.dlnviv_f
pnl = {}
for w in ['w', 'w_rent', None]:
    D = d[(d.year >= 2015) & (d.year <= 2023)].dropna(subset=['dlnviv_f', 'gP', 'x1', 'z1'] + PRED + ECON).reset_index(drop=True)
    D = D[D.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
    cc = year_ctrls(D, ['forsh_base'] + PRED + ECON)
    Rm = Resid(D, ['cy'], cc, w); xr, zr = Rm(D.x1), Rm(D.z1)
    for y in ['gP', 'dlnviv_f', 'gratio']:
        yr = Rm(D[y]); r = tsls(yr, xr, zr, Rm.w, D.cpro.values, Rm.rank + 1); pnl[f'{y}_{w or "unw"}'] = r
        print('panel', y, w, {k: round(float(v), 3) for k, v in r.items()})
res['annual_panel_central'] = pnl

# ------------------------------------------------------------------ Spain-born intermunicipal migration 2021-2024 (INE EMCR)
def emcr(tab):
    q = pd.read_csv(f'{WORK}/raw/ine_{tab}.csv', sep=';', dtype=str, encoding='utf-8-sig')
    q = q[(q['Sexo'] == 'Ambos sexos') & q['Municipios'].notna()]
    q['cmun'] = q['Municipios'].str[:5]; q['year'] = q['Periodo'].astype(int)
    q['v'] = pd.to_numeric(q['Total'].str.replace('.', '', regex=False), errors='coerce')
    return q.pivot_table(index=['cmun', 'year'], columns='País de nacimiento', values='v', aggfunc='first')
outm = emcr(69746); inm = emcr(69744)
nat = pg.set_index(['cmun', 'year'])
e = d[d.year >= 2021][['cmun', 'year', 'cpro', 'cy', 'w', 'w_rent', 'x1', 'z1', 'forsh_base'] + PRED + ECON].copy()
e['NAT'] = [nat.loc[(m_, y_), 'NAT'].iloc[0] if (m_, y_) in nat.index else np.nan for m_, y_ in zip(e.cmun, e.year)] if False else np.nan
q = pg[pg.src == 'censo'].set_index(['cmun', 'year'])
e['NAT'] = e.set_index(['cmun', 'year']).index.map(q['NAT'])
e['out_es'] = e.set_index(['cmun', 'year']).index.map(outm['España']) / e.NAT
e['in_es'] = e.set_index(['cmun', 'year']).index.map(inm['España']) / e.NAT
e['out_fb'] = e.set_index(['cmun', 'year']).index.map(outm['Extranjero']) / e.NAT
e['net_es'] = e.in_es - e.out_es
nat_mig = {}
for w in ['w', None]:
    D = e.dropna(subset=['out_es', 'in_es', 'x1', 'z1'] + PRED + ECON).reset_index(drop=True)
    D = D[D.groupby('cy').cmun.transform('size') > 1].reset_index(drop=True)
    cc = year_ctrls(D, ['forsh_base'] + PRED + ECON)
    Rm = Resid(D, ['cy'], cc, w); xr, zr = Rm(D.x1), Rm(D.z1)
    for y in ['out_es', 'in_es', 'net_es']:
        yr = Rm(D[y]); r = tsls(yr, xr, zr, Rm.w, D.cpro.values, Rm.rank + 1); r['mean_y'] = float(D[y].mean()); r['n'] = len(D)
        nat_mig[f'{y}_{w or "unw"}'] = r
        print('natives', y, w, {k: round(float(v), 4) for k, v in r.items()})
res['spain_born_migration_2021_2024'] = nat_mig
save('r16_margins.json', res)

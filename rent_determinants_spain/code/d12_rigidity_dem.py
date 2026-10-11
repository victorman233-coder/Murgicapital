"""Geographic supply constraints a la Saiz (2010): share of land within 10 km (and 20 km) of each municipality's
centroid that is sea or has slope above 15%, from the Copernicus DEM GLO-90 (open AWS registry)."""
import json, math, os, subprocess
import numpy as np, pandas as pd, rasterio
WORK = os.environ.get('WORK', '/home/user/work'); D = f'{WORK}/rent/raw/dem'; CL = f'{WORK}/rent/clean'; os.makedirs(D, exist_ok=True)
T = json.load(open(f'{WORK}/raw/geo/municipalities.json'))
sc, tr = T['transform']['scale'], T['transform']['translate']
arcs = []
for a in T['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)
def ring(idx):
    pts = []
    for i in idx:
        seg = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(seg if not pts else seg[1:])
    return np.array(pts)
def centroid(P):
    A = Cx = Cy = 0.0
    for r in P:
        x, y = r[:, 0], r[:, 1]; c = x[:-1] * y[1:] - x[1:] * y[:-1]
        a = c.sum() / 2; A += a; Cx += ((x[:-1] + x[1:]) * c).sum() / 6; Cy += ((y[:-1] + y[1:]) * c).sum() / 6
    return (Cx / A, Cy / A) if A != 0 else (np.nan, np.nan)
cent = {}
for g in T['objects']['municipalities']['geometries']:
    P = [g['arcs']] if g['type'] == 'Polygon' else g['arcs'] if g['type'] == 'MultiPolygon' else []
    if P:
        cent[g['id']] = centroid([ring(p[0]) for p in P])
M = pd.read_parquet(f'{CL}/muni_panel.parquet')
need = set(M.cmun.unique())
if os.path.exists(f'{CL}/aeat_entry_gap_2024.parquet'):
    need |= set(pd.read_parquet(f'{CL}/aeat_entry_gap_2024.parquet').cmun)
C = pd.DataFrame([(c, *cent[c]) for c in need if c in cent], columns=['cmun', 'lon', 'lat']).dropna()
R_KM = [10, 20]
tiles = set()
for _, r in C.iterrows():
    dlat = max(R_KM) / 111.0; dlon = dlat / math.cos(math.radians(r.lat))
    for la in range(math.floor(r.lat - dlat), math.floor(r.lat + dlat) + 1):
        for lo in range(math.floor(r.lon - dlon), math.floor(r.lon + dlon) + 1):
            tiles.add((la, lo))
def tname(la, lo):
    return f"Copernicus_DSM_COG_30_{'N' if la >= 0 else 'S'}{abs(la):02d}_00_{'E' if lo >= 0 else 'W'}{abs(lo):03d}_00_DEM"
for la, lo in sorted(tiles):
    f = f'{D}/{tname(la, lo)}.tif'
    if not os.path.exists(f):
        subprocess.run(['curl', '-sS', '--retry', '3', '-f', '-o', f, f'https://copernicus-dem-90m.s3.amazonaws.com/{tname(la, lo)}/{tname(la, lo)}.tif'])
print('tiles', len(tiles), 'available', sum(os.path.exists(f'{D}/{tname(*t)}.tif') for t in tiles), flush=True)
cache = {}
def tile(la, lo):
    k = (la, lo)
    if k not in cache:
        f = f'{D}/{tname(la, lo)}.tif'
        if not os.path.exists(f):
            cache[k] = None
        else:
            with rasterio.open(f) as src:
                z = src.read(1).astype(np.float32); tf = src.transform
            ny, nx = z.shape
            latc = la + 0.5
            dy = abs(tf.e) * 111320.0; dx = abs(tf.a) * 111320.0 * math.cos(math.radians(latc))
            gy, gx = np.gradient(z, dy, dx)
            slope = np.sqrt(gx ** 2 + gy ** 2) * 100
            sea = z <= 0
            cache[k] = (tf, sea, slope > 15)
    return cache[k]
out = []
for _, r in C.iterrows():
    row = {'cmun': r.cmun}
    for rk in R_KM:
        dlat = rk / 111.0; dlon = dlat / math.cos(math.radians(r.lat))
        tot = sea_n = steep_n = 0
        for la in range(math.floor(r.lat - dlat), math.floor(r.lat + dlat) + 1):
            for lo in range(math.floor(r.lon - dlon), math.floor(r.lon + dlon) + 1):
                t = tile(la, lo)
                # grid of cell centres of this tile intersecting the bounding box
                if t is None:
                    # missing tile = open sea: count its cells inside the circle approximately
                    ys = np.arange(la + 1 / 2400, la + 1, 1 / 1200); xs = np.arange(lo + 1 / 2400, lo + 1, 1 / 1200)
                    yy, xx = np.meshgrid(ys, xs, indexing='ij')
                    inside = ((yy - r.lat) * 111.0) ** 2 + ((xx - r.lon) * 111.0 * math.cos(math.radians(r.lat))) ** 2 <= rk ** 2
                    n = int(inside.sum()); tot += n; sea_n += n
                    continue
                tf, sea, steep = t
                ny, nx = sea.shape
                ys = tf.f + tf.e * (np.arange(ny) + 0.5); xs = tf.c + tf.a * (np.arange(nx) + 0.5)
                iy = np.where(np.abs(ys - r.lat) <= dlat)[0]; ix = np.where(np.abs(xs - r.lon) <= dlon)[0]
                if len(iy) == 0 or len(ix) == 0:
                    continue
                yy, xx = np.meshgrid(ys[iy], xs[ix], indexing='ij')
                inside = ((yy - r.lat) * 111.0) ** 2 + ((xx - r.lon) * 111.0 * math.cos(math.radians(r.lat))) ** 2 <= rk ** 2
                s = sea[np.ix_(iy, ix)][inside]; st = steep[np.ix_(iy, ix)][inside]
                tot += inside.sum(); sea_n += s.sum(); steep_n += (st & ~s).sum()
        row[f'sea{rk}'] = sea_n / tot if tot else np.nan
        row[f'steep{rk}'] = steep_n / max(tot - sea_n, 1)
        row[f'undev{rk}'] = (sea_n + steep_n) / tot if tot else np.nan
    out.append(row)
R = pd.DataFrame(out).merge(C, on='cmun')
R.to_parquet(f'{CL}/rigidity_dem.parquet'); print(R.describe().round(3).to_string())

#!/bin/bash
# Additional open inputs for the entry-gap redesign (all official open data; see Propuesta_rediseno_asequibilidad.md).
set -e
WORK=${WORK:-/home/user/work}; R=$WORK/rent/raw; cd $R
# Basque Country: rental market statistics from the deposit register (EMAL), municipalities and barrios, 2016-2025
curl -sSL -o emal/EMAL_barrios_municipios_2016_2025.xlsx "https://opendata.euskadi.eus/contenidos/estadistica/122417_emal_tablas_estad/opendata/EMAL.-Barrios-Municipios.-2016-2025_es.xlsx"
# Comunitat Valenciana: deposit register microdata, one CKAN package per year (2020-2026)
python - <<'PY'
import json, urllib.request, os
q = json.load(urllib.request.urlopen('https://dadesobertes.gva.es/api/3/action/package_search?q=fianzas&rows=50', timeout=120))
for p in q['result']['results']:
    for r in p.get('resources', []):
        if r.get('format', '').upper() == 'CSV' and 'fianza' in (r.get('url', '') + p['name']).lower():
            fn = os.path.join('gva', p['name'] + '.csv')
            if not os.path.exists(fn):
                os.system(f"curl -sSL --retry 3 -o '{fn}' '{r['url']}'")
            print(p['name'], r['url'])
PY
# Catalonia: seasonal leases by municipality and lease registrations/cancellations (habitatge.gencat.cat)
B=https://habitatge.gencat.cat/web/.content/home/dades/estadistiques/01_Estadistiques_de_construccio_i_mercat_immobiliari/03_Mercat_de_lloguer
curl -sSL -o cat2/lloguer_temporada_mun.xlsx "$B/08_Lloguer-de-temporada/lloguer_temporada_mun.xlsx"
curl -sSL -o cat2/saldo_contractes_htge_temp.xlsx "$B/07_Saldos/251103_Saldo_contractes_Htge_i_Temp.xlsx"
curl -sSL -o cat2/saldos_altes_cancelacions.xlsx "$B/07_Saldos/Saldos-altes_cancel_lacions.xlsx"
# AEAT: dwellings declared in IRPF 2024, new contracts vs all leases (municipalities >20k; postal codes)
curl -sSL -o aeat/aeat_newcontracts_muni_2024.html "https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfvivienda/2024/jrubik16a4b116943de994823993a0e8a448e24ac90bcd.html"
curl -sSL -o aeat/aeat_newcontracts_cp_2024.html "https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfvivienda/2024/jrubik582b4eeccd4e39730277d218cc788357e33967da.html"
# MIVAU (apps.fomento.gob.es): appraised value of free-market housing, municipalities >25k, quarterly 2005-2026
curl -sSL -o mivau/valor_tasado_muni.xls "https://apps.fomento.gob.es/BoletinOnline2/sedal/35103500.XLS"
echo done

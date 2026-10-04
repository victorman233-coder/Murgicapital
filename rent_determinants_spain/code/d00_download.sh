#!/bin/bash
# Raw inputs for "What drives rents in Spain?": every file is fetched from an official open-data endpoint.
# Usage: WORK=/path/to/work bash code/d00_download.sh
# The municipal population panel by country of birth and the shift-share instrument are built by the
# pipeline of the companion revision (../revision_JOPE-D-26-01206/code: r00_download.sh, r01, r02).
set -e
WORK=${WORK:-/home/user/work}; R=$WORK/rent/raw; mkdir -p $R/{cat,ecb}; cd $R
# INE (jaxiT3, semicolon CSV, UTF-8 with BOM)
#  59060 IPVA municipalities; 59058 IPVA provinces; 59005 IPVA provinces by contract age (new / existing)
#  39363, 39366 tourist dwellings by municipality (experimental statistic, 2020-2026)
#  10745 foreclosures on dwellings by province and owner type; 24457 mortgage interest rates; 50902 CPI
for t in 59060 59058 59005 39363 39366 10745 24457 50902; do
  curl -sS --retry 4 -o ine_$t.csv "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/$t.csv"
done
# Generalitat de Catalunya open data (Socrata): new-lease deposits by municipality and quarter, housing
# reference areas (incl. tensioned-market designation), tourism register, tourist-stay tax by municipality
S=https://analisi.transparenciacatalunya.cat
curl -sSL -o cat/lloguer_municipi.csv "$S/api/views/qww9-bvhh/rows.csv?accessType=DOWNLOAD"
curl -sSL -o cat/arees_referencia_habitatge.csv "$S/api/views/fftm-v9b6/rows.csv?accessType=DOWNLOAD"
curl -sSL -o cat/registre_turisme.csv "$S/api/views/t2h3-cgys/rows.csv?accessType=DOWNLOAD"
curl -sSL -o cat/ieet_municipi.csv "$S/api/views/q4sr-68c3/rows.csv?accessType=DOWNLOAD"
# ECB: 12-month Euribor, monthly averages
curl -sSL -o ecb/euribor12m.csv "https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA?format=csvdata"
# INE household income atlas (54 provincial tables, municipal rows kept)
python "$(dirname "$0")/d01_adrh.py"
echo "downloads complete"

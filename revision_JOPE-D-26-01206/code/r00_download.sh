#!/bin/bash
# Download every raw input of the revision from the official open-data endpoints into $WORK/raw.
# Usage: WORK=/path/to/work bash code/r00_download.sh
set -e
WORK=${WORK:-/home/user/work}; mkdir -p $WORK/raw/{c2011,c2021,cat,eurostat,gisco,geo}; cd $WORK
# Author's replication package (clean analysis files: panel, census long differences, cadastre, geography)
curl -sSL -o ESM_1.zip https://zenodo.org/api/records/23013308/files/ESM_1.zip/content && unzip -qo ESM_1.zip
# INE tables (jaxiT3 CSV, semicolon, UTF-8 with BOM)
for t in 33573 66322 59060 59061 59058 59059 59005 4721 69744 69746 69767; do
  curl -sS --retry 4 -o raw/ine_$t.csv "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/$t.csv"
done
# INE census tract indicators
curl -sSL -o raw/c2011/indicadores_seccion_censal_csv.zip https://www.ine.es/censos2011_datos/indicadores_seccion_censal_csv.zip
curl -sSL -o raw/c2011/indicadores_seccen_rejilla.xls https://www.ine.es/censos2011_datos/indicadores_seccen_rejilla.xls
(cd raw/c2011 && unzip -qo indicadores_seccion_censal_csv.zip)
curl -sSL -o raw/c2021/C2021_Indicadores.csv https://www.ine.es/censos2021/C2021_Indicadores.csv
# Eurostat
curl -sSL -o raw/eurostat/migr_imm3ctb.json "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/migr_imm3ctb?format=JSON&lang=EN&age=TOTAL&sex=T&agedef=COMPLET"
# EU-SILC by citizenship, Spain, adults (Fig. 1): overcrowding and tenure status
for t in ilc_lvho15 ilc_lvps15; do
  curl -sSL -o raw/eurostat/${t}_ES.json "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/$t?format=JSON&lang=EN&geo=ES&sex=T&age=Y_GE18"
done
# Municipal and provincial boundaries (IGN, TopoJSON version of es-atlas 0.6.0) for the maps
curl -sSL -o raw/geo/municipalities.json https://cdn.jsdelivr.net/npm/es-atlas@0.6.0/es/municipalities.json
curl -sSL -o raw/gisco/EU-27-LAU-2021-NUTS-2021.xlsx https://ec.europa.eu/eurostat/documents/345175/501971/EU-27-LAU-2021-NUTS-2021.xlsx
# Generalitat de Catalunya open data (Socrata)
curl -sSL -o raw/cat/lloguer_municipi.csv "https://analisi.transparenciacatalunya.cat/api/views/qww9-bvhh/rows.csv?accessType=DOWNLOAD"
curl -sSL -o raw/cat/arees_referencia_habitatge.csv "https://analisi.transparenciacatalunya.cat/api/views/fftm-v9b6/rows.csv?accessType=DOWNLOAD"
echo "downloads complete"

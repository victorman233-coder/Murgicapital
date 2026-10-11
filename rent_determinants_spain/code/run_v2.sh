#!/bin/bash
# Pipeline for "Insiders and Outsiders in the Rental Market: Entry Rents, Incomes and Housing Supply in Spain" (paper_v2).
# Requires the inputs of run_all.sh up to a02 (d00_download.sh, d01_adrh.py, d02_build.py, a02_local_demand_supply.py)
# and the companion revision pipeline (population by country of birth, municipal boundaries in $WORK/raw/geo).
set -e
cd "$(dirname "$0")"
export WORK=${WORK:-/home/user/work}
bash d10_download_v2.sh              # Basque EMAL, Valencian deposits, Catalan seasonal leases, AEAT 2024 tables, MIVAU appraisals,
                                     # Aragón deposit microdata, INE migrations between municipalities, INE household budget survey
python d11_adrh_extra.py             # INE ADRH demographic indicators (household size, nationality) and income sources
python d12_rigidity_dem.py           # Copernicus DEM GLO-90: sea and slope >15% within 10/20 km of each municipality
python d13_build_v2.py               # municipal panels: EMAL, Valencian deposits, Catalan seasonal leases, AEAT by postal code, MIVAU
python d14_ld_instrument.py          # long-difference shift-share instrument for all municipalities
python d15_aragon.py                 # Aragón: municipal entry-rent index with street fixed effects; lease survival by cohort
python d16_epf.py                    # household budget survey: renters' rents, incomes and floor area by group, 2016-2024
python b03_aeat_entry_gap.py         # quality-adjusted entry gap 2024 (AEAT) by municipality
python e01_main.py                   # demand shock: entry gap, stock rents, income, household size; rigidity, tourism, spillovers, tenure
python e02_panels_regulation.py      # Catalan, Aragonese, Basque and Valencian panels; tourism bins; tensioned-zone cap and seasonal leases
python e03_inference.py              # shift-share inference: Rotemberg weights, randomisation inference, AKM0; origin placebo
python e04_panel_entry.py            # annual panel with year-varying shocks; sum-of-shares control; balance; leave-one-origin-out
python e05_extensions.py             # turnover, update-cap accounting, tourism threshold, heterogeneity, AEAT postal codes
python e06_flows.py                  # moves between municipalities 2021-2024: displacement and spillovers
python f03_v2_figures.py && python t02_v2_tables.py
cd ../paper_v2 && xelatex paper.tex && xelatex paper.tex

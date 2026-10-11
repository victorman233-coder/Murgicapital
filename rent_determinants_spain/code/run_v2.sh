#!/bin/bash
# Pipeline for "Insiders and Outsiders in the Rental Market: Entry Rents, Incomes and Housing Supply in Spain" (paper_v2).
# Requires the outputs of run_all.sh (d00_download.sh, d01_adrh.py, d02_build.py, a01-a04) and the companion revision pipeline
# (../../revision_JOPE-D-26-01206/code: population by country of birth, shift-share instrument, $WORK/replication_package,
# municipal boundaries in $WORK/raw/geo). Package versions: ../requirements-v2.txt.
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
python b01_affordability_tests.py    # insiders vs entrants: national INE indices, Catalan registers (b01_affordability.json)
python b02_gap_by_type.py            # rents of all leases vs incomes by municipality size (b02_gap_by_type.json)
python b03_aeat_entry_gap.py         # value-adjusted entry gap 2024 (AEAT) by municipality
python b04_cat_history.py            # Catalan new-lease rents 2007-2025 (base-year context)
python e01_main.py                   # demand shock: entry gap, stock rents, income, household size; rigidity, tourism, spillovers, tenure
python e02_panels_regulation.py      # Catalan, Aragonese, Basque and Valencian panels; tourism bins; tensioned-zone cap and seasonal leases
python e03_inference.py              # shift-share inference: Rotemberg weights, randomisation inference, AKM0; origin placebo
python e04_panel_entry.py            # annual panel with year-varying shocks; sum-of-shares control; balance; leave-one-origin-out
python e05_extensions.py             # turnover, update-cap accounting, tourism threshold, heterogeneity, AEAT postal codes
python e06_flows.py                  # moves between municipalities 2021-2024: displacement and spillovers
python e07_review.py                 # review analyses: gap in changes, windows, over-identification, weights, coast, value adjustment, WCR, tourism pre-trends
python e08_model_checks.py           # calibration of the stock-flow model with the turnover estimates
python f03_v2_figures.py && python t02_v2_tables.py
cd ../paper_v2 && xelatex paper.tex && xelatex paper.tex

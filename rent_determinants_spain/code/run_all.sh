#!/bin/bash
# Full pipeline for "What drives rents in Spain?": downloads -> data -> analyses -> tables/figures -> paper.
# Requires the companion revision pipeline for the population panel and instrument:
#   ../revision_JOPE-D-26-01206/code/r00_download.sh, r00_parse_ine_long.py, r01_build_pop_groups.py, r02_build_extended.py
set -e
cd "$(dirname "$0")"
export WORK=${WORK:-/home/user/work}
bash d00_download.sh                 # INE, Generalitat de Catalunya, ECB; INE income atlas (d01_adrh.py)
python lit_verify.py                 # bibliographic verification against Crossref (lit/crossref_verified.json)
python d02_build.py                  # municipal panel, Catalan quarterly panel, national and provincial series
python a01_facts.py                  # stock vs new leases, geography, common vs local variance
python a02_local_demand_supply.py    # long differences 2015-2024: population (IV), supply, income, tourism
python a03_tourism.py                # tourism collapse 2020-21 and recovery: IPVA and Catalan new leases
python a04_regulation.py             # Catalan tensioned-zone cap, provinces, cap on updates
python a05_investors_credit.py       # large-owner proxies, credit series (descriptive)
python a06_ranking.py                # ranking and decomposition, by municipality size
python f01_figures.py && python t01_tables.py
cd ../paper && xelatex paper.tex && xelatex paper.tex

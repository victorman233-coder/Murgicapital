#!/bin/bash
# Full revision pipeline: downloads -> data -> analyses -> tables/figures -> paper.
set -e
cd "$(dirname "$0")"
export WORK=${WORK:-/home/user/work}; export REP=$WORK/replication_package
bash r00_download.sh
python r00_parse_ine_long.py 33573 Municipios "País de nacimiento"
python r01_build_pop_groups.py          # 33 origin groups, 2003-2025, incl. national row
python r02_build_extended.py            # predetermined covariates, FUA/coast, Catalan policy zones
python r03_parse_eurostat.py            # inflows by country of birth into other European countries
python r10_diagnostics.py               # shocks, Rotemberg, overidentification, BHJ/AKM0, shock-level balance
python r11_ri.py                        # randomisation inference by strata and statistic
python r12_falsification.py             # pre-periods, placebos, local projections, JRS, stability, symmetry
python r13_specifications.py            # specification battery, exclusions, placebo shares
python r14_event_studies.py             # Colombia-Peru, Venezuela, Ukraine episodes; DiD-IV
python r15_alt_shocks.py                # Eurostat push shocks
python r16_margins.py                   # census decomposition, composition, register-cadastre, natives
python r17_het_catalonia.py             # pre-specified heterogeneity; Catalan new-contract validation
python r19_tables.py && Y0=2015 python r19_tables.py   # main table, full and arrival periods
python r20_figures.py && python r21_tex.py
python ../tests/test_revision.py
cd ../paper && xelatex paper_revised.tex && xelatex paper_revised.tex

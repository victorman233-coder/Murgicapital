# Revision of JOPE-D-26-01206: *Immigration, Rents and Housing Occupancy in Spain*

| File / folder | Content |
|---|---|
| `Informe_referee_y_plan_de_revision.md` | Referee-style report and revision plan (Spanish) |
| `Respuesta_al_informe_y_cambios.md` | What was done for each point of the report, results, data obtained and not obtained (Spanish) |
| `paper/paper_revised.pdf`, `paper/paper_revised.tex` | Revised manuscript; tables in `paper/tab`, figures in `paper/fig`, number macros in `paper/tab/numbers_rev.tex` |
| `code/` | Download script, data builders and analyses (`run_revision.sh` runs everything in order) |
| `config/specs.yaml` | Specification registry (central specification defined before estimation) |
| `out/` | JSON/CSV results read by the tables and the text |
| `tests/test_revision.py` | Automatic checks (instrument replication, BHJ equivalence, Rotemberg sum, accounting identity, shares) |

Raw downloads (~2.5 GB) are not stored in the repository; `code/r00_download.sh` fetches them from INE, Eurostat,
the Generalitat de Catalunya and Zenodo.

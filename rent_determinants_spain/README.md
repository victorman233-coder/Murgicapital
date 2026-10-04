# What Drives Rents in Spain? Demand, Supply, Tourism and Regulation across Municipalities

| File / folder | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | Manuscript. Sections: `sec_lit.tex` (literature) and `sec_theory.tex` (framework); tables in `paper/tab`; figures in `paper/fig`; number macros in `paper/tab/numbers.tex` |
| `paper_v2/paper.pdf`, `paper_v2/paper.tex` | Second paper, *Insiders and Outsiders in the Rental Market: Entry Rents, Incomes and Housing Supply in Spain*: stock-flow model of lease resets, quality-adjusted entry gap (AEAT 2024), shift-share IV on entry vs stock rents, incomes and household size, geographic supply constraints (Copernicus DEM), tourism, the Catalan cap, tenure and spillovers. Tables in `paper_v2/tab`, figures in `paper_v2/fig`; `code/run_v2.sh` runs its pipeline |
| `Resumen_v2.md` | Summary of the second paper in Spanish: results with their status (causal or descriptive), what is not established, new data, journals |
| `Propuesta_rediseno_asequibilidad.md` | Redesign proposal (Spanish): insiders vs outsiders and the entry-rent gap, falsification tests, verified open-data inventory, designs, and target journals |
| `Resumen_y_notas.md` | Summary in Spanish: results by determinant, what is identified and what is not, data obtained and not obtained, points for the author to check |
| `code/` | Downloads, data building, analyses, tables and figures (`run_all.sh` runs everything in order) |
| `lit/` | Candidate references and their verification against Crossref (`crossref_verified.json`) |
| `out/` | JSON results read by the tables and the text |

All inputs are downloaded from public sources:

- INE: IPVA by municipality, province and contract age; tourist dwellings; household income atlas; foreclosures; mortgage rates; CPI.
- Generalitat de Catalunya open data: new-lease deposits, tensioned-zone designation, tourism register, tourist-stay tax.
- ECB: Euribor.
- The companion paper's replication pipeline (`../revision_JOPE-D-26-01206`): population by country of birth, shift-share instrument, cadastre.

Additional sources for the second paper: Basque Government (EMAL new leases, 2016–2025), Generalitat Valenciana (lease deposits), Generalitat de Catalunya (seasonal leases), AEAT (new vs all leases by municipality and postal code, 2024), Ministry of Housing (appraised values), INE ADRH tables 30832 and 30825, Copernicus DEM GLO-90.

Raw files go to `$WORK/rent/raw` and are not stored in the repository.

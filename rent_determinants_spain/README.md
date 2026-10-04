# What Drives Rents in Spain? Demand, Supply, Tourism and Regulation across Municipalities

| File / folder | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | Manuscript. Sections: `sec_lit.tex` (literature) and `sec_theory.tex` (framework); tables in `paper/tab`; figures in `paper/fig`; number macros in `paper/tab/numbers.tex` |
| `Resumen_y_notas.md` | Summary in Spanish: results by determinant, what is identified and what is not, data obtained and not obtained, points for the author to check |
| `code/` | Downloads, data building, analyses, tables and figures (`run_all.sh` runs everything in order) |
| `lit/` | Candidate references and their verification against Crossref (`crossref_verified.json`) |
| `out/` | JSON results read by the tables and the text |

All inputs are downloaded from public sources:

- INE: IPVA by municipality, province and contract age; tourist dwellings; household income atlas; foreclosures; mortgage rates; CPI.
- Generalitat de Catalunya open data: new-lease deposits, tensioned-zone designation, tourism register, tourist-stay tax.
- ECB: Euribor.
- The companion paper's replication pipeline (`../revision_JOPE-D-26-01206`): population by country of birth, shift-share instrument, cadastre.

Raw files go to `$WORK/rent/raw` and are not stored in the repository.

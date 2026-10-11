# Insiders and Outsiders in the Rental Market — resumen para el autor

- **Manuscrito:** `paper_v2/paper.pdf` (32 páginas). Es la versión revisada tras la revisión multiagente; el detalle está en `Revision_multiagente.md`.
- **Código:** `code/run_v2.sh`.
- **Origen de las cifras:** todas proceden de `out/*.json` y pasan al texto a través de `paper_v2/tab/numbers.tex`.

## Contribución central

Gran parte del deterioro de la asequibilidad del alquiler en España recae en quien **entra** en el mercado. Los contratos duran al menos cinco años, las rentas en vigor se actualizan por el IPC o por un tope legal, y cada año termina entre el 12 % y el 19 % de los contratos. Por eso el índice oficial, que promedia todos los contratos, recoge los shocks de demanda tarde y solo en parte.

El artículo:
- formaliza esto en un modelo stock-flujo. Como solo reoptimizan los hogares que firman, la elasticidad que absorbe un shock es λη y no η;
- documenta la divergencia con la AEAT 2024, cuatro registros de fianzas y los índices del INE de contratos nuevos y existentes;
- estima la respuesta a shocks locales de demanda con un instrumento shift-share.

## Resultados y su estatus

| Resultado | Cifra | Estatus |
|---|---|---|
| Renta de todos los contratos (IPVA) frente a renta por unidad de consumo, 2015–2023 | +16,5 frente a +31,0 log-puntos; el ratio cae en los 703 municipios | Descriptivo, firme |
| Brecha de entrada INE (nuevos frente a existentes) | 2,3 (2021) → 12,7 (2024); se amplía en todas las provincias | Descriptivo, firme |
| Brecha ajustada por valor (AEAT 2024) | 15,9 log-puntos; positiva en el 99,5 % de 402 municipios; ≈ 18,4 frente a contratos existentes | Descriptivo, firme |
| Renta de entrada frente a ingresos: Cataluña y Aragón | +11,7 y +9,5 desde 2015; **+1,7 y +4,0 desde 2018** | Descriptivo, sensible al año base |
| País Vasco | La renta de entrada crece menos que la renta. Dentro de la región, la diferencia aumenta con la entrada: 0,65 (0,28) | Descriptivo |
| Rotación (fianzas de Aragón) | 17,4 % anual (rango 14,9–19,2 %); Zaragoza 14,9 %; duración mediana 3,8 años | Descriptivo, con salvedades |
| Esfuerzo mediano de los inquilinos (EPF, punto medio del intervalo) | 27,6 % (2016) → 25,4 % (2024); por encima del 40 %: 26 % → 18 % | Descriptivo |
| Shock → renta de entrada implícita | 0,83 [0,25; 2,21]; GMM por orígenes 0,45 (0,11) | Causal (IV); firme en signo y orden |
| Shock → renta de todos los contratos | 0,22 [−0,09; 0,62]; GMM 0,25 (0,06) | Causal (IV) |
| Shock → brecha de entrada (nivel 2024) | 0,57 [0,11; 1,74]; GMM 0,21; solo Colombia 0,06 | Causal (IV); **tamaño no robusto** |
| Brecha en cambios (índices provinciales) | 2015–2024: 0,13 (0,22); 2021–2024: 0,33 (0,14) | Positivo pero impreciso |
| Calendario: entrada reciente frente a antigua | No concluyente; las estimaciones puntuales van en contra del modelo | Declarado |
| Shock → renta por unidad de consumo; tamaño del hogar | 0,08 (no detectable); 1,26 [0,69; 2,51] | Causal (IV) |
| Shock → llegadas de españoles; salidas de españoles | −0,54 [−2,00; −0,14]; −0,01 (no detectable) | Causal (IV); compatible también con evitación nativa |
| Rigidez geográfica × shock → brecha | 0,49 (*p* = 0,021). No se separa de la costa; efecto en la media 0,12 | Débil |
| Turismo | Reasignación de contratos por encima de ~3 % de viviendas turísticas, pero con tendencias previas (*p* < 0,001) | **Descriptivo** |
| Topes de actualización 2022–23 | Como máximo el 58 % del ensanchamiento nacional | Contable (cota del efecto mecánico) |
| Tope catalán en zonas tensionadas | Cuota de contratos de temporada +1,8 pp; rentas −4 a −5 %; contratos −18 % (estudio compañero) | DiD, con tendencias previas en el número de contratos |
| Tenencia; efectos sobre las rentas de la periferia | Hay tendencias previas; efectos sobre las rentas de la periferia pequeños e imprecisos | No se sostienen |

## Qué cambió en la revisión

Lo principal; el detalle está en `Revision_multiagente.md`, §5:

- Tabla 1 corregida: había un error de escala.
- Supuesto explícito sobre la brecha de 2015, acotado entre el 15 % y el 31 %.
- Pruebas nuevas de identificación:
  - GMM por orígenes y estimaciones con un solo origen;
  - control por la entrada 2003–2014;
  - otros pesos y exclusión de provincias;
  - conjuntos Anderson-Rubin por bootstrap salvaje.
- Brecha medida en cambios con los índices provinciales y prueba de calendario.
- Turismo pasa a ser descriptivo.
- Rigidez geográfica junto con la costa.
- Modelo con λ en la ecuación de la renta de entrada y P4 derivada.
- Resumen, introducción y conclusiones con el alcance que permiten los datos.
- 13 referencias nuevas, verificadas en Crossref.

## Qué debe decidir el autor

1. **Enfoque del artículo.** Puede presentarse como artículo de medición con evidencia causal complementaria, más defendible con los datos actuales, o como artículo causal, que es el enfoque actual (`Revision_multiagente.md`, §7).
2. **Cita del artículo compañero.** «Unpublished manuscript» o «under review».
3. **Revisión independiente.** La revisión cruzada (fase 4) no fue independiente: los agentes se cortaron por el límite de gasto. Conviene una lectura editorial humana.
4. **Pipeline.** Relanzar el pipeline completo desde cero (`run_v2.sh`) para generar el manifiesto SHA-256 de las descargas.

## Revistas sugeridas

En orden de ajuste con la versión actual:
1. *Journal of Housing Economics*.
2. *Regional Science and Urban Economics*.
3. *Journal of Urban Economics*, si se consigue un panel de la brecha o fianzas enlazadas por vivienda.

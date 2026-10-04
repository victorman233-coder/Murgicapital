# Insiders and Outsiders in the Rental Market — resumen para el autor

Manuscrito: `paper_v2/paper.pdf` (16 páginas). Código: `code/run_v2.sh`. Todas las cifras proceden de `out/e01_main.json` y `out/e02_panels_regulation.json`, a través de `paper_v2/tab/numbers.tex`.

## Contribución central

El problema de asequibilidad del alquiler en España es un problema de **entrada**. Los contratos duran al menos cinco años y las rentas en vigor se actualizan por el IPC o por un tope legal. Por eso los shocks de demanda recaen sobre el precio del contrato nuevo y no sobre el de los inquilinos que ya tienen contrato.

El artículo:
- formaliza esto en un modelo stock–flujo con tres predicciones (P1: carga en la renta de entrada; P2: la renta por unidad de consumo no responde y el ajuste se hace por tamaño del hogar; P3: amplificación donde la oferta es rígida);
- mide la brecha de entrada ajustada por calidad con las estadísticas de la AEAT de 2024;
- estima la respuesta a shocks locales de demanda con un instrumento shift-share.

## Resultados y su estatus

| Resultado | Cifra | Estatus |
|---|---|---|
| Renta de los insiders (IPVA) frente a renta por unidad de consumo, 2015–2023 | +16,5 frente a +31,0 log-puntos; el ratio cae en los 703 municipios | Original, descriptivo |
| Contratos nuevos: Cataluña, renta frente a renta del hogar | +39,0 frente a +27,3 (brecha +11,7; en el 77 % de los municipios) | Nuevo, descriptivo |
| Contratos nuevos: País Vasco (€/m²) | +21,2 frente a +26,4 (solo el 10 % de los municipios empeora) | Nuevo, descriptivo: **la tesis no es universal** |
| País Vasco: shock de demanda → asequibilidad de los entrantes (€/m² frente a renta) | 1,23; intervalo AR [0,30; 3,10] | Causal (IV), panel regional: donde llega el shock, la entrada empeora también allí |
| Brecha de entrada ajustada por calidad (AEAT 2024) | 15,9 log-puntos de media; positiva en el 99,5 % de 402 municipios | Nuevo, descriptivo |
| Brecha provincial de contratos nuevos frente a todos | 2,3 (2021) → 12,7 (2024) | Descriptivo |
| Shock de demanda (+1 pp de población) → brecha de entrada | 0,57; intervalo AR [0,11; 1,74]; F = 11 | **Causal (IV)** |
| → renta de entrada implícita | 0,83 [0,25; 2,21] | Causal (IV) |
| → renta de todos los contratos | 0,22 [−0,09; 0,62], no significativo | Causal (IV), nulo |
| → renta por unidad de consumo / por persona | 0,08 / −0,09, no significativos | Causal (IV), nulo |
| → tamaño medio del hogar | 1,26 [0,69; 2,51] | Causal (IV) |
| Rigidez geográfica (suelo no urbanizable a 10 km, DEM Copernicus) × shock → brecha | 0,49 (p = 0,019); 0,48 (p = 0,003) neto de turismo | Causal con salvedades (F parcial 5,9) |
| Rigidez × shock → renta de todos los contratos o stock de viviendas | 0,03 y 0,02, nulos | Causal, nulo |
| Turismo × shock → brecha | −0,45 (p = 0,025) | Heterogeneidad |
| Umbral turístico (Cataluña, covid/recuperación) | Efectos en los contratos nuevos solo por encima del 3 % de viviendas turísticas | Cuasi-experimental |
| Tope de zona tensionada (Cataluña) | Cuota de contratos de temporada +1,8 pp; contratos regulares −14 % | DiD y event study |
| Canal de tenencia (PTI e hipotecas) | No se sostiene | Nulo |
| Spillovers del núcleo a la periferia de la FUA | La periferia construye más (0,37; p = 0,040); las rentas no se mueven | Forma reducida |

## Qué no está establecido (lo dice el texto)

1. **Corte transversal.** La brecha AEAT es de un solo año (2024). Su respuesta al shock supone que la brecha no estaba relacionada con el flujo previsto antes del shock. El test de pre-periodo sobre todos los contratos (−0,09) lo apoya, pero no lo prueba.
2. **Renta de los entrantes.** No se observa en datos abiertos. La renta del hogar es la de todos los hogares del municipio.
3. **Interacción débil.** La interacción de rigidez tiene un F parcial de 5,9. Por eso se reportan intervalos AR y la versión neta de turismo.
4. **Primera etapa sin ponderar débil** (F = 2,3). Los resultados principales ponderan por población, como en el artículo de inmigración.
5. **Composición en Cataluña.** La renta media de los contratos nuevos cae con el shock (−0,55) por efecto composición. Por eso el resultado central usa la brecha ajustada por calidad (renta por euro de valor de referencia catastral).

## Datos nuevos descargados (todos abiertos)

- **Eustat / Gobierno Vasco:** EMAL, contratos nuevos por municipio y barrio, 2016–2025.
- **Generalitat Valenciana:** depósitos de fianzas, 2020–2026.
- **Generalitat de Catalunya:** alquiler de temporada y saldos de altas y cancelaciones de contratos.
- **AEAT:** estadística de contratos nuevos frente a todos, por municipio y por código postal, 2024.
- **MIVAU:** valor tasado por municipio.
- **INE ADRH:** tablas 30832 (tamaño del hogar, nacionalidad) y 30825 (fuentes de renta).
- **Copernicus DEM GLO-90:** 93 teselas, con las que se calcula el suelo no urbanizable por municipio.

No se ha usado ningún dato con acceso restringido. Cuando una fuente devolvía 403, se buscó la alternativa abierta.

## Revistas sugeridas

En orden de ajuste: *Journal of Urban Economics*, *Regional Science and Urban Economics*, *Journal of Housing Economics*.

Para JUE convendría reforzar el panel de la brecha de entrada (AEAT por años si se publican más ejercicios) y obtener la renta de los entrantes. Para lo segundo habría que comprobar si los microdatos de libre descarga de la Encuesta de Condiciones de Vida (INE) permiten identificar a los hogares que acaban de firmar un contrato; no lo he verificado.

## Qué debe revisar el autor

- La redacción del texto, la declaración de IA (incluida tal como la pediste) y la afiliación.
- Si prefiere presentar el País Vasco como contraejemplo en la introducción, como ya se hace, o moverlo a robustez.
- Si quiere que la referencia al artículo de inmigración (Fernández-Aguilera 2026) figure como «unpublished manuscript» o como «under review».

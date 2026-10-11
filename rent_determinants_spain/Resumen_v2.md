# Insiders and Outsiders in the Rental Market — resumen para el autor

- **Manuscrito:** `paper_v2/paper.pdf` (24 páginas).
- **Código:** `code/run_v2.sh`.
- **Origen de las cifras:** todas proceden de los ficheros de `out/` (`e01_main.json`, `e02_panels_regulation.json`, `e03_inference.json`, `e04_panel_entry.json`, `e05_extensions.json`, `e06_flows.json`, `d15_aragon.json`, `d16_epf.json`). Pasan al texto a través de `paper_v2/tab/numbers.tex`.

## Contribución central

El problema de asequibilidad del alquiler en España es un problema de **entrada**. Los contratos duran al menos cinco años, las rentas en vigor se actualizan por el IPC o por un tope legal y cada año solo se renueva uno de cada seis contratos. Por eso los shocks de demanda recaen sobre el precio del contrato nuevo y sobre quién consigue entrar, no sobre los inquilinos que ya tienen contrato.

El artículo:
- formaliza esto en un modelo stock–flujo con cinco predicciones:
  - P1: la renta de entrada absorbe el shock y el índice de todos los contratos lo recoge al ritmo de la rotación λ;
  - P2: la renta por unidad de consumo no responde y el ajuste se hace por tamaño del hogar;
  - P3: amplificación donde la oferta y la reasignación son rígidas, con umbral turístico;
  - P4: los inquilinos instalados no se van; entran menos hogares de fuera;
  - P5: los topes de actualización amplían la brecha y los topes a la renta inicial la estrechan a costa de menos contratos regulados;
- mide la brecha de entrada ajustada por calidad con la AEAT 2024, por municipio y por código postal;
- mide la renta de entrada en cuatro registros de fianzas: Cataluña, Aragón (con efectos fijos de calle), País Vasco y C. Valenciana;
- estima la respuesta a shocks locales de demanda con un instrumento shift-share.

## Ampliación del marco teórico y de las conclusiones (tu sugerencia)

**Marco teórico (sección 4, ahora con seis apartados):**
- Brecha de estado estacionario: G* = (1−λ)(g−u)/λ.
- Velocidad a la que el índice de todos los contratos recoge el shock: 1−(1−λ)^k.
- Rotación endógena (*lock-in*): por qué el ajuste en cantidades recae en quienes no consiguen entrar.
- Topes de actualización con adelanto a la renta inicial (*front-loading*): k̄ ≈ 3,7 años.
- Incidencia: quién paga el shock.
- Cinco predicciones en lugar de tres.

**Conclusiones (cuatro párrafos):**
- Resumen de los hechos y del mecanismo.
- Tres implicaciones de política: medición de rentas a la firma, oferta dirigida al flujo de entrada, y diseño de la regulación.
- Dos extensiones de datos: fianzas enlazadas por vivienda y renta de los entrantes.

## Resultados y su estatus

| Resultado | Cifra | Estatus |
|---|---|---|
| Renta de los insiders (IPVA) frente a renta por unidad de consumo, 2015–2023 | +16,5 frente a +31,0 log-puntos; el ratio cae en los 703 municipios | Descriptivo |
| Esfuerzo mediano de los hogares inquilinos (EPF) | 27,6 % (2016) → 26,4 % (2024); los que pagan más del 40 % pasan del 25 % al 19 % | Descriptivo, confirma lo anterior |
| Contratos nuevos en Cataluña frente a la renta | +39,0 frente a +27,3 (en el 77 % de los municipios) | Descriptivo |
| Contratos nuevos en Aragón (índice con efectos fijos de calle) | +36,1 frente a +26,5 de renta y +15,1 del IPVA; Zaragoza +37,6 frente a +14,9 | **Nuevo**, descriptivo, ajustado por localización |
| Contratos nuevos en el País Vasco (€/m²) | +21,2 frente a +26,4 (solo el 10 % de los municipios empeora) | Descriptivo: **la tesis no es universal** |
| Brecha de entrada ajustada por calidad (AEAT 2024) | 15,9 log-puntos; positiva en el 99,5 % de 402 municipios | Descriptivo |
| La misma brecha por código postal (15 ciudades) | Positiva en el 99,4 % de 318 códigos; no depende del nivel de renta del barrio | Nuevo, descriptivo |
| Rotación (fianzas de Aragón) | El 19,2 % de los contratos termina cada año (Zaragoza 15,7 %); duración mediana de 3,3 años; peso de los contratos nuevos en el INE: 17,6 % → 12,3 % | Nuevo, descriptivo |
| Shock de demanda (+1 pp de población) → brecha de entrada | 0,57 [0,11; 1,74]; F = 11 | **Causal (IV)** |
| → renta de entrada implícita | 0,83 [0,25; 2,21] | Causal (IV) |
| → renta de todos los contratos | 0,22 [−0,09; 0,62] | Causal (IV), nulo |
| → renta por unidad de consumo; tamaño del hogar | 0,08 (nulo); 1,26 [0,69; 2,51] | Causal (IV) |
| → salidas de españoles hacia otros municipios (2021–24) | −0,01 [−0,40; 0,27] | **Nuevo**, causal (IV), nulo |
| → llegadas de españoles desde otros municipios | −0,54 [−2,00; −0,14] por 100 habitantes | **Nuevo**, causal (IV): el ajuste en cantidades también es de entrada |
| Rigidez geográfica × shock → brecha | 0,49 (p = 0,019); 0,48 (p = 0,003) neto de turismo | Causal con salvedades (F parcial 5,9) |
| Costa × shock → brecha | +0,59 (ee 0,23) | Heterogeneidad |
| Umbral turístico (Hansen) | 2,4 % de viviendas turísticas; intervalo 2,4–3,2 % para rentas; se rechaza una pendiente común (p < 0,01) | Cuasi-experimental (colapso covid) |
| Topes de actualización 2022–24 | Explican como máximo el 58 % del aumento de la brecha nacional, de 2,3 a 12,7 puntos | Contable (cota superior) |
| Tope de zona tensionada (Cataluña) | Cuota de contratos de temporada +1,8 pp; contratos regulares −14 % | DiD |
| Prima por m² de los inquilinos extranjeros (EPF) | De −3,0 % a +0,6 % (cambio +3,5; p = 0,08) | Descriptivo, evidencia débil |
| Canal de tenencia y efectos sobre las rentas de la periferia | No se sostienen | Nulos |

## Diagnóstico de la identificación (importante)

1. **Inferencia por permutaciones y AKM: no informativa.** En la diferencia larga solo hay una realización de 33 shocks de origen. Esos shocks tienen colas muy largas porque algunos orígenes eran pequeños en 2003. Al recentrar el instrumento permutando orígenes desaparece la primera etapa (F = 0,08), y los intervalos AKM no están acotados. En el artículo compañero, con panel anual, sí funcionaba.
2. **Consecuencia.** La identificación descansa en la exogeneidad de las cuotas de asentamiento de 2003. Tres orígenes acumulan el 84 % del peso de Rotemberg: Colombia, Perú y Rumanía. El texto lo dice así y cita a Goldsmith-Pinkham et al. y a Jaeger et al.
3. **Lo que aguanta:**
   - Con el control de suma de cuotas (Borusyak–Hull–Jaravel), la brecha queda en 0,64 [0,24; 3,64], con F = 5,6.
   - Quitando cualquiera de los cinco orígenes principales, el efecto está entre 0,56 y 0,96 y los intervalos excluyen el cero.
   - La cuota rumana de 2003 se asocia con un menor crecimiento previo de los alquileres (t = −4,4). Sin Rumanía, el resultado no cambia.
4. **Panel anual (Cataluña, Aragón y Valencia), donde los shocks varían cada año:**
   - Va en la misma dirección: entrada 0,53 frente a stock 0,00.
   - Es impreciso: p de aleatorización 0,08 para la entrada.
   - El instrumento del año siguiente predice el alquiler de este año (−1,34; ee 0,81): las series anuales de fianzas tienen mucho ruido.
   - Corrobora el signo, no la magnitud.
5. **Placebo con orígenes ricos.** El punto estimado va en la dirección esperada (−0,82 frente a 0,37), pero la primera etapa de esos orígenes es débil (F = 1,3).

## Otras salvedades (recogidas en el texto)

- La brecha de la AEAT es de un solo año (2024).
- La renta de los entrantes no se observa en datos abiertos. La EPF no identifica a quién se acaba de mudar.
- La interacción de rigidez tiene un F parcial de 5,9.
- Sin ponderar, la primera etapa es débil (F = 2,3).
- El ejercicio de los topes de actualización es contable. A escala provincial no se observa el desacoplamiento entre contratos existentes y nuevos que podría esperarse.
- El censo de 2021 (personas que se mudaron el año anterior) no se ha usado. Las estadísticas de migraciones del INE dan esa información año a año y por nacionalidad.

## Datos nuevos descargados (todos abiertos)

- **Gobierno de Aragón:** microdatos del registro de fianzas (recurso 100): 458.392 fianzas de vivienda desde 1996, con calle y estado de devolución.
- **INE, Estadística de Migraciones y Cambios de Residencia:** tablas 69743 y 69745.
- **INE, Encuesta de Presupuestos Familiares:** microdatos de 2016 a 2024 (23.274 hogares-año inquilinos).
- **Fuentes de la ronda anterior:** EMAL, fianzas de la GVA, temporada en Cataluña, AEAT por municipio y código postal, MIVAU, ADRH 30832/30825 y Copernicus DEM.
- **Referencias nuevas:** cuatro, verificadas en Crossref (Adão et al. 2019, Borusyak y Hull 2023, Hansen 2000, Jaeger et al. 2018).

No se ha usado ningún dato con acceso restringido.

## Revistas sugeridas

En orden de ajuste: *Journal of Urban Economics*, *Regional Science and Urban Economics*, *Journal of Housing Economics*.

Para JUE, la debilidad principal es la identificación por cuotas de asentamiento con pocos orígenes dominantes. Lo que más la reforzaría:
- fianzas enlazadas por vivienda, que permitirían medir el reajuste directamente;
- varios años de la estadística de la AEAT para tener un panel de la brecha.

## Qué debe revisar el autor

- La redacción, la afiliación y la declaración de IA (incluida tal como la pediste).
- El tono de la sección de identificación. He preferido decir abiertamente que la inferencia por permutaciones no es informativa en la diferencia larga.
- Si quiere que el artículo de inmigración (Fernández-Aguilera 2026) figure como «unpublished manuscript» o como «under review».

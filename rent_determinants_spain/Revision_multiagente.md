# Revisión multiagente de «Insiders and Outsiders in the Rental Market»

Este documento reúne los ocho entregables de la revisión:

| # | Entregable | Sección |
|---|---|---|
| 1 | Diagnóstico ejecutivo | §1 |
| 2 | Matriz priorizada, con estado final | §2 |
| 3 | Plan de revisión | §3 |
| 4 | Manuscrito revisado | §4 (ficheros) |
| 5 | Registro de cambios | §5 |
| 6 | Análisis adicionales | §6 |
| 7 | Dictamen editorial | §7 |
| 8 | Lista de comprobación final | §8 |

La §9 recoge lo que no se pudo verificar.

## 0. Método

**Fase 1, diagnósticos independientes.** Cinco agentes reales hicieron cada uno su diagnóstico sin leer los de los demás:

| Agente | Rol |
|---|---|
| A1 | Teoría y contribución |
| A2 | Econometría e identificación |
| A3 | Datos y reproducibilidad |
| A4 | Economía de la vivienda |
| A5 | Revisión editorial |

El primer intento de A1–A4 se cortó porque la organización alcanzó su límite de gasto de API (HTTP 429). Los relancé tras el reinicio del límite y reutilizaron sus cálculos parciales. A5 completó su diagnóstico en el primer intento.

**Fase 2, integración.** El coordinador integró los informes. Las discrepancias se resolvieron según la evidencia, no por mayoría.

**Fase 3, revisión.** El coordinador revisó el artículo en este orden:
1. Ciencia: análisis nuevos y corrección de cifras.
2. Argumentación: modelo, interpretación y alcance.
3. Lenguaje.

**Fase 4, revisión cruzada.** Lancé tres revisores cruzados:
- X1: teoría y vivienda.
- X2: econometría y datos.
- X3: editorial.

Los tres se cortaron al empezar por el mismo límite de gasto (HTTP 429) y no entregaron informe. El coordinador hizo la revisión cruzada siguiendo los mismos encargos. Las comprobaciones concretas están en la §8.

**Limitación.** La fase 4 no es independiente de la fase 3: la hizo la misma instancia que redactó los cambios. Conviene que el autor, o un revisor humano, repita al menos la lectura editorial.

**Estados de la matriz:**
- **H:** hecho y verificado.
- **H\*:** hecho, con verificación parcial.
- **P:** pendiente o decisión del autor.
- **R:** rechazado, con motivo.

## 1. Diagnóstico ejecutivo

**Qué aporta el artículo.**
- Una distinción útil y bien documentada. El índice oficial de alquileres de todos los contratos (IPVA) creció menos que la renta en los 703 municipios entre 2015 y 2023. Las rentas a la firma crecieron más que los contratos en vigor en todas las provincias desde 2021: la brecha nacional pasó de 2,3 a 12,7 log-puntos. En 2024 los contratos nuevos cuestan 15,9 log-puntos más por euro de valor catastral.
- Un modelo stock-flujo sencillo que explica por qué ocurre.
- Datos abiertos nuevos para España: AEAT 2024 por municipio y código postal, cuatro registros de fianzas y la rotación de contratos estimada con 458.392 fianzas de Aragón.

**Problemas críticos encontrados en la fase 1.**
- **C1. Error de escala en la Tabla 1:** ponía 1650 en lugar de 16,5.
- **C2. Nivel presentado como cambio.** La brecha es un nivel de 2024 que se interpretaba como crecimiento.
- **C3. Identificación frágil.** Descansa en las cuotas de asentamiento de 2003 de tres orígenes, desequilibradas en características observables. La inferencia por *shocks* no es informativa.

**Qué cambia tras la revisión.**
- **C1** está corregido, con un `assert` de rango en el código.
- **C2.** El supuesto sobre la brecha de 2015 se hace explícito y se acota: pesa entre el 15 % y el 31 % en la brecha de 2024. Se añade la brecha en cambios con los índices provinciales del INE. La respuesta es positiva pero imprecisa: 0,13 (ee 0,22) desde 2015 y 0,33 (ee 0,14) entre 2021 y 2024. La prueba de calendario no es concluyente.
- **C3.** Los análisis nuevos muestran dos cosas:
  - Que la renta de entrada responde más que la de todos los contratos es robusto en todas las especificaciones: 0,83 frente a 0,22 en el estimador base y 0,45 frente a 0,25 en el GMM por orígenes.
  - El tamaño de la respuesta de la brecha no lo es: va de 0,21 a 0,57, y es 0,06 con solo el componente colombiano.

  El artículo lo dice así en el resumen, la introducción, la §8 y la discusión.
- **Turismo.** Pasa a ser descriptivo porque hay tendencias previas (*p* < 0,001).
- **Geografía y costa.** No se pueden separar.
- **Hechos sensibles al año base.** Con base 2018, la diferencia catalana entre renta de entrada e ingresos es de 1,7 log-puntos y no de 11,7.

**Valoración global.**
- Lo que el artículo puede sostener con firmeza: los hechos, el mecanismo de medición y la dirección de las respuestas.
- Lo que no puede sostener: magnitudes causales precisas de la brecha, el efecto de la rigidez geográfica separado de la costa, y efectos del turismo.

## 2. Matriz priorizada con estado final

### Críticos

| ID | Localización | Problema | Agentes | Solución aplicada | Estado |
|---|---|---|---|---|---|
| C1 | Tabla 1, fila IPVA | Error de escala: 1650,0 y 1619,0 en lugar de 16,5 y −14,4 | A1, A3, A4, A5 | Código corregido, con `assert` de rango; la tabla y las macros salen de las mismas cantidades | H |
| C2 | Resumen; §1; §7–8; Tabla 2 | La brecha es un nivel de 2024; la «renta de entrada implícita» solo es un crecimiento si G₂₀₁₅ no está correlacionada con Z | A1, A2, A3, A5 | Ec. (4) y supuesto explícito con su cota (1−λ)⁹, 15–31 %. Prueba en cambios con índices provinciales (Tabla 7A). Ventanas 2015–19 frente a 2020–24 (Tabla 7B). Lenguaje de nivel | H (resultado: impreciso y no concluyente, declarado) |
| C3 | §6, §8; Tablas 6 y A1 | Identificación por cuotas de 2003 concentrada en tres orígenes, desequilibrios observables, sensibilidad a pesos y provincias | A2, A5 | Tabla A1 (Rotemberg, estimaciones por origen, balance). GMM con prueba J. Control Jaeger. Raíz de la población como peso; sin 28/08; sin 29; una provincia fuera cada vez. WCR-AR. Estimando definido. Fragilidad declarada en el resumen y la introducción | H |

### Altos

| ID | Problema | Solución aplicada | Estado |
|---|---|---|---|
| H1 | La ec. (4) no contenía λ | Nueva ec. (5) derivada: dr* = [d ln N + λα(·)]/(λη+σ+ε). Predicción sobre λ declarada y no contrastada. Comprobación entre ecuaciones (36–50 % frente a 27 % y 54 %) | H |
| H2 | P4 no se derivaba; *lock-in* inestable; signo de κ | Suelo λ_min; signo de κ empírico; márgenes de migración ζ, ξ, κ_O; la caída del peso del INE como compatible, no como prueba | H |
| H3 | «None move out», «incumbents stay» | «No detectable change»; alternativa de evitación nativa (Card 2001; Saiz y Wachter 2011); naturalizados | H |
| H4 | Geografía frente a costa; CRV1 | Interacción conjunta con la costa; CRV1; efecto en la media (0,12); umbral calculado (61 %); P3 en sentido débil | H |
| H5 | Turismo con tendencias previas; conjunto LR inválido; contradicción en el tramo 1–3 % | Estudio de eventos anual con prueba de Wald; turismo descriptivo; conjunto LR eliminado; contradicción corregida | H |
| H6 | Medida AEAT: renovaciones, personas físicas, incentivos fiscales, «quality», comparación con todos los contratos | «Value-adjusted»; cuatro salvedades; θ = 0; 0,5; 0,7; composición; ≈ 18,4 frente a existentes | H\* (las renovaciones no se pueden cuantificar con datos abiertos) |
| H7 | Año base 2015 en el mínimo del ciclo | Bases 2016 y 2018; ciclo catalán 2008–2023 | H |
| H8 | Tamaño del hogar inconsistente | Tamaño implícito por renta y número de hogares; composición frente a hacinamiento | H |
| H9 | Dependencia del artículo compañero | Instrumento descrito por completo; solapamiento declarado; código del instrumento en el paquete (declaración de datos) | H\* (el modo de citar el artículo compañero lo decide el autor) |
| H10 | Pipeline | `b02` recuperado; `b01`, `b02`, `b04`, `e07`, `e08` en `run_v2.sh`; `d10` robusto; manifiesto; `requirements-v2.txt` | H\* (no se ha relanzado el pipeline completo desde cero; ver §9) |
| H11 | Afirmaciones excesivas | Resumen, introducción, discusión y conclusión reescritos; implicaciones de política con su grado de respaldo | H |
| H12 | Literatura | 13 referencias añadidas, verificadas por DOI en Crossref, todas citadas | H |

### Medios

| ID | Problema | Estado |
|---|---|---|
| M1 | Unidades y cifras escritas a mano | H: log-puntos por punto porcentual; cifras del modelo, umbrales y medianas como macros; macros de valor absoluto para evitar dobles negativos |
| M2 | Rotación sensible a la fecha | H: fecha real de descarga, rango 14,9–19,2 %, cohortes antes y después de 2019, salvedades |
| M3 | EPF con renta exacta incompleta en 2024 | H: punto medio del intervalo en todos los años |
| M4 | Topes de actualización y tope catalán | H: cota mecánica; adelanto; IPC medio; 2024 sin efecto; cifras del tope catalán conciliadas |
| M5 | Panel anual | H: sin recorte; AR analítico; se retira «corroborates» |
| M6 | País Vasco | H: asociación dentro de la región, 0,65 (0,28) |
| M7 | Tenencia con tendencias previas | H: el canal no se puede aislar |
| M8 | Cuentas de población | H: se desligan población y flujos |
| M9 | Hechos institucionales | H\*: tope de 2022 ligado al IGC con negociación; IRAV como límite; temporada exenta en el periodo. El cambio de 2026 en Cataluña solo está verificado por fuentes secundarias (informe de A4) |
| M10 | Notación y ec. (1) | H: ρ en lugar de β; ec. (1) como aproximación; condición exacta de ensanchamiento |
| M11 | Notas de tablas | H: CRV1, WCR, tipo de F, muestras y unidades en todas las notas |
| M12 | Estructura redundante | H: §2 y §5 fusionadas; discusión y conclusión diferenciadas |
| M13 | Ventanas desalineadas en la asequibilidad de entrantes | H: fila alineada 0,90 [−0,16; 2,30] |

### Bajos

| ID | Problema | Estado |
|---|---|---|
| B1 | «Renewed» | H: no queda ninguna aparición |
| B2 | «48 provinces» | H: figura y nota de la Tabla 7 |
| B3 | «Tensioned» | H: «stressed (tensioned)» |
| B4 | Cita de la Fig. 3a | H |
| B5 | Macros sin usar | P: siguen en `numbers.tex`. Son inofensivas, y filtrarlas obligaría a que el generador de tablas leyera el texto |
| B6 | Orden de Borusyak; título en español | R: estilo autor-año correcto |
| B7 | «Rents top the list» | H: eliminado |
| B8 | «Every new lease is registered» | H: «must be deposited» |

### Rechazados o no adoptados

- **Exposición turística en 2019** (A5). La estadística del INE empieza en agosto de 2020. Se declara como limitación.
- **Cotas de Conley, Hansen y Rossi** (A2). Se sustituyen por pruebas más directas: J por origen, control Jaeger y balance. Quedan como propuesta (§6.2).
- **ECEPOV-2021** (A1). La disponibilidad del microdato no está verificada (§6.2).

## 3. Plan de revisión (orden seguido)

1. **Correcciones críticas de cifras.** C1, el recorte del panel (M5) y la covarianza CRV1 (H4). Relanzamiento de `e01`, `e04`, `e05` y `d16`.
2. **Análisis nuevos para C2, C3, H4–H8, M6 y M13.** `e07_review.py`, más `e08_model_checks.py` y `b04_cat_history.py` para el modelo y el año base.
3. **Generador de tablas.** Tablas 1–7, A1 y A2, y unas 500 macros. Sin cifras escritas a mano en el texto, salvo constantes de diseño (θ, ρ, umbrales de tamaño).
4. **Teoría.** H1, H2, M10 y la comprobación entre ecuaciones.
5. **Hechos, estrategia, resultados y robustez** con el alcance que permiten los análisis.
6. **Discusión, conclusión, resumen e introducción**, en ese orden, para que el resumen refleje lo que se sostiene.
7. **Lenguaje.** Unidades, signos, términos (B1–B8).
8. **Revisión cruzada y auditoría final** (§8).

## 4. Manuscrito revisado

- **PDF:** `paper_v2/paper.pdf` (32 páginas). **Fuente:** `paper_v2/paper.tex`.
- **Tablas:** `paper_v2/tab/` (t1–t7, tA1, tA2), generadas por `code/t02_v2_tables.py`.
- **Macros:** `paper_v2/tab/numbers.tex`.
- **Figuras:** `paper_v2/fig/`, generadas por `code/f03_v2_figures.py`.
- **Versión anterior** (como referencia): commit `ee034fc`, fichero `rent_determinants_spain/paper_v2/paper.tex`.

**Estructura nueva:**
1. Introducción.
2. Literatura.
3. Instituciones, datos y medición.
4. Modelo (siete apartados, con «Incidence and scope»).
5. Hechos.
6. Estrategia.
7. Resultados.
8. Robustez y límites de la identificación.
9. Discusión.
10. Conclusión.
11. Apéndice con dos tablas.

## 5. Registro de cambios

Cada fila indica el texto o la cifra original, el cambio, el motivo (ID de la matriz) y cómo se verificó. «Verificado» significa que la cifra se regeneró con el código y coincide con el JSON de `out/`; las cifras pasan al texto solo a través de `paper_v2/tab/numbers.tex`.

### Ciencia: cifras, estimación e identificación

| # | Localización | Original | Cambio | Motivo | Verificación |
|---|---|---|---|---|---|
| 1 | Tabla 1, fila IPVA | 1650.0 / 1619.0 (escala ×100 dos veces) | 16,5 / 31,0 / −14,4 | C1 | `assert` de rango en `t02`; coincide con `insR`, `insY`, `insGap` |
| 2 | Tabla 2 | AR analítico solamente; errores típicos sin corrección de muestra pequeña en las interacciones | Columna WCR-AR (bootstrap salvaje restringido, Webb, 4.999 réplicas); CRV1 en todas las especificaciones | C3, H4 | `e07` (`ar_wcr`); `e01` relanzado |
| 3 | Tabla 2, panel B | Solo tamaño del hogar del atlas | Tamaño implícito por renta (0,99) y número de hogares (−0,41) | H8 | `e07` (`households`) |
| 4 | Tabla 2, panel C | Asequibilidad de entrantes con ventanas desalineadas | Fila con rentas e ingresos en 2015–2023: 0,90 [−0,16; 2,30] | M13 | `e07` (`AE23`) |
| 5 | §8 y Tabla 6 (nueva) | Solo control de suma de cuotas y exclusión de orígenes | GMM con cuatro instrumentos por origen y prueba J; estimaciones con un solo origen; control por la entrada 2003–2014; raíz de la población como peso; sin Madrid y Barcelona; sin Málaga; exclusión de una provincia cada vez | C3 | `e07` (`overid_origin`, `robust`) |
| 6 | Tabla A1 (nueva) | Balance y Rotemberg citados sin tabla | Descomposición de Rotemberg completa, estimaciones por origen y balance | C3, M11 | `e03`, `e04`, `e07` |
| 7 | Tabla 7 (nueva), panel A | La brecha solo en niveles | Brecha en cambios con los índices provinciales del INE (2015–2024 y 2021–2024) | C2 | `e07` (`provincial_changes`) |
| 8 | Tabla 7, panel B | No existía | Entradas 2015–2019 frente a 2020–2024 | C2 | `e07` (`windows`) |
| 9 | Tabla 7, panel C (antes Tabla 5B) | Panel anual con recorte del resultado; solo conjunto de aleatorización | Sin recorte; AR analítico y conjunto de aleatorización; se retira «corroborates» | M5 | `e04` relanzado |
| 10 | Tabla 4 (rigidez) | Sin costa; sin corrección de muestra pequeña | Columnas con inflow × costa conjunto; fila de costa sola; efecto en la media de la restricción | H4 | `e07` (`geo_coast`), `e01` |
| 11 | Tabla 5, panel A (turismo) | Sin contraste de tendencias previas | Fila con el *p*-valor de la prueba de Wald 2014–2018 en el registro anual | H5 | `e07` (`tourism_annual`) |
| 12 | Tabla A2 (nueva) | Elasticidad del valor implícita = 1 | θ = 0; 0,5; 0,7; 1; composición del valor y de los m² | H6 | `e07` (`value_adjustment`) |
| 13 | Tabla A2, panel B | Solo año base 2015 | Años base 2016 y 2018 (Cataluña, Aragón) y ciclo catalán 2008–2023 | H7 | `e07` (`base_years`), `b04` |
| 14 | Tabla A2, panel C | País Vasco sin explicación | Asociación dentro de la región: 0,65 (0,28) | M6 | `e07` (`basque_within`) |
| 15 | §5, rotación | 19,2 % anual con edad = 2026 − cohorte; mediana 3,3 años | 17,4 % con la fecha real de descarga (rango 14,9–19,2 %); cohortes antes y después de 2019: 17,4 % y 17,4 %; mediana con meseta 3,8 años | M2 | `e05` relanzado |
| 16 | §5, EPF | Renta exacta (42 % de casos en 2024): 27,6 → 26,4 % | Punto medio del intervalo en todos los años: 27,6 → 25,4 %; > 40 %: 26 → 18 % | M3 | `d16` relanzado |
| 17 | §4 y §5, cifras del modelo | Escritas a mano: «between 4 and 7», «8 to 14», «a sixth», «half after four», k̄ = 3,7 | Macros desde `e08`: 4,2–7,1; 8,4–14,2; 12–19 %; 41–57 %; k̄ 3,5–5,3; peso de G₂₀₁₅ 15–31 % | M1, M10 | `e08_model_checks.json` |
| 18 | §7.1 | No existía | Cociente índice/entrada que implica el modelo con el calendario real de la entrada (36–50 %) frente a 27 % (2SLS) y 54 % (GMM) | H1 (comprobación entre ecuaciones) | `e08` |
| 19 | §7.3 | «only clearly positive above about 60 %» (a ojo) | Umbral calculado: 61 %, 66 municipios, 13 % de la población | M1 | `t02` (`rigThr`) |
| 20 | §7.5 | «18 %» frente a «−0,14 log» sin conciliar | Estudio compañero: −4,4/−5,0 % rentas, −18 % contratos (−19 % sin tendencia previa); Tabla 5B: −0,14 log en la ventana 2023–2025 | M4 | `a04`, `e02` |
| 21 | Pipeline | `b02` sin productor; `b01` fuera; `d10` sin `mkdir`; entorno sin fijar | `b02` recuperado (idéntico); `b01`, `b02`, `b04`, `e07`, `e08` en `run_v2.sh`; `mkdir -p`, `curl --fail`, manifiesto SHA-256; `requirements-v2.txt` | H10 | `b02` reproduce el JSON idéntico |

### Argumentación

| # | Localización | Original | Cambio | Motivo | Verificación |
|---|---|---|---|---|---|
| 22 | §4.1 | «The gap widens whenever entry rents grow faster than the update rule» | Condición exacta: Δr* − u > λG₋₁/(1−λ); ec. (1) como aproximación de primer orden | M10 | Álgebra comprobada por el coordinador (fase 4) |
| 23 | §4.1 | No existía | Ec. (4): brecha iterada; el peso de G₂₀₁₅ en G₂₀₂₄ es (1−λ)⁹ | C2 | Álgebra |
| 24 | §4.2 | Ec. (4) sin λ: dr* = [d ln N + α(·)]/(η+ε+σ) | Ec. (5) derivada del vaciado del flujo: dr* = [d ln N + λα(·)]/(λη+σ+ε); predicción sobre λ marcada como no contrastada | H1 | Derivación en el texto |
| 25 | §4.3 | λ = λ₀ − κG con κ > 0 | Suelo λ_min; signo de κ empírico (bloqueo del inquilino frente a incentivo del arrendador); la caída del peso del INE se presenta como compatible, no como prueba | H2 | — |
| 26 | §4.3, P4 | P4 no se derivaba | Márgenes de migración: d ln M = −ζ dr*, d ln O = ξλ dr* − κ_O dG | H2 | — |
| 27 | §4.4 | β como factor de descuento (choca con el coeficiente β) | ρ; rango de k̄; adelanto en topes permanentes frente a temporales | M10, M4 | — |
| 28 | §4.6 | «show only about a sixth» | «a share λ, 12–19 %»; arrendadores de inquilinos instalados renuncian a la renta de mercado; apartado de alcance del modelo | H2, M10 | — |
| 29 | §5 | Brecha como hecho general | Año base, recuperación cíclica, excepción vasca matizada | H7, M6 | Tabla A2 |
| 30 | §3.2 | Medida «quality-adjusted» | «value-adjusted»; cuatro salvedades (personas físicas, renovaciones, grupo de comparación, incentivos fiscales); ≈ 18,4 log-puntos frente a contratos existentes | H6 | `e08` (`gap_vs_existing`) |
| 31 | §6 | Instrumento citado del artículo compañero | Fórmula completa, fuentes, solapamiento declarado, estimando definido, supuesto de niveles frente a cambios | H9, C2, C3 | — |
| 32 | §7.2 | «Incumbents stay; the households who would have moved in do not» | «No detectable change»; alternativa de evitación nativa (Card 2001; Saiz y Wachter 2011); los naturalizados cuentan como españoles | H3 | — |
| 33 | §7.3 | Amplificación geográfica como resultado | No separable de la costa; efecto en la media nulo; P3 en sentido débil | H4 | Tabla 4 |
| 34 | §7.4 | Turismo como cuasi-experimento; «Below 3 % there is no reallocation» | Descriptivo; tendencias previas; corregida la contradicción del tramo 1–3 %; se elimina el conjunto LR (no válido con heterocedasticidad) | H5 | Tabla 5 |
| 35 | §7.5 | Cota de los topes sin matices | Cota del efecto mecánico; adelanto no incluido; IPC medio frente al del mes del aniversario; en 2024 el tope no ligaba | M4 | `e05` |
| 36 | §7.6 | «no break after 2022» | Hay tendencias previas en 2019–2020: el canal de tenencia no se puede aislar | M7 | Tabla 5C |
| 37 | §8 | «The panel corroborates the direction…» | El panel no contradice el signo y no informa del tamaño | M5 | — |
| 38 | §9–10 | Discusión y conclusión repetidas; política extrapolada | Discusión: lo que apoya, lo que no, alternativas, bienestar. Conclusión: implicaciones con su grado de respaldo | H11, M12 | Lectura del coordinador (fase 4) |
| 39 | Resumen e introducción | «problem of access», «does not respond», «none move out», seis resultados sin incertidumbre | Alcance acotado; dependencia de los orígenes; tres límites explícitos | H11, C2, C3 | Lectura del coordinador (fase 4) |

### Lenguaje y forma

| # | Localización | Original | Cambio | Motivo |
|---|---|---|---|---|
| 40 | Intro | «Rents top the list of economic concerns» | Eliminado | B7 |
| 41 | Intro | «every new lease is registered» | «leases must be deposited with a public agency» | B8 |
| 42 | Fig. 2 | «48 provinces» | «46 provinces … plus Ceuta and Melilla» | B2 |
| 43 | §5 | Fig. 3a citada para 14 municipios | Cita eliminada (la figura solo muestra Zaragoza) | B4 |
| 44 | Tablas 5B, Fig. 7 | «Tensioned-zone cap» | «Rent cap in stressed (tensioned) market areas» | B3 |
| 45 | Todo | Mezcla de % y log-puntos; dobles negativos («fell by −0,54») | Log-puntos por punto porcentual de entrada; macros de valor absoluto | M1 |
| 46 | §3 | §2 Instituciones y §5 Datos separados | Fusionados en «Institutions, data and measurement» | M12 |
| 47 | §3.1 | Tope de 2022 «at 2 %»; IRAV como regla; definición de temporada | IGC con negociación; IRAV como límite; temporada exenta en el periodo, cambiada en 2026 | M9 |
| 48 | Bibliografía | 27 referencias | 40; 13 añadidas tras comprobar su DOI en Crossref | H12 |

### Cambios de la revisión cruzada (fase 4)

| # | Localización | Original (versión de la fase 3) | Cambio | Motivo |
|---|---|---|---|---|
| 49 | §7.1 | «Both are compatible with the model» | Las dos estimaciones (27 % y 54 %) quedan a ambos lados del rango del modelo (36–50 %); los intervalos no permiten distinguirlas | Precisión |
| 50 | §7.1 | «the rest is offset by fewer arrivals of other residents» | Se desligan las cuentas de población (0,82) y los flujos 2021–2024 | M8 |
| 51 | §2 | «official indices built on sitting tenants» (Crone et al. 2010) | «official rent indices have understated rent growth» | Atribución prudente |
| 52 | Intro y §9 | «tourism and regulation act»; «quantities adjust at entry»; «to a large extent» | «appear to act»; «appear to adjust» | H11 |
| 53 | §9 | «consistent with each prediction of the model» | Coherente con P1, P2 y P4; P3 y P5 más débiles; el calendario no se cumple | H11 |
| 54 | §9 | Recuperación cíclica como alternativa sin más | Se añade que el mecanismo stock-flujo implica la asimetría en ambas direcciones; hecho central reformulado con los dos hechos medidos | Coherencia |
| 55 | §8 | «the rest comes from origins with small weights» | Incluye los pesos negativos: «the other origins, several of them with small weights…» | Precisión |
| 56 | Tabla 7, nota | «48 provinces» | «the 46 provinces of the common tax regime plus Ceuta and Melilla» | B2 |

## 6. Análisis adicionales

### 6.1 Ejecutados en esta revisión

Todos se ejecutaron con el código del repositorio. Los resultados están en `out/e07_review.json`, `out/e08_model_checks.json` y `out/b04_cat_history.json`, y pasan al texto como macros. Unidades: log-puntos por punto porcentual de entrada, salvo indicación.

| # | Pregunta | Método y supuestos | Datos | Resultado | Interpretación |
|---|---|---|---|---|---|
| 1 | ¿La brecha responde también en cambios, no solo en el nivel de 2024? (C2) | 2SLS provincial. Supuesto: la media provincial ponderada del instrumento municipal conserva su validez | Índices INE de contratos nuevos y existentes, base 2015 (tabla 59005), 48 provincias | Cambio 2015–2024: 0,13 (0,22); con log población 0,39 (0,27); sin pesos 0,30 (0,32). Cambio 2021–2024: 0,33 (0,14), *p* = 0,027 | Positivo pero impreciso y menor que en niveles municipales |
| 2 | ¿La brecha de 2024 responde sobre todo a la entrada reciente, como predice el modelo? (C2) | 2SLS con dos endógenas e instrumentos por ventana. Supuesto: los dos instrumentos son separables | Ídem principal | Brecha: 1,70 (1,06) a la entrada de 2015–2019 y 0,09 (0,77) a la de 2020–2024; correlación de instrumentos 0,94 | No concluyente; las estimaciones puntuales van en contra del calendario del modelo |
| 3 | ¿Los orígenes que dan peso al instrumento dan el mismo efecto? (C3) | GMM en dos etapas con cuatro instrumentos (Colombia, Perú, Rumanía, resto) y prueba J; 2SLS con un solo origen. Supuesto: exogeneidad de las cuotas de cada origen | Ídem | Brecha: GMM 0,21 (0,11), J *p* = 0,12; solo Colombia 0,06; solo Perú 0,15; solo Rumanía 0,46. Renta de entrada: GMM 0,45 (0,11). Todos los contratos: GMM 0,25 (0,06) | El orden entrada > todos los contratos es robusto; el tamaño de la respuesta de la brecha no lo es |
| 4 | ¿Confunde el instrumento la entrada actual con la pasada? (C3) | Control por la entrada 2003–2014 (Jaeger et al. 2018) | Padrón | Brecha 0,59 [0,13; 1,76] | Sin cambio |
| 5 | ¿Dependen los resultados de los pesos o de provincias concretas? (C3) | Raíz de la población como peso; exclusión de 28 y 08; exclusión de 29; exclusión de una provincia cada vez | Ídem | Raíz: 0,73 [0,00; 4,06]; sin 28/08: 0,53 [−0,07; 3,06]; sin 29: 0,43 [0,00; 1,41]; rango 0,43–0,75 | La brecha es frágil en inferencia; la renta de entrada excluye el cero en todos los casos |
| 6 | ¿La amplificación es geográfica o costera? (H4) | 2SLS con tres endógenas: entrada, × restricción, × costa | DEM GLO-90, indicador costero | Geografía 0,70 (0,44), *p* = 0,12; costa −0,59 (0,78); costa sola 0,59 (0,23) | No separables |
| 7 | ¿Depende la brecha de la elasticidad del valor? ¿Cambia la composición? (H6) | θ ∈ {0; 0,5; 0,7; 1}; regresión del valor relativo y de los m² relativos | AEAT 2024 | 0,71; 0,64; 0,61; 0,57. Composición: valor 0,15 [−0,40; 0,58]; m² 0,22 [−0,51; 0,57] | Robusto |
| 8 | ¿Inferencia robusta con pocos *clusters*? (C3) | AR por bootstrap salvaje restringido (Webb, 4.999 réplicas) | Ídem | Brecha [0,10; 1,54]; renta de entrada [0,30; 2,04]; asequibilidad de entrantes [0,00; 1,68] | Similar al AR analítico |
| 9 | ¿Son coherentes tamaño del hogar, renta por hogar y renta por persona? (H8) | 2SLS con resultados derivados | Atlas de renta | Tamaño implícito 0,99 [0,60; 1,75]; número de hogares −0,41 [−1,65; 0,19] | Inconsistencia moderada; composición frente a hacinamiento no separable |
| 10 | ¿Tendencias previas en turismo? (H5) | Estudio de eventos anual 2014–2025 por tramo de exposición y prueba de Wald conjunta 2014–2018 | Registro catalán anual, 274 municipios | Contratos: *p* < 0,001 en los tres tramos. Rentas: 0,08; 0,035; < 0,001 | Turismo pasa a ser descriptivo |
| 11 | ¿Por qué el País Vasco no muestra la divergencia? (M6) | MCO dentro de provincia | EMAL, atlas de renta | 0,65 (0,28), n = 64 | El mecanismo opera dentro de la región |
| 12 | ¿Depende la divergencia del año base? (H7) | Crecimiento hasta 2023 desde 2015, 2016 y 2018; ciclo 2008–2023 | Registros catalán y aragonés | Cataluña: 11,7 / 8,1 / 1,7; Aragón: 9,5 / 6,9 / 4,0. Cataluña: −19,7 entre 2008 y 2015 | Mucha divergencia es recuperación cíclica |
| 13 | ¿Cuadra el modelo con las magnitudes? (H1) | Calibración con el rango de λ y el calendario real de la entrada nacional | e05, padrón | Cociente índice/entrada: 36–50 % según el modelo; 27 % (2SLS) y 54 % (GMM) observados | Compatible; no discrimina |
| 14 | ¿Sensibilidad de la rotación a la fecha de referencia? (M2) | Edad desde la fecha real de descarga; tres convenciones; cohortes antes y después de 2019 | Registro aragonés | 17,4 % (14,9–19,2 %); 17,4 % y 17,4 % por cohortes | Rango λ = 0,12–0,19 |
| 15 | ¿Esfuerzo con renta comparable entre años? (M3) | Punto medio del intervalo de ingresos | EPF 2016–2024 | 27,6 → 25,4 %; > 40 %: 26 → 18 % | La conclusión no cambia; las cifras sí |

### 6.2 Propuestos y no ejecutados

| # | Pregunta | Método | Datos necesarios | Por qué no se ejecutó |
|---|---|---|---|---|
| P1 | ¿Responde más la brecha donde λ es menor? (la predicción más distintiva) | Interacción de la entrada con la rotación municipal | Rotación por municipio: hoy solo en Aragón | Faltan datos |
| P2 | Brecha medida directamente sobre la misma vivienda | Enlace de fianzas sucesivas por inmueble | Microdatos de fianzas con identificador de vivienda (los registros los tienen, no son públicos) | Faltan datos |
| P3 | Asequibilidad de los entrantes con su propia renta | Cruce de contratos nuevos con IRPF del inquilino | Microdatos AEAT | No son públicos |
| P4 | Cotas de sensibilidad a la exclusión (Conley, Hansen y Rossi 2012) | Intervalos bajo violaciones acotadas de la exclusión | Ídem principal | Sustituido por pruebas más directas (J, Jaeger, balance); la elección de la cota de violación sería arbitraria. Referencia no añadida a la bibliografía |
| P5 | Movilidad residencial por tenencia | ECEPOV-2021 | Microdatos ECEPOV | Disponibilidad no verificada |
| P6 | Exposición turística previa a 2020 | Viviendas turísticas en 2019 | Registro turístico municipal 2019 | La estadística del INE empieza en agosto de 2020; registros autonómicos no verificados |

## 7. Dictamen editorial

**Versión original: rechazo con invitación a reenviar** (dictamen de A5 en la fase 1). Motivos:
- el error de escala de la Tabla 1;
- un nivel presentado como cambio;
- una identificación más frágil de lo que el texto admitía;
- afirmaciones de política no respaldadas.

**Versión revisada: revisión mayor** para una revista de campo (*Journal of Housing Economics*, *Regional Science and Urban Economics*). Para el *Journal of Urban Economics*, todavía no.

**Por qué ya no es un rechazo:**
- Los hechos descriptivos son sólidos y nuevos.
- El modelo es coherente y produce una predicción propia (el papel de λ).
- El texto declara con honestidad lo que la identificación no permite.

**Debilidades que un evaluador seguirá señalando, por orden de importancia:**
1. **Magnitud de la respuesta de la brecha.** Depende de qué orígenes identifican el efecto: 0,06 con Colombia, 0,21 con GMM y 0,57 en el estimador base. Los índices provinciales en cambios dan 0,13 (ee 0,22).
2. **Un solo año de la brecha a nivel municipal.** La prueba de calendario no es concluyente, y sus estimaciones puntuales van en contra del modelo.
3. **La predicción más distintiva, la del papel de λ, no se contrasta.** Faltan datos de rotación por municipio.
4. **Buena parte de la divergencia entre renta de entrada e ingresos es recuperación cíclica.** Con base 2018, Cataluña pasa de 11,7 a 1,7 log-puntos.
5. **Amplificación geográfica y turismo.** La geografía no se separa de la costa, y el turismo es solo descriptivo.

**Qué cambiaría el dictamen:**
- varios años de la estadística AEAT de contratos nuevos, que permitirían un panel de la brecha;
- fianzas enlazadas por vivienda;
- rotación municipal en al menos dos registros.

Con cualquiera de los dos primeros, el artículo podría aspirar a una revista general de economía urbana.

**Decisión que corresponde al autor: cómo enfocar el artículo.**
- **(a)** Como artículo de medición y hechos, con el modelo y la parte causal como evidencia complementaria. Es más defendible con los datos actuales. Exige reordenar: §5 pasaría a ser el núcleo y §7–8 se acortarían.
- **(b)** Como artículo causal, tal como está ahora. Es más ambicioso, pero un evaluador insistirá en la fragilidad del tamaño de la respuesta.

La revisión actual mantiene (b), con la fragilidad declarada. No he cambiado el enfoque porque es una decisión científica del autor.

## 8. Lista de comprobación final (auditoría de la fase 5)

| Comprobación | Resultado |
|---|---|
| El PDF compila sin errores, sin referencias ni citas indefinidas y sin cajas desbordadas | Sí (xelatex, dos pasadas; 0 *overfull*) |
| Todas las cifras del texto proceden de macros generadas desde `out/*.json` | Sí, salvo constantes de diseño (θ = 0,5/0,7; ρ = 0,96; umbrales). Comprobado con búsqueda de decimales en `paper.tex` |
| No hay macros duplicadas | Sí (`sort \| uniq -d` vacío) |
| La Tabla 1 tiene la escala correcta | Sí, con `assert` de rango |
| Cada referencia está citada y cada cita tiene referencia | Sí: 40/40 |
| Las referencias nuevas tienen DOI verificado en Crossref | Sí: las 13 se volvieron a consultar en la fase 5 (`lit/crossref_review_additions.json`). Autores, revista, volumen y páginas coinciden. Salvedades: Goodman y Kawai solo traen la página inicial; Sá figura como 2014 en Crossref (publicación en línea) y en el volumen 125 (2015) |
| Los componentes por origen suman el instrumento principal | Sí: correlación 1,000 y cociente mediano 1,000 (comprobado en la fase 4) |
| La prueba de Wald de tendencias previas usa la covarianza alineada con los coeficientes | Sí (comprobado en la fase 4) |
| Las afirmaciones de significación coinciden con las tablas | Revisado en la fase 4: AR que incluyen o tocan el cero (raíz de la población, sin Málaga, sin 28/08, asequibilidad de entrantes) descritos como tales |
| No quedan dobles negativos («fell by −») | Sí (búsqueda en el texto compilado) |
| No quedan términos retirados («quality-adjusted», «renewed», «corroborates», «48 provinces», «problem of access») | Sí; «quality» solo aparece en «rather than quality-adjusted» |
| Resumen, introducción y conclusión coherentes con los resultados | Sí, tras las correcciones 49–56 |
| `run_v2.sh` incluye todos los productores de ficheros que lee `t02` | Sí (`b01`–`b04`, `e01`–`e08`, `d15`, `d16`) |
| Pipeline completo relanzado desde cero en un entorno limpio | **No** (ver §9) |
| Cambios confirmados y subidos a la rama | Sí (ver el último commit) |

## 9. Lo que no se pudo verificar

- **Revisión cruzada independiente (fase 4).** Los tres agentes se cortaron por el límite de gasto. La hizo el coordinador, que también redactó los cambios, así que no es independiente.
- **Pipeline completo desde cero.** Se relanzaron:
  - las estimaciones afectadas: `e01`, `e04`, `e05`, `e07`, `e08`, `b04`, `d16`;
  - las tablas y las figuras.

  No se relanzaron desde cero las descargas (`d10`) ni la construcción de datos (`d11`–`d15`). El manifiesto SHA-256 se genera en la próxima descarga completa.
- **Hechos institucionales.**
  - Los 140 municipios catalanes de marzo de 2024 solo los confirma una fuente secundaria.
  - El cambio de régimen de los contratos de temporada en Cataluña (2026) está verificado solo en parte; el estatal (octubre de 2026) sí está verificado.
  - Fuente de ambos: informe de A4 con identificadores del BOE.
  - El alcance del IRAV según la fecha del contrato no está verificado. El texto solo dice que es un límite.
- **Contenido de las referencias.** Las atribuciones de la §2 se basan en el conocimiento de los trabajos citados, no en una relectura de los textos durante esta revisión. Los DOI sí están verificados. La frase sobre Crone et al. (2010) se suavizó por prudencia.
- **Medida AEAT.** No se puede cuantificar qué parte de los «contratos nuevos» son renovaciones con el mismo inquilino, ni el efecto de los incentivos fiscales de la Ley 12/2023 sobre las rentas declaradas.
- **Rotación.** No hay forma de separar, con datos abiertos, las fianzas no devueltas de los contratos realmente vigentes.

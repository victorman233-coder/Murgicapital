
## 15. Diseño econométrico principal

**Estimando:** el efecto de un shock exógeno de demanda local sobre la brecha de entrada y sobre la asequibilidad de entrada, frente a su efecto sobre la asequibilidad de los incumbentes.

**Ecuación principal** (diferencias largas, mercado i dentro de la provincia p, ventana 2015/16–2023/24):

ΔY_i = β · ΔPob_i + X_i'γ + δ_p + ε_i, instrumentando ΔPob_i con la llegada predicha shift-share Ẑ_i [P].

La variable dependiente ΔY se estima para cinco resultados con la misma primera etapa:

| Resultado | Coeficiente |
|---|---|
| (a) Δln R* (alquiler de entrada) | β_entrada |
| (b) Δln R̄ (alquiler de stock) | β_stock |
| (c) Δln Ỹ (renta por unidad de consumo) | β_renta |
| (d) ΔG = (a) − (b) | β_G |
| (e) ΔA^E = (a) − (c) | β_A = β_entrada − β_renta |

**Elementos del diseño:**
- **Unidad de observación:** el municipio, con errores agrupados por provincia. Robustez: áreas urbanas funcionales (sección 21).
- **Tratamiento:** la entrada de nacidos en el extranjero acumulada en relación con la población. Robustez: crecimiento total de la población instrumentado.
- **Supuesto de identificación:** la exogeneidad de los shocks nacionales por origen (Borusyak, Hull y Jaravel 2022) condicional a los controles predeterminados.
- **Inferencia:** AKM/BHJ e inferencia por aleatorización, ya implementadas en el artículo compañero.
- **Amenazas:**
  - correlación de las cuotas de 2003 con tendencias locales de demanda (ya tratada en el compañero con controles predeterminados);
  - instrumento débil fuera de los municipios grandes (F = 5,2 sin ponderar [P]);
  - composición de las fianzas (F7) → usar €/m² o celdas de tamaño.

**Interacción (mecanismo M2):** ΔY_i = β ΔPob_i + θ (ΔPob_i × Rig_i) + κ Rig_i + …, con los instrumentos Ẑ_i y Ẑ_i × Rig_i. Rig_i debe ser predeterminada y geográfica o de planeamiento, no la densidad, que es endógena a la demanda histórica (F6).

**Unidad geográfica y datos:**
- **Fase 1:** Cataluña (fianzas con superficie, si el inventario lo confirma) y las comunidades con fianzas comparables (sección 13), complementadas con SERPAVI para los niveles.
- **Fase 2:** las 48 provincias con la brecha del INE (59005), para validación externa con un diseño de exposición.

## 16. Diseños alternativos

1. **Panel anual con impulso-respuesta** sobre G_it (proyecciones locales, Jordà): la teoría predice que el efecto es inmediato en R* y se difunde a R̄ a un ritmo λ. Estimar λ implícita y compararla con los pesos del INE (17,6% en 2021 → 12,3% en 2024 [P]).
2. **Turismo** (M3):
   - Reutilizar el diseño COVID [P] con la brecha de entrada como resultado.
   - Añadir no linealidad: exposición por tramos (0–1%, 1–3%, 3–8%, >8%) y splines.
   - Añadir interacciones con rigidez y con presión migratoria.
   - Umbral estimado por máxima verosimilitud de ruptura (Hansen) con inferencia por bootstrap.
3. **Regulación de actualizaciones (M5):**
   - Diferencia en diferencias nuevo/existente × 2022–23 con exposición provincial a la inflación de actualización (cuota de contratos con aniversario en el pico del IPC).
   - Alternativa: comparar la evolución de G en Cataluña antes y después de abril de 2022.
4. **Tenencia (M4)**, solo si supera las pruebas de tendencias previas:
   - Exposición al shock de tipos medida como hipotecas por cada 1.000 hogares en 2019–2021 (INE, provincia) o como precio/renta en 2021.
   - Resultado: la brecha de entrada y el número de contratos nuevos.
5. **Regulación de entrada (M6):** el DiD apilado de la ZMRT [P], reutilizado con ΔG y con la composición del contrato (superficie, tramo de renta) como resultados.

## 17. Tests de identificación

- **Primera etapa:** F efectivo de Montiel Olea–Pflueger; pesos de Rotemberg; equivalencia BHJ en el nivel de los shocks [P].
- **Balance:** de los shocks por origen sobre características predeterminadas (renta, edad, vivienda vacía y tasa de construcción de 2011) [P].
- **Exclusión:** el shock no debe predecir los ingresos por unidad de consumo antes de la llegada (2015 sobre 2016–2023).
- **Monotonía en λ:** el efecto sobre R̄ debe crecer con el horizonte y el efecto sobre G debe decrecer.
- **Para la ZMRT y la regulación:** tendencias previas por cohorte, ajuste lineal (ya hecho [P]) y Rambachan–Roth.

## 18. Placebos

1. **Brecha de entrada antes del boom migratorio:** el shock de 2016–2023 no debe predecir ΔG de 2012–2015, con fianzas anuales desde 2005 en Cataluña.
2. **Shock migratorio de orígenes «ricos»** (UE-15, Reino Unido, Alemania): la predicción es menor traslado al alquiler de entrada por unidad de población, porque su composición de ingresos es mayor (ω alto).
3. **Turismo:** el primer trimestre de 2020 como placebo [P] (−0,14; p = 0,32); los municipios sin viviendas turísticas como placebo de la recuperación.
4. **ZMRT:** efectos sobre municipios no designados de comarcas distintas (falso tratamiento).
5. **Tipos:** shock de tipos sobre el stock (IPVA), que no debe moverse en el corto plazo [N] (lo confirma F8).

## 19. Robustez

- Denominadores alternativos:
  - renta por unidad de consumo (media y mediana);
  - renta por persona;
  - por hogar, solo para mostrar el sesgo por *doubling up*;
  - renta de los deciles bajos de la ADRH (distribución, si existe en tabla municipal);
  - salario (AEAT por municipio, si está disponible).
- Alquiler por m² y con superficie fija; celdas de tamaño.
- Muestras:
  - excluir Madrid y Barcelona;
  - excluir los municipios con ZMRT a partir de 2024;
  - sin ponderar y ponderando por inquilinos de 2011.
- Ventanas 2015–2019 (antes de los topes) y 2019–2024.
- Inferencia por aleatorización de orígenes y AKM0 [P].

## 20. Heterogeneidad

Preespecificada:
- tamaño (5 clases) [N: el gradiente de A^E va de +5,8 a +20,1 en Cataluña];
- núcleo frente a periferia de área urbana funcional;
- costa frente a interior;
- tramos de exposición turística;
- cuartiles de rigidez de oferta;
- cuota de alquiler en 2011 (profundidad del mercado);
- cuota de renta de origen extranjero.

Por tipo de hogar (con microdatos de ECV/EPF, por comunidad autónoma):
- jóvenes de menos de 35 años;
- nacidos en el extranjero;
- primer quintil de renta.

## 21. Spillovers

- **Unidad de mercado:** área urbana funcional (Eurostat/GISCO, correspondencia LAU–FUA ya descargada [P]), con la distinción núcleo/periferia.
- **Diseño:** el shock del núcleo (Ẑ_núcleo) sobre la brecha de entrada y la población de la periferia, controlando por el shock propio de la periferia:
  ΔG_periferia = β_propio Ẑ_propio + β_núcleo Ẑ_núcleo + …
- **Flujos de población:** la Estadística de Variaciones Residenciales del INE (origen–destino municipal, sección 13) permite medir si el shock del núcleo expulsa residentes hacia la periferia. El *gravity* de esos flujos sirve como peso del shock vecino (W·Ẑ).
- **Controles contaminados:** los vecinos tratados indirectamente no se usan como control puro. Se estima el efecto total del área (FUA) y la descomposición directo/indirecto.
- **Evidencia previa [P]:** los spillovers a contiguos son pequeños e imprecisos (0,06; ee 0,07), con el IPVA como resultado. Con la brecha de entrada, la predicción es mayor.

## 22. Figuras

| # | Contenido | Datos | Estado |
|---|---|---|---|
| 1 | Δln alquiler frente a Δln renta (unidad de consumo) por municipio, 2015–2023, con los nuevos contratos en Cataluña superpuestos | IPVA, fianzas, ADRH | Factible ya [N] |
| 2 | Índice nuevo frente a existente (España e INE por provincia; Cataluña con fianzas) | INE 59004/59005; fianzas | Ya existe [P] (fig. 1) |
| 3 | Esfuerzo de entrada (12·R*/Y) y de stock a lo largo del tiempo | Fianzas, SERPAVI, ADRH | Factible en Cataluña [N] |
| 4 | Brecha de entrada por provincia, 2021–2024; Cataluña 2005–2025 | INE, fianzas | Factible ya |
| 5 | Shock de demanda (IV) sobre R*, R̄, Ỹ y A^E | Instrumento [P] | Por estimar sobre fianzas armonizadas |
| 6 | Efecto marginal del shock por cuartil de rigidez | Rigidez (sección 13) | Requiere datos nuevos |
| 7 | Turismo: estudio de eventos de la brecha de entrada y no linealidad por tramos | [P] + extensión | Factible |
| 8 | Shock de tipos × exposición | Pendiente de una exposición válida | Hoy fallido (F8) |
| 9 | Regulación: G antes y después del tope del 2% y de la ZMRT | INE, fianzas | Factible |
| 10 | Spillovers núcleo → periferia (FUA) | EVR, FUA | Requiere EVR |

## 23. Tablas

1. Estadísticos descriptivos (municipio, FUA, provincia).
2. Alquiler e ingresos por tipo de municipio [N: ya calculado en `out/b02_gap_by_type.json`].
3. Shocks de demanda y alquiler (entrada, stock).
4. Shocks de demanda e ingresos (por persona, por unidad de consumo, por hogar) [N: F5].
5. Shocks de demanda y A^E, A^I, G.
6. Heterogeneidad por rigidez de oferta.
7. Turismo (colapso, recuperación, umbrales).
8. Tenencia y tipos (o, si el diseño falla, una tabla honesta de exposiciones probadas y sus tendencias previas).
9. Regulación (tope de actualización, ZMRT: precio, cantidad, composición).
10. Robustez y medidas alternativas de asequibilidad.

## 24. Nueva estructura del paper

1. **Introducción:** la paradoja del insider/outsider.
2. **Instituciones y medición:** contratos, duración, indexación y topes; qué mide cada índice; la identidad del índice.
3. **Hechos:** la asequibilidad de los insiders mejora en todas partes y la de entrada empeora; el gradiente por tamaño [N].
4. **Modelo:** stock-flow con reset, ingresos y composición; predicciones.
5. **Datos:** fianzas armonizadas, SERPAVI, ADRH, INE e instrumento.
6. **Estrategia empírica:** IV shift-share sobre G y A^E; interacción con la rigidez.
7. **Resultados principales:** traslado de la demanda a la entrada y a los ingresos.
8. **Mecanismos:** rigidez de oferta; turismo (reasignación en la entrada).
9. **Extensiones:** regulación de la actualización y de la entrada.
10. **Spillovers metropolitanos.**
11. **Discusión:** bienestar, insiders y outsiders, política.
12. **Conclusión.**

Apéndice: la descomposición contable con inflación, el ranking antiguo, los grandes propietarios y los tipos.

## 25. Nuevo título

**«Insiders and Outsiders in the Rental Market: Entry Rents, Incomes and Housing Supply in Spain»**

Alternativa: «The Rising Cost of Entering the Rental Market: Evidence from Spain».

## 26. Nuevo abstract (borrador; las cifras marcadas [por estimar] dependen de los diseños pendientes)

> Spanish tenants who stay in their homes have seen rents grow more slowly than their incomes: between 2015 and 2023 the official index of rents on all leases rose by 17 log points and median income per consumption unit by 31, and the gap narrowed in every one of the 703 municipalities covered. Households entering the market faced the opposite. In Catalonia, where every new lease is registered, rents on new contracts rose by 40 log points, 13 more than median income per consumption unit, in almost nine out of ten municipalities, and 20 points more in Barcelona. We build a stock-flow model with long leases, indexed updates and rent resets in which demand shocks are absorbed at entry, and show that [por estimar: an exogenous immigration-driven demand shock widens the entry-rent gap by X and raises entry rents relative to incomes by Y, more where land is scarce]. Tourism shocks operate through the same entry margin, and caps on updates widen the gap while caps on new contracts narrow it at the cost of fewer leases. The rental affordability problem in Spain is a problem of access, not of tenure.

## 27. Nueva introducción (estructura y primer párrafo)

**Primer párrafo propuesto:**

> In Spain, rents are at the top of public concern, yet the average rent paid by tenants has grown no faster than their incomes. Between 2015 and 2023 the official rent index, which covers all leases in force, rose by 17 log points, while median household income per consumption unit rose by 31; in none of the 703 municipalities with an official index did rents outpace incomes. The rent faced by households signing a new lease tells a different story: in Catalonia, it rose 13 log points more than income, and the gap between new and existing leases widened by about 22 points. This paper argues that the Spanish rental affordability problem is a problem of entry.

**Párrafos siguientes:**
1. Por qué ocurre: los contratos largos, la indexación y los topes trasladan el ajuste al reset.
2. Qué hacemos: la medición, el modelo y la identificación.
3. Resultados (por estimar).
4. Contribución frente a la literatura: Genesove (2003); Ambrose, Coulson y Yoshida (2015); Diamond, McQuade y Qian (2019); Autor, Palmer y Pathak (2014); Saiz (2010); Hsieh y Moretti (2019); Barron, Kung y Proserpio (2021).
5. Política.

## 28. Claims que sí pueden sostenerse hoy

1. [D] Para los contratos vigentes, el alquiler creció menos que la renta mediana por unidad de consumo en todos los municipios con IPVA entre 2015 y 2023 [N].
2. [D] En Cataluña, la ratio alquiler-de-entrada/renta (por unidad de consumo) subió unos 13 puntos (2015–2023) y la de stock/renta bajó unos 9; la brecha de entrada se abrió unos 22 puntos [N].
3. [D] La brecha nuevo/existente se abrió en todas las provincias entre 2021 y 2024 (media simple 9,4 puntos, ponderada 10,2; rango 3,6–14,6) [N].
4. [C] El shock migratorio eleva el alquiler de stock (0,41–0,50) sin respuesta del stock de vivienda [P][N].
5. [C] El turismo actúa en el margen de entrada: el colapso bajó el alquiler de entrada y subió el número de contratos; la recuperación los revirtió [P].
6. [C] El tope de la ZMRT redujo el alquiler de entrada (≈5%) y el número de contratos firmados (≈18% en la primera oleada) [P].
7. [D] El tope del 2% mantuvo el índice de stock por debajo del IPC (cota superior del 6%) [P].

## 29. Claims que NO deben hacerse

1. «El alquiler se ha descolgado de los ingresos en España». Falso para los insiders [N].
2. «La inmigración empeora la asequibilidad». No identificado: el efecto sobre la renta por hogar es positivo por *doubling up* y el efecto por unidad de consumo es impreciso [N].
3. «La rigidez de oferta amplifica el efecto». No demostrado: los proxies actuales dan el signo contrario (F6).
4. «Los tipos de interés empujaron hacia el alquiler y subieron las rentas». No identificado; el diseño de exposición probado falla (F8).
5. «Los fondos explican la subida». Sin evidencia [P].
6. «El tope reduce la oferta de vivienda». Reduce los contratos depositados, que no es lo mismo [P].
7. «La inflación explica el problema». Es contabilidad [P].
8. Cualquier cifra de esfuerzo «de los inquilinos» calculada con la renta de todos los hogares sin advertirlo.

## 30. Resultados que serían realmente novedosos

1. **β_G > 0 con β_stock pequeño y β_renta ≈ 0:** la demanda se traslada a la entrada y no a los ingresos de los entrantes. Es evidencia causal de un mercado insider/outsider; no conozco una estimación así para Europa.
2. **Que la brecha de entrada responda al tope de la actualización:** la regulación pro-insider desplaza el ajuste a los outsiders. Es novedoso y relevante para la política.
3. **Un umbral turístico en la brecha de entrada.**
4. **Una medida de rigidez de oferta para municipios españoles** con validación (respuesta del stock al shock) y su interacción con la asequibilidad de entrada.
5. **El sesgo del denominador:** la asequibilidad por hogar mejora mecánicamente con el *doubling up*, lo que vincula con el resultado del artículo compañero.

## 31. Resultados que serían solo descriptivos

- Las ratios y gradientes por tamaño (F1–F3, F9).
- Cualquier comparación nacional de índices.
- La relación MCO entre brecha y llegada de población.
- Grandes propietarios.
- Las series de tipos sin exposición válida.

## 32. Revistas razonables (sin garantías)

| Escenario | Nivel razonable |
|---|---|
| **Solo hechos (F1–F4, F9) + modelo + turismo y ZMRT ya identificados** | Buen paper descriptivo-causal en revistas de campo: *Journal of Housing Economics*, *Regional Science and Urban Economics*, *Journal of Regional Science*, *SERIEs*, *Papers in Regional Science* |
| **+ IV de la brecha de entrada (β_G, β_A) con fianzas de ≥3 comunidades, ajustadas por superficie, e inferencia shift-share sólida** | Contribución fuerte de economía urbana: *Regional Science and Urban Economics*, *Journal of Economic Geography*, *Real Estate Economics*; con suerte, *Journal of Urban Economics* |
| **+ reset real en la misma vivienda (fianzas enlazadas), ingresos de los entrantes (microdatos), rigidez de oferta validada y tope de actualización como experimento** | Potencial internacional: *Journal of Urban Economics*, *AEJ: Economic Policy*; general interest solo si el mecanismo insider/outsider se generaliza más allá de España |

**Qué falta para subir de nivel:**
1. Fianzas armonizadas fuera de Cataluña, con superficie.
2. Ingresos de los entrantes, no la media del municipio.
3. Una medida de rigidez exógena.
4. La observación del reset en la misma vivienda, que requiere acceso administrativo.
5. Inferencia shift-share robusta con pocos orígenes dominantes, ya trabajada en el compañero.

## 33. Qué parte del proyecto tiene mayor valor científico

**[I] El hecho insider/outsider y su explicación estructural** (contratos largos e indexados → reset). Tres razones:
1. Es nuevo como hecho cuantificado con datos administrativos.
2. Reinterpreta el debate español: el índice oficial «no ve» la crisis porque mide a los insiders.
3. Genera predicciones causales nítidas (β_G) que los diseños existentes del paper (shift-share, COVID turístico, ZMRT, tope del 2%) pueden contrastar con un único resultado común.

El mayor riesgo es de datos: la armonización de fianzas fuera de Cataluña y los ingresos de los entrantes.

---

## Próximos pasos concretos (en orden)

1. Armonizar las fianzas de las comunidades confirmadas (sección 13): Cataluña + las que tengan municipio × año, número de contratos y renta, idealmente €/m².
2. Construir R* por m² (o en celdas de tamaño) y Ỹ por unidad de consumo (ADRH), y A^E, A^I y G por municipio y año.
3. Reestimar el IV shift-share sobre (a)–(e) y reportar β_A = β_entrada − β_renta con inferencia AKM y AR.
4. Construir la rigidez de oferta predeterminada (SIU/Catastro/MDT) y estimar la interacción.
5. Reutilizar los diseños de turismo y ZMRT con G como resultado.
6. Probar exposiciones alternativas al shock de tipos. Si fallan las tendencias previas, apéndice.
7. Spillovers FUA con EVR.

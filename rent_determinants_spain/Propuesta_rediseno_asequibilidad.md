# Propuesta de transformación del artículo
## De «What Drives Rents in Spain?» a un artículo sobre la brecha entre alquiler e ingresos de quien entra al mercado

**Etiquetas usadas en todo el documento** (regla 14):
- **[P]** resultado del paper original;
- **[N]** evidencia nueva obtenida en esta revisión con datos abiertos (scripts `code/b01_affordability_tests.py`, resultados en `out/b01_affordability.json` y `out/b02_gap_by_type.json`);
- **[I]** inferencia económica;
- **[H]** hipótesis por contrastar;
- **[C]** resultado causal;
- **[D]** resultado descriptivo.

> **Advertencia previa.** Antes de proponer nada intenté falsar con los datos ya descargados la hipótesis que plantea el encargo: *«los alquileres, sobre todo los de nuevos contratos, crecieron más que los ingresos de los hogares que necesitan entrar al mercado, y más donde la oferta no responde»*. El resultado obliga a **reformularla**. La propuesta parte de lo que sobrevive a esa prueba, no de la historia previa.

---

## 0. Lo que dicen los datos antes de rediseñar nada: pruebas de falsación

| # | Prueba | Resultado | Tipo |
|---|---|---|---|
| F1 | ¿Creció el alquiler medio de todos los contratos (IPVA) más que la renta de los hogares, 2015–2023? | **No.** IPVA +17,2 log-puntos frente a renta neta por hogar (ADRH) +29,0 y por persona +31,4. La ratio alquiler-de-stock/renta **cayó** entre 12 y 14 puntos. | [N][D] |
| F2 | ¿Ocurre en algún tipo de municipio lo contrario? | **No.** En los 703 municipios con IPVA, el alquiler de stock creció menos que la renta mediana por unidad de consumo; ningún municipio tiene brecha positiva. La caída es menor en las grandes ciudades: −19,5 puntos en municipios de 10.000–20.000 habitantes y −7,9 en los de más de 500.000. | [N][D] |
| F3 | ¿Y los nuevos contratos? (Cataluña, 123 municipios, fianzas, 2015–2023) | **Sí.** Alquiler de nuevos contratos +39,7; IPVA +18,0; renta mediana por unidad de consumo +27,0. La ratio nuevo-contrato/renta **sube** 12,7 puntos (en el 87% de los municipios) y la de stock/renta **baja** 9,0. La brecha de entrada se abre 21,6 puntos. Por tamaño, la ratio de entrada sube +5,8 en municipios de 10.000–20.000 habitantes y +20,1 en Barcelona. Con renta por hogar: +12,0 y −9,7. | [N][D] |
| F4 | España, índice INE por antigüedad del contrato | Nuevos contratos +17,6 log-puntos entre 2021 y 2024; existentes +7,2; IPC +14,3. Entre 2021 y 2023, nuevos +9,2 frente a una renta por hogar de +12,4: a escala nacional, la divergencia de los nuevos contratos solo aparece con el salto de 2024 (+8,8%), año para el que aún no hay renta ADRH. | [N][D] |
| F5 | Shock de demanda (shift-share) sobre alquiler y renta, diferencias largas 2015–2023 | Alquiler de stock: 0,50 (AR [0,05; 1,09]). Renta por persona: 0,11 (AR [−0,40; 1,29]). Renta mediana por unidad de consumo: −0,03 (AR [−0,48; 1,05]). Renta por hogar: **1,37** (AR [0,70; ∞)). La brecha alquiler−renta cambia de signo según el denominador: +0,52 por unidad de consumo frente a −0,87 por hogar. F (primera etapa) = 9,1. | [N][C] para el alquiler; ingresos imprecisos |
| F6 | Shock de demanda × rigidez de oferta (proxies disponibles) | La densidad **reduce** el efecto sobre el alquiler (−0,13 por d.t., p = 0,047), al contrario de lo previsto. La vacancia de 2011 no interactúa (0,00). La tasa de construcción previa no interactúa con el alquiler (−0,12, p = 0,40), pero sí aumenta la respuesta del stock (+0,32, p = 0,12). | [N]; amplificación no demostrada |
| F7 | Shock de demanda sobre el alquiler de nuevos contratos en Cataluña | **Negativo** (−1,14; AR [−2,76; −0,40]; n = 123). La fianza media no está ajustada por calidad ni tamaño: la llegada de hogares de menor renta desplaza la composición hacia viviendas más baratas. No es un test válido sin ajuste por composición. | [N]; amenaza de composición |
| F8 | Tipos hipotecarios: shock 2022–23 × proporción de propietarios con hipoteca en 2011 | IPVA: sin ruptura (2022–24 ≈ 0). Nuevos contratos en Cataluña: −1,1% por d.t. (signo contrario al previsto), y el número de contratos tiene tendencia previa (−4,8%, p < 0,001). **La exposición no identifica el canal.** | [N]; diseño fallido |
| F9 | Provincias: la brecha de entrada (nuevo − existente) 2021–2024 frente a la entrada de nacidos en el extranjero 2021–2024 | La brecha media es de 10,2 puntos (rango 3,6–14,6) y se asocia con la llegada de población (0,78; p = 0,005; MCO, 48 provincias). | [N][D] |
| F10 | Brecha de entrada en niveles, 2024 (AEAT, estadística de viviendas declaradas en el IRPF: nuevos contratos frente al total, 402 municipios de más de 20.000 habitantes) | En España, 816 €/mes en contratos nuevos frente a 729 € en el total; rentabilidad bruta del 6,8% frente al 5,7%. Brecha media ponderada: bruta 13,9 log-puntos (positiva en el 100% de municipios); por m² 16,3 (98,8%); **ajustada por calidad** (alquiler por euro de valor de referencia catastral) 15,9 (99,5%). Las viviendas que entran tienen menor valor de referencia (145.067 € frente a 154.022 €): la composición juega en contra de la brecha, no a favor. | [N][D] |
| F11 | Shock de demanda (IV shift-share, 2016–2024) sobre la brecha de entrada de 2024 (AEAT) | Brecha bruta **0,57** (AR [0,15; 1,40]); por m² 0,26 (AR [−0,19; 1,12]); ajustada por calidad **0,43** (AR [−0,04; 1,27]); alquiler de stock 0,46 (AR [0,10; 0,80]). F = 20,0; n = 402. El alquiler de entrada responde aproximadamente el doble que el de stock (0,46 + 0,43 frente a 0,46), aunque la versión ajustada por calidad aún no excluye el cero. | [N][C], preliminar |
| F12 | Correlatos de la brecha ajustada (MCO, dentro de provincia) | Municipios de la primera oleada ZMRT: −4,3 puntos (p = 0,008); dentro de Cataluña −3,5 (p = 0,09). Exposición turística +0,27 por punto (n.s.). Densidad n.s. | [N][D] |

**Conclusión de las pruebas [I]:**
1. **No existe una divergencia generalizada alquiler–renta.** Para los inquilinos que ya están dentro, el alquiler creció menos que la renta local en todos los municipios.
2. **La divergencia existe en la entrada.** Es grande, se amplía con el tamaño de la ciudad y se abre sobre todo desde 2022.
3. **El denominador importa.** Con la renta por hogar, un shock migratorio parece *mejorar* la asequibilidad: con más adultos por hogar sube la renta del hogar sin que suba la de cada persona. Es el mismo margen de hacinamiento que documenta el artículo compañero.
4. **Con los proxies disponibles no se ve amplificación por rigidez de oferta.** Hacen falta medidas de rigidez mejores (sección 13).

5. **Con datos nacionales (AEAT 2024), el shock de demanda abre la brecha de entrada** (F11): es la primera prueba causal a favor del mecanismo, aún imprecisa una vez se ajusta por calidad. La regulación del reset (ZMRT) se asocia con una brecha menor (F12).

Por tanto, la hipótesis del encargo se sostiene **solo para los hogares que entran**, y sobre esa base se construye la propuesta.

---

## 1. Diagnóstico del artículo actual

**Lo que funciona:**
- La distinción entre stock de contratos y contratos nuevos [P], con la identidad del índice.
- Un instrumento de demanda con primera etapa razonable y sin tendencias previas [P][C].
- Un diseño de turismo con predicción de signo opuesto en precio y cantidad [P][C].
- Una evaluación del tope catalán con controles limpios [P][C].
- El reconocimiento honesto de los shocks comunes [P].

**Lo que falla como contribución:**
1. **La pregunta es una colección.** «¿Qué determina el alquiler?» lleva a un ranking heterogéneo de factores de naturaleza distinta.
2. **El factor número uno del ranking es contable.** La inflación vía indexación ocupa el primer puesto y no responde a ninguna pregunta económica sobre asequibilidad.
3. **La variable dependiente es la equivocada para la pregunta social.** El IPVA promedia contratos antiguos indexados; por construcción infravalora lo que paga quien entra.
4. **Falta el denominador.** No hay ingresos en la variable dependiente; la renta aparece solo como regresor descriptivo.
5. **Ningún diseño explica por qué la brecha es mayor en unos mercados que en otros**, que es la pregunta que de verdad interesa.

## 2. Qué debe conservarse

| Elemento | Nuevo papel |
|---|---|
| Modelo stock-flow e identidad del índice (ec. 5) | Núcleo teórico, ampliado con la renta y el *reset* (sección 7) |
| Distinción nuevo/existente (INE 59004/59005/59008; fianzas) | Variable dependiente central |
| Instrumento shift-share de inmigración | Shock de demanda principal |
| Diseño del colapso turístico 2020–21 | Segundo shock de demanda, específico del margen de entrada |
| Tope catalán (ZMRT) con DiD apilado | Extensión: qué ocurre cuando se regula el *reset* |
| Tope del 2% a las actualizaciones | Extensión: protección de incumbentes y traslado del ajuste a la entrada |
| Catastro y respuesta nula del stock | Mecanismo de oferta (respuesta de cantidad) |
| Varianza común frente a local | Motivación: por qué la brecha difiere entre mercados pese a shocks comunes |

## 3. Qué debe eliminarse o relegarse

| Resultado actual | Clasificación | Destino |
|---|---|---|
| «La inflación explica toda la subida nominal del IPVA» | D. Descomposición contable | Sección de medición o apéndice; sirve para deflactar |
| Tope del 2%: −5,9 puntos | D (cota superior) | Mecanismo de medición: por qué el stock no refleja el mercado |
| Elasticidad de 0,41 del IPVA a la inmigración | A, pero con otra variable | Se reestima sobre la brecha de entrada |
| Respuesta nula del catastro | B. Mecanismo | Se mantiene (oferta) |
| Turismo: colapso y recuperación en nuevos contratos | A/B | Mecanismo y prueba de que el ajuste ocurre en la entrada |
| Turismo: efecto nacional medio casi nulo | C. Auxiliar | Se sustituye por umbrales y heterogeneidad |
| Tope ZMRT: −5% precio, −18% contratos | B/extensión | Se mantiene, ampliado a cantidad y composición |
| Renta: asociación MCO 0,08 | E. Descriptivo | Se elimina como «determinante»; la renta pasa al denominador |
| Grandes propietarios (ejecuciones, sociedades en el registro turístico) | E | Apéndice, con advertencia |
| Euríbor | E | Apéndice, salvo que prospere el diseño de la sección 16 |
| Ranking de «contribuciones» | F | Eliminar; se sustituye por una descomposición de la brecha |
| Variación entre provincias (63%) | C | Motivación |

## 4. Nueva pregunta de investigación

> **¿Por qué en España el coste de entrar al mercado de alquiler se ha separado de la capacidad de pago de los hogares, mientras el coste de quienes ya están dentro no lo ha hecho, y por qué esa brecha es mucho mayor en unos mercados que en otros?**

En inglés: *Why did the cost of entering the Spanish rental market diverge from household incomes while incumbent tenants' costs did not, and why is this divergence so much larger in some markets than in others?*

## 5. Nueva hipótesis central

**[H] La asequibilidad del alquiler en España no se ha deteriorado de forma general. Se ha deteriorado para quien entra.**
- Con contratos largos (RDL 7/2019), actualizaciones indexadas y, después, topadas (2022–2024), el ajuste del mercado a los shocks de demanda se concentra en el **reset** del alquiler al cambiar de inquilino.
- Donde la oferta no responde y el shock de demanda es mayor (grandes ciudades, mercados turísticos), la renta de entrada se separa de los ingresos de los entrantes, mientras la de los incumbentes sigue a la inflación.
- El resultado es un mercado de **insiders y outsiders**.

**Predicciones falsables:**
- **H1.** La ratio renta de entrada / ingreso sube, y la ratio renta de stock / ingreso no sube.
  - Estado: sostenida en Cataluña 2015–2023 [N] y, de forma incipiente, en España 2021–2024 [N].
- **H2.** Un shock de demanda exógeno aumenta la brecha de entrada (log nuevo − log existente) más que el alquiler de stock.
  - Por contrastar [H]. Indicio descriptivo provincial en F9.
- **H3.** El efecto de H2 es mayor donde el *turnover* es mayor antes del shock (más resets) y donde la oferta es más rígida.
  - Por contrastar [H]. Con los proxies actuales no se observa amplificación (F6).
- **H4.** Las reglas que protegen al incumbente (topes a la actualización) amplían la brecha de entrada; las que limitan el reset (topes a nuevos contratos) la reducen a costa de la cantidad.
  - Parcialmente contrastable [P][H].
- **H5.** El shock de demanda no eleva los ingresos por unidad de consumo en la misma proporción.
  - Indicio [N]: β por unidad de consumo ≈ 0, pero con intervalo amplio.

## 6. Nueva contribución

**[I]** La contribución con más potencial es **B: «The rising cost of entering the rental market»**, reformulada como **«Insiders and outsiders in the rental market»**.

1. **Medición.**
   - Se muestra que el indicador oficial (stock) y la percepción social (entrada) divergen por una razón estructural (ec. 5), no por error de medida.
   - Se cuantifica con datos administrativos que la brecha de entrada se abrió unos 22 puntos en ocho años en Cataluña (2015–2023) y unos 10 puntos en tres años en las provincias españolas (2021–2024) [N].
2. **Causalidad.**
   - Se identifica que los shocks de demanda, migratorio y turístico, se trasladan sobre todo a la renta de entrada, y que la rigidez de oferta y la regulación de actualizaciones determinan cuánto.
   - Es el núcleo causal y aún está **por estimar** sobre la variable nueva.
3. **Política.**
   - Los topes a la actualización y las prórrogas protegen al insider y desplazan el ajuste a la entrada.
   - Los topes a la entrada reducen la brecha, pero también la cantidad [P].

**Comparación de las siete contribuciones posibles:**

| Contribución | Novedad | Identificación con datos abiertos | Potencial | Papel |
|---|---|---|---|---|
| A. Divergencia alquiler–renta en España | Media; además, falsa para los insiders (F1–F2) | Descriptiva | Bajo como tesis general | Hecho motivador, reformulado |
| **B. El coste creciente de entrar al mercado** | **Alta** (insider/outsider con datos administrativos) | **IV shift-share sobre G (AEAT 2024; paneles de fianzas)** | **Alto** | **Contribución central** |
| C. Elasticidad de oferta y asequibilidad | Media-alta | Requiere rigidez exógena (DEM, construcción histórica); hoy F6 sale en contra | Medio-alto | Mecanismo M2 |
| D. Inmigración, oferta y asequibilidad | Media (literatura amplia; artículo compañero) | Sí [P] | Medio | Shock de identificación |
| E. Turismo y asequibilidad local | Media (Barcelona, Madrid, Lisboa) | Sí, con el COVID [P] | Medio | Mecanismo M3 / umbrales |
| F. Tipos, sustitución de tenencia y alquiler | Alta si se identificara | No (F8) | Incierto | Apéndice |
| G. Regulación y reset | Alta | Parcial: ZMRT [P][C]; tope del 2% sin variación transversal | Alto como extensión | Extensión |

Las demás contribuciones posibles (A, C–G) quedan subordinadas: la A es el hecho descriptivo que motiva, la C es el mecanismo, la D y la E son los shocks de identificación y la G es la extensión. La F no se identifica con los datos actuales (F8).

## 7. Nuevo modelo teórico

Se amplía el modelo stock-flow de la sección 4 del paper actual. Se mantienen la oferta y la demanda locales (ec. 3) y se añaden tres elementos:

**(i) Contratos con duración y reset.**
- Cada año termina una fracción λ_i de contratos. El nuevo contrato se firma a la renta de mercado R*_it; los demás se actualizan con u_t = min(π_t, cap_t).
- El alquiler medio de stock es:
  ln R̄_it = λ_i ln R*_it + (1−λ_i)(ln R̄_i,t−1 + u_t).
- La brecha de entrada es:
  G_it ≡ ln R*_it − ln R̄_it = (1−λ_i)[G_i,t−1 + Δln R*_it − u_t].
- **Predicción 1:** la brecha crece cuando el crecimiento del alquiler de mercado supera la actualización y es más persistente cuanto menor es λ (contratos largos).
- **Predicción 2:** un tope a u_t (2022–23) aumenta G uno a uno con (π_t − cap_t) para un R* dado. El RDL 7/2019 reduce λ y alarga la persistencia de G.

**(ii) Ingresos y composición.**
- La asequibilidad de entrada es A^E_it = ln R*_it − ln Y^E_it, donde Y^E es el ingreso por unidad de consumo de los hogares que buscan alquiler. La de incumbentes es A^I_it = ln R̄_it − ln Y^I_it.
- Un shock de demanda d ln N_it eleva R* en d ln N/Ψ_i (ec. 3 del paper) y altera Y^E por dos vías:
  - (a) los salarios locales, con elasticidad ω_i (Roback/Moretti);
  - (b) la composición de los entrantes, con un término c_it: los inmigrantes recientes tienen menor ingreso.
- Entonces:
  d A^E = (1/Ψ_i − ω_i) d ln N − c_it.
- **La asequibilidad de entrada empeora si y solo si el traslado al alquiler (1/Ψ_i) supera el traslado a ingresos (ω_i).**
- Si Y^E se mide por hogar, la duplicación de hogares (*doubling up*) eleva Y^E artificialmente: es el margen η del paper. Por eso la medida correcta es **por unidad de consumo**.

**(iii) Rigidez de oferta y turismo.**
- Ψ_i = η + ε_θ + ε_ℓ + σ_i. Un σ_i bajo (suelo, topografía, planeamiento) y un ε_ℓ bajo (poca vivienda reasignable) suben 1/Ψ_i.
- El turismo entra como −ψ_i d ln P^S en la oferta y, de nuevo, solo se manifiesta en R*: los contratos vigentes no se reasignan a turismo hasta que vencen.

**Predicciones formales:**

| Variable | Efecto de un shock de demanda |
|---|---|
| R* (entrada) | 1/Ψ_i, inmediato |
| R̄ (stock) | λ_i/Ψ_i el primer año; converge a 1/Ψ_i |
| Y por unidad de consumo | ω_i − composición |
| Población | 1 (P1 del paper: sin desplazamiento de nativos) [P] |
| Stock de vivienda | σ_i/Ψ_i |
| A^E (asequibilidad de entrada) | Empeora más donde σ_i es bajo, ω_i es bajo y λ_i es alto en el corto plazo |

Además, la brecha alquiler-de-entrada / alquiler-de-stock crece con el shock y decrece con λ.

## 8. Nueva variable dependiente principal

Se evaluaron las seis candidatas del encargo:

| Variable | Contenido económico | Datos | Problemas | Papel |
|---|---|---|---|---|
| A. log(R/Y) con el stock | Bajo para la pregunta: mide a los insiders | IPVA (índice) + ADRH | El IPVA es un índice, no un nivel. Las ratios en niveles requieren SERPAVI o fianzas | Comparación (insiders) |
| B. Δlog(R/IPC) | Solo deflacta | Sí | No incorpora la capacidad de pago | Descriptiva |
| C. Δlog(R/Y) | Asequibilidad media | Sí | Mezcla insiders y outsiders; el denominador cambia por composición | Secundaria |
| **D. Brecha de entrada: log R_nuevo − log R_existente** | **Alto:** mide directamente el reset y el reparto del ajuste. **Se cancelan los shocks comunes y la renta** | **AEAT 2024** (402 municipios de más de 20.000 habitantes, con m² y valor catastral: ajuste por calidad); INE por provincia (2021–2024); fianzas (Cataluña, País Vasco, C. Valenciana, Aragón) | Composición; en la AEAT, un solo corte transversal | **Principal para la causalidad** |
| **E. Brecha real de asequibilidad de entrada: [log R_nuevo − log Y] − [log R_existente − log Y]** | Idéntica a D si Y es común a ambos grupos. Gana contenido solo con ingresos distintos para entrantes e incumbentes (Y^E, Y^I) | Requiere microdatos (ECV/EPF) por comunidad | Tamaño muestral | **Principal para el titular**: A^E − A^I |
| F. Reset en la misma vivienda | El más limpio: elimina la calidad | No hay datos abiertos de pares de contratos por vivienda. En las fianzas catalanas no se enlazan contratos | No disponible en abierto | Solo con acceso administrativo (sección 12) |

**Decisión [I]:**
- **Variable dependiente causal principal:** D, la brecha de entrada, porque los shocks comunes, la inflación y el ingreso local se cancelan, y su respuesta a un shock exógeno es la predicción más directa del modelo.
- **Resultado de asequibilidad para el titular:** A^E = log(R_nuevo) − log(Y por unidad de consumo); en paralelo, A^I con el stock. La diferencia A^E − A^I da la cifra que responde a la pregunta del paper.
- **Ajuste por composición obligatorio:** usar el alquiler por m² o en celdas de tamaño cuando los datos lo permitan (fianzas con superficie, SERPAVI por m²).

## 9. Definición exacta de la brecha alquiler–renta

Para cada mercado i (municipio o área urbana funcional) y año t:
- **Brecha de insiders:** A^I_it = ln R̄_it − ln Ỹ_it, con R̄ el alquiler medio de los contratos vigentes (IPVA encadenado a un nivel SERPAVI de 2015 o la mediana de las fianzas vigentes) e Ỹ la renta mediana por unidad de consumo (ADRH, INE).
- **Brecha de entrada:** A^E_it = ln R*_it − ln Ỹ_it, con R* la renta mediana de los contratos firmados en t (fianzas), preferiblemente por m² y multiplicada por una superficie de referencia constante.
- **Cambio de asequibilidad:** ΔA^E_it = Δln R*_it − Δln Ỹ_it.
  - ΔA^E se descompone en traslado de la demanda al alquiler y traslado a la renta (β_rent − β_inc, sección 15).
- **Ratio de esfuerzo de entrada** (en niveles, para la presentación): 12·R*_it / Y_hogar_it.
  - [N] En Cataluña sube del 20,7% en 2015 al 23,4% en 2023, con la renta neta media de todos los hogares (ADRH). Con la renta de los hogares inquilinos sería mayor; está por estimar.

## 10. Definición de la brecha de entrada

- **G_it = ln R*_it − ln R̄_it**, en el mismo mercado y periodo y con la misma metodología.
  - Fuente coherente: el INE publica índices de contratos nuevos y existentes por provincia (tabla 59005, 2021–2024) con pesos (59008/59009/59010).
  - El cambio ΔG_it = Δln Índice_nuevo − Δln Índice_existente es metodológicamente homogéneo [N]: 10,2 puntos de media provincial entre 2021 y 2024.
- **En niveles y ajustada por calidad, para toda España de régimen común:** con la estadística de viviendas declaradas en el IRPF de la AEAT, 2024 (municipios de más de 20.000 habitantes y códigos postales):
  - G^VR_i = ln(R_nuevo/VR_nuevo) − ln(R_total/VR_total) = ln(rentabilidad_nuevo/rentabilidad_total), donde VR es el valor de referencia catastral.
  - Mide cuánto más se paga por euro de vivienda al entrar [N]: 15,9 log-puntos de media.
- **A escala municipal y con horizonte largo:** fianzas (nuevos contratos) frente a IPVA municipal (stock). Las metodologías difieren (media de contratos frente a índice), así que el nivel de G no es interpretable, pero su cambio sí, con ajuste por composición.
- **Reset en sentido estricto:** ln R_nuevo(v) − ln R_anterior(v) para la misma vivienda v. No es observable en abierto; sería la versión del paper con datos administrativos de fianzas enlazados por vivienda (INCASÒL, AVS, Agencia de Vivienda Social de Madrid…).

## 11. Mecanismos económicos

| Mecanismo | Predicción falsable | Variación cuasi-exógena | Estado |
|---|---|---|---|
| **M1. Demanda demográfica** (inmigración) | ΔG > 0 y ΔA^E > 0 donde llega más población predicha; ΔA^I ≈ 0 | Shift-share de orígenes (33 orígenes, cuotas de 2003) [P] | Instrumento validado [P]; aplicarlo a G y a A^E |
| **M2. Rigidez de oferta** (mecanismo de amplificación) | ∂ΔA^E/∂(shock) mayor donde σ_i es bajo | Shock × rigidez predeterminada (suelo urbanizable disponible antes de 2015, pendiente, suelo ya urbanizado, tasa histórica de construcción), instrumentando con Z × rigidez | F6 negativo con proxies pobres; requiere SIU/Catastro/MDT |
| **M3. Turismo** (shock de reasignación en la entrada) | El colapso de 2020–21 baja R* y sube los contratos; la recuperación los revierte; efecto no lineal por encima de un umbral | Colapso COVID × exposición [P][C] | Identificado [P]; falta umbrales y heterogeneidad |
| M4. Tenencia (tipos) | La subida de tipos de 2022 eleva R* donde el comprador marginal está más restringido | Shock de tipos × exposición predeterminada (cuota de compradores primerizos, precio/renta, hipotecas por hogar antes de 2022) | F8 fallido con la cuota de hipotecados de 2011; probar otras exposiciones |
| M5. Regulación de la actualización | El tope 2022–23 amplía G más donde hay más contratos indexados al IPC | Shock nacional × exposición: cuota de contratos con actualización en 2022 (por antigüedad, Cataluña) o comparación nuevo/existente | Parcial [P] |
| M6. Regulación de la entrada | La ZMRT reduce G y el número de contratos; sustitución hacia temporada o habitaciones | DiD apilado [P][C] | Identificado en precio y cantidad; la sustitución no es observable con fianzas |
| M7. Composición y gentrificación | La renta media sube porque entran hogares ricos | Comparar renta mediana por unidad de consumo, distribución (deciles ADRH) y origen del entrante | Amenaza que hay que tratar, no mecanismo central |

**[I] Selección:** **M1 (demanda) + M2 (rigidez) + M3 (turismo)** como los 2–3 mecanismos; M5 y M6 como extensión (regulación y reset); M4 en el apéndice salvo que una exposición nueva supere las pruebas de tendencias previas.

## 12. Datos adicionales necesarios (derivados de la identificación, no de la disponibilidad)

| Necesidad que impone el diseño | Por qué | Fuente abierta encontrada | Si no hay fuente abierta |
|---|---|---|---|
| Alquiler de **nuevos** contratos por municipio y año, con superficie | Variable dependiente (G, A^E); ajuste por composición | AEAT 2024 (corte transversal nacional, con m² y valor catastral); fianzas de Cataluña, País Vasco, C. Valenciana y Aragón | Fianzas de Madrid, Andalucía, Baleares, Galicia y Canarias: solo con petición administrativa |
| Alquiler del **stock** en niveles | A^I en niveles; base para encadenar el IPVA | SERPAVI (MIVAU): la metodología de 2026 documenta 2011–2024 por sección censal y municipio, pero el XLSX nacional no es accesible (403 en mivau.gob.es); copia oficial del Ayuntamiento de Madrid; AEAT 2023–2024 | Petición formal al MIVAU o al INE |
| Reset en la misma vivienda | Elimina la calidad (F) | No existe en abierto | Microdatos de fianzas enlazados por vivienda (INCASÒL, Gobierno Vasco, GVA, Aragón), por convenio de investigación |
| Ingreso de los **entrantes** (jóvenes, inmigrantes recientes, inquilinos) | Denominador correcto de A^E | Ver bloque A del inventario (ADRH por unidad de consumo; microdatos ECV/EPF por comunidad) | Datos fiscales por edad o nacionalidad del declarante (AEAT), solo por petición |
| Rigidez de oferta **predeterminada** | Interacción shock × rigidez (M2) | Ver bloque B (suelo, MDT, año de construcción) | SIU del MIVAU (bloqueado) |
| Exposición válida al shock de tipos | M4 | Ver bloque C | — |
| Flujos origen-destino municipales | Spillovers y sorting | Ver bloque D | — |

## 13–14. Inventario de fuentes abiertas, con enlaces oficiales verificados

**Cómo se verificó:**
- Cada enlace se comprobó el 4 de octubre de 2026 con una petición HTTP: código 200/206 y cabecera o primeras filas visibles.
- Las fuentes de contratos las verificó un agente de inventario y las cinco más relevantes las re-verifiqué yo.
- No se ha eludido ningún control de acceso. Cuando una fuente devolvió 403 se buscó una vía oficial alternativa y se documenta abajo.

### Bloque R. Alquileres (nuevos contratos, stock, resets)

| Ámbito | Organismo | Dataset | URL oficial | Periodo | Unidad | Frec. | Variables | Licencia | Formato | Descarga automática | Limitaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|
| España (régimen común) | **AEAT** | Estadística de viviendas declaradas en el IRPF 2024. Comparativa de rentabilidad y precios de alquiler como vivienda habitual **con los nuevos contratos**, municipios de más de 20.000 habitantes | https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfvivienda/2024/jrubik16a4b116943de994823993a0e8a448e24ac90bcd.html (versión por código postal: …/jrubik582b4eeccd4e39730277d218cc788357e33967da.html) | 2024 (nuevos contratos solo en la edición 2024) | Comunidad, provincia, municipio de más de 20.000 habitantes (474 filas, 408 municipios), código postal (más de 200 viviendas) | Anual | Alquiler medio mensual (total/nuevos), m² medios, valor de referencia catastral medio, rentabilidad bruta | No indicada | HTML | Sí (lectura de la tabla HTML; verificado: 474 filas) | Medias, no medianas; sin País Vasco ni Navarra; un solo año con nuevos contratos |
| España (régimen común) | INE | IPVA: índices municipales (59060), por distrito (59061), por antigüedad del contrato y pesos (59004, 59005, 59008–59010) | https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/59005.csv (API: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/59005) | 2011–2024; nuevo/existente 2021–2024 | Municipio de más de 10.000 habitantes, distrito, provincia | Anual | Índice (base 2015) y variación | No indicada | CSV/JSON | Sí | Solo índices, sin niveles |
| España | INE | IRAV, índice de referencia para la actualización anual de los arrendamientos de vivienda (72975) | https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/72975 | Desde diciembre de 2024 (agosto de 2026: 2,47) | Nacional | Mensual | Tasa anual | No indicada | JSON | Sí | Es la regla de actualización u_t, no un alquiler |
| España | MIVAU | SERPAVI: metodología (documenta la «BD Sistema Estatal Índices de Alquiler de Vivienda») | https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/2026-03-18_Metodologia_SERPAVI.pdf | 2011–2024 (régimen común); Navarra 2021–2024; Gipuzkoa 2022–2024; Álava y Bizkaia 2024 | Sección censal, distrito, municipio, provincia, comunidad (con 10 o más viviendas) | Anual | Número de viviendas; €/m²·mes; €/mes; m² (mediana, p25 y p75; colectiva/unifamiliar) | — | PDF (la base es XLSX) | **No:** la página de descarga de mivau.gob.es devuelve 403 (CloudFront). No se ha localizado el XLSX en cdn.mivau.gob.es | Mide el **stock** declarado en el IRPF, no los nuevos contratos |
| Madrid (ciudad) | Ayuntamiento de Madrid | Copia de SERPAVI 2024 por distritos y secciones | https://www.madrid.es/UnidadesDescentralizadas/UDCEstadistica/Nuevaweb/Edificaci%C3%B3n%20y%20Vivienda/Mercado%20de%20la%20Vivienda/Sistema%20Estatal%20de%20%C3%8Dndices%20de%20Referencia%20del%20Precio%20del%20Alquiler%20de%20Vivienda/2022_2023_2024_2025/INDICE_ESTATAL_%20ALQUILER%20_distritos2024.xlsx | 2024 | Distrito y sección | Anual | Las de SERPAVI | No indicada | XLSX | Sí | Solo Madrid ciudad |
| Comunidad de Madrid | Instituto de Estadística CM | Copias del IPVA por antigüedad, del alquiler medio AEAT por municipio y de los arrendamientos notariales | https://datos.comunidad.madrid/dataset/19f85a43-949b-4486-a122-583cc7a291d6/resource/c85f2c9a-91e4-4b29-ad1c-36270f72b7f2/download/indice-de-precios-de-la-vivienda-en-alquiler-por-antiguedad-de-contrato-base-2015.csv | 2021–2024 / 2023–2024 / 2010–2025 | Comunidad / municipio | Anual | Índices; €/mes (AEAT); número de arrendamientos notariales | CC BY | CSV/JSON (CKAN) | Sí | Copias secundarias; el registro de fianzas de la AVS no está publicado |
| **Cataluña** | Generalitat / INCASÒL (fianzas) | Preu mitjà del lloguer d'habitatges per municipi (qww9-bvhh) | https://analisi.transparenciacatalunya.cat/resource/qww9-bvhh.csv | 2007–2026T1 | Municipio | Anual 2007–2018; trimestral desde 2019 | Contratos (habitatges), renta media (renda), tramo | Términos de uso del portal | CSV/JSON (Socrata) | Sí | Media, no mediana; sin m² municipal; contratos de más de un año |
| Cataluña | Generalitat (habitatge.gencat.cat) | Ficheros del mercado de alquiler: municipios trimestral; Barcelona por barrios (€/m²); AMB y municipios de más de 100.000 habitantes por barrio (€/m² y superficie) | https://habitatge.gencat.cat/web/.content/home/dades/estadistiques/01_Estadistiques_de_construccio_i_mercat_immobiliari/03_Mercat_de_lloguer/02_Lloguers_per_ambits_geografics/Lloguer_mitja/municipis_trimestral_lloguer.xlsx | Municipios 2005–2026; barrios de Barcelona 2000–2026; AMB 2019–2024 | Municipio, distrito, barrio | Trimestral | Contratos, renta media, €/m², m² | No indicada | XLSX | Sí | €/m² solo donde cruza con el Catastro |
| Cataluña | Generalitat (habitatge.gencat.cat) | **Altas y cancelaciones de fianzas (rotación)** y **alquiler de temporada** por municipio | …/03_Mercat_de_lloguer/07_Saldos/Saldos-altes_cancel_lacions.xlsx; …/07_Saldos/251103_Saldo_contractes_Htge_i_Temp.xlsx; …/08_Lloguer-de-temporada/lloguer_temporada_mun.xlsx (misma ruta base) | 2019–2026 (temporada 2023–2026) | Barcelona, AMB, resto, ZMRT; temporada por municipio | Trimestral | Altas, bajas, saldo; contratos de temporada | No indicada | XLSX | Sí (verificado: 200) | Permite medir la **rotación (λ)** y la **sustitución hacia el alquiler de temporada** tras la ZMRT |
| **País Vasco** | Gobierno Vasco, EMAL (Estadística del Mercado de Alquiler, a partir de fianzas) | EMAL. Barrios-Municipios. 2016-2025 | https://opendata.euskadi.eus/contenidos/estadistica/122417_emal_tablas_estad/opendata/EMAL.-Barrios-Municipios.-2016-2025_es.xlsx | 2016T1–2025T4 | Municipios de más de 20.000 habitantes (trimestral), de más de 5.000 (anual); barrios de las capitales | Trimestral / anual | **Nº de fianzas por fecha de inicio** (nuevos contratos); €/mes; €/m² construido; stock vigente a 31/12/2024 y 31/12/2025 | CC BY 4.0 | XLSX/ODS | Sí (verificado: 206) | Solo libre, colectiva y vivienda habitual; faltan municipios de menos de 5.000 habitantes |
| País Vasco | Gobierno Vasco, EMAL | EMAL 2016-2025 (territorios, tamaño, áreas funcionales) | https://opendata.euskadi.eus/contenidos/estadistica/122417_emal_tablas_estad/opendata/EMAL-2016-2025_es.ods | 2016–2025 | Territorio histórico, tramo de tamaño, área funcional, comarca | Trimestral / anual | Fianzas por tipo (habitual/temporada/local); **fianzas finalizadas**; €/m² | CC BY 4.0 | ODS/XLSX | Sí | Sin detalle municipal |
| **C. Valenciana** | GVA, Registro de Fianzas | Registro de las fianzas de alquiler de viviendas (un paquete CKAN por año, viv-reg-fia-AAAA) | https://dadesobertes.gva.es/dataset/6d018222-e7d8-4e82-b5d3-db307312b5ab/resource/7a9430fd-b889-45db-b16d-8f5a3a674d23/download/fianzas-depositadas-por-municipio.csv (resto de años: https://dadesobertes.gva.es/api/3/action/package_search?q=fianzas) | 2020–2026 | **Microdato por fianza** (municipio y código postal) | Anual, actualizado de forma continua | Año, municipio, CP, importe de la fianza, devuelta (sí/no) | CC BY | CSV/JSON/XLSX | Sí (verificado: 206 y cabecera) | Sin renta: la fianza legal equivale a una mensualidad, así que es un proxy; régimen ordinario; validar la cobertura (≈33.000 filas en 2024) |
| **Aragón** | Gobierno de Aragón | Fianzas de alquileres depositadas (recurso 100, microdatos del registro) | https://opendata.aragon.es/GA_OD_Core/download?resource_id=100&formato=csv | 1996–2025 (≈621.000 filas; ≈462.000 de vivienda) | Calle dentro del municipio (nombre, sin código INE) | Anual | Año, provincia, calle, municipio, tipo, año de devolución, **total_rentas**, importe de fianzas | CC BY 4.0 | CSV/JSON/XLSX | Sí (verificado: cabecera y filas) | El significado del campo «año» debe confirmarse (coincide con el año de devolución en casi todos los casos); hay que filtrar por tipo «Vivienda» |
| Aragón | Gobierno de Aragón | Recuento diario de fianzas (recurso 101) | https://opendata.aragon.es/GA_OD_Core/download?resource_id=101&formato=csv | 1999–2025 | Provincia | Diario | Fianzas nuevas formalizadas y devueltas | CC BY 4.0 | CSV | Sí | Solo provincia |

**Sin fuente abierta comparable** (buscado, no encontrado o inaccesible):

| Fuente o región | Resultado |
|---|---|
| SERPAVI completo (XLSX) | mivau.gob.es y transportes.gob.es devuelven 403 (CloudFront); los nombres de fichero plausibles en cdn.mivau.gob.es dan 404; serpavi.mivau.gob.es es un visor con reCAPTCHA, sin descarga masiva |
| datos.gob.es | 403 a curl (Incapsula). Su API, consultada vía WebFetch, solo devuelve los conjuntos ya listados |
| Navarra (Nastat) | Conexión reiniciada |
| Andalucía | El CKAN no tiene fianzas |
| Comunidad de Madrid | El registro de fianzas de la AVS no está publicado |
| Canarias | ISTAC: solo encuestas |
| Galicia | Panel de Power BI sin descarga |
| Baleares | No hay datos abiertos |
| Asturias | El host de SADEI no resuelve |
| Cantabria, Castilla y León, Castilla-La Mancha, Extremadura, Murcia, La Rioja | Nada basado en registro |
| Open Data BCN | No tiene series de alquiler; usar los ficheros de habitatge.gencat |
| **Resets por vivienda** | No existen en abierto en ninguna región |

**Armonización con Cataluña (nuevos contratos, municipio × año, número de contratos):**
1. **País Vasco (EMAL):** la mejor; incluye €/m².
2. **C. Valenciana:** número de contratos y proxy de renta a partir de la fianza.
3. **Aragón:** número de contratos y renta, previa confirmación del campo «año» y la asignación de códigos INE.
4. **Resto de España:** solo el corte AEAT 2024 y los índices INE.

Las diferencias de concepto deben tratarse con efectos fijos de región × año y con resultados en tasas de variación:
- Cataluña cubre todos los contratos de más de un año; el País Vasco, solo vivienda colectiva habitual.
- La C. Valenciana ofrece fianzas, no rentas.
- Los umbrales de secreto difieren.

### Bloque A. Ingresos y salarios (denominador de la asequibilidad)

**Convenciones del bloque:**
- **«INE csv»** significa https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/&lt;id&gt;.csv.
- **«INE tpx»** significa https://www.ine.es/jaxi/files/tpx/es/csv_bdsc/&lt;id&gt;.csv.
- **Licencia del INE:** CC BY 4.0 (aviso legal en https://ine.es/dyngs/AYU/index.htm?cid=125).
- **[R]** indica que lo re-verifiqué yo además del agente de inventario.

| Organismo | Dataset | URL / tabla | Periodo | Unidad | Frec. | Variables | Formato / descarga | Uso y limitaciones |
|---|---|---|---|---|---|---|---|---|
| INE (ADRH, op. 353) | Indicadores de renta media y mediana | INE csv **30824** (toda España); por provincia, p. ej. 31097 (Madrid) y 30896 (Barcelona) [R: ya descargada y usada] | 2015–2023 | Municipio, distrito, sección | Anual | Renta neta y bruta por persona y por hogar; **media y mediana por unidad de consumo** | CSV, sí | **Denominador principal (por unidad de consumo).** Todos los hogares, no solo inquilinos |
| INE (ADRH) | Distribución por fuente de ingresos | INE csv **30825** [R: 200; «Fuente de ingreso: salario;2023;70,6»] | 2015–2023 | Sección | Anual | Peso de salarios, pensiones, desempleo y otras prestaciones | CSV, sí | Exposición salarial; heterogeneidad de ω (traslado a ingresos) |
| INE (ADRH) | Indicadores demográficos | INE csv **30832** [R: 200; «Edad media de la población;2023;40,8»] | 2015–2023 | Sección | Anual | Edad media, % menores de 18, % de 65 o más, **% de nacionalidad española**, tamaño medio del hogar, % hogares unipersonales | CSV, sí | **Tamaño del hogar:** permite separar el *doubling up* (F5); composición |
| INE (ADRH) | Gini y P80/P20 | INE csv **37677** | 2015–2023 | Sección | Anual | Gini, P80/P20 | CSV, sí | Composición y gentrificación |
| INE (ADRH) | Población bajo umbrales de renta por sexo, edad y nacionalidad | INE csv **30826–30831** | 2015–2023 | Sección | Anual | % bajo umbrales fijos y relativos | CSV, sí | **Mejor proxy por sección de entrantes de baja renta** |
| AEAT | Estadística de los declarantes del IRPF por municipios | https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfmunicipios/2023/home.html (ediciones 2015–2024) | 2015–2024 | Municipio de más de 1.000 habitantes | Anual | Rendimientos del trabajo, del capital inmobiliario (alquileres), renta disponible, declaraciones | HTML, requiere extracción | Salario por declarante (≠ hogar); permite **renta de 2024** (la ADRH llega a 2023) |
| AEAT | Mercado de trabajo y pensiones en las fuentes tributarias | https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/mercado/2024/home.html | 2023–2024 (ediciones vistas) | Provincia × edad × sexo | Anual | Asalariados, salario medio anual | HTML | **Salario de los jóvenes por provincia**: denominador de entrantes |
| INE (EAES; EPA) | Estructura salarial; salarios por decil | INE csv **28191**, **28201** (por edad), **66241** (deciles) | 2008/2006–2024 | Comunidad autónoma | Anual | Media, mediana, deciles | CSV, sí | Solo comunidad autónoma |
| INE | **ECV, microdatos** | https://www.ine.es/ftp/microdatos/ecv/ecv_b2013/datos_2024.zip (2004–2025); diseño https://www.ine.es/metodologia/t25/dise%C3%B1o_registro_ecv.pdf | 2004–2025 | Comunidad autónoma | Anual | Tenencia (mercado o renta reducida), **alquiler pagado**, renta disponible, edad | ZIP, sí | **Esfuerzo de los inquilinos por edad y comunidad**. No verificado si identifica contratos recientes |
| INE | EPF, microdatos | https://www.ine.es/ftp/microdatos/epf2006/datos_2024.zip (2006–2025) | 2006–2025 | Comunidad autónoma; tamaño del municipio | Anual | Régimen de tenencia, ingresos, gasto en alquiler, cuota hipotecaria | ZIP, sí | Esfuerzo por tamaño de municipio |
| Seguridad Social | Afiliación por municipios | https://www.seg-social.es/descarga/es/Muni082026 [R] (ficheros mensuales desde 2024) | 2024–2026 | Municipio | Mensual | Afiliados por régimen | XLSX, sí | Empleo, no salario; serie corta |
| SEPE | Paro registrado por municipios | https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/datos_abiertos/datos/Paro_por_municipios_2024_csv.csv (2006–2026) | 2006–2026 | Municipio | Mensual | Parados por sexo, edad y sector | CSV, sí | Holgura laboral; útil para el balance del instrumento |

**Medida correcta de ingresos [I]:**
- **Ideal:** ingreso por unidad de consumo de los hogares que firman un contrato. No existe en abierto.
- **Mejor aproximación municipal:** mediana de la renta por unidad de consumo (ADRH 30824), con el tamaño del hogar (30832) para cuantificar el *doubling up*. Se complementa con el salario de los jóvenes (AEAT mercado de trabajo, provincia) y con el esfuerzo de los inquilinos de la ECV/EPF (comunidad autónoma).
- **La renta por hogar debe evitarse como denominador** (F5).

### Bloque B. Rigidez de oferta

| Organismo | Dataset | URL / tabla | Periodo | Unidad | Variables | Uso y limitaciones |
|---|---|---|---|---|---|---|
| Copernicus (ESA), bucket abierto en AWS | **Copernicus DEM GLO-30** | https://copernicus-dem-30m.s3.amazonaws.com/ [R] (teselas COG GeoTIFF, p. ej. Copernicus_DSM_COG_10_N40_00_W004_00_DEM) | Estático | Malla de 30 m | Elevación (pendiente derivable) | **Rigidez geográfica a la Saiz:** % de suelo con pendiente mayor del 15% en un radio de 10–15 km del centroide, más el agua y la costa |
| IGN/CNIG | MDT por WCS | https://servicios.idee.es/wcs-inspire/mdt?request=GetCapabilities&service=WCS (licencia CC BY 4.0 scne.es) | Estático | 5–1.000 m | Elevación | Alternativa oficial española al DEM |
| INE Censo 2021 | Viviendas por año de construcción del edificio | INE tpx **59527** [R] (municipios de más de 50.000 habitantes y capitales); microdatos https://www.ine.es/ftp/microdatos/censopv/cen21/CensoViviendas_2021.zip (municipios de más de 10.000) | 2021 | Municipio | Viviendas por década de construcción | **Tasa histórica de construcción** (respuesta pasada de la oferta), predeterminada |
| INE Censo 2021 | Viviendas vacías (consumo eléctrico) | INE tpx **59531** | 2021 | Municipio | Vacías y de bajo consumo | Holgura reasignable (ε_ℓ) |
| INE Urban Audit | Superficie y uso del suelo | INE csv **69326** (áreas urbanas funcionales) | 2010–2024 | Unas 70 áreas urbanas | Suelo residencial, agrícola y natural | Suelo ya desarrollado (solo grandes áreas) |
| MIVAU (apps.fomento.gob.es) | Viviendas libres iniciadas y terminadas; precio del suelo urbano; parque estimado | https://apps.fomento.gob.es/BoletinOnline2/sedal/32100500.XLS; …/36400500.XLS; …/33100500.XLS | 2001/2004/2008–2026 | Provincia | Iniciadas, €/m² de suelo, parque | Respuesta de cantidad y escasez de suelo por provincia |
| INE | Índices de costes de materiales y mano de obra | INE csv **8381**, **8377** | Hasta 2026M03 | Nacional | Índices | Coste de construcción (shock común) |
| Catastro (ya en el pipeline) | Viviendas por municipio | Paquete de replicación del artículo compañero (2013–2025) | 2013–2025 | Municipio | Viviendas | Respuesta del stock (resultado, no rigidez) |

**No verificado (bloqueado):**
- **SIU del MIVAU** (suelo urbanizable): 403 en mivau.gob.es.
- **Estadísticas del Catastro por municipio** (solares, superficie urbana): 403 del servidor, «Hemos denegado el acceso desde su dirección IP».
- **Licencias municipales de obra:** 403 en mivau.gob.es.

**Alternativa honesta:** construir la rigidez con el DEM (pendiente), la costa (ya disponible) y la tasa histórica de construcción del Censo 2021, y validarla con la respuesta del catastro al shock (debe predecir σ_i).

### Bloque C. Tenencia, hipotecas y precios

| Organismo | Dataset | URL / tabla | Periodo | Unidad | Uso |
|---|---|---|---|---|---|
| INE (op. 40) | Hipotecas por naturaleza de la finca | INE csv **3200** (provincia, mensual 2003–2026); tipo inicial **24457**; por entidad **3216** | 2003–2026 | Provincia | **Exposición provincial al shock de tipos:** hipotecas sobre viviendas por hogar en 2019–2021 |
| INE Censo 2011 | Indicadores por sección: **t18_2 = propiedad con pagos pendientes** | https://www.ine.es/censos2011_datos/indicadores_seccion_censal_csv.zip [R: usada en F8] | 2011 | Sección | Única medida de hipotecados por sección; F8 muestra que no es una exposición válida |
| INE Censo 2021 | Indicadores por sección (t20: propiedad/alquiler/otros) | https://www.ine.es/censos2021/C2021_Indicadores.csv | 2021 | Sección | Sin desglose de hipoteca |
| INE Urban Audit | **Niveles de alquiler** (media, mediana, cuartiles, €/m²), precio de la vivienda, % de vacías | INE csv **69323** [R] (áreas urbanas), **69302** (113 ciudades) | 2010–2024 | Área urbana funcional y ciudad | **Precio/alquiler y precio/renta por área urbana:** exposición al canal de tenencia |
| MIVAU | Valor tasado de vivienda libre en municipios de más de 25.000 habitantes | https://apps.fomento.gob.es/BoletinOnline2/sedal/35103500.XLS [R] | 2005T1–2026T2 | Municipio (por nombre) | **Precio de compra/renta** antes de 2022 como exposición al canal de tenencia |
| MIVAU | Transacciones por municipio | https://apps.fomento.gob.es/BoletinOnline2/sedal/34010210.XLS | 2004–2026 | Municipio (por nombre) | Compraventas; demanda de compra |
| Banco de España | Tipos de nuevas operaciones de vivienda por plazo | https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/be1904.csv (zip be19) | 2003–2026 | Nacional | El shock (serie temporal) |
| INE (op. 7) | Compraventas por régimen y estado; % comprador persona jurídica | INE csv **6150** (provincia); **50256** (nacional) | 2007–2026 | Provincia / nacional | Compradores persona jurídica solo a escala nacional |
| Notariado | Portal Estadístico del Notariado | https://www.penotariado.com/inmobiliario/ | — | — | **No abierto:** aplicación JS sin API; las condiciones prohíben la redistribución |

### Bloque D. Estructura espacial, movilidad y sorting

| Organismo | Dataset | URL / tabla | Periodo | Unidad | Uso |
|---|---|---|---|---|---|
| Eurostat | Correspondencia FUA–LAU 2021 | https://ec.europa.eu/eurostat/documents/345175/501971/FUA-LAU-2021.xlsx (1.262 filas españolas) | 2021 | Municipio → FUA | **Mercado relevante**: núcleo y corona |
| INE | **EMCR microdatos** (migraciones interiores municipio → municipio) | https://www.ine.es/ftp/microdatos/emcr/datos_2024.zip (2021–2024) | 2021–2024 | Municipios de 10.000 o más habitantes | **Spillovers núcleo → periferia** por edad y nacionalidad |
| INE | **EVR microdatos** (variaciones residenciales) | https://www.ine.es/ftp/microdatos/varires/datos_2021.zip (1988–2021) | 1988–2021 | Municipios de 10.000 o más habitantes | Serie larga de flujos; pesos de gravedad predeterminados |
| INE | EMCR tablas | INE csv **69743** [R], **69745**, **69742**, **75690** | 2021–2024 | Municipio / provincia / inframunicipal | Entradas y salidas totales |
| INE Censo 2021 | **Microdatos de personas** (municipio de trabajo; residencia 1 y 10 años antes; tenencia; año de construcción) | https://www.ine.es/ftp/microdatos/censopv/cen21/CensoPersonas_2021.zip | 2021 | Municipios de más de 10.000 habitantes | **Commuting** (mercado laboral relevante) y **movers frente a incumbentes**: quién se mudó en el último año, tenencia y nacionalidad. Permite construir **ingresos de entrantes por proxy** (empleo y nivel educativo de quienes se mudaron) |
| INE (experimental) | Movilidad con teléfonos móviles 2019 | https://www.ine.es/experimental/movilidad/exp_em1_descargas.zip | 2019 | Áreas de movilidad | Flujos diarios; un solo año |

**No accesible:**
- **Estudio de movilidad con big data del MITMA:** 403 del cortafuegos.
- **Atlas Digital de Áreas Urbanas:** aplicación sin descarga masiva verificada.

### Lo que el inventario cambia del diseño [I]

1. **El reset se puede medir en niveles y ajustado por calidad para toda España de régimen común**, pero solo en 2024 (AEAT). Un panel de nuevos contratos solo existe para Cataluña, el País Vasco, la C. Valenciana y Aragón.
2. **El ingreso de los entrantes no existe en abierto a escala local.** Lo más riguroso es:
   - la mediana por unidad de consumo (ADRH) a escala municipal;
   - el esfuerzo de los inquilinos por edad (ECV/EPF) a escala de comunidad autónoma;
   - y, como novedad, el censo de 2021 con los movers del último año (residencia un año antes) para caracterizar a quién entra.
3. **La rigidez de oferta debe construirse con geografía** (DEM y costa) y con la construcción histórica, no con densidad. El SIU y el Catastro están bloqueados.
4. **Los spillovers se pueden estudiar con flujos origen-destino oficiales** (EMCR 2021–2024; EVR 1988–2021).
5. **Para el canal de tipos**, la exposición más prometedora es el precio de compra/renta antes de 2022 (valor tasado MIVAU por municipio y ADRH): se encarece más el acceso donde la vivienda es más cara respecto a la renta. Debe superar las tendencias previas que fallaron en F8.

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

**Unidad geográfica y datos (en orden de prioridad):**
1. **Corte transversal nacional, AEAT 2024** (402 municipios de régimen común con más de 20.000 habitantes): G^VR (ajustada por calidad) y G^m² sobre la llegada acumulada 2016–2024 instrumentada.
   - Resultado preliminar [N] (F11): brecha bruta 0,57 (AR [0,15; 1,40]); ajustada 0,43 (AR [−0,04; 1,27]).
   - Ampliar a códigos postales (la AEAT los publica cuando superan las 200 viviendas) mejora la potencia y permite efectos fijos de municipio con variación entre barrios.
2. **Paneles de fianzas armonizados** para la dinámica (λ, persistencia, eventos):
   - Cataluña 2005–2026 (municipio × trimestre; €/m² y superficie en barrios de Barcelona, AMB y municipios de más de 100.000 habitantes);
   - País Vasco 2016–2025 (EMAL, municipios de más de 5.000 habitantes, €/m²);
   - C. Valenciana 2020–2026 (microdatos de fianzas; la fianza aproxima un mes de renta);
   - Aragón 1996–2025 (microdatos con renta).
3. **Las 48 provincias con la brecha del INE (59005, 2021–2024)**, como validación externa y para el diseño del tope del 2%.

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
4b. [C, preliminar] El mismo shock abre la brecha de entrada de 2024 (bruta 0,57, AR [0,15; 1,40]); la versión ajustada por calidad es del mismo orden (0,43), pero todavía no excluye el cero [N].
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

---

## Respuesta al criterio final de éxito

**Pregunta:** ¿por qué la asequibilidad se deterioró mucho más en unos mercados que en otros pese a la inflación y los shocks comunes?

| # | Qué hay que cuantificar | Respuesta posible hoy | Qué falta |
|---|---|---|---|
| 1 | Cuánto subieron realmente los alquileres en términos reales | Stock: −1 log-punto real entre 2015 y 2023 (IPVA 17,2 frente a IPC 18,3). Entrada: España +3,4 reales en 2021–2024 (nuevos 17,6 frente a IPC 14,3); Cataluña +21 reales en 2015–2023 (39,7 frente a 18,3) [N][D] | Paneles de entrada en más comunidades |
| 2 | Cuánto aumentaron los ingresos | Renta mediana por unidad de consumo +31 log-puntos nominales (≈ +13 reales) en 2015–2023 (ADRH) [N][D] | Renta de 2024 (AEAT por municipios); ingreso de los entrantes |
| 3 | Cuánto se abrió la brecha alquiler/renta | Insiders: −14 puntos (todos los municipios). Entrantes en Cataluña: +13 (87% de municipios), de +6 a +20 según el tamaño [N][D] | Lo mismo para el País Vasco, la C. Valenciana y Aragón |
| 4 | Cuánto de la brecha explica la demanda | Brecha de entrada en 2024: +0,43–0,57 por punto de entrada acumulada (IV, F = 20); la versión ajustada por calidad aún no excluye el cero [N][C prelim.] | Precisión: códigos postales, paneles, inferencia AKM |
| 5 | Cuánto, la falta de respuesta de la oferta | La oferta no responde al shock (−0,06) [P][C]. La amplificación por rigidez no está demostrada (F6) | Rigidez exógena (DEM, construcción histórica) |
| 6 | Cuánto, el turismo | En entrada: −0,30% por punto de exposición en el colapso y +0,44% en la recuperación [P][C]; en el umbral superior del 13% de exposición, 4–6% del alquiler de entrada | Umbrales y tramos; brecha de entrada como resultado |
| 7 | Cuánto, el paso de la propiedad al alquiler | **No identificado** (F8) | Exposición precio/renta antes de 2022 con tendencias previas superadas |
| 8 | Cuánto, la regulación | Tope del 2%: hasta 6% del stock (contable) [P]. ZMRT: −4/−5% en entrada, −18% de contratos [P][C]; brecha de entrada −4,3 puntos (F12) [N][D] | Sustitución hacia temporada (ficheros de habitatge.gencat 2023–2026) |
| 9 | En qué mercados es más grave | Grandes ciudades (gradiente de +6 a +20 en Cataluña; menor caída insider en ciudades de más de 500.000 habitantes) y mercados con alta llegada de población; turismo solo en la cola [N][D] | Validar el gradiente fuera de Cataluña |

**Conclusión honesta:**
- Con datos abiertos se puede **identificar** que el ajuste a los shocks de demanda se concentra en el reset y que la oferta no responde.
- **No se puede identificar todavía** la amplificación por rigidez ni el canal de tipos.
- El **ingreso del entrante** solo se aproxima.
- La mejora decisiva requiere dos datos administrativos: fianzas enlazadas por vivienda y renta del inquilino. Merece la pena pedirlos por convenio al INCASÒL, al Gobierno Vasco, a la GVA, al Gobierno de Aragón y a la AEAT.

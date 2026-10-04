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

**Conclusión de las pruebas [I]:**
1. **No existe una divergencia generalizada alquiler–renta.** Para los inquilinos que ya están dentro, el alquiler creció menos que la renta local en todos los municipios.
2. **La divergencia existe en la entrada.** Es grande, se amplía con el tamaño de la ciudad y se abre sobre todo desde 2022.
3. **El denominador importa.** Con la renta por hogar, un shock migratorio parece *mejorar* la asequibilidad: con más adultos por hogar sube la renta del hogar sin que suba la de cada persona. Es el mismo margen de hacinamiento que documenta el artículo compañero.
4. **Con los proxies disponibles no se ve amplificación por rigidez de oferta.** Hacen falta medidas de rigidez mejores (sección 13).

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
| **D. Brecha de entrada: log R_nuevo − log R_existente** | **Alto:** mide directamente el reset y el reparto del ajuste. **Se cancelan los shocks comunes y la renta** | INE por provincia (2021–2024); fianzas (Cataluña y otras comunidades por confirmar) | Composición de lo que se alquila (tamaño, calidad) | **Principal para la causalidad** |
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

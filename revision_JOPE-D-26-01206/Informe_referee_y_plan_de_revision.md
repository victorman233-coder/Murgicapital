# Informe de referee y plan de revisión integral

**Manuscrito:** *Absorbed by Crowding: Immigration, Rents and Housing Occupancy in Spain* (JOPE-D-26-01206), V. M. Fernández-Aguilera.
**Base de la revisión:** versión enviada al *Journal of Population Economics* (38 páginas de manuscrito más el formulario). "l. NN" remite a la numeración de líneas del manuscrito; "T" a sus tablas y "Fig." a sus figuras.
**Fecha:** 4 de octubre de 2026.

---

## Convenciones y reglas de este informe

| Etiqueta | Significado |
|---|---|
| **[M]** | Resultado ya obtenido y publicado en el manuscrito (se cita tabla o línea). |
| **[E]** | Análisis ejecutable con los datos que el manuscrito ya usa: IPVA municipal, de distritos y provincial; Padrón y estadística continua de población por país de nacimiento; censos 2011 y 2021 por sección; catastro; IGN; atlas de renta (ADRH); viviendas turísticas; EU-SILC agregado. |
| **[N]** | Requiere fuentes nuevas. Su disponibilidad, cobertura, periodo y escala **no están verificadas** en este informe y deben comprobarse antes de comprometerse a usarlas. |
| **[NI]** | No identificable con la información disponible. Debe presentarse como hipótesis abierta. |

Además sigo tres reglas:

1. No anticipo el resultado de ninguna prueba propuesta. Los únicos números que aparecen son los publicados en el manuscrito o cálculos aritméticos hechos con ellos, y en ese caso muestro la operación.
2. Describo las fuentes nuevas según lo que sé de ellas, pero siempre hay que verificarlas. Ninguna recomendación da por supuesto que el acceso esté confirmado.
3. Aparte de las referencias del propio manuscrito, cito solo unos pocos trabajos metodológicos estándar (lista al final). El autor debe comprobar sus datos bibliográficos antes de incorporarlos.

## Mapa del informe

| Punto del encargo | Dónde se responde |
|---|---|
| 1. Identificación causal e inferencia shift-share | A.3, A.5, C.4 |
| 2. Tendencias previas y placebos | C.5, C.6, E |
| 3. Medición del precio del alquiler | D.1–D.5 |
| 4. Ocupación y hacinamiento | D.6, C.7 |
| 5. Estrategia de estimación y especificaciones | C.1–C.3 |
| 6. Fuerza del instrumento | C.9 |
| 7. Mecanismos | C.7 |
| 8. Heterogeneidad | C.8 |
| 9. Magnitud económica | C.10 |
| 10. Datos y transparencia | I.2, I.3 |
| 11. Interpretación y política | G |
| 12. Entregables | A–I |

---

## A. Diagnóstico de referee

### A.1 Evaluación global

El artículo aborda una pregunta de primer orden para la política de vivienda en España: cuánta de la presión demográfica de la ola migratoria posterior a 2015 se ha trasladado a los alquileres y cómo se ha alojado el resto. Para ello combina datos administrativos de buena resolución (IPVA municipal y de distritos, Padrón y estadística continua de población por país de nacimiento, censos por sección y catastro) con el instrumental moderno de los diseños *shift-share*. Su intuición central es valiosa y está poco explorada: una elasticidad pequeña de los precios no implica una presión pequeña si lo que se ajusta es la cantidad de vivienda por persona.

Sin embargo, leídas en conjunto, **las tablas del propio manuscrito no sostienen los titulares del título, del resumen y de las conclusiones**:

1. **La elasticidad de 0,30 [M, T3-B] procede sobre todo de la comparación entre continentes de origen.** Viene del contraste entre municipios donde se asentaron en 2003 inmigrantes latinoamericanos y africanos y municipios donde se asentaron europeos (l. 333–343). Si solo se usa la composición por países dentro de cada continente, el instrumento es débil (F = 4,5) y el intervalo Anderson-Rubin con *bootstrap* salvaje es [−0,06, ∞) [M, T4-B].
2. **Identificado con las innovaciones del instrumento, el efecto desaparece en la especificación preferida.** Esa variación es la que menos sufre la crítica de Jaeger et al. (2018). Con covariables, la proyección local en h = 0 es −0,029 (EE 0,238) y la suma del modelo de dos instrumentos es 0,077 (0,113) [M, T13]. Además, el adelanto en h = −2 es significativo tanto con controles mínimos como con covariables [M, T13-B].
3. **El resultado no es estable entre ponderaciones, comparaciones ni periodos.** Sin ponderar es 0,181 (forma reducida 0,049, EE 0,040). Comparando solo municipios de la misma clase de tamaño es 0,153. Excluyendo el mayor municipio de cada provincia es 0,175. Y **cambia de signo en 2020–2024** (−0,457, EE 0,277) [M, T3-C, T10-C, T14, T9-C], justo el periodo de mayores llegadas.
4. **La variable dependiente no mide el precio que pagan los recién llegados.** Es un índice del stock de contratos declarados en vigor, con actualizaciones limitadas por ley desde 2022, que excluye el alquiler informal y el de habitaciones (l. 158–163). No es el precio de entrada.
5. **El "hacinamiento" (*crowding*) no está medido como tal.** Se mide como personas por vivienda principal, y la definición cambia entre el censo de 2011 (basado en enumeración y muestra) y el de 2021 (basado en registros) (nota 1 al pie de la p. 21 del manuscrito). Según el propio modelo del artículo, ese indicador es sobre todo un efecto composición, no un empeoramiento de las condiciones de alojamiento.

Mi lectura es que el manuscrito documenta de forma creíble dos hechos:

- **(a)** En la muestra ponderada, y sobre todo en 2012–2019, los municipios con mayor entrada predicha registran un crecimiento contemporáneo algo mayor del índice de contratos en vigor que el resto de municipios de su provincia.
- **(b)** A corto plazo, la población adicional se aloja en el parque registrado existente, cuyo tamaño no responde de forma detectable.

En cambio, **no están establecidos**: que 0,30 sea un parámetro causal estable, que el ajuste principal sea el hacinamiento, ni que la inmigración explique un 10 % del crecimiento de los alquileres. El artículo puede convertirse en una contribución sólida si reduce el alcance de sus afirmaciones y refuerza tres frentes: la variación identificadora (diseños con shocks de expulsión comparados dentro de cada continente), la medición del precio de entrada y la separación entre composición y hacinamiento.

### A.2 Principales fortalezas

1. **Pregunta relevante y bien delimitada.** El periodo es de una gran ola migratoria: de 6,16 a 9,46 millones de nacidos en el extranjero entre 2015 y 2025 (l. 2–3). El contexto institucional (topes de actualización, alquiler de habitaciones) es relevante para la política.
2. **Datos superiores a los habituales en esta literatura.** Las rentas proceden de declaraciones tributarias y no de anuncios. Hay tres escalas espaciales: provincia, municipio y distrito. La inmigración se mide por país de nacimiento, lo que la hace robusta a la naturalización. El catastro es anual y los censos están a nivel de sección.
3. **Unir precio y cantidad es una aportación conceptual real.** El artículo integra el margen de ocupación en un modelo de equilibrio espacial que traduce los coeficientes estimados en parámetros (Proposiciones 1 y 2).
4. **El instrumental de inferencia ya aplicado es de nivel alto.** Incluye intervalos Anderson-Rubin analíticos y con *bootstrap* salvaje restringido, inferencia por aleatorización con recentrado (Borusyak y Hull, 2023), pesos de Rotemberg, regresión a nivel de shock, exclusión de la propia provincia en el shock y control de la exposición total.
5. **Transparencia poco común.** El autor publica resultados que debilitan su tesis (T4-B, T9-C, T10-C, T13, T15) y una sección de limitaciones honesta (l. 496–504). El paquete de replicación genera todos los números desde los ficheros oficiales (l. 527–530, 676–681). Esto es lo que hace posible esta revisión.
6. **Disciplina en los controles.** El autor evita deliberadamente controles contemporáneos endógenos como el empleo o la construcción (l. 236–237).

### A.3 Las cinco amenazas más graves a la credibilidad causal

#### Amenaza 1. La variación identificadora es, en la práctica, un contraste entre tipos de municipio definidos por el continente de origen de su inmigración en 2003

- **Evidencia [M]:**
  - Al permutar los shocks dentro de cada continente sin controlar la exposición continental, la primera etapa observada no se distingue de las permutadas (p = 0,29, l. 335–337).
  - Con controles de exposición continental, F = 4,5 y el intervalo AR con *bootstrap* salvaje es [−0,06, ∞) (T4-B).
  - El instrumento está desequilibrado respecto a la renta (0,559), la población (1,235), la proporción de alquiler (0,506), las personas por vivienda (−0,374) y la intensidad turística (0,335) (T12, ponderado). Incluso condicionando en las demás covariables siguen siendo significativas la población (0,308), el alquiler (0,206) y las personas por vivienda (0,091).
  - El número efectivo de orígenes es 15,8 (T4-A).
- **Por qué importa:**
  - Según los patrones de asentamiento conocidos, que el autor debe documentar con sus propios datos, en 2003 la inmigración latinoamericana se concentraba en grandes ciudades y sus coronas, la europea occidental en municipios costeros residenciales y turísticos, y la marroquí y la de Europa del Este en municipios agrícolas y de construcción intensiva.
  - Después de 2015, estos tipos de municipio tuvieron trayectorias de alquiler distintas por causas ajenas a la inmigración: la recuperación del empleo en servicios urbanos, el turismo y la vivienda de uso turístico, y el ciclo agrícola.
  - Con unos 16 orígenes efectivos, fuertemente correlacionados dentro de cada continente y persistentes en el tiempo, el argumento de "muchos shocks" de Borusyak, Hull y Jaravel (2022) no garantiza la consistencia.
  - El supuesto de identificación se reduce entonces a esto: *la trayectoria temporal de las llegadas latinoamericanas frente a las europeas no está correlacionada con las tendencias diferenciales de alquiler de esos tipos de municipio, condicionando en controles lineales por año*. Es un supuesto mucho más exigente de lo que sugiere la l. 260.
- **Un cálculo con la T4-C:**
  - Los seis orígenes mostrados suman unos pesos de Rotemberg de α = 0,870.
  - Su contribución es Σ α·β = 0,270·0,41 − 0,223·0,18 + 0,149·0,67 − 0,097·0,40 − 0,088·0,13 − 0,043·0,21 ≈ **0,111**.
  - Si la descomposición es exacta, como en Goldsmith-Pinkham et al. (2020), los ≈ 0,19 restantes del 0,303 proceden de 27 orígenes con un peso neto de ≈ 0,13. Eso implica elasticidades por origen muy altas (≈ 1,5 de media ponderada) en orígenes que el texto no muestra.
  - Hace falta la tabla completa de los 33 orígenes.

#### Amenaza 2. Dinámica: el efecto preferido desaparece cuando se identifica con innovaciones del instrumento, y hay un adelanto significativo

- **Evidencia [M, T13]:**
  - Con covariables, la proyección local da −0,029 (0,238) en h = 0. La suma del modelo de dos instrumentos es 0,077 (0,113).
  - El adelanto en h = −2 es 0,171 (0,066) con controles mínimos y 0,098 (0,052) con covariables. En h = −4 es 0,40 y 0,36, imprecisos.
- **Problema lógico en la interpretación (l. 353–356):**
  - El autor atribuye el adelanto a la "selección hacia vivienda asequible". Ese argumento explica por qué la entrada **observada** se correlaciona con alquileres pasados (y por qué MCO < VI), pero **no puede explicar que el instrumento lo haga**: los inmigrantes no eligen el instrumento.
  - Que la innovación del instrumento prediga el crecimiento pasado del alquiler indica una de dos cosas. O bien el instrumento está correlacionado con la dinámica local de rentas, lo que viola la exogeneidad. O bien las innovaciones del instrumento están autocorrelacionadas y el adelanto recoge efectos de shocks anteriores, lo que exige controlar más rezagos.
  - Ambas posibilidades debilitan la identificación basada en el nivel del instrumento.
- **Por qué importa (Jaeger et al., 2018):**
  - Las participaciones de 2003 predicen también las entradas del *boom* (2003–2008) y las salidas de la crisis (2009–2014).
  - Los ajustes de largo plazo de esas oleadas pudieron mover los alquileres de 2012–2024 en los mismos municipios, con independencia de las nuevas llegadas. Ejemplos plausibles: ejecuciones hipotecarias concentradas entre inmigrantes del *boom*, stock bancario que vuelve al mercado de alquiler, reagrupación familiar, nacimientos.
- **Inconsistencia interna:** con efectos fijos municipales la elasticidad sube a 0,593 (T3-B, col. 5), mientras que la proyección local en h = 0 es −0,03. Ambas explotan sobre todo variación temporal dentro del municipio, así que hay que reconciliarlas con la misma muestra.

#### Amenaza 3. El parámetro es inestable y depende del estimando (pesos, comparaciones por tamaño y periodo)

- **Evidencia [M]:**
  - Sin ponderar: 0,181 (0,150), con intervalo AR [−0,12, 0,55] (T3-C).
  - Dentro de provincia × año × clase de tamaño: 0,153 (0,134) (T10-C).
  - Sin el mayor municipio de cada provincia: 0,175. Sin los de más de 100.000 habitantes: 0,168. Por ciudadanía en lugar de país de nacimiento: 0,205 (0,184) (T14).
  - Por subperiodos: 0,301 (0,148) en 2012–2019 frente a −0,457 (0,277) en 2020–2024 (T9-C).
- **Un cálculo:** si ambos subperiodos fueran independientes, el estadístico t de la diferencia sería (0,301 + 0,457) / √(0,148² + 0,277²) = 0,758 / 0,314 ≈ **2,4**. El parámetro no es estable justo en el periodo de mayores llegadas, y el texto no lo trata como tal (l. 431–434).
- **Qué implica:**
  - El 0,30 es, sobre todo, el efecto de comparar la ciudad principal con municipios menores de su provincia (como reconoce el propio autor en las l. 461–464), con pesos de población de 2003 y con un efecto concentrado en 2012–2019. Es la dimensión más expuesta a tendencias urbanas diferenciales.
  - La muestra de estimación incluye 2012–2014, años de salidas netas: la población nacida fuera bajó de 6,68 a 6,16 millones entre 2011 y 2015 (l. 2–3).
  - Por tanto, parte de la variación identificadora son **salidas**. Interpretarla como efecto de las llegadas exige que la respuesta sea simétrica, un supuesto fuerte para un índice de contratos en vigor con rigidez nominal a la baja.
  - Si el shock rumano, el de mayor peso, fue sobre todo negativo tras 2012, el problema se agrava. El autor debe mostrar el signo y la trayectoria de los shocks de los orígenes con más peso.

#### Amenaza 4. La variable dependiente no mide el precio que afrontan los nuevos residentes y está sujeta a cambios institucionales correlacionados con la exposición

- **Qué cubre el IPVA [M, l. 154–163]:** contratos en vigor, renta por m², solo mercado declarado, sin País Vasco ni Navarra y con topes de actualización desde 2022.
- **Cobertura de arrendadores (a verificar en la metodología del INE):** si el índice se construye solo con el IRPF, quedan fuera los arrendadores personas jurídicas, que tributan por Sociedades. Su peso es mayor en las grandes ciudades.
- **Atenuación y rezago:**
  - Un índice de stock refleja los precios de entrada solo a través de la rotación de contratos.
  - A corto plazo, β(stock) ≈ λ·β(contrato nuevo), donde λ es la proporción de contratos que rotan en el año.
  - La duración mínima pasó a 5 años (7 con arrendador persona jurídica) con el RDL 7/2019, lo que previsiblemente reduce λ dentro de la muestra. Eso es una fuente adicional de inestabilidad entre subperiodos.
  - Paradoja que el texto debe explicar: si las rentas de entrada suben y quedan fijadas durante el contrato, el índice de stock debería mostrar **más** persistencia que el precio de mercado, no menos.
- **Cambios de política dentro de cada provincia, que los efectos fijos provincia × año no absorben (fechas y municipios a verificar):**
  - La contención de rentas de la Ley catalana 11/2020, aplicada en un subconjunto de municipios hasta su anulación en 2022.
  - Las zonas tensionadas de la Ley 12/2023, en vigor en Cataluña desde 2024.
  - Los cambios en las reducciones del IRPF por arrendamiento desde 2024, que pueden alterar qué se declara.
  - Todos se concentran en municipios con alta exposición migratoria.
- **Consecuencia para el modelo:** la Proposición 2 usa β_L en (1 − c)/β_L. Si β(IPVA) ≈ λ·β(precio de mercado), la suma ε + δ′ queda sobrestimada en un factor 1/λ.

#### Amenaza 5. El "hacinamiento" no está medido ni identificado como tal, y la cuota de "más de la mitad" es imprecisa y frágil

- **La cuota depende de la especificación [M, T5-A]:**
  - La cifra de "más de la mitad" sale de 0,451/0,799 ≈ 56 % en la especificación ponderada con covariables, sin intervalo de confianza para el cociente.
  - Con las cifras de la misma tabla:

  | Especificación | Hacinamiento | Residentes netos | Cuota |
  |---|---|---|---|
  | Ponderada con covariables | 0,451 | 0,799 | **56 %** |
  | Sin ponderar | 0,447 | 1,209 | **37 %** |
  | Controles mínimos | 0,509 | 0,138 | **> 300 %** |

  - El texto (l. 362–363) dice que la estimación sin ponderar "es la misma", pero lo es solo el numerador.
- **Ruptura de medición:**
  - En 2021 los hogares se construyen a partir de las inscripciones en el registro de cada vivienda (nota 1 al pie de la p. 21 del manuscrito). Las personas por vivienda heredan así la calidad del Padrón.
  - Esa calidad incluye inscripciones donde no se reside, inscripciones múltiples y falta de inscripción, y probablemente está correlacionada con la llegada reciente de inmigrantes.
- **Composición frente a hacinamiento, según el propio modelo:**
  - La Proposición 2 implica c = (1 − κ) + η·β_L. Con c = 0,46 y β_L = 0,30:
    - Con η = 0,2, el componente de precio (η·β_L) es 0,06, un 13 % de c.
    - Con η = 0,5, es 0,15, un 33 % de c.
    - Con η = 0,7, es 0,21, un 46 % de c.
  - Es decir, **según el modelo del artículo, entre un 54 % y un 87 % del "crowding" medido es composición**: los recién llegados viven en hogares más grandes. Eso no implica por sí mismo que empeoren las condiciones de ningún hogar.
- **Personas por vivienda catastral (T5-C):**
  - La elasticidad de 1,23 es un cociente entre población y stock **total**. Sube mecánicamente cuando la población crece y el stock no.
  - No distingue entre ocupar viviendas vacías y aumentar las personas por vivienda ocupada. El autor lo reconoce en las l. 372–373, pero el resumen no.
- **Faltan las medidas que harían falta para hablar de hacinamiento:** no hay habitaciones, ni un umbral normativo de hacinamiento, ni ningún resultado de bienestar. El dato de EU-SILC es nacional y descriptivo.

#### Problema adicional, de interpretación más que de identificación: la extrapolación agregada

- La T11 multiplica una elasticidad **relativa** dentro de provincia por la entrada **nacional**.
- La propia T15 muestra que el efecto de mercado no está identificado: F = 0,3 al controlar la exposición. El diseño relativo elimina por construcción el efecto común ("intercepto ausente").
- La permanencia que supone el cálculo (l. 470) contradice la dinámica estimada con covariables.
- La composición de las llegadas de 2015–2024 no coincide con los pesos implícitos del instrumento (véase C.10).
- El resultado negativo de 2020–2024 no se incorpora.

### A.4 Recomendación editorial simulada

**Para JOPE o JUE: revisión mayor.**

- **Justificación:**
  - La pregunta, los datos y la transparencia del autor justifican otra ronda.
  - La mayoría de los problemas son de interpretación o de diagnósticos ausentes que **pueden ejecutarse con los datos actuales** (sección I, etapas 0 y 1).
- **Condiciones para aceptar:**
  - (i) Reescribir título, resumen y conclusiones para que digan solo lo identificado (sección G).
  - (ii) Completar los diagnósticos imprescindibles de B.1.
  - (iii) Presentar la ocupación como ocupación, con intervalos de confianza para las cuotas y la descomposición entre composición y ocupación intra-grupo.
  - (iv) Eliminar de resumen y conclusiones las atribuciones agregadas basadas en estimaciones entre provincias no identificadas.
- **Si los diagnósticos fallan:** si el efecto solo se sostiene con la variación entre continentes y no supera las pruebas de tendencias previas y de innovaciones, el artículo debe replantearse. Pasaría a ser un trabajo cuidadoso de **contabilidad de los márgenes de absorción con evidencia causal sugestiva sobre precios**. Sería publicable en una revista de campo, pero con otras afirmaciones.

**Para una revista generalista (JPE, AER, REStud): rechazo en su forma actual.**

- La variación identificadora no es suficientemente creíble para estimar un parámetro estable.
- La tesis sobre hacinamiento y bienestar necesita microdatos que el artículo no tiene.
- Para competir en ese nivel haría falta una fuente de variación más nítida, como diseños con shocks de expulsión dentro de continente (MI-1) o shocks de otros destinos (MI-2), además de datos de precio de entrada (D-1, D-2).

### A.5 Revisión crítica de la identificación (punto 1)

#### A.5.1 Condiciones de validez del instrumento

Sea el estimador 2SLS con un solo instrumento, controles W y pesos ω:

$$\hat\beta=\frac{\sum_{i,t}\omega_i\,z_{it}\,y^{\perp}_{it}}{\sum_{i,t}\omega_i\,z_{it}\,m^{\perp}_{it}},\qquad z_{it}=\sum_{o=1}^{33}s_{io}\,g^{(-p)}_{ot},$$

donde ⊥ indica que la variable se ha residualizado respecto a W y a los efectos fijos provincia × año. La interpretación causal puede apoyarse en una de tres condiciones, que **no son intercambiables**:

- **(a) Exogeneidad de las participaciones** (Goldsmith-Pinkham, Sorkin y Swift, 2020).
  - Exige E[s_io · u_it | W] = 0 para cada origen o y cada año t.
  - Es decir, la distribución por origen de 2003 no se relaciona con los shocks relativos de alquiler posteriores a 2012.
  - El autor la descarta con razón (l. 258–262): la T12 muestra que las participaciones están correlacionadas con características que predicen la dinámica de rentas.
- **(b) Exogeneidad de los shocks** (Borusyak, Hull y Jaravel, 2022). Exige dos cosas:
  - $E[g_{ot}\mid \bar u_{ot}, q_o]=\mu_t' q_o$, con $\bar u_{ot}=\sum_i \omega_i s_{io}u_{it}/\sum_i\omega_i s_{io}$: los shocks no están relacionados con el error estructural medio de los municipios expuestos a cada origen.
  - Que haya **muchos** shocks con pesos pequeños ($\sum_o \bar s_o^2\to 0$) y con dependencia débil entre ellos.
  - La exposición incompleta se trata con el control $S_i$ × año, como hace el manuscrito.
  - El punto débil está en los "muchos shocks": 33 orígenes, de los cuales 5 son residuos continentales, unos 16 efectivos, con correlación dentro de continente y persistencia temporal.
- **(c) Asignación de shocks con un proceso conocido** (Borusyak y Hull, 2023).
  - Se recentra el instrumento con su esperanza bajo el proceso de asignación: $\tilde z_{it}=z_{it}-\mu_{it}$.
  - Es consistente **si** el proceso está bien especificado. Por ejemplo, intercambiabilidad de las trayectorias de crecimiento entre orígenes dentro de estratos definidos ex ante.
  - La intercambiabilidad entre los 33 orígenes es poco creíble: mezcla grupos UE y no UE, grandes y pequeños, y residuos continentales con tasas de crecimiento extremas. Dentro de continente es más defendible, pero allí la primera etapa es débil.

Además hacen falta dos condiciones adicionales:

- **Relevancia.**
- **Monotonicidad u homogeneidad para la interpretación LATE.** Con efectos heterogéneos por origen, 2SLS es un promedio con pesos que pueden ser negativos; la suma de pesos negativos es −0,091 [M, T4-C].

**Posibles violaciones de la restricción de exclusión, específicas del contexto español:**

| Canal | Mecanismo | Tipo de amenaza |
|---|---|---|
| Atracción sectorial nacional | Las llegadas por origen responden a la demanda española de trabajo (servicios urbanos, construcción, agricultura), cuya incidencia local se concentra en los municipios expuestos a esos orígenes. | Shocks |
| Demanda de vivienda de no residentes ligada al origen | Shocks del país de origen mueven la demanda de segunda residencia o de compra sin alterar el flujo registrado. Ejemplos: el tipo de cambio de la libra tras 2016, el Brexit, la "golden visa" (Ley 14/2013). Afectan a municipios costeros expuestos a británicos y alemanes. | Exclusión en sentido estricto |
| Artefactos de registro | Bajas por caducidad de extranjeros no comunitarios sin residencia permanente, comprobaciones de residencia de comunitarios, inscripciones ligadas al Brexit. Mueven el flujo medido sin mover la demanda real. | Medición (atenúa β o lo sesga si se correlaciona con políticas locales) |
| Alojamiento institucional | Llegadas inscritas en centros de acogida, por ejemplo en Canarias desde 2020 o en la acogida de protección internacional. Aumentan el padrón sin demanda en el mercado de alquiler. | Medición |
| Legado del *boom* (JRS) | Ejecuciones hipotecarias, stock bancario, reagrupación y nacimientos de cohortes anteriores, correlacionados con $s_{io}$. | Participaciones × dinámica |
| Políticas municipales | Contención de rentas en Cataluña 2020–2022, zonas tensionadas desde 2024, regulación de viviendas turísticas. Varían dentro de cada provincia. | Factor de confusión dentro de la provincia |

#### A.5.2 Participaciones de 2003 y tendencias previas

- **2003 está en mitad del *boom* (2000–2008).** Las participaciones reflejan clasificación por demanda de trabajo, disponibilidad de alquiler, amenidades costeras y redes.
- **La T12 confirma el desequilibrio,** pero lo relevante no es el nivel de las características sino si la exposición se correlaciona con **tendencias** de alquiler, empleo, actividad, oferta y demografía.
- **El IPVA empieza en 2011, así que no hay periodo previo limpio para los alquileres.** La prueba de 2012–2014 (l. 314–315) no es un periodo previo:
  - (i) Forma parte de la muestra de estimación.
  - (ii) Son años de salidas netas, con el instrumento activo y mayoritariamente negativo, de modo que mezcla efecto y tendencia previa.
  - (iii) Usa el promedio temporal del instrumento.
  - (iv) Su intervalo condicional, −0,037 ± 1,96·0,057 = [−0,15, 0,08] en desviaciones típicas, no descarta tendencias previas moderadas.
- **Propuesta (detallada en C.5):**
  - Probar con resultados anteriores a 2011: población nacida en España del Padrón 2003–2011 [E], precios de tasación, paro registrado y censo de 2001 [N].
  - Probar con rentas 2011–2014 sobre los shocks **futuros** (2015–2024), controlando los contemporáneos [E].

#### A.5.3 Shocks nacionales correlacionados con shocks económicos heterogéneos

El autor debe documentar la serie nacional de cada origen con mucho peso y argumentar caso por caso si es de expulsión o de atracción:

- **Colombia, Venezuela, Perú, Honduras.**
  - Expulsión: la crisis venezolana.
  - Política migratoria: la exención de visado Schengen para Colombia (diciembre de 2015) y Perú (marzo de 2016).
  - Atracción: la recuperación del empleo en servicios en 2015–2019 y 2022–2024.
  - Su exposición se concentra en las grandes áreas urbanas, donde a la vez crecieron el empleo en servicios y el turismo.
- **Rumanía y Bulgaria:** flujos vinculados al ciclo de la construcción y la agricultura en España y a destinos alternativos en la UE.
- **Marruecos:** contratación en origen para campañas agrícolas y reagrupación familiar, con exposición en zonas agrícolas de ciclo propio.
- **Reino Unido y Alemania:** jubilación, tipo de cambio, Brexit, segundas residencias. Exposición en municipios turísticos costeros.
- **Ucrania (2022):** expulsión limpia por la guerra, pero con poca exposición en 2003 (participación del 1,3 % de los extranjeros, T4-C).

Excluir la propia provincia del shock (l. 248–249) elimina el sesgo mecánico de la propia observación, **pero no los factores de atracción comunes** a muchas provincias.

#### A.5.4 Separar las amenazas de las participaciones y las de los shocks

| Origen de la amenaza | Amenaza concreta | Cómo se manifestaría | Pruebas (sección) |
|---|---|---|---|
| Participaciones | Las amenidades, la estructura sectorial, el tamaño y la profundidad del alquiler en 2003 predicen tendencias post-2012 | Tendencias previas por tipo de municipio; la estimación cae al controlar sector × año o tamaño × provincia × año | Pesos de Rotemberg y tendencias previas por origen principal; VI exactamente identificada por origen; prueba de sobreidentificación; controles económicos × año; participaciones placebo (C.5, E) |
| Participaciones × dinámica | Legado del *boom* (JRS) | Adelantos significativos; efecto nulo al usar innovaciones; correlación alta entre la entrada predicha del *boom* y la posterior | Modelo de dos instrumentos con F de Sanderson-Windmeijer; control del *boom* × año; proyecciones locales con rezagos (C.6) |
| Shocks | Atracción nacional sectorial; canales de demanda de vivienda propios de cada origen | Equilibrio a nivel de shock que falla; resultados distintos con shocks de otros destinos | Equilibrio y tendencias previas a nivel de shock; shocks alternativos de expulsión; estudios de evento por origen (C.5, MI-1, MI-2) |
| Shocks | Artefactos de registro | Primera etapa impulsada por orígenes con limpiezas administrativas | Contraste con flujos de la EVR; excluir años y orígenes afectados (MI-3) |
| Interacción | Pocos shocks efectivos y contraste entre continentes | La inferencia y la identificación dependen de 2 o 3 contrastes | Diseño dentro de continente con AR por aleatorización; AKM0; estratos de permutación (C.4) |

#### A.5.5 Inferencia *shift-share* moderna: qué resuelve cada procedimiento

| Procedimiento | Qué resuelve | Qué no resuelve | Interpretación que permite |
|---|---|---|---|
| EE agrupados por provincia (42 conglomerados) | Correlación arbitraria dentro de cada provincia | Correlación entre municipios de provincias distintas con mezclas de origen parecidas (exposición común a los mismos shocks). Adão, Kolesár y Morales (2019) muestran que eso puede producir un exceso de rechazos grave. | Válida si los residuos de distintas provincias son independientes, lo que no es plausible en *shift-share* |
| WCR *bootstrap* (Webb) con AR | Pocos conglomerados de tamaño desigual; instrumentos débiles | Igual que la anterior: hereda el supuesto de independencia entre provincias | Prueba robusta a debilidad, condicional a ese supuesto |
| AKM (Adão, Kolesár y Morales, 2019) | Correlación inducida por la exposición, tratando los shocks como fuente de aleatoriedad; permite agrupar shocks (por ejemplo origen × años) | Sesgo por endogeneidad de los shocks; pocos shocks efectivos (su asintótica es en número de shocks) | EE válidos bajo el diseño de shocks con muchos shocks independientes |
| AKM0 (con la hipótesis nula impuesta, invertido por prueba) | Mejor tamaño en muestras finitas y con shocks de colas pesadas o pocos efectivos; intervalos asimétricos | Endogeneidad de los shocks | **Recomendado como complemento asintótico principal** |
| Regresión a nivel de shock (BHJ 2022) | Equivalencia numérica con el 2SLS; permite controles y equilibrio a nivel de shock y agrupación por origen | Lo mismo que AKM. Además, aquí 0,234 ≠ 0,303 (T4-A), lo que indica que la regresión no está construida de forma equivalente. **Hay que reconciliarlo.** | Diagnóstico y transparencia |
| Aleatorización con recentrado (Borusyak y Hull, 2023) | Exposición no aleatoria (sesgo, mediante el recentrado) e inferencia exacta en muestra finita **si** la asignación está bien especificada | Una asignación mal especificada; la intercambiabilidad entre continentes es dudosa | **Recomendada como inferencia principal**, con estratos de permutación fijados ex ante |
| AR por aleatorización (el estadístico Σ z̃ (y − β₀ m) del propio manuscrito) | A la vez debilidad del instrumento y correlación por exposición, bajo intercambiabilidad | La validez del supuesto de intercambiabilidad | Es el procedimiento más coherente con la estructura del instrumento |

**Recomendación:**

- **Inferencia principal:** AR por aleatorización con permutaciones dentro de estratos fijados ex ante. Por ejemplo, continente, o continente × tamaño del grupo de origen en 2003.
- **Complementos:** AKM0 como complemento asintótico y WCR-AR por provincia como comprobación.
- **Regla de decisión:** las conclusiones deben basarse en el procedimiento creíble más conservador.
- **No se trata de elegir el estimador más sofisticado:** cada uno responde a una pregunta distinta, y el texto debe decir cuál.

---

## B. Plan de revisión priorizado

Cada modificación indica el problema que resuelve, el método, los datos que necesita y cómo afectaría a las conclusiones.

### B.1 Imprescindibles para que las conclusiones causales sean creíbles

**I-1. Hacer explícita la variación identificadora y someter a prueba el contraste entre continentes.**
- *Problema:* la amenaza 1.
- *Método:*
  - Tabla de estadísticos de los shocks al estilo BHJ: media, desviación típica, rango intercuartílico, número efectivo (1/HHI) por origen y por origen × año, mayor peso, autocorrelación de cada origen, correlación dentro de continente.
  - Tabla completa de pesos de Rotemberg (33 orígenes), con gráfico de β_o frente al F de cada origen (Goldsmith-Pinkham et al., 2020).
  - VI con las 33 participaciones como instrumentos separados (LIML) y prueba J.
  - Además del control de exposición continental de la T4-B, que elimina casi toda la variación, añadir a la especificación central **controles económicos especificados × año**. Atacan directamente los canales por los que la composición continental podría confundirse con la demanda local: estructura sectorial de 2011 (agricultura, construcción, hostelería, industria), litoral, intensidad turística previa (segundas residencias de 2011 [E] o 2001 [N]), clase de tamaño × provincia × año, y núcleo o periferia de área urbana funcional × año.
- *Datos:* [E] para todo salvo la estructura sectorial municipal. El censo 2011 la ofrece si se publica a escala municipal; si no, habría que usar la afiliación por municipio [N].
- *Efecto:* si β sobrevive a esos controles, la credibilidad aumenta mucho. Si cae hacia cero, el 0,30 debe interpretarse como una tendencia diferencial por tipo de municipio, no como un efecto de la inmigración.

**I-2. Tendencias previas con periodos previos de verdad.**
- *Problema:* la prueba de 2012–2014 no es un periodo previo (A.5.2), el adelanto en h = −2 es significativo y no hay pruebas conjuntas.
- *Método:* regresiones especificadas en C.5:
  - (F1) placebo de shocks futuros sobre rentas 2011–2014;
  - (F2) resultados anteriores a 2011;
  - (F4) proyecciones locales con más rezagos del instrumento, prueba conjunta de adelantos y sensibilidad tipo Rambachan y Roth (2023);
  - pruebas de equivalencia y potencia (Roth, 2022).
- *Datos:* [E] para rentas y población; [N] para precios y paro.
- *Efecto:* establecer o refutar el supuesto central. Un resultado no significativo no valida nada por sí solo; se debe informar del rango de tendencias que la prueba puede descartar.

**I-3. Reconciliar la dinámica y la crítica de Jaeger, Ruist y Stuhler.**
- *Problema:* la amenaza 2. Con innovaciones y covariables la estimación es ≈ 0, y con efectos fijos municipales 0,59.
- *Método:*
  - Misma muestra equilibrada para todas las variantes.
  - Correlación entre la entrada predicha del *boom* (2003–2008) y la de 2015–2024.
  - Controlar la entrada predicha del *boom* × año.
  - Modelo de dos instrumentos con F de Sanderson y Windmeijer y AR conjunto.
  - Decidir y justificar qué estimando es el titular.
- *Datos:* [E].
- *Efecto:* si la correlación es muy alta, JRS no puede separar corto y largo plazo y hay que decirlo. Si el efecto solo aparece con el nivel del instrumento, el titular de "efecto en el año de llegada" debe retirarse.

**I-4. Estabilidad temporal y simetría.**
- *Problema:* la amenaza 3, con el resultado negativo de 2020–2024 y las salidas de 2012–2014.
- *Método:*
  - Modelo combinado con interacción subperiodo × entrada, instrumentada con instrumento × subperiodo, y prueba formal de igualdad.
  - Separar años de entradas y de salidas predichas (C.5, F8).
  - Excluir 2024.
  - Controles o exclusiones por municipios con contención de rentas o declarados tensionados.
- *Datos:* [E] más la lista de municipios afectados por cada norma [N, pública].
- *Efecto:* si la inestabilidad se confirma, no hay elasticidad única que aplicar a 2015–2024 y la T11 debe rehacerse por periodos.

**I-5. Elevar la inferencia al estándar del diseño.**
- *Problema:* la correlación por exposición, pocos shocks y pocos conglomerados.
- *Método (C.4):*
  - AKM0 con shocks origen × año agrupados por origen;
  - AR por aleatorización dentro de estratos;
  - WCR por provincia;
  - umbral tF de Lee et al. (2022);
  - reconciliar la equivalencia BHJ (0,234 frente a 0,303).
- *Datos:* [E].
- *Efecto:* todos los intervalos de los titulares pasan a ser los del procedimiento creíble más conservador.

**I-6. Documentar el IPVA y reetiquetar el estimando.**
- *Problema:* la amenaza 4.
- *Método:*
  - Describir con la metodología del INE el tipo de índice (viviendas emparejadas o medias estratificadas), cómo trata entradas y salidas, si cubre a arrendadores personas jurídicas, el número de observaciones por municipio y año y los umbrales de publicación.
  - Denominar el estimando "renta media por m² de los contratos declarados en vigor".
  - Comprobar si el instrumento predice la **cobertura** del índice (número de arrendamientos declarados), si esa información está disponible.
- *Datos:* [E] para la documentación; [N] para recuentos (SERPAVI y AEAT).
- *Efecto:* acota qué precio se mide y permite traducir β(stock) en β(entrada) mediante la rotación (D.1).

**I-7. Ocupación: intervalos para las cuotas y separación entre composición y ocupación intra-grupo.**
- *Problema:* la amenaza 5.
- *Método (C.7):*
  - Estimación conjunta (2SLS apilado) de todos los componentes en una misma muestra, periodo y especificación.
  - Intervalos de Fieller y *bootstrap* para la cuota "ocupación / residentes netos".
  - Ocupación contrafactual por composición, con la ocupación de 2011 por grupo fija.
  - Contraste entre registros y censo en 2021.
  - Dejar de usar el término *crowding* salvo con medidas basadas en habitaciones.
- *Datos:* [E] con datos ecológicos de 2011; [N] con microdatos censales.
- *Efecto:* convierte "más de la mitad" en un intervalo y en una partición entre composición y ocupación intra-grupo. Probablemente obliga a cambiar el título.

**I-8. Rehacer la magnitud agregada.**
- *Problema:* el intercepto ausente, la permanencia, la composición y la inestabilidad.
- *Método (C.10):*
  - Retirar del resumen y de las conclusiones las cifras entre provincias.
  - Presentar la cuota como función de β, con todos los intervalos y supuestos explícitos.
  - Versión por subperiodos y versión ponderada por la composición de origen observada.
- *Datos:* [E].
- *Efecto:* el "10 %" pasa a ser "entre ~1 % y ~20 % bajo supuestos A1–A4, sin poder descartar valores menores en 2020–2024".

**I-9. Controles verdaderamente predeterminados.**
- *Problema:* la renta de 2015 (ADRH) se mide **dentro** del periodo muestral (2012–2024) y puede estar afectada por las entradas y salidas de 2012–2014, que cambian la renta media por persona por composición. La l. 232–233 afirma lo contrario.
- *Método:*
  - Sustituirla por indicadores de 2001 o 2011 (nivel educativo, paro, estructura sectorial).
  - Como robustez, todas las covariables con valores del censo de 2001, anteriores a las participaciones de 2003.
- *Datos:* [E] con el censo 2011; [N] con el censo 2001.
- *Efecto:* elimina una posible vía de "mal control".

**I-10. Reescribir las afirmaciones.**
- *Problema:* hay afirmaciones que exceden la evidencia.
- *Método:* sección G.
- *Datos:* ninguno.
- *Efecto:* alinea el texto con lo identificado.

### B.2 Muy importantes para fortalecer la contribución

**MI-1. Estudios de evento por origen con shocks de expulsión, dentro de cada continente.**
- *Problema:* el contraste entre continentes.
- *Método:*
  - Usar episodios con fecha nítida: la exención de visado para Colombia y Perú (diciembre de 2015 y marzo de 2016), la crisis venezolana y la guerra de Ucrania (2022).
  - La exposición es la participación de 2003 de esos orígenes, y la comparación se hace con municipios de exposición latinoamericana (o de Europa del Este) **del mismo nivel** a otros orígenes (C.5, F3b).
- *Datos:* [E].
- *Efecto:* aporta variación casi experimental, con fechas y adelantos, que no depende del contraste urbano frente a costero. Riesgo: primeras etapas débiles por origen, que hay que tratar con AR.

**MI-2. Shocks alternativos de expulsión.**
- *Problema:* la atracción española como determinante de $g_{ot}$.
- *Método:* sustituir $g_{ot}$ por las entradas del origen o en otros países europeos o de la OCDE, o predecir $g_{ot}$ con condiciones del país de origen (renta, inflación, conflicto).
- *Datos:* [N] (Eurostat y la base de migraciones internacionales de la OCDE; verificar cobertura por país de nacimiento y años).
- *Efecto:* si β se mantiene, desaparece la principal crítica a los shocks. Riesgo de instrumento débil para orígenes que emigran casi solo a España.

**MI-3. Relocalización de residentes con la Estadística de Variaciones Residenciales (EVR, INE).**
- *Problema:* la respuesta de los nacidos en España se infiere de cambios de stock contaminados por nacimientos y defunciones.
- *Método:* salidas y entradas de nacidos en España por municipio, edad y destino (misma provincia u otra), y bajas por caducidad de los extranjeros.
- *Datos:* [N, pública; verificar desagregación].
- *Efecto:* prueba directa del desplazamiento y de la Proposición 1, que predice difusión dentro de la provincia.

**MI-4. Participaciones más antiguas.**
- *Método:* censo de 2001 o Padrón de 1998–2002 por nacionalidad o país de nacimiento.
- *Datos:* [N].
- *Efecto:* participaciones menos contaminadas por la clasificación del *boom*. Es preferible a usar las participaciones de 2008 o 2011, que fortalecen la primera etapa (F de 86 y 92, T14) pero son **más endógenas**. Usarlas porque elevan el F sería elegir especificaciones por su fuerza.

**MI-5. Movimiento natural de la población.**
- *Método:* nacimientos por nacionalidad de la madre y defunciones por municipio (estadística del Movimiento Natural de la Población, INE).
- *Datos:* [N, verificar desagregación].
- *Efecto:* separa nacimientos y defunciones de la variación de nacidos en España. Recuérdese que los hijos de inmigrantes nacidos en España cuentan como "nacidos en España". Permite controlar la parte del aumento de la ocupación debida a nacimientos en hogares inmigrantes ya asentados, que es una violación de la exclusión específica de ese resultado.

**MI-6. Distribución y niveles de renta (SERPAVI).**
- *Método:* percentiles 25, 50 y 75 por municipio y sección.
- *Datos:* [N; verificar años, escala y si comparte fuente tributaria con el IPVA].
- *Efecto:* comprobar si el efecto se concentra en el tramo bajo del mercado y expresar magnitudes en euros.

**MI-7. Horizonte de la respuesta de la oferta.**
- *Método:* proyecciones locales del stock catastral a 5–8 años, licencias o visados, y restricciones físicas al estilo de Saiz (2010): pendiente, agua y espacios protegidos.
- *Datos:* [E] para el catastro; [N] para el resto.
- *Efecto:* "el stock no respondió" pasa a ser una afirmación con horizonte explícito.

**MI-8. Disciplina en el modelo.**
- *Método:*
  - Estimar todos los momentos en la misma muestra y con el mismo horizonte.
  - Sensibilidad de los parámetros a los momentos (Andrews, Gentzkow y Shapiro, 2017).
  - Conjuntos identificados para ε y δ′.
  - Añadir la elección de régimen de tenencia y la relación entre stock y contratos nuevos mediante la rotación.
- *Datos:* [E].
- *Efecto:* evita presentar como estimaciones parámetros que no lo son (T6-B).

**MI-9. Heterogeneidad preespecificada** (C.8), con tres o cuatro dimensiones y corrección por comparaciones múltiples.

**MI-10. Ponderación con sentido económico.**
- *Método:*
  - Peso por hogares en alquiler de 2011 (el inquilino típico) frente a sin ponderar (el municipio típico).
  - Pesos de precisión si el INE publica el número de observaciones.
  - Interpretar la diferencia como heterogeneidad (Solon, Haider y Wooldridge, 2015).
- *Datos:* [E].

### B.3 Deseables si hay recursos o datos adicionales

- **D-1. Rentas de contratos nuevos de los registros de fianzas autonómicos.**
  - Cataluña es el caso mejor documentado; otras comunidades, a verificar.
  - Sirven para una submuestra de validación de β(entrada) frente a β(stock).
  - Datos: [N].
- **D-2. Microdatos de anuncios (Idealista, Fotocasa).**
  - Permiten un índice hedónico de precios ofertados, rentas de habitaciones y tiempo en el mercado.
  - Datos: [N, acceso por convenio o compra. El *scraping* plantea problemas legales y de condiciones de uso].
- **D-3. Microdatos censales de 2011 y 2021.**
  - Permiten medir habitaciones, hacinamiento según la norma de Eurostat y estructura del hogar por origen.
  - Datos: [N; verificar qué variables y qué identificación geográfica tiene cada censo].
- **D-4. Microdatos de la ECV (EU-SILC española) y de la EPF.**
  - Contienen sobrecarga de costes, hacinamiento y renta pagada por país de nacimiento.
  - Solo sirven de forma descriptiva y por comunidad autónoma.
  - Datos: [N].
- **D-5. Emancipación de jóvenes nacidos en España (EPA).**
  - Mide el margen de "hacinamiento" de los nativos: retraso en la formación de hogares.
  - Datos: [N].
- **D-6. Población en establecimientos colectivos y centros de acogida.**
  - Sirve para excluir entradas sin demanda en el mercado de alquiler.
  - Datos: [N].
- **D-7. Compras de vivienda por extranjeros por nacionalidad (Notariado, Registradores).**
  - Sirven para estudiar el canal comprador y la sustitución entre tenencias.
  - Datos: [N].

---

## C. Especificación econométrica propuesta

### C.1 Notación y definición de variables

| Símbolo | Definición |
|---|---|
| $i$, $p(i)$, $a(i)$, $k(i)$ | Municipio (699 con IPVA), su provincia (42), su área urbana funcional y su clase de tamaño en 2011 (10–20 mil, 20–50 mil, 50–100 mil, más de 100 mil habitantes) |
| $t$ | Año, 2012–2024. Para las pruebas de largo plazo, ventanas 2011–2014 y 2015–2024 |
| $R_{it}$ | IPVA general del municipio (base 2015) |
| $y_{it}=\Delta\ln R_{it}$ | Crecimiento logarítmico anual del IPVA |
| $F_{it}$, $P_{it}$ | Población nacida en el extranjero y población total a 1 de enero (Padrón hasta 2021, estadística continua desde 2022; diferencias siempre dentro de la misma fuente) |
| $m_{it}=(F_{i,t+1}-F_{it})/P_{it}$ | Entrada neta de nacidos en el extranjero sobre la población. Para la dinámica, usar flujos de enero a enero sin solapamiento: el promediado centrado del manuscrito (l. 217–219, 250) introduce una correlación mecánica entre años consecutivos |
| $s_{io}=F_{io,2003}/P_{i,2003}$ | Participación de 2003 del origen $o$ (33 grupos). Robustez con 2001 o 1998–2002 [N] |
| $S_i=\sum_o s_{io}$, $S_{ic}=\sum_{o\in c}s_{io}$ | Exposición total y exposición por continente $c$ |
| $g^{(-p)}_{ot}$ | $(F^{(-p)}_{o,t+1}-F^{(-p)}_{o,t})/F^{(-p)}_{o,2003}$: crecimiento nacional del origen $o$, excluida la provincia propia |
| $z_{it}=\sum_o s_{io}\,g^{(-p(i))}_{ot}$ | Instrumento *shift-share* |
| $\mu_{it}$, $\tilde z_{it}=z_{it}-\mu_{it}$ | Esperanza del instrumento bajo permutaciones de las trayectorias $\{g_{ot}\}_t$ entre orígenes **dentro de estratos** fijados ex ante, e instrumento recentrado (Borusyak y Hull, 2023) |
| $\mathbf{x}_i$ | Controles predeterminados (C.3) |
| $\omega_i$ | Pesos (C.3) |

### C.2 Modelo principal, primera etapa y forma reducida

**Ecuación estructural (central):**

$$y_{it}=\beta\,m_{it}+\lambda_{p(i)t}+\sum_{\tau}\mathbf{1}[t=\tau]\big(\phi_\tau S_i+\mathbf{x}_i'\boldsymbol\gamma_\tau\big)+u_{it}\qquad(1)$$

**Primera etapa:**

$$m_{it}=\pi\,\tilde z_{it}+\tilde\lambda_{p(i)t}+\sum_{\tau}\mathbf{1}[t=\tau]\big(\tilde\phi_\tau S_i+\mathbf{x}_i'\tilde{\boldsymbol\gamma}_\tau\big)+v_{it}\qquad(2)$$

**Forma reducida:**

$$y_{it}=\rho\,\tilde z_{it}+\bar\lambda_{p(i)t}+\sum_{\tau}\mathbf{1}[t=\tau]\big(\bar\phi_\tau S_i+\mathbf{x}_i'\bar{\boldsymbol\gamma}_\tau\big)+e_{it},\qquad \beta=\rho/\pi.\qquad(3)$$

- **Efectos fijos:** $\lambda_{p(i)t}$ son efectos fijos provincia × año y mantienen el estimando del manuscrito, la elasticidad local relativa β_L.
- **Qué es β:** el efecto de una entrada equivalente al 1 % de la población sobre el crecimiento del IPVA del municipio, **relativo a su provincia**, en el año de la entrada.
- **Qué publicar:** primero ρ y π, porque son lo que el diseño identifica directamente; después β con su conjunto AR.

**Versión en diferencias largas (complementaria, alinea horizontes con el censo y los distritos):**

$$\Delta_{15\to24}\ln R_i=\beta^{LD}M_i+\lambda_{p(i)}+\phi S_i+\mathbf{x}_i'\boldsymbol\gamma+u_i,\qquad M_i=\frac{F_{i,2024}-F_{i,2015}}{P_{i,2015}},\qquad Z_i=\sum_o s_{io}\,G^{(-p)}_o,\qquad(4)$$

con $G^{(-p)}_o$ el crecimiento acumulado 2015–2024 del origen $o$ sobre su stock de 2003, encadenando diferencias dentro de cada fuente como hace el manuscrito.

### C.3 Efectos fijos, controles, ponderación, errores estándar y valores extremos (punto 5)

| Elemento | Central | Solo robustez | No usar | Justificación |
|---|---|---|---|---|
| Efectos fijos territoriales y temporales | Provincia × año | Área urbana funcional × año (solo para municipios en áreas funcionales); **provincia × clase de tamaño × año** (prueba de estrés principal, [M] 0,153); comunidad autónoma × año (solo para comparar) | Año solo (no identifica nada relativo) | La provincia es un mercado administrativo; el área funcional es el mercado económico. El efecto fijo por tamaño elimina el contraste ciudad–periferia |
| Exposición | $S_i$ × año (imprescindible) | $S_{ic}$ × año (dentro de continente) | Omitirla (T3: la estimación cae a 0,08 por confusión) | Exposición incompleta (BHJ 2022) |
| Controles predeterminados | Fijados ex ante: ln población, proporción de alquiler, proporción de viviendas no principales, proporción con estudios superiores, tasa de paro, estructura sectorial (agricultura, construcción, hostelería) y litoral. Todos de 2011 (o 2001) × año | Versión con valores de 2001 [N]; viviendas turísticas de 2020 × año | Renta de 2015 (ADRH; posterior a 2012); empleo, construcción, renta o población nativa contemporáneos; stock catastral; viviendas turísticas medidas dentro del periodo como control central | Los controles deben ser anteriores a los shocks que identifican y no deben poder ser resultado del tratamiento |
| Tendencias municipales | — | Efectos fijos municipales en la ecuación de crecimiento (equivalen a tendencias lineales en nivel) | Como especificación central | **Ventaja:** absorben tendencias lineales diferenciales. **Riesgos:** con entradas persistentes absorben parte del efecto; se estiman con datos posteriores al tratamiento (Wolfers, 2006); con el IPVA desde 2011 no hay periodo previo para estimarlas por separado; reducen la potencia |
| Ponderación | Estimandos coprincipales, publicados juntos: (a) **sin ponderar**, el municipio típico; (b) **por hogares en alquiler de 2011**, el inquilino típico, que es el estimando natural de un índice de alquiler | Población de 2003 (la del manuscrito); pesos de precisión (inversa de la varianza o número de contratos, si el INE lo publica) | Elegir el peso según el resultado | Con heterogeneidad, ponderar cambia el estimando. La diferencia 0,30 / 0,18 se debe tratar como heterogeneidad por tamaño y estimarse de forma explícita |
| Errores estándar | Conglomerados por provincia con WCR (Webb) para AR; **AKM0** con shocks origen × año agrupados por origen; AR por aleatorización dentro de estratos | Conley espacial a 50 y 100 km; dos vías provincia y año ([M] 0,138) | Errores por municipio como principales ([M] 0,086; infravaloran) | 42 conglomerados de tamaño desigual y correlación por exposición entre provincias |
| Valores extremos | Informar del mínimo y el máximo del análisis por *jackknife* | Recortar $y$ al 1/99 %; excluir las observaciones con $m$ por encima del percentil 99,5; DFBETA por municipio y provincia; omitir una provincia, una comunidad autónoma o un origen cada vez | — | El IPVA de municipios pequeños se calcula con pocos contratos |

**Malos controles que hay que evitar expresamente:**

- Cualquier variable que pueda responder a la entrada de inmigrantes durante 2012–2024: empleo, afiliación, paro, renta media, construcción, stock catastral, viviendas turísticas, población nativa.
- Variables de 2011 que respondieron a la inmigración del *boom*. Son admisibles respecto a los shocks posteriores a 2011, pero conviene comprobar la robustez con sus versiones de 2001.

### C.4 Inferencia: procedimientos y cómo publicarlos

- **AR (un instrumento):**
  - Para cada β₀ se regresa $y_{it}-\beta_0 m_{it}$ sobre $\tilde z_{it}$ y los controles, y se contrasta el coeficiente de $\tilde z$.
  - El intervalo es $\{\beta_0:\ AR(\beta_0)\le\chi^2_{1,0.95}\}$.
  - Se calcula con tres varianzas o distribuciones nulas: (i) por provincia con WCR; (ii) AKM0 (shocks como fuente de aleatoriedad); (iii) por aleatorización, con el estadístico $T(\beta_0)=\sum\omega_i\tilde z^{\pi}_{it}(y_{it}-\beta_0 m_{it})^{\perp}$ bajo permutaciones π dentro de estratos.
  - Con un solo instrumento, AR, LM y CLR coinciden, y AR es el procedimiento robusto estándar.
- **Prueba t:** si se usa, publicar el F efectivo (Montiel Olea y Pflueger, 2013; con un instrumento equivale al F robusto) y aplicar el valor crítico ajustado de Lee et al. (2022). Con F ≈ 35 ese valor crítico es claramente mayor que 1,96 (el 1,96 solo es válido con F > 104,7).
- **Varias variables endógenas** (dinámica, orígenes, interacciones, difusión): publicar el F condicional de Sanderson y Windmeijer (2016) por cada variable y el rk de Kleibergen y Paap (2006). Usar AR conjunto y AR por proyección (conservador) para cada coeficiente.
- **Modelos sobreidentificados** (las 33 participaciones como instrumentos): CLR (Moreira, 2003), LIML y prueba J.
- **Cocientes** (cuotas de absorción, parámetros del modelo): intervalos de Fieller (Fieller, 1954) o *bootstrap* por pares de provincias en el sistema conjunto. **No** usar el método delta con denominadores imprecisos.

**Tabla de resultados principal propuesta** (una fila por especificación):

| Especificación | ρ (forma reducida) | π (primera etapa) | β 2SLS | F efectivo | AR-WCR provincia | AKM0 | AR aleatorización (estratos) | p (β = 0) |
|---|---|---|---|---|---|---|---|---|

### C.5 Pruebas de falsificación

**(F1) Placebo de shocks futuros en el periodo previo de rentas [E]:**

$$\Delta_{11\to14}\ln R_i=\theta\,Z^{post}_i+\psi\,Z^{pre}_i+\lambda_{p(i)}+\phi S_i+\mathbf{x}_i'\boldsymbol\gamma+e_i,$$

con $Z^{post}_i=\sum_o s_{io}G_o^{15\to24}$ y $Z^{pre}_i=\sum_o s_{io}G_o^{11\to14}$.

- *Hipótesis nula:* θ = 0.
- *Resultado preocupante:* θ significativo, o un intervalo de θ que no excluya magnitudes comparables a la forma reducida de (4) escalada al mismo horizonte.
- *Interpretación si falla:* la exposición a los shocks de 2015–2024 predice la dinámica previa, y el diseño confunde inmigración con tendencias por tipo de municipio.

**(F2) Resultados anteriores a 2011** [E con el Padrón; N con el resto]: la misma regresión con variables dependientes de 2003–2011:

- crecimiento de la población nacida en España (Padrón);
- precio de tasación (municipios de más de 25.000 habitantes; verificar);
- paro registrado;
- cambios censales 2001–2011 en régimen de tenencia y viviendas vacías.

Un resultado preocupante sería que la exposición a los shocks post-2015 predijera dinámicas previas de precios o empleo.

**(F3a) Adelantos del instrumento en el panel anual [E]:**

$$y_{it}=\beta m_{it}+\sum_{k=1}^{2}\theta_k\tilde z_{i,t+k}+\sum_{l=1}^{3}\psi_l\tilde z_{i,t-l}+\lambda_{p(i)t}+\ldots+u_{it}.$$

- Hipótesis nula: θ_k = 0.
- Hay que publicar la matriz de correlaciones temporales de $\tilde z$. Con shocks persistentes la potencia es baja, y eso debe decirse.

**(F3b) Estudios de evento por origen con shocks de expulsión, dentro de continente [E]:**

$$y_{it}=\sum_{k\neq -1}\theta_k\,\big(E^{X}_i\times\mathbf{1}[t=t_X+k]\big)+\sum_{k}\vartheta_k\,\big(E^{\bar X}_{i,c}\times\mathbf{1}[t=t_X+k]\big)+\lambda_{p(i)t}+\ldots+u_{it}.$$

- $E^X_i$ es la participación de 2003 de los orígenes afectados por el episodio X:
  - Colombia y Perú, con $t_X$ = 2016 (exenciones de visado);
  - Venezuela, con $t_X$ el año de ruptura que muestre la serie nacional;
  - Ucrania, con $t_X$ = 2022.
- $E^{\bar X}_{i,c}$ es la participación de los **demás** orígenes del mismo continente. La comparación es así dentro de cada continente.
- Versión instrumental: θ_k de la forma reducida dividido por la primera etapa del mismo episodio.
- *Resultado preocupante:* adelantos distintos de cero, o efectos posteriores sin primera etapa.

**(F4) Proyecciones locales con más rezagos y pruebas conjuntas [E]:**

$$\ln R_{i,t+h}-\ln R_{i,t-1}=\beta_h m_{it}+\sum_{l=1}^{L}\theta_{hl}\tilde z_{i,t-l}+\lambda^h_{p(i)t}+\ldots+e^h_{it},\qquad h\in\{-5,\dots,5\},$$

con $m_{it}$ instrumentada por $\tilde z_{it}$, L ∈ {1, 2, 3} y la **misma muestra equilibrada para todos los h**.

- Prueba conjunta de que β_h = 0 para h ∈ {−5, …, −2}.
- Sensibilidad tipo Rambachan y Roth (2023): suponer que el sesgo posterior está acotado por M̄ veces la mayor desviación previa y publicar el valor de M̄ a partir del cual el intervalo incluye el cero. Ese método se diseñó para diferencias en diferencias con tratamiento discreto, así que debe presentarse como análisis de sensibilidad, no como corrección.
- Publicar también el rango de tendencias previas que el diseño puede descartar (pruebas de equivalencia y potencia, Roth, 2022).

**(F5) Instrumentos placebo con participaciones alternativas [E]:**

- (a) **Participaciones permutadas:** se reasignan aleatoriamente los vectores $\{s_{io}\}_o$ entre municipios de la misma provincia y clase de tamaño, manteniendo los shocks. Se repite unas 1.000 veces y se compara la forma reducida observada con esa distribución.
- (b) **Pseudo-participaciones explicadas por observables:** se predice $s_{io}$ a partir de $\mathbf{x}_i$ (modelo fraccional por origen) y se construye $z^{pseudo}_{it}=\sum_o\hat s_{io}g_{ot}$.
  - Si $z^{pseudo}$ predice las rentas tanto como $z$, el efecto opera a través de características observables del municipio, no de las redes de origen.
- *Resultado preocupante:* que la forma reducida observada no sea atípica respecto a (a), o que (b) reproduzca la mayor parte de ρ.

**(F6) Resultados de control negativo.**

- Hay pocos resultados del mercado de vivienda que la inmigración no pueda afectar. Las pruebas más limpias son las temporales (F1–F4).
- Como control negativo demográfico se propone la tasa de mortalidad de los nacidos en España mayores de 65 años [N, Movimiento Natural de la Población].
  - No debería responder a corto plazo a las entradas.
  - Si el instrumento la predice, capta estructura por edades y envejecimiento, que confunde los resultados sobre población nativa y ocupación.

**(F7) Exclusiones, presentadas como gráfico de bosque con la banda del intervalo de referencia, no como lista de asteriscos [E]:**

- omitir un origen cada vez (33) y un continente cada vez;
- omitir una comunidad autónoma (15) y una provincia (42) cada vez;
- excluir los núcleos metropolitanos, los municipios costeros, las islas, el sureste agrícola (Almería, Murcia, Huelva), los municipios catalanes con contención de rentas, 2020–2021 y 2024.

**(F8) Simetría entre entradas y salidas [E]:**

$$y_{it}=\beta^{+}m_{it}\mathbf{1}[\tilde z_{it}>0]+\beta^{-}m_{it}\mathbf{1}[\tilde z_{it}\le 0]+\ldots$$

instrumentando cada término con el instrumento multiplicado por el mismo indicador. Es válido porque la partición la define el instrumento, no el tratamiento.

- Hipótesis nula: β⁺ = β⁻.
- Si se rechaza, el estimando agregado mezcla respuestas a llegadas y a salidas y no debe aplicarse a 2015–2024 sin separarlas.

**Regla de interpretación para todas las pruebas:**

- Un placebo no significativo **no demuestra** validez. Hay que informar del intervalo y de qué magnitudes descarta.
- Un placebo significativo no invalida necesariamente el diseño, pero obliga a:
  - (i) incorporar el factor de confusión como control especificado, o
  - (ii) restringir la afirmación causal a la variación que supera la prueba (por ejemplo, dentro de continente o 2012–2019).

### C.6 Dinámica y la crítica de Jaeger, Ruist y Stuhler

- **(D1) Modelo de dos instrumentos:**
  - $y_{it}=\beta_0 m_{it}+\beta_1 m_{i,t-1}+\ldots$, con instrumentos $\tilde z_{it}$ y $\tilde z_{i,t-1}$.
  - Publicar el F de Sanderson y Windmeijer por cada variable endógena (el manuscrito da 10,6 y 11,3, que parecen F individuales) y AR para (β₀, β₁) y para β₀ + β₁.
- **(D2) Control del legado:** añadir $Z^{boom}_i\times$ año, con $Z^{boom}_i=\sum_o s_{io}G_o^{03\to08}$, y lo mismo con $Z^{bust}_i$ (2008–2012).
- **(D3) Diagnóstico previo y obligatorio:** las correlaciones $\text{corr}(Z^{boom},Z^{post})$ y $\text{corr}(\tilde z_{it},\tilde z_{i,t-1})$.
  - Si son muy altas, la separación entre corto y largo plazo no está identificada, y así debe decirse.
- **(D4) Reconciliación:** una tabla con la misma muestra que compare:
  - (a) el nivel del instrumento, que da 0,303;
  - (b) los efectos fijos municipales, que dan 0,593;
  - (c) el control de $\tilde z_{t-1}$;
  - (d) la proyección local en h = 0, que da −0,029;
  - (e) el modelo de dos instrumentos.
  - Hay que explicar qué variación usa cada columna.

### C.7 Mecanismos y ocupación (puntos 4 y 7)

**Sistema conjunto.** Para cada resultado k, en **la misma muestra, el mismo periodo y la misma especificación**:

$$Y^k_i=\beta^k M_i+\lambda^k_{p(i)}+\phi^k S_i+\mathbf{x}_i'\boldsymbol\gamma^k+u^k_i,\qquad M_i\ \text{instrumentado con } Z_i,$$

estimado como 2SLS apilado con conglomerados por provincia comunes a todas las ecuaciones, para disponer de $\mathrm{Cov}(\hat\beta^k,\hat\beta^l)$. Los resultados $Y^k$, normalizados por la población inicial, son:

- residentes netos (registro);
- nacidos en España, separados en crecimiento natural (Movimiento Natural de la Población [N]) y saldo migratorio, con destino en la misma provincia o en otra (EVR [N]);
- stock catastral;
- viviendas ocupadas, en el censo;
- viviendas no principales;
- personas por vivienda principal (censo) y por vivienda catastral (registro y catastro);
- personas en viviendas alquiladas;
- precios de venta [N].

**Cuota de absorción con intervalo:**

- $\theta=\beta^{ocup}/\beta^{netos}$, con intervalo de Fieller y *bootstrap* por pares de provincias.
- Publicarla para las cuatro especificaciones de la T5-A. Hoy las cuotas puntuales van del 37 % al más del 300 % (A.3).

**Composición frente a ocupación intra-grupo [E con datos ecológicos de 2011; N con microdatos].** Sea $H_i/P_i=\sum_g\pi_{ig}h_{ig}$, con $\pi_{ig}$ la proporción de población del grupo $g$ (nacidos en España y regiones de nacimiento) y $h_{ig}$ las viviendas por persona del grupo. Entonces:

$$\Delta\frac{H_i}{P_i}=\underbrace{\sum_g\Delta\pi_{ig}\,\bar h_{ig}}_{\text{composición}}+\underbrace{\sum_g\bar\pi_{ig}\,\Delta h_{ig}}_{\text{ocupación intra-grupo}}.$$

- **Implementación factible ya:** usar los $h_g$ de 2011 que la T6-C estima por regresión ecológica para construir la ocupación **predicha por composición**, $\Delta(H/P)^{comp}_i=\sum_g\Delta\pi_{ig}h_{g,2011}$.
- Después se instrumentan por separado el componente de composición y el residuo intra-grupo.
- Si la respuesta observada coincide con la predicha por composición, el *crowding* es composición.
- La regresión ecológica tiene sesgos conocidos: supone que no hay efectos de contexto, es decir, que los nativos de secciones con muchos inmigrantes no tienen hogares de tamaño distinto. Por eso es preferible repetirlo con microdatos censales [N].

**Qué mecanismos identifica cada evidencia:**

| Mecanismo | ¿Identificado en forma reducida (si el VI es válido)? | Supuestos adicionales | Solo con el modelo | Prueba propuesta |
|---|---|---|---|---|
| Demanda directa de alquiler (β_L) | Sí, para el índice de stock relativo a la provincia | Que el IPVA mida el precio relevante; si no, β(entrada) ≈ β(stock)/λ | — | Validación con contratos nuevos (D-1); rotación (D.1) |
| Respuesta de la oferta | Sí, para el stock catastral a corto plazo (−0,10, EE 0,08) | Horizonte; subdivisiones no registradas | ε como elasticidad estructural | Proyecciones locales a 5–8 años; licencias; heterogeneidad por suelo (MI-7) |
| Conversión de viviendas vacías y secundarias | Débilmente (0,82, EE 0,53, T5-A) | Ruptura de definición entre censos | Separar ε entre conversión y construcción | Series anuales de viviendas vacías (si existen); consumo eléctrico [N, NI probable] |
| Ocupación | Sí (personas por vivienda principal y por vivienda catastral) | Comparabilidad 2011–2021; calidad del Padrón | Separar composición y precio (κ, η) | Descomposición anterior; microdatos |
| Sustitución entre alquiler y propiedad | Parcial (0,22 personas en viviendas que pasan a alquiler) | Medición de la tenencia en 2021 (registros) | — | Proporción de alquiler; precios de venta; compras por nacionalidad (D-7) |
| Desplazamiento de residentes | Débil (−0,20 n.s. en el censo; −0,70 y −0,99 a 1–2 años en proyecciones locales) | Nacimientos de hijos de inmigrantes cuentan como nacidos en España; defunciones | δ′ | EVR por destino; Movimiento Natural (MI-3, MI-5) |
| Difusión dentro de la provincia | **No**: los efectos fijos provincia × año la absorben; la provincia está mal identificada (F = 0,3) | — | Proposición 1 (β_J > β_L) | EVR origen–destino; efectos sobre vecinos con análisis de potencia |
| Composición del hogar | Parcial | Datos por grupo | κ | Descomposición; microdatos |

**Análisis de sensibilidad del modelo:**

- Presentar los parámetros ε, δ′ y κ como **calibración con conjuntos identificados**. Hoy los intervalos de la T6-B son [0,23, 13,69] para ε + δ′, [−0,95, 10,69] para ε y [−3,04, 8,00] para δ′: no son informativos.
- Añadir la matriz de sensibilidad de Andrews, Gentzkow y Shapiro (2017).
- Mostrar cómo cambia ε + δ′ con:
  - (i) β_L en el año de llegada frente a β_L en diferencias largas: 0,131 en 2011–2021 con covariables (T5-A) da (1 − 0,46)/0,131 ≈ 4,1, frente a 1,8;
  - (ii) β_L corregido por rotación;
  - (iii) η entre 0 y 1.

### C.8 Heterogeneidad preespecificada (punto 8)

**Especificación:**

$$y_{it}=\beta m_{it}+\beta_h\,m_{it}\tilde h_i+\lambda_{p(i)t}+\sum_\tau\mathbf{1}[t=\tau]\big(\phi_\tau S_i+\mathbf{x}_i'\boldsymbol\gamma_\tau+\kappa_\tau\tilde h_i\big)+u_{it},$$

- Instrumentos: $\tilde z_{it}$ y $\tilde z_{it}\tilde h_i$.
- $\tilde h_i$ es una característica predeterminada, estandarizada, cuyo efecto principal × año se controla.
- Alternativa más transparente: dividir la muestra por terciles de $h$, con primeras etapas separadas, y publicar F y AR por tercil.
- Advertencia: la interacción solo se interpreta como heterogeneidad del efecto si la validez del instrumento no varía con $h$.

**Dimensiones propuestas (pocas y con hipótesis previa):**

| Dimensión | Medida predeterminada | Hipótesis previa | Datos |
|---|---|---|---|
| H1. Elasticidad de la oferta | Proporción de suelo no urbanizable por pendiente superior al 15 %, agua o mar y espacios protegidos en un radio dado (al estilo de Saiz, 2010); viviendas vacías en 2001 y 2011 | β y la respuesta de la ocupación son mayores, y la respuesta del stock menor, donde la oferta es inelástica y hay pocas vacías | [N] MDT del IGN, línea de costa, Natura 2000; [E] vacías 2011 |
| H2. Profundidad del mercado de alquiler | Proporción de hogares en alquiler en 2011 | Con más alquiler, la misma entrada es un shock menor sobre el stock en alquiler (β menor). Pero el índice de stock rota más (β medido mayor). Hay que declarar ex ante cuál domina o separarlo con rotación | [E] |
| H3. Composición del shock (predicción iv del modelo) | Shock efectivo de demanda de alquiler $z^R_{it}=\sum_o s_{io}g_{ot}\kappa_o\rho_o$, con κ_o y la propensión a alquilar ρ_o de 2011 por origen | Prueba directa: $z^R$ debe predecir el alquiler una vez controlado $z$ | [E] |
| H4 (validez, no mecanismo). Tamaño y densidad | Clase de tamaño; núcleo o periferia | Diagnóstico de la amenaza 3, no hipótesis económica | [E] |

**Un cálculo de comprobación de la predicción (iv)** con números del manuscrito:

- El modelo implica que la demanda efectiva de alquiler por inmigrante es proporcional a κ·ρ. Con la T6-C:
  - África: 0,63 · 0,71 = 0,45.
  - Latinoamérica: 0,95 · 0,69 = 0,66.
  - UE: 1,09 · 0,46 = 0,50.
- El modelo predice por tanto Latinoamérica > UE ≈ África.
- Las estimaciones de la T9-B ordenan África (1,58) > América (0,77) > Europa (0,09). El orden entre África y América es **el contrario** al que predice el modelo.
- Los intervalos se solapan, así que hay que hacer una prueba formal de igualdad. En cualquier caso, la afirmación de las l. 424–426 no se sostiene como confirmación del modelo.

**Potencia y comparaciones múltiples:**

- Con errores de las interacciones en torno a 0,02–0,05 por desviación típica (T9-A), el efecto mínimo detectable (80 % de potencia, 5 % a dos colas) es ≈ 2,8 × EE, es decir, unos 0,05–0,15 por desviación típica. Solo se detectará heterogeneidad grande, y eso debe decirse.
- Hay que corregir por comparaciones múltiples dentro de la familia preespecificada (de 3 a 4 dimensiones por dos ponderaciones): Romano y Wolf (2005) con *bootstrap* salvaje, o valores q de Benjamini y Hochberg (1995) o Anderson (2008).
- Las siete interacciones actuales de la T9-A deben pasar a un apéndice exploratorio, marcadas como tales.
- La variable de turismo de 2020 es posterior al tratamiento.

### C.9 Fuerza del instrumento (punto 6)

- **Consecuencias de la debilidad (F ≈ 4,5 dentro de continente; 4,8 sin los tres orígenes principales; 3,4 en la clase de 20–50 mil; 4,9 en Asia):**
  - El 2SLS exactamente identificado no tiene momentos finitos y su mediana está sesgada hacia MCO (0,07–0,17).
  - Las pruebas de Wald rechazan en exceso y los errores estándar no son informativos.
  - Por eso **la estimación puntual de 0,617 (0,396) no debe comentarse como tal**. El resultado es el conjunto AR [−0,06, ∞): la variación dentro de continente no excluye el cero y no acota el efecto por arriba.
- **Estadísticos de primera etapa:**
  - Con un instrumento, el F efectivo (robusto, por provincia) y además el F calculado con la varianza AKM a nivel de shock.
  - Con varias variables endógenas, el F de Sanderson y Windmeijer y el rk de Kleibergen y Paap.
  - Con 33 instrumentos, el F efectivo de Montiel Olea y Pflueger con su umbral para τ = 10 %.
  - Pesos de Rotemberg también de la primera etapa: qué orígenes dan la fuerza. Sin Rumanía el F cae de 35 a 13,6 (T14).
- **Intervalos:** AR o CLR como objeto principal. El intervalo t solo si F supera el umbral de Lee et al. (2022) para el nivel elegido.
- **Sensibilidad a la composición de orígenes:** omitir un origen cada vez y un continente cada vez, informando del F y del AR de cada caso.
- **Ventanas temporales:** 2012–2019, 2015–2024, 2020–2024 y diferencias largas 2015–2019 y 2019–2024, con el F y el AR de cada una. La primera etapa en 2020–2024 tiene F = 14,0 (T9-C).
- **Instrumentos alternativos, solo si tienen justificación causal:**
  - (i) participaciones de 1998–2002 o 2001, más predeterminadas y posiblemente más débiles;
  - (ii) shocks de expulsión, a partir de entradas en otros destinos o de condiciones en el origen;
  - (iii) episodios concretos por origen (F3b).
  - **No se recomiendan:** participaciones de 2008 o 2011 elegidas por su F (86–92; T14), entradas rezagadas como instrumento, ni instrumentos espaciales o de distancia sin modelo.
- **¿Deben seguir siendo centrales las estimaciones puntuales?**
  - No cuando el conjunto AR es amplio o no está acotado. El titular debe ser el intervalo ("entre ~0 y ~0,6"), con la estimación puntual como dato secundario.
  - Cualquier magnitud de política debe calcularse sobre todo el intervalo.
  - Si el conjunto no está acotado, no se puede extraer ninguna conclusión de magnitud.

### C.10 Magnitud económica: de la elasticidad local al efecto agregado (punto 9)

**Fórmula y supuestos.** La T11 calcula $\text{cuota}=\beta\cdot M^{nac}/G^{nac}$, con $M^{nac}$ = 6,5 % de entrada acumulada y $G^{nac}$ = 20,6 puntos log del IPVA. Es decir, cuota = 0,3155·β. Exige cuatro supuestos que el texto debe declarar:

- **(A1)** La elasticidad nacional es al menos β_L. Es un supuesto del modelo (Proposición 1), no está identificado: con la exposición controlada, la elasticidad provincial tiene F = 0,3 (T15).
- **(A2)** Permanencia del nivel. Las propias proyecciones locales con covariables no detectan efecto en ningún horizonte.
- **(A3)** La composición por origen de 2015–2024 tiene la misma elasticidad que la implícita en los pesos del instrumento.
- **(A4)** No hay efectos de equilibrio general: oferta de trabajo en la construcción, renta, formación de hogares de los nativos [NI].

El diseño relativo elimina por construcción el efecto común. Es el problema del "intercepto ausente" (Chodorow-Reich, 2020; Wolf, 2023), y su signo es indeterminado fuera del modelo.

**Cuotas implicadas por las estimaciones publicadas** (cálculo propio: 0,3155·β):

| Fuente de β | β | Cuota implícita |
|---|---|---|
| AR-WCR, extremo inferior (T4-A) | 0,02 | 0,6 % |
| AR analítico, extremo inferior (T11) | 0,10 | 3,2 % |
| Provincia × año × clase de tamaño (T10-C) | 0,153 | 4,8 % |
| Sin ponderar (T3-C) | 0,181 | 5,7 % |
| Covariables, ponderado (T3-B) | 0,303 | 9,6 % |
| Controles mínimos (T3-A) | 0,539 | 17,0 % |
| AR-WCR, extremo superior (T4-A) | 0,62 | 19,6 % |
| Coeficiente de América aplicado a toda la entrada (T9-B; ilustrativo) | 0,766 | 24,2 % |
| Subperiodo 2020–2024 (T9-C) | −0,457 | negativa |

**Presentación recomendada:**

- **(1)** Un gráfico de la cuota frente a β, con bandas para cada procedimiento de inferencia y marcas para cada especificación, en lugar de una cifra puntual.
- **(2)** Una versión por subperiodos: la entrada de 2015–2019 por β(2012–2019) más la entrada de 2020–2024 por β(2020–2024), con sus intervalos. El autor dispone de las entradas por subperiodo [E].
- **(3)** Una versión ponderada por la composición observada de las entradas, con elasticidades por origen y su incertidumbre. La fila "América" de la tabla muestra que el 10 % no es robusto a la composición.
- **(4)** Magnitudes relativas, que no requieren A1–A4:
  - Pasar del percentil 10 al 90 de la entrada anual (−0,43 % → 1,42 %, es decir 1,85 pp; T1) implica 1,85 × 0,30 ≈ 0,56 pp más de crecimiento del alquiler en el año. La diferencia P90–P10 del crecimiento anual del alquiler es de 5,71 pp, así que esa diferencia de entradas equivale a ~10 % de la dispersión.
  - Una desviación típica de entrada (1,01 pp) equivale a ≈ 0,13 desviaciones típicas del crecimiento del alquiler (0,306/2,32).
- **(5)** Magnitudes en euros al mes por vivienda típica, si se obtienen niveles (SERPAVI [N]).

**Conclusiones que se mantienen con intervalos amplios o efectos heterogéneos:**

- *Se mantiene* que, bajo A1–A4 y con la elasticidad local, la entrada **no explica la mayor parte** del crecimiento del IPVA en 2015–2024: el extremo superior del intervalo está cerca del 20 %.
- *No se mantiene* que esas cifras sean "mínimos" (l. 472–473), porque A1 depende del modelo y el signo de A4 es desconocido.
- *No se mantiene* que la cifra sea "alrededor de un 10 %" como estimación precisa. Con la composición observada o con la inestabilidad temporal, el rango plausible es amplio en ambas direcciones.

---

## D. Nueva estrategia de medición de alquileres (punto 3) y de la ocupación (punto 4, en D.6)

### D.1 Qué mide el IPVA y qué precio afrontan los nuevos residentes

**Lo que dice el manuscrito [M, l. 154–163]:**

- El IPVA se construye con los rendimientos de arrendamiento declarados en el IRPF y la información catastral.
- Mide la evolución de la renta por m² de los **contratos en vigor** a composición constante.
- Excluye el alquiler informal y el de habitaciones, el País Vasco y Navarra, y desde 2022 está sujeto a topes de actualización.

**Lo que hay que verificar en la metodología del INE y documentar en el artículo:**

1. **Tipo de índice.** ¿Compara las mismas viviendas alquiladas en dos años consecutivos (índice emparejado) o son medias estratificadas a composición constante? ¿Cómo entran las viviendas que se alquilan por primera vez y cómo salen las que dejan de alquilarse? Esto decide si la conversión de vacías en alquiler (0,22 personas por inmigrante en viviendas que pasan a alquiler, T5-A) aparece en el índice.
2. **Cobertura de arrendadores.** Si la base es el IRPF, quedan fuera los arrendadores personas jurídicas, cuyo peso es mayor en Madrid y Barcelona.
3. **Unidad.** ¿Renta anual declarada? ¿Cómo se tratan los contratos de parte del año? ¿Qué superficie se usa: la construida catastral?
4. **Número de observaciones** por municipio y año, y umbrales de publicación, para construir pesos de precisión y un registro de la muestra.
5. **Cambios normativos con efecto sobre lo declarado:** las reducciones por arrendamiento de vivienda del IRPF a partir de 2024 (Ley 12/2023).

**El margen que mide frente al margen relevante para los recién llegados:**

- El precio que paga un recién llegado es la **renta de entrada**: la de un contrato nuevo, a menudo una habitación y a veces informal, por persona o por habitación.
- El IPVA es un **índice de stock**. Con una proporción de contratos que rotan en el año λ_t, su variación es aproximadamente

$$\Delta\ln R^{stock}_{t}\approx\lambda_t\big(\ln r^{nuevo}_t-\ln r^{sustituido}_t\big)+(1-\lambda_t)\,u_t,$$

  donde $u_t$ es la actualización de los contratos vigentes (IPC o tope legal). Por tanto:

- **A corto plazo,** $\beta^{stock}\approx\lambda\,\beta^{entrada}$. Si λ ronda la inversa de la duración media de los contratos, β(entrada) es varias veces β(stock). Eso hay que estimarlo, no suponerlo.
- **El índice de stock debería mostrar persistencia,** porque los aumentos en la renta de entrada quedan fijados durante el contrato. Un efecto que "no persiste" en un índice de stock exige explicación: ruido, reversión de la renta de entrada o un artefacto de composición.
- **λ cambia dentro de la muestra.** Las duraciones mínimas aumentaron con el RDL 7/2019 y las actualizaciones se toparon desde 2022. Eso altera la sensibilidad del índice entre subperiodos: es una explicación alternativa, que debe contrastarse, del resultado negativo de 2020–2024.
- **El modelo usa un precio de mercado R.** Calibrarlo con β(stock) sobrestima ε + δ′ en un factor 1/λ (amenaza 4).

### D.2 Fuentes candidatas: qué precio miden y qué hay que comprobar

| Fuente | Concepto de precio | Escala y frecuencia | Ventajas | Problemas y selección | Estado |
|---|---|---|---|---|---|
| IPVA general | Pagado, contratos en vigor, €/m² | 699 municipios y 347 distritos; anual, 2011–2024 | Cobertura amplia, administrativo, comparable | Stock; topes; sin informal ni habitaciones; posiblemente sin personas jurídicas | [M] |
| IPVA por antigüedad del contrato | Pagado, contratos nuevos frente a vigentes | **Solo provincias**; desde 2021 | Separa entrada y stock | No permite el diseño municipal; solo los años con topes | [M] |
| SERPAVI (sistema estatal de referencia) | Pagado (misma base tributaria), niveles y percentiles, €/m² y €/mes | Sección, distrito, municipio; anual (años a verificar) | Niveles; distribución (percentil 25); escala muy fina | Comparte fuente con el IPVA (no es independiente); posibles cambios metodológicos | [N] |
| Registros de fianzas autonómicos | Pagado, **contratos nuevos** | Municipio o distrito; trimestral; varía por comunidad (Cataluña, la mejor documentada) | Precio de entrada efectivo | Solo algunas comunidades; cumplimiento del depósito; comparabilidad entre comunidades | [N] |
| Anuncios (Idealista, Fotocasa) | **Ofertado**, con características; habitaciones | Geolocalizado; alta frecuencia | Hedónico; habitaciones; tiempo en el mercado | No es precio de transacción; duplicados; cuota de mercado cambiante; condiciones de uso y acceso | [N] |
| Microdatos tributarios (AEAT) con referencia catastral | Pagado, por vivienda | Vivienda; anual | Índice de alquileres repetidos; nuevos frente a vigentes por municipio | Acceso por convenio, incierto | [N] |
| ECV y EPF (microdatos) | Pagado por el hogar; carga sobre la renta | Comunidad autónoma o grado de urbanización; anual | Por país de nacimiento; sobrecarga de costes | No sirve para el diseño local | [N] |

### D.3 Comprobaciones de cobertura, comparabilidad y selección antes de usar una fuente

1. **Cobertura.** Contratos u observaciones de la fuente frente al stock en alquiler estimado (hogares en alquiler del censo) y frente al flujo esperado (stock × λ), por municipio y año.
2. **Composición.** Distribución de superficies, antigüedad y tipología frente al stock en alquiler catastral o censal.
3. **Estabilidad temporal de la cobertura.** Cuota de mercado de cada portal; cambios normativos que afecten al depósito de fianzas o a lo declarado.
4. **Selección correlacionada con el tratamiento, la comprobación decisiva.** Regresar la cobertura sobre $\tilde z_{it}$. Si las entradas predichas reducen la cobertura del mercado declarado (más informalidad u habitaciones), el índice está seleccionado en la dirección que atenúa β.
5. **Diferencia entre precio ofertado y precio de contrato.** En las zonas donde coinciden anuncios y fianzas (Cataluña) y por segmento.
6. **Alineación temporal** entre trimestres y año natural del IRPF, y emparejamiento geográfico por sección, distrito y municipio.
7. **Duplicados y anuncios republicados** en las fuentes de anuncios.

### D.4 Índice hedónico o estrategia equivalente

**Cuando haya microdatos con características** (anuncios, fianzas con referencia catastral, AEAT):

$$\ln r_{jmt}=\alpha_{mt}+\mathbf{X}_j'\boldsymbol\theta_{r(m)}+\varepsilon_{jmt},$$

- $\mathbf{X}_j$ incluye superficie (con splines), habitaciones, baños, planta, ascensor, estado, antigüedad del edificio (del catastro si se puede enlazar), tipología y amueblado. $\boldsymbol\theta$ varía por región.
- $\alpha_{mt}$ es el índice por municipio y periodo.
- **Es preferible la versión por imputación con cesta fija** (características del stock en alquiler municipal de 2011) a la de variables ficticias de tiempo, porque mantiene la cesta constante.

**Alternativas:**

- **Índice de alquileres repetidos** de la misma vivienda en contratos sucesivos, si hay identificador de vivienda. Controla la calidad no observada, pero está seleccionado hacia las viviendas que rotan.
- **Renta por persona y por habitación**, a partir de los anuncios de habitaciones. Es el precio relevante para los hogares compartidos.

### D.5 Variable principal, alternativas e interpretación

**Decisión recomendada:**

- **Variable principal para toda la muestra: el IPVA general.**
  - Es la única con cobertura nacional homogénea, frecuencia anual y escala municipal en 2011–2024, y procede de pagos efectivos.
  - Pero se reetiqueta como *renta media por m² de los contratos declarados en vigor*, y el texto deja de presentarla como el precio que afrontan los recién llegados.
- **Variable coprincipal en una submuestra de validación: la renta de contratos nuevos de los registros de fianzas** donde exista serie municipal (Cataluña como mínimo, a verificar).
  - Ahí se estima β(entrada) con el mismo diseño y se compara con β(stock) en **los mismos municipios y años**.
  - Si no fuera factible, la alternativa honesta es estimar λ con la información disponible y presentar β(entrada) = β(stock)/λ como **traducción bajo supuestos**, no como estimación.
- **Robustez:**
  - percentiles 25, 50 y 75 de SERPAVI;
  - índice hedónico de anuncios;
  - renta de habitaciones;
  - IPVA sin los municipios con contención de rentas ni 2024.

**Cómo cambia la interpretación de β con cada medida:**

| Medida | Concepto | Interpretación de β | Relación esperada si el mecanismo del artículo es correcto |
|---|---|---|---|
| Precio ofertado (anuncios) | Lo que piden los arrendadores por la unidad marginal | Presión sobre las expectativas de oferta; aproximación del coste de búsqueda en mercados tensos | β(oferta) ≥ β(contrato nuevo) |
| Pagado en contratos nuevos | Coste de entrada en el mercado formal | La más cercana al R del modelo; coste para quien llega o se muda | β(nuevo) > β(stock) |
| Pagado en contratos en vigor (IPVA) | Coste medio de todos los inquilinos | Efecto sobre la renta pagada por el inquilino medio; suavizado y rezagado | β(stock) ≈ λ·β(nuevo) a corto plazo; acumulativo a medio plazo |
| Coste de acceso | Renta más garantías, honorarios y barreras documentales | Coste efectivo de acceder; incluye el racionamiento no en precios | No medido [NI]; aproximaciones: rentas de habitaciones, informalidad |
| Por m² frente a por persona o habitación | El precio por m² no recoge cambios en el espacio consumido | Si los hogares comparten, el coste por persona puede caer aunque suba el €/m² | Hay que reportar ambos cuando sea posible |

---

### D.6 Medición de la ocupación y del hacinamiento (punto 4)

#### D.6.1 Seis conceptos que el artículo debe separar

| Concepto | Definición operativa | ¿Lo mide hoy el artículo? | Datos para medirlo |
|---|---|---|---|
| Ocupación residencial | Personas por vivienda ocupada | Sí (censos; registro y catastro, este último sobre stock **total**) | [M] |
| Hacinamiento | Habitaciones por debajo de una norma (definición de Eurostat según composición del hogar) | No (solo EU-SILC nacional, descriptivo) | Microdatos censales 2011 (habitaciones) [N]; ECV [N]; verificar si el censo 2021 tiene habitaciones |
| Compartir por elección | Pisos compartidos o corresidencia en red por preferencia | No [NI con los datos actuales] | Encuestas con motivo; tipo de hogar |
| Compartir por restricción | Compartir por asequibilidad, documentación o discriminación | No | Respuesta de la ocupación al precio (término η·β_L); renta del hogar; evidencia experimental de discriminación en el alquiler en España (por ejemplo Bosch, Carnero y Farré, 2010) |
| Cambios en la composición de los hogares | Reagrupación, nacimientos, envejecimiento, tamaño por origen | Implícitamente, mezclado con la ocupación | Descomposición de C.7; Movimiento Natural de la Población [N] |
| Cambios en el tamaño y uso del parque | Vacías y secundarias que pasan a uso; subdivisiones; locales convertidos en vivienda | Parcialmente (conversión imprecisa) | Catastro (subdivisiones registradas) [E]; censo |

#### D.6.2 Resultados adicionales propuestos según la disponibilidad de datos

- **Personas por habitación y por dormitorio:** censo 2011 (microdatos) y ECV [N].
- **Hogares por vivienda.**
  - Solo es medible en 2011. En el censo de 2021, el hogar se construye con las inscripciones del Padrón en cada vivienda (nota 1, p. 21), así que es, por construcción, uno por vivienda (a verificar).
  - Por tanto, en 2021 los hogares compartidos aparecen como hogares más grandes. Esto es una razón más para no comparar 2011 y 2021 sin ajustes.
- **Tasa de hacinamiento según la norma de Eurostat:** ECV por comunidad autónoma y año; censo 2011 por municipio con microdatos [N].
- **Sobrecarga del coste de la vivienda** (más del 40 % de la renta disponible): ECV por país de nacimiento [N].
- **Acceso a vivienda independiente:** tasas de jefatura de hogar por edad, y jóvenes nacidos en España que viven con sus padres (EPA [N]). Es un margen de "hacinamiento" de los nativos que el artículo no considera.
- **Diferencias entre nacidos en España y en el extranjero:** ocupación por grupo con datos ecológicos [E] o microdatos [N].

#### D.6.3 ¿Se identifica el efecto sobre la ocupación con el mismo instrumento?

- **En principio sí:** la forma reducida sobre cualquier resultado está identificada si el instrumento es válido para ese resultado.
- **Pero la exclusión es específica de cada resultado.** Las participaciones de 2003 predicen dinámicas de ocupación **independientes** de las nuevas llegadas:
  - nacimientos en hogares inmigrantes ya asentados (sus hijos son "nacidos en España");
  - reagrupación (que sí entra en el flujo);
  - envejecimiento de los nativos, que reduce el tamaño de los hogares;
  - la ruptura de medición entre 2011 y 2021, si la calidad del Padrón se correlaciona con la exposición.
- **Requisitos:**
  - (i) controlar los nacimientos por nacionalidad de la madre y la estructura por edades de 2011 × año [N y E];
  - (ii) usar como principal la serie anual coherente (registro y catastro), sabiendo que mide población por vivienda **total**;
  - (iii) comprobar en 2021 si el instrumento predice la discrepancia entre la ocupación censal y la de registro y catastro.

#### D.6.4 Cómo evitar inferir un empeoramiento del bienestar sin evidencia

- Hablar de **"mayor ocupación"**, no de *crowding* ni de "coste".
- Recordar que ocupar viviendas antes vacías es un **uso más intensivo de un stock ocioso**, potencialmente eficiente.
- Para hablar de un coste de bienestar haría falta mostrar, en este orden:
  - (a) que la ocupación aumenta **dentro** de cada grupo, no solo por composición;
  - (b) que supera normas de hacinamiento;
  - (c) que responde al precio o se concentra en hogares con restricciones de renta o de acceso;
  - (d) idealmente, consecuencias como salud, escolarización o movilidad laboral.
- Con los datos actuales solo es abordable una parte de (a), mediante la descomposición ecológica. Lo demás es [N] o [NI].
- **Formulación propuesta:** *"A large part of the adjustment takes place through more intensive use of the existing stock. Higher occupancy partly reflects the larger households of newcomers; our data do not allow us to determine whether, or for whom, it reflects overcrowding or a welfare loss."*

---

## E. Matriz de pruebas de robustez

Prioridad: **A** = imprescindible; **M** = muy importante; **B** = deseable. "Datos" indica [E] o [N].

| # | Prueba | Amenaza que aborda | Implementación | Resultado preocupante | Prio. | Efecto posible sobre la interpretación |
|---|---|---|---|---|---|---|
| 1 | Estadísticos de los shocks y número efectivo (origen y origen × año), autocorrelación y correlación dentro de continente [E] | Pocos shocks; dependencia | Tabla al estilo BHJ | 1/HHI bajo; un origen con más del 20 % del peso; correlación intra-continente alta | A | Apoyarse en aleatorización y AKM0; hablar de "pocos contrastes efectivos" |
| 2 | Pesos de Rotemberg completos (33) y gráfico de β_o frente a F_o [E] | Dependencia de pocos orígenes; heterogeneidad | Goldsmith-Pinkham et al. (2020) | Gran parte de β procede de orígenes con poco peso y β_o extremos (ya sugerido: ≈ 0,19 de 0,303 fuera de los seis primeros) | A | El "efecto" es específico de una combinación de orígenes |
| 3 | LIML con las 33 participaciones y prueba J [E] | Heterogeneidad o participaciones inválidas | 2SLS frente a LIML; prueba J robusta | Rechazo y LIML ≠ 2SLS | M | Heterogeneidad: el estimando depende de la composición |
| 4 | Controles sectoriales, de litoral y de turismo previo × año [E/N] | Confusión por la demanda local asociada a las participaciones | Añadir a (1) | β cae hacia 0 o cambia de signo | A | El 0,30 sería una tendencia por tipo de municipio |
| 5 | Provincia × clase de tamaño × año ([M] 0,153) | Tendencias ligadas al tamaño | Ya hecho; añadir AR, AKM0 y aleatorización | Ya preocupante: no significativo | A | El titular debe ser el rango 0,15–0,30 o explicar por qué el contraste ciudad–periferia es válido |
| 6 | Área urbana funcional × año [E/N] | Definición del mercado | Efectos fijos por área urbana | Cambio sustancial | M | Precisa el mercado relevante (Proposición 1) |
| 7 | Diseño dentro de continente con AR por aleatorización ([M] F = 4,5; AR [−0,06, ∞)) | Contraste entre continentes | Estratos fijados ex ante; publicar primero el AR | AR incluye el 0 (ya ocurre) | A | La afirmación causal queda condicionada al supuesto de A.3, que debe hacerse explícito |
| 8 | Estudios de evento por origen con shocks de expulsión (F3b) [E] | Endogeneidad de los shocks; contraste entre continentes | Colombia/Perú 2016, Venezuela, Ucrania 2022 frente a otros orígenes del mismo continente | Adelantos ≠ 0; primera etapa nula | A/M | Si superan la prueba, es la evidencia causal más limpia del artículo |
| 9 | Shocks alternativos (entradas a otros destinos; condiciones en el origen) [N] | Atracción española | Sustituir $g_{ot}$ | β distinto; F débil | M | Separa expulsión de atracción |
| 10 | Equilibrio y tendencias previas a nivel de shock [E] | Exogeneidad de los shocks | Regresar $g_{ot}$ sobre medias ponderadas por exposición de características y tendencias previas | Correlación significativa | A | Invalida la lectura basada en shocks |
| 11 | Placebo de shocks futuros en rentas 2011–2014 (F1) [E] | Tendencias previas | Ec. F1 | θ comparable a la forma reducida | A | Hay que restringir o abandonar la afirmación causal |
| 12 | Resultados anteriores a 2011 (F2) [E/N] | Tendencias previas en precios, empleo y población | Ec. F2 | Coeficientes significativos | A | Ídem |
| 13 | Proyecciones locales con rezagos extra, adelantos conjuntos y sensibilidad tipo Rambachan–Roth (F4) [E] | Confusión dinámica | Ec. F4, muestra equilibrada | Adelantos persistentes; M̄ de ruptura pequeño | A | El efecto del año de llegada no es creíble |
| 14 | Crítica JRS: control del *boom* y correlación entre entradas predichas (D2, D3) [E] | Confusión entre corto y largo plazo | Ver C.6 | Correlación muy alta, o β cae al controlar el *boom* | A | El estimando no distingue llegada de legado |
| 15 | Reconciliar efectos fijos municipales (0,593) con la proyección local en h = 0 (−0,029) (D4) [E] | Coherencia interna | Misma muestra | Discrepancia sin explicar | A | Hay que elegir y justificar el estimando titular |
| 16 | Interacción por subperiodo y simetría entre entradas y salidas (F8) [E] | Inestabilidad del parámetro | Modelo combinado | Diferencia significativa (t ≈ 2,4 aproximado) | A | No hay elasticidad única; la T11 debe hacerse por periodo |
| 17 | Contención de rentas y zonas tensionadas; excluir 2024 [N, lista pública] | Política dentro de la provincia | Control × año o exclusión | β cambia, sobre todo en 2020–2024 | A (barata) | Explica (o no) el signo negativo reciente |
| 18 | Pesos: hogares en alquiler, sin ponderar, precisión [E] | Estimando | C.3 | Cambio de signo o de tamaño | A | Heterogeneidad explícita por tamaño |
| 19 | Omitir una provincia, comunidad u origen cada vez (gráfico de bosque) [E] | Observaciones influyentes | F7 | Una unidad determina el resultado | M | Hay que acotar el ámbito |
| 20 | AKM0, aleatorización por estratos, WCR, tF [E] | Exposición, pocos conglomerados, instrumento débil | C.4 | El intervalo incluye el 0 | A | Cambia el titular de inferencia |
| 21 | Equivalencia BHJ (0,234 frente a 0,303) [E] | Implementación | BHJ (2022), Prop. 1 | No coinciden | A (barata) | Error de código o de especificación |
| 22 | Controles de 2001; quitar la renta de 2015 [E/N] | Malos controles | C.3 | β cambia | M | Hay que elegir un conjunto predeterminado |
| 23 | Ocupación predicha por composición frente a observada (C.7) [E] | Composición frente a hacinamiento | Descomposición | Observada ≈ composición | A | Retirar *crowding*; cambiar el título |
| 24 | Intervalos para las cuotas de absorción (Fieller y *bootstrap* en sistema conjunto) [E] | Precisión | C.4, C.7 | El intervalo cubre de ~30 % a más del 100 % | A | "Más de la mitad" pasa a ser "una parte importante, imprecisa" |
| 25 | Coherencia entre registro y censo en 2021 [E] | Ruptura de medición | Comparar ambas medidas de ocupación y regresar la discrepancia sobre $\tilde z$ | La discrepancia se correlaciona con $\tilde z$ | M | La ocupación censal 2011–2021 no es fiable para este fin |
| 26 | Movimiento natural de los nacidos en España (nacimientos y defunciones) [N] | Desplazamiento mal medido | MI-5 | El componente natural explica la "salida" | M | Hay que reinterpretar la relocalización |
| 27 | Salidas de nativos por destino (EVR) [N] | Relocalización y difusión | MI-3 | Salidas hacia la misma provincia proporcionales a la entrada | M | Contrasta la Proposición 1 |
| 28 | Proyecciones locales del stock a 5–8 años y licencias [E/N] | Horizonte de la oferta | MI-7 | Respuesta positiva a largo plazo | M | Matiza "el stock no respondió" |
| 29 | Cobertura del índice tributario frente a $\tilde z$ [N] | Selección en el resultado | D.3.4 | $\tilde z$ predice menor cobertura | M | β atenuado por informalidad |
| 30 | Validación con contratos nuevos (fianzas) [N] | Medición del precio | D.5 | β(nuevo) ≈ β(stock), en contra de la lógica de la rotación, o β(nuevo) mucho mayor | M | Recalibrar el modelo y la magnitud |
| 31 | Participaciones placebo permutadas y pseudo-participaciones (F5) [E] | Exposición genérica | F5 | La pseudo-participación reproduce ρ | M | El efecto opera por observables, no por redes |
| 32 | Control negativo: mortalidad de nativos mayores de 65 (F6) [N] | Confusión demográfica | F6 | Coeficiente significativo | B | Los resultados de población y ocupación están contaminados |

**Cómo leer la matriz.**

- Robustez no es acumular especificaciones. Cada fila responde a una amenaza concreta.
- La conclusión debe depender del subconjunto de filas A, no del número de filas "superadas".
- Las filas 5, 7, 13 y 16 ya tienen resultados [M] preocupantes. Las revisiones deben **explicarlos o incorporarlos a la interpretación**, no compensarlos con nuevas especificaciones favorables.

---

## F. Nueva estructura del artículo

**Título (alternativas):**

- *Immigration, Rents and Housing Occupancy: Evidence from Spain*
- *How Spain Housed Its Newcomers: Immigration, Rents and the Use of the Housing Stock*
- *Higher Occupancy, Modest Relative Rent Effects: Immigration and Housing in Spain*. Úsese solo si las pruebas A lo sostienen.

**Secciones:**

1. **Introducción.** Pregunta; diseño; resultados **con intervalos**; qué está y qué no está identificado; contribución.
2. **Contexto institucional y datos.**
   - Mercado de alquiler español: tenencia; duración de contratos (RDL 7/2019); topes de actualización (RDL 6/2022, Ley 12/2023); contención en Cataluña; zonas tensionadas.
   - Llegadas de 2015–2024 por origen.
   - Fuentes: Padrón y estadística continua; IPVA; censo; catastro.
3. **Medición.**
   - 3.1 Qué mide el IPVA y su relación con el precio de entrada (rotación).
   - 3.2 Ocupación frente a hacinamiento; la ruptura entre los censos de 2011 y 2021.
   - 3.3 Validación en la submuestra con contratos nuevos (si existe).
4. **Marco conceptual (resumido).** Modelo con ocupación endógena y tenencia. Qué momentos se identifican en forma reducida y qué parámetros dependen del modelo.
5. **Diseño empírico.**
   - Instrumento; representación a nivel de shock; supuesto de identificación enunciado para este diseño.
   - Estadísticos de los shocks; pesos de Rotemberg; equilibrio.
   - Inferencia (C.4).
   - Especificación central fijada ex ante.
6. **Efectos sobre los alquileres.** Forma reducida, primera etapa y 2SLS; diferencias largas; conjuntos AR, AKM0 y por aleatorización.
7. **Validez.**
   - Tendencias previas (F1–F4); estudios de evento por origen (F3b); shocks alternativos.
   - Diseño dentro de continente; estabilidad temporal y simetría; exclusiones (gráfico de bosque).
8. **Márgenes de ajuste.** Sistema conjunto: población, stock, ocupación (composición frente a intra-grupo), tenencia, relocalización de nativos.
9. **Heterogeneidad preespecificada.**
10. **Magnitudes: de lo local a lo agregado.** Cuota en función de β; supuestos A1–A4; por subperiodo y composición; magnitudes relativas.
11. **Discusión e implicaciones** (ver G).
12. **Conclusión.**

**Tablas y figuras propuestas:**

| N.º | Contenido | Sustituye o amplía |
|---|---|---|
| Fig. 1 | Hechos nacionales (sin cambios) más la serie de llegadas por continente | Fig. 1 |
| Fig. 2 | Mapas de entrada, alquiler y **exposición predicha** | Fig. 2 |
| T1 | Descriptivos más el registro de la muestra (municipios y observaciones en cada paso) | T1 |
| T2 | Estadísticos de los shocks y equilibrio a nivel de shock | Nueva |
| Fig. 3 | Pesos de Rotemberg y β_o frente a F_o (33 orígenes) | T4-C |
| T3 | Resultado principal: ρ, π, β, F y cuatro intervalos, con las especificaciones central, sin ponderar, por tamaño y dentro de continente | T3 y T4 |
| Fig. 4 | Proyecciones locales con adelantos (misma muestra), prueba conjunta y M̄ de ruptura | Fig. 4 y T13 |
| T4 | Falsificación: F1, F2, F3a, F5 y F8 | Nueva |
| Fig. 5 | Estudios de evento por origen con shocks de expulsión (F3b) | Nueva |
| Fig. 6 | Gráfico de bosque de exclusiones y especificaciones | T14 |
| T5 | Márgenes de ajuste, sistema conjunto, con intervalos de Fieller para las cuotas | T5 |
| T6 | Composición frente a ocupación intra-grupo | Nueva |
| T7 | Heterogeneidad preespecificada con valores q | T9 y T10 |
| Fig. 7 | Cuota agregada en función de β, con bandas | T11 |
| Apéndice | Modelo; calibración con conjuntos identificados; difusión espacial con potencia; escala (armonizada); segmentos provinciales del IPVA (descriptivos) | T6, T7, T8, T15 |

---

## G. Cambios concretos en el texto (punto 11)

Las formulaciones alternativas están en inglés, el idioma del manuscrito, para poder incorporarlas directamente. Los intervalos que aparecen entre corchetes con "[to be computed]" corresponden a análisis propuestos que aún no se han hecho.

### G.1 Afirmaciones que deben reescribirse, matizarse o retirarse

| # | Ubicación | Texto actual (resumido) | Problema | Propuesta | Acción |
|---|---|---|---|---|---|
| 1 | Título | *Absorbed by Crowding* | Afirma hacinamiento (con carga de bienestar) como mecanismo principal, sin medirlo | Ver alternativas en F | Reescribir |
| 2 | Resumen | "raises local rents by about 0.3 % in the year of arrival" | Es un efecto relativo, sobre un índice de stock, frágil a la especificación | *"Within provinces, an inflow equal to 1% of the population is associated with an increase of about 0.3% in the average rent of declared contracts in force in the year of arrival (weak-IV-robust 95% interval: 0.02–0.62)."* | Matizar |
| 3 | Resumen; l. 38 | "the effect does not persist" | Con covariables no hay efecto en ningún horizonte, tampoco en h = 0 (T13) | *"We cannot detect effects beyond the arrival year; with baseline covariates, estimates identified from innovations in the instrument are close to zero at all horizons."* | Matizar |
| 4 | Resumen; l. 39 | "does not spread to neighbouring municipalities" | Ausencia de significación ≠ ausencia de efecto. Los intervalos llegan a 0,26 (contiguos: 0,060 + 1,96·0,101) y 0,29 (anillo de 0–15 km) | *"We find no detectable effect of inflows into neighbouring municipalities on a municipality's rent relative to its province; the confidence intervals do not rule out spillovers of a size comparable to the own effect."* | Matizar |
| 5 | Resumen; l. 39–41 | "is not larger in big cities" | Diferencia capitales–resto −0,138 (0,114), no significativa. Además, la identificación descansa en el contraste ciudad–periferia | *"Point estimates are smaller in larger municipalities, but differences across size classes are imprecise, and the design does not identify market-wide effects, which is where pressure in large cities would appear."* | Matizar |
| 6 | Resumen; l. 42–44 | "Over half of the added population was absorbed by more persons per dwelling" | La cuota varía del 37 % al más del 300 % según la especificación, no tiene intervalo, cruza la ruptura censal y es sobre todo composición | *"Between the 2011 and 2021 censuses, a substantial but imprecisely estimated share of the net population increase [interval to be computed] is accounted for by higher persons per primary dwelling, largely reflecting the larger households of newcomers."* | Matizar |
| 7 | Resumen | "the housing stock did not respond" | Solo vale a corto plazo y para el stock registrado | *"The registered (cadastral) housing stock shows no detectable short-run response (elasticity −0.10, s.e. 0.08)."* | Matizar |
| 8 | Resumen; l. 50–52; l. 515–516 | "Immigration explains about a tenth of rent growth … up to one fifth under cross-province associations" | Elasticidad relativa aplicada a la entrada nacional; supuestos A1–A4; las asociaciones entre provincias no están identificadas | *"Under explicit assumptions — that the within-province elasticity applies nationally and that effects are permanent — the estimates imply that immigration accounts for between about 1 and 20 percent of national rent-index growth in 2015–2024; the data cannot rule out smaller contributions in 2020–2024."* Eliminar las cifras entre provincias | Matizar y retirar |
| 9 | Resumen (última frase) | "The main adjustment is crowding, a cost that rent indices miss." | "Coste" no está demostrado; *crowding* no está medido | *"A large part of the adjustment takes place through more intensive use of the existing stock — margins that rent indices do not capture."* | Reescribir |
| 10 | l. 15–16 | "demographic pressure has been absorbed mainly through more persons per dwelling and only to a small extent through higher relative rents" | Compara un efecto relativo con un margen agregado; "mainly" no está establecido | *"Our estimates suggest that a large part of the demographic pressure was accommodated within the existing stock, while effects on relative rents of contracts in force were modest and imprecisely estimated."* | Matizar |
| 11 | l. 205–206; 307–308; 353–356 | El adelanto en h = −2 refleja "selection towards affordable housing" | El instrumento no lo eligen los migrantes; un adelanto del instrumento indica correlación con la dinámica local o efectos de shocks previos | *"The instrument's innovation is associated with lower rent growth in the preceding year. Because the instrument is not chosen by migrants, this pattern cannot reflect selection; it indicates either correlation between exposure and local rent dynamics or effects of earlier shocks. We address it in Section X."* | Reescribir |
| 12 | l. 232–233 | Los controles "are measured before the migration wave, so they cannot be a consequence of it" | La renta de 2015 es posterior al inicio de la muestra (2012) | Sustituir el control y decir: *"All controls are measured in 2011 or earlier."* | Corregir |
| 13 | l. 314–315 | "does not predict rent growth in 2012–2014, before the migration wave" | 2012–2014 forma parte de la muestra y fueron años de salidas netas | *"Because 2012–2014 is part of the estimation sample and a period of net outflows, it is not a pre-period; Section X reports tests based on genuine pre-periods."* | Reescribir |
| 14 | l. 326–327 | 15,8 orígenes efectivos, "enough for the asymptotic approximation" | Es moderado, con correlación intra-continente y persistencia | *"The effective number of origins (15.8) is moderate; we therefore rely primarily on randomisation inference and null-imposed AKM0 intervals."* | Matizar |
| 15 | l. 342–343 | "Both sources of variation give the same sign" | Dentro de continente el AR-WCR incluye el 0 y no está acotado | *"Within-continent variation yields a positive but imprecise estimate whose weak-IV-robust interval includes zero and is unbounded above; the main estimate therefore rests on cross-continent contrasts in 2003 settlement, and its causal interpretation requires that ... [state the assumption]."* | Reescribir |
| 16 | l. 372–374 | "The result does not depend on the change in method between the two censuses." | La serie de registro y catastro mide población por vivienda **total**: confirma la absorción en el stock, no el hacinamiento | *"The register–cadastre series confirms that additional population was housed within the existing registered stock; it does not distinguish between higher occupancy of occupied dwellings and the occupation of previously vacant ones."* | Reescribir |
| 17 | l. 384–389 | La conversión pesa más que la salida de residentes; "highly elastic non-price margins" | Intervalos de ε [−0,95, 10,69] y δ′ [−3,04, 8,00] | *"The split of ε+δ′ into supply and mobility is not informative given the bootstrap intervals."* | Retirar la afirmación |
| 18 | l. 407–411 | La presión "spreads evenly across the provincial market"; la evidencia MCO "favours the second reading" | Las asociaciones MCO con la entrada del resto de la provincia no son causales | Retirar o reformular como asociación descriptiva | Retirar |
| 19 | l. 449–452; 491–493 | Los contratos nuevos responden 2,4 veces más; los topes desplazan el ajuste y perjudican a quien busca vivienda | Diseño provincial no identificado (T15), solo 2022–2024, sin comparación previa a los topes y sin prueba de la diferencia | Pasar a un apéndice descriptivo; retirar de las implicaciones de política | Retirar |
| 20 | l. 469–473 | "Since the local elasticity is a lower bound … these figures are minima" | Es una cota inferior solo dentro del modelo (A1), y A4 tiene signo desconocido | *"Within the model, the local elasticity is a lower bound on the market elasticity; outside it, general-equilibrium effects of unknown sign mean that these figures should not be read as bounds."* | Matizar |
| 21 | l. 482–484 | El coste "falls on immigrants themselves and on poorer households" | No hay evidencia por renta | *"Higher occupancy is concentrated among foreign-born households; whether it also affects lower-income native households cannot be assessed with these data."* (solo si C.7 lo muestra) | Matizar o retirar |
| 22 | l. 487–489 | Movilizar viviendas vacías es "the only supply margin that currently responds" | Conversión 0,82 (0,53), imprecisa | *"The data are consistent with the occupation of previously vacant or secondary dwellings, but this margin is imprecisely estimated."* | Matizar |
| 23 | l. 490–491 | "The relevant scale for policy is the provincial or metropolitan market, because pressure spreads within each market without a distance gradient" | La escala de mercado no está identificada | *"Our design identifies relative effects within provinces; market-level effects, which matter most for policy, are not identified."* | Reescribir |
| 24 | l. 493–494; 424–426 | La presión depende de la tenencia de cada origen | El orden África > América contradice el orden κ·ρ del modelo, y los intervalos se solapan | *"Point estimates differ by region of birth, but differences are imprecise and their ranking does not match the model's prediction based on household size and tenure."* | Matizar |
| 25 | l. 48–50; 175–178 | Duplicación del hacinamiento entre extranjeros (EU-SILC) | Es nacional y descriptivo, sin vínculo causal con las entradas locales | Presentarlo como contexto, no como evidencia del mecanismo | Matizar |
| 26 | Tabla 11, nota | "6.5 % between 2016 and 2024" frente a "2015–2024" en el texto | Inconsistencia | Unificar | Corregir |

### G.2 Clasificación de las conclusiones

**Respaldadas directamente por las estimaciones,** condicionadas a la validez del instrumento y con los matices de A.3:

- En 2012–2019 y en la muestra ponderada, una mayor entrada predicha se asocia con un mayor crecimiento contemporáneo del índice de contratos declarados en vigor, relativo a la provincia. El intervalo robusto a instrumentos débiles excluye el cero en la especificación ponderada con covariables.
- A corto plazo, la población adicional se aloja en el parque registrado existente. El stock catastral no muestra una respuesta detectable.
- Entre 2011 y 2021, las personas por vivienda principal aumentan con la entrada predicha. El coeficiente es estable entre especificaciones (0,45–0,51 personas por inmigrante), aunque hay que tener en cuenta la ruptura censal.

**Compatibles con los resultados, pero no demostradas:**

- Que la presión se difunda por el mercado provincial.
- Que la elasticidad local sea una cota inferior de la de mercado.
- Que el efecto sobre la renta de entrada sea mayor que sobre el stock.
- Que la conversión de viviendas vacías sea el principal margen de oferta.
- Que la relocalización de nativos sea lenta y moderada.
- Que la mayor ocupación refleje restricciones y no preferencias.
- Que los efectos sean mayores para orígenes que alquilan más.

**Deben eliminarse o matizarse sustancialmente:**

- Que el ajuste principal sea el **hacinamiento**.
- Que ese ajuste sea un **coste** que los índices no captan.
- Que "más de la mitad" se absorba por hacinamiento.
- Que la inmigración explique "un décimo" o "hasta un quinto" del crecimiento del alquiler.
- Que los topes a la actualización desplacen el ajuste hacia los contratos nuevos (elasticidad 2,4 veces mayor).
- Que la escala relevante para la política sea la provincia porque la presión se difunde sin gradiente.
- Que el efecto "no persista" y "no se difunda" (en lugar de "no detectado").
- Que el coste recaiga en los hogares pobres.

### G.3 Resumen propuesto (en inglés; solo usa resultados ya publicados en el manuscrito)

> Spain's foreign-born population grew by more than three million between 2015 and 2025 while the official rent index rose by about a fifth. Using tax-based rent indices for 699 municipalities, population registers by country of birth, census tracts and the cadastre, I study how local rents and the use of the housing stock respond to immigrant inflows predicted from the 2003 settlement of 33 origin groups. Within provinces, an inflow equal to 1% of the population is associated with an increase of about 0.3% in the average rent of declared contracts in force in the year of arrival (weak-IV-robust 95% interval: 0.02–0.62). This estimate rests mainly on differences between municipalities settled by Latin American and African versus European immigrants; it is smaller and imprecise when comparisons are restricted to municipalities of similar size, and imprecise when only within-continent variation is used. Additional population is accommodated within the existing registered stock, which shows no detectable short-run response. Persons per dwelling rise with inflows, partly because newcomers live in larger households; the data do not allow us to determine how much of this reflects overcrowding. Under explicit assumptions, the estimates imply that immigration accounts for a minority of national rent growth in 2015–2024, between about 1 and 20 percent.

*(Si las pruebas de B.1 refuerzan el resultado, la frase "rests mainly on…" puede sustituirse por la descripción de la evidencia nueva. Si lo debilitan, el resumen debe decirlo.)*

### G.4 Conclusión propuesta (en inglés)

> Immigration after 2015 increased housing demand in Spain. In the short run, this demand was accommodated mostly within the existing stock: registered population per dwelling rose with inflows and the registered stock did not respond detectably. Within provinces, rents of declared contracts in force rose modestly in municipalities receiving larger predicted inflows, but this relative effect is imprecisely estimated, relies mainly on contrasts between municipalities settled by different continental origin groups, and is not stable over time; in 2020–2024, a period of rent caps and the largest inflows, it cannot be detected. The paper therefore does not identify the effect of immigration on the national level of rents; under the assumption that the local elasticity applies nationally, immigration accounts for a minority of rent growth. Higher occupancy is a quantitatively important margin of adjustment that rent indices do not capture. Part of it reflects the household structure of newcomers and part may reflect affordability constraints; distinguishing them, and assessing their welfare consequences, requires data on rooms, entry rents and household composition that are not yet available at the local level. Measuring these margins regularly — entry rents, room rents and occupancy relative to dwelling size — would make it possible to answer the question this paper poses with greater precision.

---

## H. Límites que no pueden resolverse

Estos problemas seguirían abiertos aunque se aplicara todo el plan. Deben declararse como tales.

1. **La elasticidad de mercado y el efecto nacional [NI].**
   - Con 42–48 provincias y la exposición controlada, el *shift-share* no tiene fuerza (F = 0,3).
   - Los efectos de equilibrio general (oferta de trabajo en la construcción, renta, formación de hogares, emigración de nativos) no están identificados.
   - Cualquier cifra agregada es contabilidad condicionada a supuestos.
2. **La exclusión no se puede contrastar.**
   - Las pruebas de B.1 contrastan implicaciones, no el supuesto.
   - Con pocos contrastes efectivos, siempre habrá factores de confusión por tipo de municipio que no puedan descartarse del todo.
3. **El alquiler informal y el de habitaciones** quedan fuera de las fuentes tributarias. Ninguna fuente pública conocida los mide con escala municipal y cobertura nacional. Los anuncios de habitaciones son una aproximación parcial y seleccionada.
4. **El precio de entrada a escala municipal en toda España** solo existe parcialmente (fianzas en algunas comunidades). Fuera de ellas, β(entrada) solo puede inferirse con supuestos sobre la rotación.
5. **Las consecuencias de bienestar de la mayor ocupación [NI]** con datos agregados. Distinguir preferencia de restricción requiere microdatos con habitaciones, renta, composición y, idealmente, información sobre el motivo de compartir.
6. **La comparabilidad entre los censos de 2011 y 2021** está limitada por el cambio de método. Los hogares de 2021 se construyen desde el Padrón y la ocupación incorpora su calidad. No hay forma de reconstruir hacia atrás el concepto de 2021 ni hacia delante el de 2011.
7. **Población no registrada o mal registrada.** Inscripciones sin residencia efectiva, la falta de inscripción de una parte de los recién llegados y las bajas administrativas introducen error de medida en el tratamiento, posiblemente distinto por origen.
8. **Las políticas simultáneas** (topes, contención, zonas tensionadas, regulación turística) coinciden en el tiempo y en el espacio con las mayores llegadas de 2020–2024. Separar sus efectos con un único instrumento es, en el mejor caso, parcial.
9. **Validez externa.** Quedan fuera el País Vasco, Navarra y los municipios de menos de 10.000 habitantes (un 25 % de la población, l. 196–197), donde se concentra parte de la inmigración agrícola.
10. **Los parámetros del modelo** son cocientes de estimaciones ruidosas. Con los datos disponibles solo admiten conjuntos identificados amplios, no estimaciones puntuales.

---

## I. Hoja de ruta ejecutable

### I.1 Secuencia por etapas

| Etapa | Tareas (IDs de B, C y E) | Datos | Coste | Depende de | Resultado |
|---|---|---|---|---|---|
| **0. Auditoría** (1–2 semanas) | Registro de la muestra (8.118 → municipios con IPVA → 42 provincias → 699; 9.087 → 9.060 observaciones; 1.268 en el censo; 700 frente a 699); documentación del IPVA (I-6); equivalencia BHJ (E21); armonizar muestras entre tablas, proyecciones locales y especificación base (E15); fijar **por escrito** la especificación central, los pesos, los estratos de permutación y las familias de heterogeneidad **antes** de ejecutar lo nuevo (por ejemplo, con un registro fechado en Zenodo u OSF) | [E] | Bajo | — | Base auditada y plan de análisis registrado |
| **1A. Inferencia y diagnósticos de shocks** (2–3 semanas) | AKM0; aleatorización dentro de estratos; WCR; tF; F de Sanderson y Windmeijer (I-5, E20); estadísticos de shocks, Rotemberg completo, LIML y prueba J, equilibrio a nivel de shock (I-1, E1–3, E10) | [E] | Bajo | 0 | Saber qué variación identifica y con qué inferencia |
| **1B. Validez temporal** (2–4 semanas) | F1, F3a, F4 con rezagos extra y prueba conjunta; JRS (D1–D4); subperiodos y simetría (F8); exclusión de 2024 (I-2 a I-4; E11, E13–16) | [E] | Bajo–medio | 0, 1A | Decide si el titular es "efecto en el año de llegada" |
| **1C. Confusión por tipo de municipio** (2 semanas) | Controles sectoriales, de litoral y de turismo previo × año; provincia × tamaño × año; área urbana × año; pseudo-participaciones y participaciones permutadas (F5); gráfico de bosque de exclusiones (E4–6, E19, E31) | [E] (sectores de 2011 si el censo los publica por municipio) | Bajo | 1A | Decide si el 0,30 es inmigración o tipo de municipio |
| **1D. Estudios de evento por origen** (2–3 semanas) | F3b: Colombia/Perú 2016, Venezuela, Ucrania 2022, dentro de cada continente (MI-1, E8) | [E] | Medio | 1A | Posible evidencia causal más limpia |
| **1E. Ocupación con los datos actuales** (2 semanas) | Sistema conjunto; Fieller y *bootstrap*; composición predicha con los $h_g$ de 2011; registro frente a censo en 2021 (I-7; E23–25) | [E] | Bajo–medio | 0 | Cuota con intervalo; composición frente a intra-grupo |
| **1F. Reescritura** (1–2 semanas) | Magnitudes (I-8, C.10); texto (G); estructura (F) | — | Bajo | 1A–1E | Manuscrito alineado con la evidencia |
| **2. Datos públicos nuevos** (1–3 meses) | EVR (MI-3); participaciones de 2001 o 1998–2002 (MI-4); resultados previos a 2011 (F2); Movimiento Natural (MI-5); SERPAVI (MI-6); Eurostat y OCDE para shocks alternativos (MI-2); listas de municipios con contención o tensionados (I-4); controles de 2001 (I-9); MDT, costa y espacios protegidos para la oferta (H1); stock a largo plazo y licencias (MI-7); fianzas de Cataluña (D-1) | [N] | Medio | 1 | Refuerzo de tendencias previas, mecanismos y precio de entrada |
| **3. Datos costosos o inciertos** (3–12 meses) | Microdatos de anuncios (D-2); microdatos de la AEAT; microdatos censales con habitaciones (D-3); ECV y EPF (D-4); EPA para emancipación (D-5); centros colectivos (D-6); compras por nacionalidad (D-7) | [N] | Alto | 2 | Hacinamiento propiamente dicho; bienestar; precio de entrada nacional |

**Puntos de decisión tras la etapa 1:**

- **Si F1, F3a y F4 no muestran tendencias previas, β sobrevive a 1C y los estudios de evento (1D) confirman el signo:**
  - Mantener la afirmación causal sobre el índice de stock relativo.
  - Presentar la variación entre continentes como validada indirectamente.
- **Si el efecto solo sobrevive con la variación entre continentes y falla 1B o 1C:**
  - Reformular el artículo como **contabilidad de márgenes de absorción con evidencia causal sugestiva** sobre precios.
  - Restringir las afirmaciones causales a la variación que supere las pruebas (por ejemplo, 2012–2019 o episodios concretos).
- **Si la inestabilidad temporal se confirma (F8 y subperiodos):** abandonar la elasticidad única y la cuota agregada 2015–2024 en su forma actual.

### I.2 Datos adicionales priorizados (punto 10)

Toda la información de disponibilidad, escala y años debe verificarse.

| Prioridad | Fuente | Variable que permitiría construir | Nivel geográfico | Frecuencia | Problemas de acceso | Sesgos de cobertura | Pregunta empírica |
|---|---|---|---|---|---|---|---|
| 1 | INE, Estadística de Variaciones Residenciales | Altas y bajas por país de nacimiento, edad y destino; bajas por caducidad | Municipio; flujos origen–destino | Anual | Pública | Retrasos de inscripción; bajas administrativas | Desplazamiento de nativos; difusión dentro de la provincia (Proposición 1); artefactos de registro |
| 2 | Censo 2001 y Padrón 1998–2002 | Participaciones de origen anteriores al *boom*; controles de 2001 | Municipio | Puntual | Pública | Clasificación por nacionalidad o país de nacimiento según el año | Instrumento más predeterminado; controles no contaminados |
| 3 | Valor tasado (ministerio competente), paro registrado (SEPE), Padrón 2003–2011 | Resultados previos a 2011 | Municipio (tasación solo en los grandes) | Trimestral o mensual | Pública | Tasación solo en municipios grandes; cambios de método | Tendencias previas (F2) |
| 4 | INE, Movimiento Natural de la Población | Nacimientos por nacionalidad de la madre; defunciones | Municipio o provincia (verificar) | Anual | Pública | Desagregación por nacionalidad a escala fina | Separar el componente natural de la variación de nativos; exclusión en la ocupación |
| 5 | Eurostat y base de migraciones internacionales de la OCDE | Entradas por origen en otros destinos | País | Anual | Pública | Definiciones distintas por país; años | Shocks de expulsión alternativos (MI-2) |
| 6 | SERPAVI | Percentiles y niveles de renta (€/m² y €/mes) | Sección, distrito, municipio | Anual (años a verificar) | Pública | Misma fuente tributaria que el IPVA; personas físicas | Distribución del efecto; magnitudes en euros |
| 7 | Normativa autonómica (Ley catalana 11/2020; declaraciones de zonas tensionadas) | Indicador de municipio y periodo con contención | Municipio | Fechas | Pública | — | Confusión por política dentro de la provincia |
| 8 | Registro de fianzas de Cataluña (y de otras comunidades) | Renta de contratos nuevos | Municipio o distrito | Trimestral | Pública en Cataluña; desigual en el resto | Cumplimiento del depósito; solo algunas comunidades | β(entrada) frente a β(stock); rotación |
| 9 | IGN (MDT), costa, Natura 2000; planeamiento urbanístico (SIU, verificar) | Restricciones físicas y de planeamiento a la oferta | Municipio o cuadrícula | Puntual | Pública | Calidad del planeamiento | Heterogeneidad por elasticidad de la oferta (H1) |
| 10 | Catastro (descargas alfanuméricas por municipio) | Stock por superficie, antigüedad y subdivisiones | Parcela o municipio | Anual | Pública con registro | Sin País Vasco ni Navarra; retrasos en el alta | Oferta a largo plazo; subdivisiones; cesta hedónica |
| 11 | Microdatos censales 2011 y 2021 | Habitaciones, personas, tenencia y estructura del hogar por origen | Municipio solo para los grandes (verificar) | Puntual | Pública con restricciones | Muestra en 2011; definiciones de registro en 2021 | Hacinamiento según norma; composición frente a intra-grupo |
| 12 | Microdatos de anuncios (Idealista, Fotocasa) | Índice hedónico ofertado; rentas de habitaciones | Geolocalizado | Diaria o mensual | Convenio o compra; condiciones de uso | Solo ofertado; cuota de mercado cambiante | Precio de entrada; compartir vivienda |
| 13 | ECV, EPF y EPA (microdatos) | Hacinamiento, sobrecarga, renta pagada, emancipación por país de nacimiento | Comunidad autónoma o provincia | Anual o trimestral | Pública | Muestras pequeñas de extranjeros | Contexto descriptivo; margen de los nativos |
| 14 | AEAT (microdatos de arrendamientos con referencia catastral) | Contratos nuevos frente a vigentes por vivienda | Vivienda | Anual | Convenio, incierto | Solo personas físicas | Índice de alquileres repetidos; β(entrada) nacional |
| 15 | Notariado y Registradores | Compras por nacionalidad del comprador | Provincia o municipio (verificar) | Trimestral | Pública en parte | Agregación | Canal comprador europeo; sustitución entre tenencias |

### I.3 Estructura reproducible del proyecto

```
replication/
├── README.md                  # procedencia de cada fichero, versión, fecha de descarga, licencia
├── config/
│   ├── specs.yaml             # tabla de especificaciones: id, resultado, tratamiento, instrumento,
│   │                          #   controles, efectos fijos, pesos, muestra, agrupación, inferencia, estado (central/robustez)
│   ├── strata.yaml            # estratos de permutación fijados ex ante
│   └── analysis_plan.md       # plan registrado (fechado) antes de ejecutar análisis nuevos
├── data/
│   ├── raw/                   # descargas inmutables con suma de verificación (sha256)
│   ├── intermediate/
│   └── analysis/
├── code/
│   ├── 00_download/           # un script por fuente; nunca se editan los datos a mano
│   ├── 01_clean/              # armonización Padrón/estadística continua, 33 orígenes, censos, catastro
│   ├── 02_instrument/         # participaciones, shocks dejando fuera la provincia, recentrado, permutaciones
│   ├── 03_samples/            # registro de la muestra: cada exclusión con motivo y recuento
│   ├── 04_estimation/         # 2SLS, diferencias largas, proyecciones locales, sistema conjunto
│   ├── 05_inference/          # AR (analítico, WCR), AKM0, aleatorización, tF, F de Sanderson-Windmeijer, Fieller
│   ├── 06_falsification/      # F1–F8
│   ├── 07_heterogeneity/      # H1–H4 con corrección por comparaciones múltiples
│   ├── 08_model/              # momentos, conjuntos identificados, sensibilidad de los parámetros
│   └── 09_tables_figures/
├── output/
│   ├── tables/  figures/
│   └── logs/sample_flow.csv   # registro de la muestra legible
├── tests/                     # comprobaciones automáticas, véase abajo
├── docs/
│   ├── codebook.md            # definición exacta de cada variable (fórmula, fuente, tabla INE)
│   ├── limitations.md         # límites de cada fuente (sección H)
│   └── deviations.md          # cambios respecto al plan registrado y su motivo
├── environment.lock           # versiones exactas de las dependencias
└── Makefile (o Snakefile)     # reproduce todo con una orden
```

**Comprobaciones automáticas mínimas (`tests/`):**

- Las participaciones suman $S_i$.
- El instrumento recentrado tiene media cero bajo las permutaciones.
- La equivalencia BHJ entre el 2SLS y la regresión a nivel de shock se cumple hasta el redondeo.
- La identidad de la descomposición (4) del manuscrito se cumple.
- Cada número del texto procede de un fichero de resultados, como ya hace el autor (l. 678–679).

### I.4 Indispensable frente a deseable, teniendo en cuenta el acceso

- **Indispensable y ejecutable ya [E]:** etapas 0 y 1 completas (1A–1F). No requieren microdatos administrativos y resuelven la mayoría de los problemas de credibilidad y de interpretación.
- **Indispensable si es factible, con datos públicos [N]:** EVR, participaciones de 2001, resultados previos a 2011, Movimiento Natural, listas de contención de rentas y SERPAVI.
- **Deseable:** fianzas, anuncios, microdatos censales, ECV, EPF, EPA y AEAT.
- **Si el acceso a microdatos no es viable,** la alternativa honesta es:
  - (i) limitar las afirmaciones sobre hacinamiento a "mayor ocupación";
  - (ii) presentar β(entrada) solo como traducción con supuestos de rotación;
  - (iii) dejar el bienestar como pregunta abierta, explicando qué datos la resolverían.

---

## Referencias metodológicas añadidas (verificar antes de citar)

Además de las ya citadas en el manuscrito (Adão et al., 2019; Anderson y Rubin, 1949; Andrews et al., 2019; Borusyak y Hull, 2023; Borusyak et al., 2022 y 2025; Davidson y MacKinnon, 2010; Goldsmith-Pinkham et al., 2020; Jaeger et al., 2018; Montiel Olea y Pflueger, 2013; Roodman et al., 2019; Saiz, 2010; Webb, 2023, entre otras):

- Anderson, M. L. (2008). Multiple inference and gender differences in the effects of early intervention. *Journal of the American Statistical Association*, 103(484), 1481–1495.
- Andrews, I., Gentzkow, M., y Shapiro, J. M. (2017). Measuring the sensitivity of parameter estimates to estimation moments. *Quarterly Journal of Economics*, 132(4), 1553–1592.
- Benjamini, Y., y Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B*, 57(1), 289–300.
- Bosch, M., Carnero, M. A., y Farré, L. (2010). Information and discrimination in the rental housing market: Evidence from a field experiment. *Regional Science and Urban Economics*, 40(1), 11–19.
- Chodorow-Reich, G. (2020). Regional data in macroeconomics: Some advice for practitioners. *Journal of Economic Dynamics and Control*, 115.
- Conley, T. G. (1999). GMM estimation with cross sectional dependence. *Journal of Econometrics*, 92(1), 1–45.
- Fieller, E. C. (1954). Some problems in interval estimation. *Journal of the Royal Statistical Society B*, 16(2), 175–185.
- Kleibergen, F., y Paap, R. (2006). Generalized reduced rank tests using the singular value decomposition. *Journal of Econometrics*, 133(1), 97–126.
- Lee, D. S., McCrary, J., Moreira, M. J., y Porter, J. (2022). Valid t-ratio inference for IV. *American Economic Review*, 112(10), 3260–3290.
- Moreira, M. J. (2003). A conditional likelihood ratio test for structural models. *Econometrica*, 71(4), 1027–1048.
- Rambachan, A., y Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*, 90(5), 2555–2591.
- Romano, J. P., y Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica*, 73(4), 1237–1282.
- Roth, J. (2022). Pretest with caution: Event-study estimates after testing for parallel trends. *American Economic Review: Insights*, 4(3), 305–322.
- Sanderson, E., y Windmeijer, F. (2016). A weak instrument F-test in linear IV models with multiple endogenous variables. *Journal of Econometrics*, 190(2), 212–221.
- Solon, G., Haider, S. J., y Wooldridge, J. M. (2015). What are we weighting for? *Journal of Human Resources*, 50(2), 301–316.
- Stock, J. H., y Yogo, M. (2005). Testing for weak instruments in linear IV regression. En D. W. K. Andrews y J. H. Stock (eds.), *Identification and Inference for Econometric Models*. Cambridge University Press.
- Wolf, C. K. (2023). The missing intercept: A demand equivalence approach. *American Economic Review*, 113(8), 2232–2269.
- Wolfers, J. (2006). Did unilateral divorce laws raise divorce rates? A reconciliation and new results. *American Economic Review*, 96(5), 1802–1820.

**Normativa española citada** (comprobar fechas, ámbito y municipios afectados): RDL 7/2019, RDL 6/2022, Ley 12/2023, Ley catalana 11/2020 y su anulación parcial en 2022, Ley 14/2013 ("golden visa"), y las exenciones de visado Schengen para Colombia (2015) y Perú (2016).

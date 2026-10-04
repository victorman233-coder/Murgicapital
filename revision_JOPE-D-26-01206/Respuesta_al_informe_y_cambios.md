# Revisión aplicada: qué se hizo con cada punto del informe

**Manuscrito revisado:** `paper/paper_revised.pdf` (fuente: `paper/paper_revised.tex`), titulado *Immigration, Rents and Housing Occupancy in Spain*.
**Código:** `code/` (orden de ejecución en `code/run_revision.sh`). **Resultados:** `out/`. **Comprobaciones automáticas:** `tests/test_revision.py`.

Todos los números del manuscrito revisado salen de los resultados mediante macros (`paper/tab/numbers_rev.tex`); no hay cifras escritas a mano.

> **Aviso importante antes de enviar.** Varios resultados nuevos cambian las conclusiones del artículo original (sección 1 de este documento). El texto se ha reescrito para reflejarlos fielmente. Como autor, debes revisar todo, confirmar que compartes las decisiones (en particular la especificación central) y comprobar las referencias bibliográficas añadidas. Lo que no pude verificar está señalado en la sección 4.

---

## 1. Cómo cambian las conclusiones

| Afirmación del manuscrito original | Qué muestran los análisis nuevos | Cómo queda en la revisión |
|---|---|---|
| Elasticidad del alquiler ≈ 0,30 | La estimación depende de controlar por la renta de 2015, medida dentro del periodo muestral. Con controles predeterminados de 2011 (educación, estructura de edad) y estructura económica de 2012, la especificación central da **0,13** en 2012–2024 (AR [−0,08, 0,35]) y **0,24** en el periodo de llegadas 2015–2024 (AR [0,07, 0,59]). En 2012–2014, años de salidas, la respuesta es ≈ 0. | Se presenta como efecto relativo positivo en los años de llegadas, más pequeño y menos robusto de lo que se afirmaba. |
| Inferencia robusta excluye el cero | En 2015–2024, el cero queda excluido con AR por provincia, *bootstrap* salvaje y aleatorización entre todos los orígenes. **No** queda excluido con AKM0 (*shocks* agrupados por origen: [−0,56, 0,82]) ni con aleatorización dentro de continente (no acotado). | Se dice explícitamente que la significación depende del supuesto sobre los *shocks*. |
| El efecto se invierte en 2020–2024 (−0,46) | Era un **artefacto**: el código original omitía la interacción año × controles del primer año de cada submuestra. Con todas las interacciones, 2020–2024 da +0,31. | Se corrige y se explica en una nota al pie. |
| La discrepancia 0,234 (nivel de shock) frente a 0,303 | Se debe a usar *shocks* nacionales (0,226) en lugar de excluir la provincia, más los efectos fijos de año a nivel de *shock*. La equivalencia exacta de BHJ se cumple. | Se explica en una nota. |
| Hacinamiento ("crowding") es el ajuste principal; "más de la mitad" | La ocupación sube de forma robusta (≈ 0,45 personas por inmigrante), pero la cuota es imprecisa: 0,64, Fieller [0,34, 1,19] y *bootstrap* [−0,53, 1,73]. La composición entre continentes **no** explica la subida (predice −0,08), al contrario de lo que yo suponía en el informe. | Título y texto pasan a hablar de "ocupación", no de hacinamiento ni de coste de bienestar. |
| El stock no respondió | Se confirma a corto plazo: catastro −0,24 (0,16). La primera etapa es débil con los controles centrales (F ≈ 5). | Se mantiene, con horizonte explícito y la advertencia sobre la primera etapa. |
| La inmigración explica ~10 % del alquiler | Con la especificación central del periodo de llegadas: 7,5 % (2,2 %–18,6 %); en el periodo completo, entre 0 y 11 %; en el episodio Colombia–Perú, 20 %. | Se presenta solo bajo los supuestos A1–A4, sin hablar de "mínimos". |
| No persiste, no se difunde, no es mayor en grandes ciudades | Las proyecciones locales basadas en innovaciones tienen primera etapa muy débil (F 2,8–6,8). No se detectan efectos sobre municipios vecinos, pero los intervalos son amplios. | Se retiran las afirmaciones de persistencia y difusión. |
| Los contratos nuevos responden 2,4 veces más | Diseño provincial no identificado. | Se retira de las conclusiones. |

**Hallazgo nuevo y más limpio.** La exención de visado Schengen para Colombia y Perú (2016), comparando municipios con la misma exposición latinoamericana, da **0,64** con pesos de población:

- *Bootstrap* AR [0,04, 1,80].
- Primera etapa F = 9,4.
- Sin tendencias previas en alquileres.
- Sin pesos es imprecisa.

---

## 2. Correspondencia con el plan del informe

### Imprescindibles (B.1)

| Punto | Hecho | Resultado / dónde |
|---|---|---|
| I-1 Variación identificadora | Sí: estadísticos de *shocks*, Rotemberg completo (33 orígenes), LIML y J, controles económicos especificados × año, efectos fijos provincia × tamaño × año y área urbana × año | Tabla 2, Fig. 3, Tabla 3, Fig. 4, Tabla A (Rotemberg). Número efectivo de orígenes 15,8; correlación media entre trayectorias 0,71; J = 137 (p ≈ 0); Rumanía α = 0,31 con *shock* negativo. |
| I-2 Tendencias previas | Sí: placebo de *shocks* futuros sobre rentas 2011–2014 y placebos demográficos 2003–2011 con el Padrón. No hay precios anteriores a 2011 (fuente bloqueada, sección 3). | Tabla 4. Rentas 2011–2014: −0,085 (p = 0,075). El placebo demográfico desaparece con los controles centrales. |
| I-3 Dinámica / JRS | Sí: correlación *boom*–post (0,74), control del *boom*, proyecciones locales equilibradas con 3 rezagos, F de Sanderson-Windmeijer, reconciliación en la misma muestra | Tabla 4, Fig. A1. Las innovaciones no tienen fuerza: la dinámica no está identificada. |
| I-4 Estabilidad y simetría | Sí: ventanas, entradas frente a salidas, signo del instrumento, controles de contención de rentas y zonas tensionadas (Cataluña) | Tabla 4C. Corregido el artefacto de 2020–2024. |
| I-5 Inferencia | Sí: AR analítico, WCR (Webb), aleatorización por estratos (todos, terciles de tamaño, continentes; estadístico estudentizado), AKM0 agrupado por origen, reconciliación de BHJ | Tabla 3, Tablas A2–A3. |
| I-6 IPVA | Parcial: documentación, reetiquetado del estimando y validación con fianzas de Cataluña (rotación 31 %, traslado lento). El número de contratos por municipio en la AEAT o SERPAVI no es accesible. | Sección 4.1, Tabla A (Cataluña). |
| I-7 Ocupación | Sí: estimación conjunta, intervalos de Fieller y *bootstrap*, descomposición por composición, contraste censo frente a registro y catastro en 2021 | Tabla 6, Fig. 6. |
| I-8 Magnitud | Sí: cuota en función de β, supuestos A1–A4, periodo de llegadas y episodio | Tabla 7, Fig. 7. |
| I-9 Controles predeterminados | Sí: la renta de 2015 se sustituye por censo 2011 y DIRCE 2012 | Especificación central (`config/specs.yaml`). |
| I-10 Reescribir afirmaciones | Sí: título, resumen, introducción, discusión y conclusiones | Secciones 1, 9 y 10 del manuscrito. |

### Muy importantes (B.2)

| Punto | Hecho | Resultado |
|---|---|---|
| MI-1 Episodios de expulsión | Sí: Colombia/Perú 2016, Venezuela 2017, Ucrania 2022 | Solo Colombia/Perú es utilizable (Tabla 5, Fig. 5). |
| MI-2 *Shocks* alternativos | Sí, con Eurostat (entradas en 12 países europeos) | Sin poder predictivo (F = 0,1); no se puede usar. |
| MI-3 Relocalización de nativos | Parcial: la EMCR del INE solo tiene datos municipales para 2021–2024 | Primera etapa débil (F = 3,5); no informativo. |
| MI-4 Participaciones antiguas | No: el Padrón 1998–2002 por nacionalidad solo existe a escala nacional o provincial en el INE | Se declara como limitación. |
| MI-5 Movimiento natural | No: no encontré los nacimientos municipales por nacionalidad de la madre en un formato descargable | Limitación. |
| MI-6 SERPAVI | No: aplicación con reCAPTCHA y datos masivos en el dominio del ministerio, que devuelve 403 | Limitación. |
| MI-7 Oferta | Parcial: catastro anual. MDT (CNIG) y licencias no accesibles. | Densidad y viviendas vacías como aproximación a la elasticidad de oferta en la heterogeneidad. |
| MI-8 Disciplina del modelo | Sí: se retira la cuantificación de ε y δ′ (no acotados) y se explica en el apéndice B | Sección 3, apéndice B. |
| MI-9 Heterogeneidad preespecificada | Sí: H1 (vacías, densidad), H2 (alquiler), H3 (demanda efectiva) con q de Benjamini-Hochberg | Ninguna sobrevive (q mínimo 0,18). |
| MI-10 Ponderación | Sí: población 2003, hogares en alquiler 2011 y sin ponderar en todas las tablas principales | Tabla 3 y Tablas A. |

### Deseables (B.3)

- **D-1 Fianzas:** hecho para Cataluña (Incasòl).
- **D-2 Anuncios:** no; Idealista devuelve 403 y su uso requiere convenio.
- **D-3 a D-7 Microdatos (censo, ECV, EPF, EPA), centros de acogida y compras por nacionalidad:** no realizados.

---

## 3. Datos obtenidos y datos que no se pudieron obtener

**Obtenidos** (todos con descarga automática en `code/r00_download.sh`):

- INE: Padrón por país de nacimiento (33573), censo anual (66322), IPVA (59060, 59061, 59058, 59059, 59005), DIRCE (4721), EMCR (69744, 69746, 69767), indicadores por sección de los censos 2011 y 2021.
- Eurostat: migr_imm3ctb y LAU 2021 (áreas urbanas funcionales, litoral, grado de urbanización).
- Generalitat de Catalunya: fianzas Incasòl y zonas de política de vivienda.
- Zenodo: tu paquete de replicación.

**No obtenidos y por qué:**

- **Ministerio de Vivienda (mivau.gob.es) y datos.gob.es:** responden 403 a servidores en la nube. Afecta al valor tasado, a SERPAVI y al Atlas de Áreas Urbanas.
- **CNIG:** sin conexión.
- **Idealista:** 403.
- **Padrón municipal 1998–2002 y nacimientos municipales por nacionalidad de la madre:** no encontré tablas municipales descargables en el INE.

Si quieres incorporar estos datos, se podría hacer desde una sesión en tu ordenador, con el navegador, porque esta sesión en la nube no puede usar tu Chrome.

---

## 4. Lo que debes revisar tú antes de enviar

1. **La especificación central.** Está definida en el informe antes de estimarla y documentada en `config/specs.yaml`. Debes estar de acuerdo con ella y con presentar el periodo 2015–2024 como estimando de "llegadas".
2. **Datos normativos citados en el texto:**
   - Exenciones de visado: diciembre de 2015 para Colombia y marzo de 2016 para Perú.
   - RDL 7/2019, RDL 6/2022 y Ley 12/2023.
   - La aproximación de los 61 municipios de la Ley catalana 11/2020: áreas de demanda fuerte con más de 20.000 habitantes. Reproduce exactamente 61 municipios, pero conviene contrastarlo con la lista oficial.
3. **Referencias añadidas, cuyos datos bibliográficos debes comprobar:** Benjamini y Hochberg (1995), Chodorow-Reich (2020), Fieller (1954), Lee et al. (2022), Sanderson y Windmeijer (2016), Solon et al. (2015) y Wolf (2023). Les he quitado los DOI que no podía verificar.
4. **La declaración sobre IA generativa:** está redactada en primera persona del autor, así que debes confirmarla.
5. **El paquete de Zenodo:** habría que actualizarlo con el código de la revisión (`code/`, `config/`, `tests/`).
6. **La carta de respuesta a los referees:** si llega a haberla, este documento sirve de base, pero tendría que redactarse en inglés.

---

## 5. Revisión de las figuras

Todas las figuras se generan ahora con el mismo estilo (`code/rev_style.py`). La Fig. 1 y los mapas se reconstruyen desde los ficheros brutos de INE, Eurostat e IGN (`code/r22_figures_context.py`), en lugar de copiarse del paquete original.

| Figura | Problema | Corrección |
|---|---|---|
| Fig. 1 (contexto) | En el panel (d) la línea unía 2022 con 2024 como si 2023 existiera. | Eurostat no ha publicado el dato de 2023 para España en `ilc_lvps15`. La serie se corta en ese año, se señala en el gráfico y en la nota. El panel (a) llega ya al censo de 2025. |
| Fig. 2 (mapas) | Los municipios con entrada neta negativa, los que no tienen dato y el primer tramo se pintaban en blanco y parecían huecos. Además había finas grietas blancas entre polígonos. | Hay una categoría propia para el descenso neto (naranja) y otra para «sin dato / sin índice municipal» (gris). La escala azul empieza en un tono visible. Los bordes de cada municipio se rellenan de su color, con lo que desaparecen las grietas. Se excluye Gibraltar. |
| Fig. 3 | El título del panel (b) salía cortado, las etiquetas se solapaban y siete estilos de línea casi iguales eran difíciles de distinguir. | Cada línea lleva su nombre al final. Los nueve β fuera de ±3 se dibujan como flechas en el borde (todos con peso menor que 0,01). El título está acortado. |
| Fig. 4 | Había mucho espacio vacío y etiquetas largas. Los intervalos truncados no se distinguían. | Las filas se agrupan con encabezados y etiquetas cortas. Unas flechas marcan los intervalos que salen del eje y una línea discontinua el conjunto AR no acotado. Una línea punteada marca la estimación central. |
| Fig. 5 y A1 | El año de referencia no se distinguía. | Se marca con un punto hueco. |
| Fig. 6 | El bigote de «New dwellings» sin ponderar quedaba cortado. | El eje se ajusta a los intervalos, hay separación entre barras y la leyenda va encima. |
| Fig. 7 | Las etiquetas se solapaban con los intervalos, y las filas no coincidían con la tabla 7. | Es un único panel con las mismas seis filas y orden que la tabla 7, y el mismo truncamiento en cero. |

---

## 6. Reproducción

```
export WORK=/ruta/de/trabajo    # descargas (~2,5 GB) y ficheros intermedios
bash code/run_revision.sh       # descarga, construye, estima, genera tablas, figuras y PDF
```

**Entorno:** Python 3.11, pandas 2.3, pyfixest 0.60, linearmodels 7.0, scipy, matplotlib; XeLaTeX (TeX Live 2023).

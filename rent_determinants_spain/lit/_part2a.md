
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

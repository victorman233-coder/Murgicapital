# Qué determina la subida del alquiler en España: resumen del artículo y notas

**Artículo:** *What Drives Rents in Spain? Demand, Supply, Tourism and Regulation across Municipalities* (`paper/paper.pdf`, 22 páginas, en inglés).

## 1. Qué hace el artículo

1. **Marco teórico (sección 4).** Es un modelo stock-flujo del mercado local de alquiler de larga duración.
   - Los determinantes entran en una sola condición de equilibrio:
     - población;
     - renta;
     - demanda turística (los pisos pasan de residentes a turistas);
     - oferta;
     - coste de uso de la vivienda en propiedad (tipos y crédito);
     - regulación.
   - De ahí salen cinco predicciones (P1–P5).
   - Incluye además una identidad que conecta el alquiler de mercado con el índice del INE (IPVA). El IPVA mide todos los contratos vigentes, y la mayoría solo se actualizan con el IPC.
2. **Literatura (sección 3).** Está organizada por determinante y usa 45 referencias. Las de revista y libro se han verificado una a una en Crossref (`lit/crossref_verified.json`); el resto se comprobaron en la fuente original (PDF o resumen).
3. **Diseños empíricos (secciones 6–7).** Hay uno por determinante:
   - **Población (inmigración):** diferencias largas 2015–2024 dentro de provincia, con el instrumento shift-share de tu artículo anterior. Incluye un test de falsificación.
   - **Pisos turísticos:** el colapso del turismo en 2020–21 y la recuperación posterior, como experimento natural.
     - Con el IPVA para toda España.
     - Con los contratos nuevos (fianzas) de Cataluña por trimestre: precios y número de contratos.
   - **Regulación:**
     - Tope catalán en zonas tensionadas (marzo y octubre de 2024), con diferencias en diferencias apiladas con controles limpios y ajuste por tendencias previas.
     - Tope del 2% a las actualizaciones (2022–23), mediante la identidad contable del índice.
   - **Renta, grandes propietarios y crédito:** solo asociaciones descriptivas, y así se dice en el texto.
4. **Ranking (sección 8).** Se hace a tres niveles:
   - el índice nacional;
   - las diferencias entre municipios de una misma provincia;
   - los contratos nuevos en Cataluña.

   Incluye además un desglose por tamaño de municipio.

## 2. Resultados principales, por orden de importancia

| Determinante | Efecto estimado | ¿Identificado? |
|---|---|---|
| Inflación (vía actualización IPC de los contratos) | +21,1 puntos log; el IPVA subió 20,6 entre 2015 y 2024, es decir, **en términos reales el alquiler medio de todos los contratos no subió (−0,4%)** | Contabilidad, no causal |
| Tope del 2% a las actualizaciones (2022–23) | −5,9 puntos log (cota superior: hasta un 6,1% menos) | Contabilidad |
| Crecimiento de población por inmigración | +2,9 puntos log (rango 0,2–5,4); elasticidad 0,41; explica el 12% de las diferencias entre municipios de una provincia; mayor en las grandes ciudades | Sí (IV, sin tendencias previas) |
| Renta de los hogares | +1,0 puntos log (−0,1 a 2,2) | No (solo asociación) |
| Pisos turísticos | Casi nulo a escala nacional (+0,16 en 2015–19; −0,14 en 2019–24), pero relevante en municipios turísticos: −0,30% en el alquiler nuevo por punto de cuota turística durante el colapso y +0,44% en la recuperación; con un 13% de pisos turísticos, del orden del canal de población | Sí (colapso del turismo como experimento) |
| Oferta de vivienda | No respondió a la demanda (+3,8% en todos los tamaños): es lo que convierte la demanda en precio | Sí (IV) |
| Tope en zonas tensionadas (Cataluña, 2024) | −4% a −5% en el alquiler de contratos nuevos; −18% en el número de contratos en la primera oleada | Sí (DiD apilado) |
| Fondos y grandes propietarios | Sin asociación con los indicadores públicos disponibles | No |
| Tipos de interés y crédito | Coinciden en el tiempo con la aceleración de los contratos nuevos | No (shock común) |

**Mensajes clave:**
- **La subida es de los contratos nuevos, no del alquiler medio.**
  - En Cataluña, el alquiler de los contratos nuevos subió un 53% entre 2015 y 2024, frente a un 23% del índice de todos los contratos (igual que el IPC).
  - En España, los contratos nuevos subieron un 19,3% entre 2021 y 2024, frente a un 7,5% de los existentes.
- **La mayor parte de la variación es común dentro de cada provincia** (63%). Por diseño, esa parte no se puede atribuir a factores locales.

## 3. Datos: todo descargado de fuentes públicas

**Obtenidos:**
- **INE:**
  - IPVA municipal, provincial y por antigüedad del contrato;
  - viviendas turísticas por municipio (2020–2026);
  - Atlas de Distribución de Renta (2015–2023);
  - ejecuciones hipotecarias por provincia y titular;
  - tipos hipotecarios;
  - IPC.
- **Generalitat de Catalunya** (datos abiertos):
  - fianzas (contratos nuevos) por municipio y trimestre;
  - zonas tensionadas;
  - Registro de Turismo (104.548 pisos turísticos, con titular persona física o sociedad);
  - impuesto sobre estancias turísticas.
- **BCE:** Euríbor.
- **Pipeline de tu artículo anterior:** población por país de nacimiento, instrumento y catastro.

**No obtenidos (y alternativa honesta adoptada):**
- **Inside Airbnb:** devuelve 403. Se usa la estadística del INE.
- **SERPAVI y datos del Ministerio de Vivienda:** devuelven 403. Los contratos nuevos solo se observan en Cataluña.
- **Titularidad de viviendas en alquiler por municipio:** no existe en abierto. Los fondos solo se pueden aproximar, y el artículo no hace afirmaciones causales.
- **Lista completa de los municipios de la ley catalana 11/2020:** no está accesible. Esa ley se cita con la literatura (Jofre-Monseny et al. 2023) y no se reestima.

## 4. Lo que debes revisar tú

1. **Afiliación y correo:** he usado los de tu artículo anterior (Universidad de Almería, vfa084@ual.es).
2. **Cita del trabajo de Pérez García (arXiv 2602.08631):** el documento tiene fecha de julio de 2025 y figura en arXiv en 2026. Comprueba si ya está publicado.
3. **Revista objetivo:** el formato es el de tu artículo anterior. Encaja en *Journal of Housing Economics*, *Regional Science and Urban Economics* o *Journal of Urban Economics*, según el énfasis.
4. **Afirmaciones sobre normativa:** RDL 7/2019, RDL 6/2022, Ley 12/2023 y la aplicación catalana en marzo y octubre de 2024. Las he contrastado con fuentes públicas, pero conviene que un jurista las revise.

## 5. Reproducción

```
export WORK=/ruta/de/trabajo
bash ../revision_JOPE-D-26-01206/code/run_revision.sh   # población, instrumento y catastro (artículo compañero)
bash code/run_all.sh                                     # descargas, datos, análisis, tablas, figuras y PDF
```

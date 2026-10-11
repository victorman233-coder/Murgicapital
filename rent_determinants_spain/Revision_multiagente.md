# Revisión multiagente de «Insiders and Outsiders in the Rental Market»

## Método

Cinco diagnósticos independientes, cada uno hecho por un agente real con un rol distinto:

| Agente | Rol |
|---|---|
| A1 | Teoría y contribución |
| A2 | Econometría e identificación |
| A3 | Datos y reproducibilidad |
| A4 | Economía de la vivienda |
| A5 | Revisión editorial |

**Incidencia.** El primer intento de A1–A4 se cortó porque la organización alcanzó su límite de gasto de API. Los relancé tras el reinicio del límite y reutilizaron sus cálculos parciales. A5 completó su diagnóstico en el primer intento. Ningún agente leyó los informes de los demás.

**Coordinación.** El coordinador integró los informes. Las discrepancias se resolvieron según la evidencia, no por mayoría. Las afirmaciones de los agentes que el coordinador comprobó se marcan como tales.

**Estados:**
- **A:** aceptado.
- **R:** rechazado.
- **H:** resuelto (*hecho*).
- **P:** pendiente o decisión del autor.

## Matriz priorizada (fase 2)

### Críticos

| ID | Localización | Problema | Agentes | Solución | Recurso | Estado |
|---|---|---|---|---|---|---|
| C1 | Tabla 1, fila IPVA | Error de escala: 1650.0 y 1619.0 en lugar de 16,5 y −14,4. **Verificado:** `t02_v2_tables.py` multiplica dos veces por 100. | A1, A3, A4, A5 | Corregir el código y generar la tabla desde las mismas cantidades que las macros. Añadir un `assert` de rango. | código | A |
| C2 | Resumen; §1; §7–8; Tabla 2 | La brecha es un **nivel** de 2024. La «renta de entrada implícita» (crecimiento del IPVA más el nivel de 2024) solo es un crecimiento si G₂₀₁₅ es nula u ortogonal a Z. P1 habla de cambios. | A1, A2, A3, A5 | Presentarla como efecto sobre el nivel. Prueba en cambios con los índices provinciales del INE (base 2015). Separar la entrada reciente (2020–24) de la anterior (2015–19). Hacer explícito el supuesto y acotarlo con (1−λ)^9. | estimación + texto | A |
| C3 | §6, §8; Tabla 6 | Identificación por cuotas de 2003: tres orígenes concentran el 84 % del peso de Rotemberg y hay desequilibrios observables; la inferencia por *shocks* no es informativa. Sensible a los pesos (con √P el AR roza el 0), a excluir las provincias 28 y 08 o la 29, y al instrumento del artículo compañero (AR incluye el 0). | A2, A5 | Tabla de balance completa (apéndice). Prueba J con un instrumento por origen. Control por la entrada 2003–2014 (Jaeger). Sensibilidad a pesos y a provincias. Definir el estimando (LATE ponderado por población). Reflejar la fragilidad en el resumen y la introducción. | estimación + texto | A |

### Altos

| ID | Localización | Problema | Agentes | Solución | Recurso | Estado |
|---|---|---|---|---|---|---|
| H1 | §4.2, ec. (4) | El bloque de mercado no contiene λ. La derivación stock-flujo da dr* = [d ln N + λα(·)]/(λη+σ+ε). Se pierde la predicción distintiva: la brecha responde más donde λ es menor. | A1, A5 | Volver a derivar (4); añadir la predicción sobre λ, marcada como no contrastada. | teoría | A |
| H2 | §4.3, P4 | P4 no se deriva del modelo; el *lock-in* puede ser inestable; el signo de κ es ambiguo. La caída del peso del INE coincide con la reforma de 2019 y los topes. | A1, A4, A2 | Derivar P4 con una elasticidad de localización de los entrantes externos. Suelo para λ. Presentar la caída del peso como compatible, no como prueba. | teoría + texto | A |
| H3 | §8.2; resumen | «None move out» e «incumbents stay» no se observan: falta la tenencia, los naturalizados cuentan como españoles, los flujos de extranjeros son en parte mecánicos y existe la explicación alternativa de la evitación nativa. | A1, A2, A3, A5 | Lenguaje de «sin efecto detectable» y «compatible con». Discutir la alternativa (Card 2001; Saiz y Wachter 2011). | texto + bibliografía | A |
| H4 | §8.3; Tabla 4 | La rigidez geográfica no se separa de la costa. El efecto se concentra en la costa; en la restricción media es 0,12. La interacción no tiene inferencia robusta a instrumentos débiles ni corrección de muestra pequeña. | A2, A5, A1 | Interacción conjunta con la costa. Corrección CRV1. Informar del efecto en la media. Reformular P3. | estimación + texto | A |
| H5 | §8.4; Tabla 5A | Turismo: tendencias previas fuertes en el registro anual (2014–2019) y exposición medida en agosto de 2020. El conjunto LR del umbral no es válido con heterocedasticidad. Contradicción: «below 3 % no reallocation» frente a coeficientes negativos y significativos en el tramo 1–3 %. | A2, A5, A1 | Estudio de eventos anual con pre-periodo. Pasar a lenguaje descriptivo. Eliminar el conjunto LR. Corregir la contradicción. | estimación + texto | A |
| H6 | §2/§5; medida | La brecha AEAT incluye renovaciones con el mismo inquilino; solo cubre arrendadores personas físicas; hay incentivos fiscales distintos (Ley 12/2023); «ajustado por calidad» es excesivo; compara con todos los contratos, incluidos los nuevos. | A4, A2 | Precisar la medida. Llamarla «ajustada por valor». Sensibilidad a la elasticidad (0,5 y 0,7). Composición (valor y m²). Corrección frente a los contratos preexistentes. | texto + estimación | A |
| H7 | §5 hechos | El año base 2015 está cerca del mínimo del ciclo: en Cataluña, con base 2018, la diferencia es +1,7. Hay ruptura metodológica del IPVA en 2021. | A4 | Sensibilidad al año base (2016 y 2018) en Cataluña y Aragón. Discutir el componente cíclico. | estimación + texto | A |
| H8 | §7.1; Tabla 2B | Inconsistencia del tamaño del hogar: d_hh − d_pp = 0,99 frente a d_hhsize = 1,26. El número implícito de hogares es −0,41 (no significativo). | A1, A2 | Informar del tamaño implícito por renta y del número de hogares. Matizar P2 (composición frente a hacinamiento). | estimación + texto | A |
| H9 | §6; dependencias | Dependencia del artículo compañero: el instrumento y el panel no se describen por sí mismos; el tope catalán se cita sin tabla propia. | A5, A3 | Describir el instrumento completo. Declarar el solapamiento. Incluir el código en el paquete. | texto + decisión del autor | A/P |
| H10 | Pipeline | `b02` sin script que lo genere (recuperado y verificado idéntico); `b01` fuera del pipeline; `d10` falla sin `mkdir`; entorno sin fijar. | A3 | `b02_gap_by_type.py` (**hecho**, idéntico). Añadir b01 y b02 a `run_v2.sh`. `mkdir -p` y `curl --fail`. Manifiesto SHA-256. Lock de entorno. | código | A |
| H11 | Todo el texto | Afirmaciones excesivas y nulos presentados como efectos cero («does not respond», «problem of access», política extrapolada). | A5, A2, A1, A4 | Reescribir el resumen, la introducción, la discusión y la conclusión con alcance acotado. | texto | A |
| H12 | Bibliografía | Falta literatura sobre insider–outsider, descuento por antigüedad, índices de nuevos inquilinos, control de rentas y movilidad, y evitación nativa. | A1, A4, A5 | Añadir solo referencias verificadas en Crossref y pertinentes. | bibliografía | A |

### Medios

| ID | Problema | Agentes | Solución | Estado |
|---|---|---|---|---|
| M1 | Unidades: log-puntos frente a %, «0.57 %», dobles negaciones, cifras escritas a mano (8,8 / 2,8 / 18 % / λ = 0,18) | A3, A5 | Una convención (log-puntos); macros | A |
| M2 | Rotación en Aragón: la edad depende de la fecha de descarga (19,2 / 15,9 / 14,9 %); fianzas no devueltas ≠ fin del contrato; mezcla de regímenes legales; mediana sin meseta | A3, A2, A4 | Fecha real de descarga, rango de sensibilidad, cohortes antes y después de 2019 | A |
| M3 | EPF 2024: renta exacta solo en el 42 % | A3 | Medida por punto medio del intervalo en todos los años | A |
| M4 | Topes: 18 % frente a −0,14 log; solo 2022–23; adelanto de rentas (*front-loading*) no incluido; IPC medio; cuota de contratos indexados | A3, A1, A5, A2 | Una sola especificación; rango; reformular la cota | A |
| M5 | Panel anual: recorte del resultado; esquema de aleatorización elegido; prueba de adelanto desfavorable | A2, A5 | Sin recorte; ambos esquemas y AR analítico; retirar «corroborates» | A |
| M6 | País Vasco sin explicar | A4 | Descomposición dentro de la región (pendiente del flujo) | A |
| M7 | Tenencia: tendencias previas en 2019–2020 | A5 | Reformular | A |
| M8 | Cuentas de población (0,82 frente a flujos) | A5 | No ligar las cifras; distintas definiciones | A |
| M9 | Hechos institucionales: el tope de 2022 ligado al IGC con negociación; el IRAV es un límite; el régimen de temporada cambió en 2026 | A4 | Precisar | A |
| M10 | Notación (β, ε, A, P_i, mayúsculas); ec. (1) como aproximación; «widens whenever» incorrecto | A1, A5 | Corregir | A |
| M11 | Notas de tablas incompletas (Share, EE, tipo de F, AR «throughout») | A5 | Corregir | A |
| M12 | Estructura redundante (§2 con §5; Discusión con Conclusión) | A5 | Fusionar §2 y §5; recortar repeticiones | A |
| M13 | Asequibilidad de entrantes con ventanas desalineadas | A2, A3 | Mencionar; la versión alineada da 0,90 [−0,16; 2,30] | A |

### Bajos

| ID | Problema | Solución | Estado |
|---|---|---|---|
| B1 | «Renewed» | «relet» | A |
| B2 | «48 provinces» | «46 provinces plus Ceuta and Melilla» | A |
| B3 | «Tensioned» | «stressed (tensioned) market areas» | A |
| B4 | Fig. 3a citada para 14 municipios aunque solo muestra Zaragoza | Corregir la cita | A |
| B5 | Macros sin usar | Limpiar | A |
| B6 | Orden de Borusyak; título en español | Mantener | R (estilo autor-año correcto) |
| B7 | «Rents top the list of economic concerns» | Eliminar | A |
| B8 | «Every new lease is registered» | «must be deposited» | A |

### Rechazados o no adoptados

- **«Medir la exposición turística en 2019»** (A5). No es factible: la estadística experimental del INE empieza en agosto de 2020. Se declara como limitación.
- **«Cotas de Conley-Hansen-Rossi»** (A2). Se sustituye por pruebas más directas (J por origen, control Jaeger, balance). Queda como análisis pendiente.
- **«ECEPOV-2021»** (A1). La disponibilidad del microdato no está verificada. Pendiente.

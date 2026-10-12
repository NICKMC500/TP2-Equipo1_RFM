# Reporte técnico de revisión — TP2 Equipo 1 RFM

## Alcance

Esta revisión toma como punto de partida la migración de Sakila realizada en el TP1. Se revisaron y reforzaron las Actividades 0 a 3 del análisis RFM. 
## 1. Portabilidad del esquema (Actividad 0)

Los nombres físicos introducidos durante la migración a SQL Server quedan centralizados en `esquema.py`:

- `MAPEO_TABLAS` relaciona las 16 tablas canónicas de Sakila con las tablas locales en español.
- `MAPEO_COLUMNAS` contiene las columnas RFM de `customer`, `rental` y `payment`.
- `renderizar_sql()` reemplaza en forma controlada tokens como `{{customer}}` y `{{payment.amount}}` por identificadores SQL Server válidos.

Los archivos `sql/conjunto_trabajo.sql` y `sql/reconciliacion.sql` usan esos tokens y el notebook trabaja con nombres canónicos internos (`customer_id`, `recency_days`, `monetary_amount`). Para adaptar el proyecto a otra migración, se debe cambiar únicamente `esquema.py`.

La reconciliación compara tabla canónica, nombre local, filas del origen MySQL, filas de SQL Server y diferencia. Los conteos coinciden para 15 de las 16 tablas. La excepción es `payment`: el volcado de origen registra 16.049 filas y SQL Server contiene 16.044, una diferencia de -5. Esta diferencia se conserva visible y documentada; no se inventan ni reconstruyen filas.

## 2. Conjunto de trabajo y métrica RFM (Actividad 1)

`sql/conjunto_trabajo.sql` construye una fila por cliente con:

- **Recency:** días entre el último alquiler del cliente y la fecha máxima de alquiler del conjunto.
- **Frequency:** cantidad de alquileres distintos.
- **Monetary:** suma de pagos vinculados a alquileres.

La fecha máxima proviene de la base y no de `GETDATE()`, por lo que el cálculo es reproducible. En pandas se reconstruye la misma métrica desde el detalle crudo. La comparación usa `assert_frame_equal` y finaliza correctamente: las métricas de los 599 clientes coinciden. En la ejecución de validación, la consulta agregada de SQL Server tardó aproximadamente 0,06 s y la reconstrucción sobre el detalle en pandas aproximadamente 0,26 s; los tiempos deben recalcularse en la máquina de entrega.

## 3. Quintiles RFM: qcut y NTILE(5)

Se emplean ambas técnicas solicitadas y el desempate por `customer_id` hace reproducible el orden de valores empatados.

Hay 599 clientes, cifra que no es múltiplo de cinco. Por ese motivo `pandas.qcut` y `SQL Server NTILE(5)` distribuyen los restos en límites distintos. El notebook muestra el resultado real:

| Métrica | Coincidencia qcut vs NTILE | Casos frontera |
|---|---:|---:|
| R | 99,7 % | 2 |
| F | 99,7 % | 2 |
| M | 99,7 % | 2 |

Además se calcula una puntuación pandas que replica exactamente la regla de reparto de `NTILE`; esa validación da 100 % para R, F y M. Esto permite explicar la diferencia metodológica con evidencia, en lugar de ocultarla o manipular las categorías.

## 4. Perfilado y calidad de datos (Actividad 2)

El notebook presenta forma, muestra aleatoria con semilla, tipos, nulos, duplicados por clave de negocio y estadísticos descriptivos con percentiles 1, 5, 25, 50, 75, 95 y 99.

Resultados de la validación actual:

- 599 clientes; ninguna columna nula; ningún `customer_id` duplicado.
- Seis clientes (1,0 %) quedan fuera del límite IQR monetario superior. Se mantienen como clientes de alto valor plausibles, no como errores.
- No existen pagos sin alquiler, monto asociado a pagos sin alquiler, clientes sin pagos, pagos negativos ni pagos asociados a otro cliente.
- Cada uno de los cinco controles anteriores se calcula con la misma regla en SQL Server y pandas; las cinco comparaciones dan coincidencia.
- La diferencia de cinco pagos de la reconciliación es consistente con filas del origen sin alquiler que no fueron migradas. El resultado se declara como diagnóstico consistente, no como certeza sobre datos que ya no están en SQL Server. Como RFM solo suma pagos asociados a alquileres, no altera la métrica calculada.

Las reglas de negocio verificadas son: no se admiten pagos negativos y la recencia no puede ser negativa. También se verifica la integridad cliente-pago-alquiler.

## 5. Visualizaciones y decisiones (Actividad 3)

Se generan imágenes PNG de 150 dpi en `graficos/`:

- `heatmap_rfm_monto.png`: heatmap obligatorio de recencia versus frecuencia, con intensidad según monto promedio.
- `monto_por_frecuencia_narrativo.png`: barras con categoría destacada y anotación; el quintil 5 de frecuencia concentra el mayor monto promedio.
- `distribucion_monto_clientes.png`: distribución del monto total por cliente y línea de promedio.

Hallazgos actuales:

1. Priorizar la fidelización del quintil de frecuencia 5, que logra el mayor monto promedio.
2. Hay 19 clientes con segmento RFM 555; son candidatos a beneficios de permanencia.
3. Hay 120 clientes en el quintil de menor recencia; corresponde evaluar campañas de reactivación segmentada.

Limitación: el análisis es histórico y descriptivo; no incorpora costo de campañas, preferencias de películas ni evidencia causal.

## 6. Entorno y validación

Todo se verificó con `venv_tp2`: compilación de `config_conexion.py` y `esquema.py`, sintaxis de las 11 celdas del notebook y ejecución secuencial de las celdas. Para dejar evidencia en el archivo final, abrir `notebooks/analisis.ipynb` con el kernel `venv_tp2`, ejecutar **Run All** y guardar el notebook.

Antes de hacer commit, el equipo debe revisar conjuntamente los cambios pendientes y confirmar que nadie modificó los archivos que pertenecen al pipeline.

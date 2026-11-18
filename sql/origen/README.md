# Archivos utilizados como referencia de la carga de TP1

Se conservaron copias exactas de `sakila_carga_sql_server.sql` y
`sakila_sql_server.sql` aportadas por el equipo desde la carpeta TP.
Son traducciones a SQL Server. No son una copia verificada por separado del
volcado MySQL original mencionado en la devolución.

No deben ejecutarse al correr el análisis: el DDL puede eliminar y crear
tablas. El notebook solo lee los archivos para contar las tuplas y acreditar
la población de `film_text` mediante el trigger AFTER INSERT de `film`.

`mapeo_carga.json` describe estos archivos históricos. El mapeo de la base
destino continúa en `esquema.py`; cambiarlo para otro equipo no cambia los
nombres de los archivos archivados.

Las cantidades no están escritas en este manifiesto: se calculan desde las
tuplas. La evidencia generada guarda las huellas SHA-256 y el método de cada
tabla en `informe/evidencia_reconciliacion.json`.

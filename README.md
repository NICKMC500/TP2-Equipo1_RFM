# Trabajo Práctico 2 - Segmentación RFM (Sakila)

**Materia:** Seminario de Actualización / Bases de Datos 2026  
**Equipo:** Equipo 1

## Estado del proyecto

- [x] **Actividad 0:** reconciliación del origen Sakila y SQL Server.
- [x] **Actividad 1:** métricas RFM, quintiles y contraste SQL/pandas.
- [x] **Actividad 2:** perfilado, atípicos y controles de calidad.
- [x] **Actividad 3:** visualizaciones narrativas exportadas.
- [x] **Actividad 4:** pipeline ETL de reemplazo de snapshot, con evidencia de dos ejecuciones.
- [x] **Actividad 5:** informe final, diagnóstico de calidad y anexo de IA.

## Preparación del entorno

1. Crear y activar el entorno virtual requerido:

   ```powershell
   python -m venv venv_tp2
   .\venv_tp2\Scripts\Activate.ps1
   ```

2. Instalar las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. Tener SQL Server, **ODBC Driver 18 for SQL Server** y la base `sakila`
   creada y cargada mediante los scripts de migración compartidos por el equipo.

La conexión utiliza autenticación integrada de Windows y no guarda credenciales.
Si la instancia no es `./SQLEXPRESS`, se puede configurar antes de abrir el
notebook:

```powershell
$env:SQL_SERVER = ".\OTRA_INSTANCIA"
$env:SQL_DATABASE = "sakila"
$env:SQL_ODBC_DRIVER = "ODBC Driver 18 for SQL Server"
```

## Ejecución del análisis

Abrir `notebooks/analisis.ipynb` con el kernel de `venv_tp2`, ejecutar **Run
All** y guardar el notebook con las salidas visibles. Se obtiene:

- reconciliación de las 16 tablas contra el archivo real de carga de TP1;
- métricas RFM en SQL Server y pandas, resultados iguales y tiempos medidos;
- comparación de `pd.qcut` y `NTILE(5)` con tratamiento explícito de límites;
- perfilado, atípicos y controles de calidad reproducibles;
- tres gráficos PNG a 150 dpi dentro de `graficos/`.

## Ejecución del pipeline

Con `venv_tp2` activo, ejecutar desde la raíz del repositorio:

```powershell
python .\pipeline\pipeline_tp2.py
```

El proceso suma los pagos vinculados a alquileres con el mismo criterio del
notebook, combina los 599 clientes con el archivo de
prueba `pipeline/datos/perfil_comercial_clientes.csv` y calcula sus puntajes
RFM. Conserva los clientes sin perfil externo mediante una unión izquierda.
La carga crea `dbo.TP2_SegmentacionRFM` si falta y reemplaza sus filas dentro
de una transacción. Se necesitan permisos de creación y escritura sobre el
destino. No modifica las tablas de origen.

Para repetir y guardar la prueba completa de dos ejecuciones:

```powershell
python .\pipeline\verificar_idempotencia.py
```

La prueba invoca el archivo final por línea de comandos, ejecuta la consulta
`sql/verificar_destino.sql` tras cada carga, compara conteos, sumas y todas las
columnas de negocio y calcula una huella SHA-256 del resultado ordenado.
`fecha_proceso` registra la ejecución y puede variar; se excluye de la igualdad
de negocio. No se afirma igualdad literal de esa marca de auditoría.
`pipeline/Evidencia.log` y `pipeline/evidencia_idempotencia.json` conservan la
prueba actual junto con la huella del script ejecutado. El log de trabajo
`pipeline/pipeline.log` queda ignorado por Git.

## Estructura

```text
config_conexion.py   conexión sin credenciales
esquema.py           mapeo canónico al esquema local en español
reconciliar_origen.py conteo del archivo exacto de carga, sin ejecutarlo
sql/                 consultas, reglas y copias del origen usado en TP1
notebooks/           actividades 0 a 3
graficos/            visualizaciones exportadas
pipeline/            actividad 4, mantenida por el equipo responsable
informe/             informe final, diagnóstico de calidad y anexo de IA
```

## Nota de reconciliación

La corrección posterior a la devolución elimina los conteos escritos a mano.
`reconciliar_origen.py` cuenta las tuplas INSERT de
`sql/origen/sakila_carga_sql_server.sql`, copia exacta del archivo de `TP`
indicado por el equipo. Es el script traducido utilizado en la migración a
SQL Server, no se lo presenta como un volcado MySQL independiente.

```powershell
python .\reconciliar_origen.py
```

El archivo contiene 16.044 pagos y su identificador máximo es 16.049. Los
huecos 424, 7011, 10840, 14675 y 15458 no son filas perdidas durante la
migración. Las 16 tablas coinciden con la base revisada. `film_text` se
deriva del INSERT de `film` mediante el trigger AFTER INSERT acreditado en
el DDL adjunto; el informe diferencia este conteo derivado de los INSERT
directos. Las huellas de ambos archivos y los métodos quedan guardados en
`informe/evidencia_reconciliacion.json` al ejecutar el notebook.

Los scripts archivados en `sql/origen` contienen DDL y nombres físicos por
ser evidencia de TP1. No se ejecutan durante el análisis. Las consultas del
TP2 siguen resolviendo los nombres del origen desde `esquema.py`.
`sql/origen/mapeo_carga.json` conserva la correspondencia histórica del
archivo archivado; no se edita al adaptar la base destino en `esquema.py`.

## Correcciones y defensa oral

Las reglas temporales verifican devolución anterior al alquiler y pago
anterior al alquiler, tanto en SQL como en pandas. El gráfico narrativo
compara el promedio por cliente de monto / alquileres; el histograma
delimita un piloto comercial concreto. El informe y el diagnóstico se
actualizaron para reflejar estas correcciones.

`informe/correcciones_y_preparacion.md` detalla los cambios y las prácticas
del oral. Los textos `informe/wiki_*.md` están preparados para actualizar la
wiki: requieren revisión del equipo y publicación en el aula.

Para regenerar el informe (5 páginas), el diagnóstico (2 páginas) y la guía
oral desde los resultados verificados, dentro de `venv_tp2`:

```powershell
pip install -r requirements_documentacion.txt
python .\informe\generar_documentacion.py
python -m unittest discover -s tests -v
```

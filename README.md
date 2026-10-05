# TP2 - Segmentación de clientes por valor (RFM)

Materia: Seminario de Actualización - Equipo 1.

## Preparación

1. Crear y activar un entorno virtual:

   ```powershell
   python -m venv venv_tp2
   .\venv_tp2\Scripts\Activate.ps1
   ```

2. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. Tener SQL Server, **ODBC Driver 18 for SQL Server** y la base `sakila`
   creada y cargada con los scripts compartidos por el equipo.

4. Si la instancia no es `./SQLEXPRESS`, definir antes de abrir el notebook:

   ```powershell
   $env:SQL_SERVER = ".\OTRA_INSTANCIA"
   $env:SQL_DATABASE = "sakila"
   ```

No se guardan credenciales: la conexión utiliza autenticación integrada de
Windows.

## Ejecución del análisis

Abrir `notebooks/analisis.ipynb` con el kernel de `venv_tp2` y ejecutar **Run
All**. El notebook debe quedar guardado con sus salidas visibles. Produce:

- tabla de reconciliación de las 16 tablas;
- métrica RFM en SQL y pandas, con comparación de resultados y tiempos;
- validación `NTILE(5)` contra `qcut`;
- perfilado y controles de calidad de la variante;
- tres PNG a 150 dpi dentro de `graficos/`.

## Estructura

```text
config_conexion.py   conexión sin credenciales
esquema.py           mapeo canónico de tablas y columnas al esquema local
sql/                 reconciliación y conjunto de trabajo RFM
notebooks/           actividades 0 a 3
graficos/            visualizaciones exportadas
pipeline/            actividad 4, mantenida por el equipo responsable
informe/             actividad 5 y anexo de IA
```

## Nota sobre reconciliación

El volcado estándar de Sakila tiene 16.049 pagos y 16.044 alquileres. Si la
tabla `pago` presenta una diferencia de cinco filas, se debe documentar si los
pagos sin alquiler del origen fueron omitidos durante la migración y cuál es su
impacto sobre los ingresos.

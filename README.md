# Trabajo Práctico 2 - Segmentación RFM (Sakila)

**Materia:** Seminario de Actualización / Bases de Datos 2026  
**Equipo:** Equipo 1

## Estado del proyecto

- [x] **Actividad 0:** reconciliación del origen Sakila y SQL Server.
- [x] **Actividad 1:** métricas RFM, quintiles y contraste SQL/pandas.
- [x] **Actividad 2:** perfilado, atípicos y controles de calidad.
- [x] **Actividad 3:** visualizaciones narrativas exportadas.
- [ ] **Actividad 4:** pipeline ETL idempotente, a cargo del integrante responsable.
- [ ] **Actividad 5:** informe final y anexo de IA.

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

- reconciliación de las 16 tablas, con origen MySQL, SQL Server y diferencia;
- métricas RFM en SQL Server y pandas, resultados iguales y tiempos medidos;
- comparación de `pd.qcut` y `NTILE(5)` con tratamiento explícito de límites;
- perfilado, atípicos y controles de calidad reproducibles;
- tres gráficos PNG a 150 dpi dentro de `graficos/`.

## Estructura

```text
config_conexion.py   conexión sin credenciales
esquema.py           mapeo canónico al esquema local en español
sql/                 reconciliación y conjunto de trabajo RFM
notebooks/           actividades 0 a 3
graficos/            visualizaciones exportadas
pipeline/            actividad 4, mantenida por el equipo responsable
informe/             informe final, anexo de IA y reporte de revisión
```

## Nota de reconciliación

El volcado estándar de Sakila registra 16.049 pagos y 16.044 alquileres. En
esta migración, `pago` tiene cinco filas menos; el notebook conserva la
diferencia visible y evalúa su impacto mediante controles de pagos sin
alquiler. No se altera ni se inventa información de origen.

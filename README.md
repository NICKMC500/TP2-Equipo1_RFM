```
# 📊 Trabajo Práctico 2 - Segmentación RFM (Base de Datos Sakila)
**Materia:** Seminario de Lenguajes / BD 2026  
**Equipo:** Equipo 1  
**Repositorio:** `https://github.com/NICKMC500/TP2-Equipo1_RFM.git`

---

## 📌 Estado del Proyecto
* [x] **Actividad 0:** Reconciliación de filas T-SQL vs. Python.
* [x] **Actividad 1:** Extracción de métricas RFM y discretización por quintiles (`pd.qcut` vs. `NTILE(5)`).
* [x] **Actividad 2:** Profiling de calidad, detección de atípicos (IQR) y reglas de negocio.
* [x] **Actividad 3:** Visualización narrativa (Mapa de Calor de Recencia vs. Frecuencia exportado).
* [ ] **Actividad 4:** Pipeline ETL automatizado e idempotente (`pipeline/pipeline_tp2.py`).
* [ ] **Actividad 5:** Informe técnico final (`informe/informe.pdf`) y Anexo de IA (`informe/anexo_ia.md`).

---

## 🚀 Guía de Inicio Rápido para el Equipo

### 1. Clonar el Repositorio
Abran la terminal (Git Bash o PowerShell) en la carpeta de sus proyectos y ejecuten:
```bash
git clone https://github.com/NICKMC500/TP2-Equipo1_RFM.git
cd TP2-Equipo1_RFM

```

### 2\. Crear y Activar el Entorno Virtual

```
# Crear entorno virtual
python -m venv venv_tp2

# Activar en Windows (PowerShell)
.\venv_tp2\Scripts\Activate.ps1

# Activar en Git Bash / Linux / macOS
source venv_tp2/bin/activate

```

### 3\. Instalar Dependencias

```
pip install -r requirements.txt

```

### 4\. Configurar Conexión Local a SQL Server

Asegúrense de revisar el archivo `config_conexion.py` y verificar que el nombre del servidor o puerto coincida con su instancia local de SQL Server con la base de datos `sakila` (migrada en español).

---

## 📂 Estructura del Repositorio

```
TP2-Equipo1_RFM/
├── README.md                  # Guía de inicio e instrucciones del proyecto
├── .gitignore                 # Filtro de archivos excluidos de Git
├── requirements.txt           # Librerías necesarias (Pandas, SQLAlchemy, Seaborn, etc.)
├── config_conexion.py         # Módulo de conexión a SQL Server
├── esquema.py                 # Mapeo de nombres canónicos a español
├── sql/
│   ├── reconciliacion.sql     # Consulta de conteo de filas
│   └── conjunto_trabajo.sql   # Consulta de extracción de métricas RFM
├── notebooks/
│   └── analisis.ipynb         # Notebook con Actividades 0, 1, 2 y 3
├── graficos/
│   └── heatmap_rfm_monto.png  # Mapa de calor exportado a 150 dpi
├── pipeline/                  # [Pendiente] Script ETL de la Activ
```

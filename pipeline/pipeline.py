"""
Pipeline ETL RFM que reutiliza config_conexion.py y esquema.py del proyecto.
Ejecutar desde la raíz:
    python .\pipeline\pipeline.py
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import text

# Al ejecutar este archivo directamente, Python agrega pipeline/ a sys.path.
# Agregamos la raíz del proyecto para importar sus módulos compartidos.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from config_conexion import engine
from esquema import renderizar_sql


DIRECTORIO_PIPELINE = Path(__file__).resolve().parent
DIRECTORIO_DATOS = DIRECTORIO_PIPELINE / "datos"
RUTA_CSV = DIRECTORIO_DATOS / "perfil_comercial_clientes.csv"
RUTA_DDL = DIRECTORIO_DATOS / "crear_tabla_rfm.sql"
RUTA_RESPALDO = DIRECTORIO_DATOS / "respaldo_rfm.sql"
TABLA_DESTINO = "[dbo].[TP2_SegmentacionRFM]"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(DIRECTORIO_PIPELINE / "pipeline.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("pipeline_rfm")


# La plantilla usa nombres canónicos de Sakila. renderizar_sql() sustituye
# {{customer}}, {{rental.customer_id}}, etc. según el diccionario de esquema.py.
CONSULTA_RFM_CANONICA = """
WITH fecha_maxima AS (
    SELECT MAX({{rental.rental_date}}) AS max_rental_date
    FROM {{rental}}
),
rental_por_cliente AS (
    SELECT
        {{rental.customer_id}} AS customer_id,
        COUNT_BIG(*) AS rental_frequency,
        MAX({{rental.rental_date}}) AS last_rental_date
    FROM {{rental}}
    GROUP BY {{rental.customer_id}}
),
payment_por_cliente AS (
    SELECT
        {{payment.customer_id}} AS customer_id,
        SUM(CAST({{payment.amount}} AS DECIMAL(12, 2))) AS monetary_amount
    FROM {{payment}}
    GROUP BY {{payment.customer_id}}
)
SELECT
    c.{{customer.customer_id}} AS customer_id,
    c.{{customer.first_name}} AS first_name,
    c.{{customer.last_name}} AS last_name,
    CASE
        WHEN rc.last_rental_date IS NULL THEN NULL
        ELSE DATEDIFF(DAY, rc.last_rental_date, fm.max_rental_date)
    END AS recency_days,
    COALESCE(rc.rental_frequency, 0) AS rental_frequency,
    COALESCE(pc.monetary_amount, 0) AS monetary_amount
FROM {{customer}} AS c
CROSS JOIN fecha_maxima AS fm
LEFT JOIN rental_por_cliente AS rc
    ON rc.customer_id = c.{{customer.customer_id}}
LEFT JOIN payment_por_cliente AS pc
    ON pc.customer_id = c.{{customer.customer_id}}
ORDER BY c.{{customer.customer_id}};
"""


def extraer():
    """Extrae métricas RFM de la DB y lee el CSV complementario."""
    logger.info("ETAPA 1/4 - EXTRACCIÓN: inicio.")
    if not RUTA_CSV.exists():
        raise FileNotFoundError(f"No se encontró el CSV: {RUTA_CSV}")

    # El SQL escrito aquí usa nombres canónicos. Los nombres locales en español
    # solo se obtienen mediante esquema.py.
    consulta_sql = renderizar_sql(CONSULTA_RFM_CANONICA)
    logger.info("Consulta RFM preparada usando el diccionario esquema.py.")

    try:
        with engine.connect() as conexion:
            logger.info("Consultando customer, rental y payment en SQL Server...")
            df_db = pd.read_sql(text(consulta_sql), conexion)
        logger.info("Extracción desde SQL Server completada: %d filas.", len(df_db))
    except Exception:
        logger.exception("No se pudo extraer desde SQL Server.")
        raise

    logger.info("Leyendo datos complementarios desde %s...", RUTA_CSV.name)
    try:
        df_csv = pd.read_csv(RUTA_CSV)
        logger.info("CSV leído correctamente: %d filas.", len(df_csv))
    except Exception:
        logger.exception("No se pudo leer el CSV complementario.")
        raise


    if df_db.empty:
        raise ValueError("La consulta SQL no devolvió clientes.")

    # Validar que ambos orígenes respeten el nombre canónico de la clave.
    if "customer_id" not in df_db.columns:
        raise ValueError(
            "La consulta SQL no devolvió la columna canónica customer_id. "
            "Revisá CONSULTA_RFM_CANONICA y esquema.py."
        )
    
    if "customer_id" not in df_csv.columns:
        raise ValueError(
            "El CSV debe contener la columna canónica customer_id."
        )

    # Validar que las claves no sean nulas.
    if df_db["customer_id"].isna().any():
        raise ValueError("La extracción SQL contiene customer_id nulos.")

    if df_csv["customer_id"].isna().any():
        raise ValueError("El CSV contiene customer_id nulos.")

    # Validar que las claves sean únicas en la extracción SQL.
    if df_db["customer_id"].duplicated().any():
        raise ValueError(
            "La extracción SQL contiene customer_id duplicados."
        )

    # El CSV complementario debe tener una sola fila por cliente.
    if df_csv["customer_id"].duplicated().any():
        raise ValueError(
            "El CSV contiene customer_id duplicados; "
            "el merge sería ambiguo."
        )

    # Evitar que el merge falle o pierda coincidencias por tipos diferentes.
    try:
        df_db["customer_id"] = pd.to_numeric(
            df_db["customer_id"], errors="raise"
        ).astype("int64")

        df_csv["customer_id"] = pd.to_numeric(
            df_csv["customer_id"], errors="raise"
        ).astype("int64")
    except (ValueError, TypeError, OverflowError):
        raise ValueError(
            "customer_id debe contener identificadores enteros válidos "
            "en ambos orígenes."
        )

    logger.info(
        "Validación de claves completada: SQL=%d clientes, CSV=%d registros.",
        len(df_db),
        len(df_csv),
    )

    return df_db, df_csv


def _puntuar_quintiles(serie, invertir=False):
    """Asigna puntuaciones de 1 a 5; rank(method='first') resuelve empates."""
    etiquetas = [5, 4, 3, 2, 1] if invertir else [1, 2, 3, 4, 5]
    rangos = pd.to_numeric(serie, errors="coerce").fillna(0).rank(method="first")
    return pd.qcut(rangos, q=5, labels=etiquetas).astype(int)


def transformar(df_db, df_csv):
    """Limpia, hace merge con el CSV y calcula puntuaciones RFM."""
    logger.info("ETAPA 2/4 - TRANSFORMACIÓN: inicio.")
    logger.info("Datos DB: %d filas; CSV: %d filas.", len(df_db), len(df_csv))

    df = df_db.copy()
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="raise").astype(int)
    df["rental_frequency"] = pd.to_numeric(
        df["rental_frequency"], errors="coerce"
    ).fillna(0).astype(int)
    df["monetary_amount"] = pd.to_numeric(
        df["monetary_amount"], errors="coerce"
    ).fillna(0.0)
    df["recency_days"] = pd.to_numeric(df["recency_days"], errors="coerce")

    max_recency = df["recency_days"].max()
    recencia_sin_alquiler = 0 if pd.isna(max_recency) else float(max_recency) + 1
    df["recency_days"] = df["recency_days"].fillna(recencia_sin_alquiler)

    df_csv = df_csv.copy()
    df_csv["customer_id"] = pd.to_numeric(
        df_csv["customer_id"], errors="raise"
    ).astype(int)

    logger.info("Combinando DB + CSV mediante pandas.merge() por customer_id...")
    df = df.merge(
        df_csv,
        on="customer_id",
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    coincidencias = int((df["_merge"] == "both").sum())
    sin_csv = int((df["_merge"] == "left_only").sum())
    logger.info("Merge: %d coincidencias y %d clientes sin perfil en el CSV.",
                coincidencias, sin_csv)
    df.drop(columns="_merge", inplace=True)

    df["perfil_comercial"] = df["perfil_comercial"].fillna("Sin perfil")
    df["canal_preferido"] = df["canal_preferido"].fillna("No informado")
    df["descuento_sugerido_pct"] = pd.to_numeric(
        df["descuento_sugerido_pct"], errors="coerce"
    ).fillna(0).clip(0, 100)

    if len(df) < 5:
        raise ValueError("Se necesitan al menos cinco clientes para calcular quintiles.")

    logger.info("Calculando scores R, F y M mediante quintiles en pandas...")
    df["score_recencia"] = _puntuar_quintiles(df["recency_days"], invertir=True)
    df["score_frecuencia"] = _puntuar_quintiles(df["rental_frequency"])
    df["score_monto"] = _puntuar_quintiles(df["monetary_amount"])
    df["segmento_rfm"] = (
        df["score_recencia"].astype(str)
        + df["score_frecuencia"].astype(str)
        + df["score_monto"].astype(str)
    )
    df["fecha_proceso"] = datetime.now().replace(microsecond=0)

    # Hasta este punto se mantienen nombres canónicos. El renombrado se hace
    # exclusivamente para adaptar el DataFrame al esquema de la tabla destino.
    df_final = df[[
        "customer_id", "first_name", "last_name", "recency_days",
        "rental_frequency", "monetary_amount", "score_recencia",
        "score_frecuencia", "score_monto", "segmento_rfm",
        "perfil_comercial", "canal_preferido", "descuento_sugerido_pct",
        "fecha_proceso",
    ]].rename(columns={
        "customer_id": "id_cliente",
        "first_name": "nombre",
        "last_name": "apellido",
        "recency_days": "recencia_dias",
        "rental_frequency": "frecuencia",
        "monetary_amount": "monto_total",
    })
    logger.info("Transformación finalizada: %d filas y %d segmentos distintos.",
                len(df_final), df_final["segmento_rfm"].nunique())
    return df_final


def _literal_sql(valor):
    """Serializa valores para el archivo de respaldo SQL y escapa comillas."""
    if pd.isna(valor):
        return "NULL"
    if isinstance(valor, (pd.Timestamp, datetime)):
        return "'" + valor.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if hasattr(valor, "item"):
        valor = valor.item()
    if isinstance(valor, bool):
        return "1" if valor else "0"
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, float):
        return format(valor, ".10g")
    return "'" + str(valor).replace("'", "''") + "'"


def guardar_respaldo_sql(df_final):
    """Genera sentencias de recuperación si la carga falla después de transformar."""
    logger.warning("Generando respaldo SQL del resultado transformado...")
    columnas = list(df_final.columns)
    columnas_sql = ", ".join(f"[{col}]" for col in columnas)
    lineas = [
        "-- Respaldo generado por pipeline.py",
        "SET XACT_ABORT ON;",
        "BEGIN TRY",
        "    BEGIN TRANSACTION;",
        f"    DELETE FROM {TABLA_DESTINO};",
    ]
    for _, fila in df_final.iterrows():
        valores = ", ".join(_literal_sql(fila[col]) for col in columnas)
        lineas.append(
            f"    INSERT INTO {TABLA_DESTINO} ({columnas_sql}) VALUES ({valores});"
        )
    lineas.extend([
        "    COMMIT TRANSACTION;",
        "END TRY",
        "BEGIN CATCH",
        "    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;",
        "    THROW;",
        "END CATCH;",
    ])
    RUTA_RESPALDO.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    logger.warning("Respaldo SQL guardado en %s.", RUTA_RESPALDO)


def cargar(df_final):
    """Crea la tabla destino si falta y reemplaza sus filas transaccionalmente."""
    logger.info("ETAPA 3/4 - CARGA: inicio; filas a cargar: %d.", len(df_final))
    if df_final["id_cliente"].duplicated().any():
        raise ValueError("Carga cancelada: id_cliente duplicados.")

    try:
        with engine.begin() as conexion:
            logger.info("Verificando/creando la tabla destino si no existe...")
            ddl = RUTA_DDL.read_text(encoding="utf-8")
            # DDL no tiene GO; puede ejecutarse como un solo bloque.
            conexion.exec_driver_sql(ddl)

            logger.info("Eliminando el snapshot anterior dentro de la transacción...")
            conexion.exec_driver_sql(f"DELETE FROM {TABLA_DESTINO}")

            logger.info("Insertando el nuevo snapshot...")
            df_final.to_sql(
                name="TP2_SegmentacionRFM",
                schema="dbo",
                con=conexion,
                if_exists="append",
                index=False,
                chunksize=500,
            )
            logger.info("Inserción completada; se confirmará la transacción.")
        logger.info("COMMIT realizado correctamente.")
        if RUTA_RESPALDO.exists():
            RUTA_RESPALDO.unlink()
            logger.info("Respaldo anterior eliminado porque la carga tuvo éxito.")
    except Exception:
        logger.exception("Error de carga: se revierte la transacción si estaba abierta.")
        try:
            guardar_respaldo_sql(df_final)
        except Exception:
            logger.exception("No se pudo generar el respaldo SQL.")
        raise


def ejecutar_pipeline():
    """Orquestador principal: extraer -> transformar -> cargar -> verificar."""
    inicio = datetime.now()
    logger.info("=" * 72)
    logger.info("INICIO DEL PIPELINE ETL: %s", inicio.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        df_db, df_csv = extraer()
        df_final = transformar(df_db, df_csv)
        cargar(df_final)

        logger.info("ETAPA 4/4 - VERIFICACIÓN: contando filas en la tabla destino...")
        with engine.connect() as conexion:
            cantidad = conexion.execute(
                text(f"SELECT COUNT(*) FROM {TABLA_DESTINO}")
            ).scalar_one()

        logger.info("Destino: %d filas; esperado: %d filas.", cantidad, len(df_final))
        if cantidad != len(df_final):
            raise RuntimeError(
                f"La cantidad cargada ({cantidad}) no coincide con la esperada ({len(df_final)})."
            )
        logger.info("PIPELINE FINALIZADO CORRECTAMENTE. Duración: %s.",
                    datetime.now() - inicio)
    except Exception:
        logger.exception("PIPELINE FALLÓ. Se propaga el error para no ocultar el fallo.")
        raise
    finally:
        # engine pertenece a config_conexion.py y se reutiliza en todo el proyecto.
        logger.info("Fin del proceso ETL.")


if __name__ == "__main__":
    ejecutar_pipeline()

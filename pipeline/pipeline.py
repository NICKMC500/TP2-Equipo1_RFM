import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine, text

BASE = Path(__file__).resolve().parent
DATOS = BASE / "datos"
CSV = DATOS / "perfil_comercial_clientes.csv"
DDL = DATOS / "crear_tabla_rfm.sql"
RESPALDO = DATOS / "respaldo_rfm.sql"
DESTINO = "dbo.TP2_SegmentacionRFM"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(BASE / "pipeline.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("etl_rfm")


def crear_engine():
    servidor = os.getenv("SQL_SERVER", r".\SQLEXPRESS")
    #servidor = os.getenv("SQL_SERVER", "FAMILIAAMORPC")
    base_datos = os.getenv("SQL_DATABASE", "sakila")
    driver = os.getenv("SQL_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
    odbc = (
        f"DRIVER={{{driver}}};SERVER={servidor};DATABASE={base_datos};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    url = URL.create("mssql+pyodbc", query={"odbc_connect": odbc})
    log.info("Conectando a SQL Server: servidor=%s, base=%s, driver=%s",
             servidor, base_datos, driver)
    return create_engine(url, pool_pre_ping=True, fast_executemany=True)


def extraer():
    """Extrae métricas agregadas desde SQL Server y lee el CSV ficticio."""
    log.info("ETAPA 1/3 - EXTRACCIÓN: comienza.")
    if not CSV.exists():
        raise FileNotFoundError(f"No existe el CSV: {CSV}")

    consulta = text("""
        WITH fecha_maxima AS (
            SELECT MAX(fecha_alquiler) AS max_fecha FROM dbo.alquiler
        ),
        alquiler_cliente AS (
            SELECT id_cliente, COUNT_BIG(*) AS frecuencia,
                   MAX(fecha_alquiler) AS ultima_fecha
            FROM dbo.alquiler GROUP BY id_cliente
        ),
        pago_cliente AS (
            SELECT id_cliente, SUM(CAST(monto AS DECIMAL(12,2))) AS monto_total
            FROM dbo.pago GROUP BY id_cliente
        )
        SELECT c.id_cliente, c.nombre, c.apellido,
               CASE WHEN ac.ultima_fecha IS NULL THEN NULL
                    ELSE DATEDIFF(DAY, ac.ultima_fecha, fm.max_fecha) END AS recencia_dias,
               COALESCE(ac.frecuencia, 0) AS frecuencia,
               COALESCE(pc.monto_total, 0) AS monto_total
        FROM dbo.cliente c
        CROSS JOIN fecha_maxima fm
        LEFT JOIN alquiler_cliente ac ON ac.id_cliente = c.id_cliente
        LEFT JOIN pago_cliente pc ON pc.id_cliente = c.id_cliente
        ORDER BY c.id_cliente
    """)
    engine = crear_engine()
    try:
        with engine.connect() as conn:
            log.info("Ejecutando consulta de clientes, alquileres y pagos...")
            df_sql = pd.read_sql(consulta, conn)
        log.info("SQL Server devolvió %d filas.", len(df_sql))
    finally:
        engine.dispose()
        log.info("Conexión de extracción cerrada.")

    log.info("Leyendo CSV ficticio: %s", CSV.name)
    df_csv = pd.read_csv(CSV)
    log.info("CSV leído: %d filas.", len(df_csv))
    if df_sql.empty:
        raise ValueError("La consulta no devolvió clientes.")
    if df_csv["id_cliente"].duplicated().any():
        raise ValueError("El CSV contiene id_cliente duplicados.")
    return df_sql, df_csv


def _quintil(serie, invertir=False):
    etiquetas = [5, 4, 3, 2, 1] if invertir else [1, 2, 3, 4, 5]
    return pd.qcut(serie.fillna(0).rank(method="first"), q=5, labels=etiquetas).astype(int)


def transformar(df_sql, df_csv):
    """Limpia, combina con merge y calcula los scores/segmentos RFM."""
    log.info("ETAPA 2/3 - TRANSFORMACIÓN: comienza.")
    df = df_sql.copy()
    df["id_cliente"] = df["id_cliente"].astype(int)
    df["frecuencia"] = pd.to_numeric(df["frecuencia"]).fillna(0).astype(int)
    df["monto_total"] = pd.to_numeric(df["monto_total"]).fillna(0)
    df["recencia_dias"] = pd.to_numeric(df["recencia_dias"])
    max_recencia = df["recencia_dias"].max()
    df["recencia_dias"] = df["recencia_dias"].fillna(
        0 if pd.isna(max_recencia) else max_recencia + 1
    )

    df_csv = df_csv.copy()
    df_csv["id_cliente"] = df_csv["id_cliente"].astype(int)
    log.info("Uniendo DataFrame SQL con CSV mediante merge por id_cliente (left join).")
    df = df.merge(df_csv, on="id_cliente", how="left", validate="one_to_one", indicator=True)
    coinciden = int((df["_merge"] == "both").sum())
    faltantes = int((df["_merge"] == "left_only").sum())
    log.info("Merge completado: %d coincidencias y %d clientes sin perfil CSV.",
             coinciden, faltantes)
    df.drop(columns="_merge", inplace=True)
    df["perfil_comercial"] = df["perfil_comercial"].fillna("Sin perfil")
    df["canal_preferido"] = df["canal_preferido"].fillna("No informado")
    df["descuento_sugerido_pct"] = pd.to_numeric(
        df["descuento_sugerido_pct"], errors="coerce"
    ).fillna(0).clip(0, 100)

    if len(df) < 5:
        raise ValueError("Se requieren al menos cinco clientes para calcular quintiles.")
    log.info("Calculando quintiles RFM...")
    df["score_recencia"] = _quintil(df["recencia_dias"], invertir=True)
    df["score_frecuencia"] = _quintil(df["frecuencia"])
    df["score_monto"] = _quintil(df["monto_total"])
    df["segmento_rfm"] = (
        df["score_recencia"].astype(str)
        + df["score_frecuencia"].astype(str)
        + df["score_monto"].astype(str)
    )
    df["fecha_proceso"] = datetime.now().replace(microsecond=0)
    cols = [
        "id_cliente", "nombre", "apellido", "recencia_dias", "frecuencia",
        "monto_total", "score_recencia", "score_frecuencia", "score_monto",
        "segmento_rfm", "perfil_comercial", "canal_preferido",
        "descuento_sugerido_pct", "fecha_proceso",
    ]
    resultado = df[cols].copy()
    log.info("Transformación terminada: %d filas; %d segmentos distintos.",
             len(resultado), resultado["segmento_rfm"].nunique())
    return resultado


def _literal_sql(v):
    if pd.isna(v):
        return "NULL"
    if isinstance(v, (pd.Timestamp, datetime)):
        return "'" + v.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return format(v, ".10g")
    return "'" + str(v).replace("'", "''") + "'"


def guardar_respaldo_sql(df):
    """Escribe un script SQL si falla la carga tras transformar los datos."""
    log.warning("Intentando guardar respaldo SQL del DataFrame transformado...")
    cols = list(df.columns)
    nombres = ", ".join(f"[{c}]" for c in cols)
    lineas = [
        "-- Respaldo generado por pipeline.py",
        "SET XACT_ABORT ON;",
        "BEGIN TRY",
        "  BEGIN TRANSACTION;",
        f"  DELETE FROM {DESTINO};",
    ]
    for _, row in df.iterrows():
        vals = ", ".join(_literal_sql(row[c]) for c in cols)
        lineas.append(f"  INSERT INTO {DESTINO} ({nombres}) VALUES ({vals});")
    lineas += ["  COMMIT TRANSACTION;", "END TRY", "BEGIN CATCH",
               "  IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;", "  THROW;", "END CATCH;"]
    RESPALDO.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    log.warning("Respaldo escrito en: %s", RESPALDO)


def cargar(df_final):
    """Crea destino si falta y reemplaza los datos dentro de una transacción."""
    log.info("ETAPA 3/3 - CARGA: se cargarán %d filas.", len(df_final))
    if df_final["id_cliente"].duplicated().any():
        raise ValueError("Carga cancelada: id_cliente duplicados.")
    engine = crear_engine()
    try:
        with engine.begin() as conn:
            log.info("Verificando/creando la tabla destino...")
            conn.exec_driver_sql(DDL.read_text(encoding="utf-8"))
            log.info("Eliminando filas anteriores dentro de la transacción...")
            conn.exec_driver_sql(f"DELETE FROM {DESTINO}")
            log.info("Insertando nuevo snapshot en SQL Server...")
            df_final.to_sql("TP2_SegmentacionRFM", con=conn, schema="dbo",
                            if_exists="append", index=False, chunksize=500)
            log.info("Insert ejecutado; confirmando transacción.")
        log.info("COMMIT confirmado. Filas cargadas: %d.", len(df_final))
        if RESPALDO.exists():
            RESPALDO.unlink()
            log.info("Respaldo anterior eliminado tras carga exitosa.")
    except Exception:
        log.exception("Falló la carga; SQLAlchemy intentará hacer rollback.")
        try:
            guardar_respaldo_sql(df_final)
        except Exception:
            log.exception("No se pudo generar el respaldo SQL.")
        raise
    finally:
        engine.dispose()
        log.info("Conexión de carga cerrada.")


def ejecutar_pipeline():
    """Orquestador principal: extracción -> transformación -> carga -> verificación."""
    inicio = datetime.now()
    log.info("=" * 68)
    log.info("INICIO DEL PIPELINE ETL: %s", inicio.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        df_sql, df_csv = extraer()
        df_final = transformar(df_sql, df_csv)
        cargar(df_final)
        engine = crear_engine()
        try:
            with engine.connect() as conn:
                total = conn.execute(text(f"SELECT COUNT(*) FROM {DESTINO}")).scalar_one()
            log.info("VERIFICACIÓN: destino tiene %d filas; DataFrame tenía %d.",
                     total, len(df_final))
            if total != len(df_final):
                raise RuntimeError("La cantidad de filas cargadas no coincide con la esperada.")
        finally:
            engine.dispose()
        log.info("PIPELINE FINALIZADO CORRECTAMENTE. Duración: %s", datetime.now() - inicio)
    except Exception:
        log.exception("PIPELINE FALLÓ; se propaga la excepción para devolver código de error.")
        raise


if __name__ == "__main__":
    ejecutar_pipeline()

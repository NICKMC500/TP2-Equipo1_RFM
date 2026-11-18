"""Ejecuta dos veces el archivo final por CLI y guarda evidencia reproducible."""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
from sqlalchemy import text

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from config_conexion import engine


def verificar():
    script = RAIZ / "pipeline" / "pipeline_tp2.py"
    consulta = (RAIZ / "sql" / "verificar_destino.sql").read_text(encoding="utf-8")
    evidencia = RAIZ / "pipeline" / "Evidencia.log"
    resumen = {"fecha": datetime.now().isoformat(timespec="seconds"),
               "script": "pipeline/pipeline_tp2.py",
               "sha256_script": hashlib.sha256(script.read_bytes()).hexdigest(),
               "consulta_control": consulta,
               "excluida_de_comparacion": ["fecha_proceso"], "ejecuciones": []}
    anteriores = None
    with evidencia.open("w", encoding="utf-8") as log:
        log.write("Evidencia de la versión final del pipeline\n")
        log.write(json.dumps({k: v for k, v in resumen.items() if k != "ejecuciones"}, ensure_ascii=False, indent=2) + "\n")
        for intento in (1, 2):
            comando = [sys.executable, str(script)]
            log.write(f"\nEJECUCIÓN {intento}: python pipeline/pipeline_tp2.py\n")
            resultado = subprocess.run(comando, cwd=RAIZ, capture_output=True,
                                       text=True, encoding="utf-8", errors="replace",
                                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            log.write(resultado.stdout + resultado.stderr)
            log.flush()
            if resultado.returncode:
                raise RuntimeError(f"La ejecución {intento} falló; revisar {evidencia}")
            with engine.connect() as conexion:
                control = pd.read_sql_query(text(consulta), conexion).iloc[0].to_dict()
                datos = pd.read_sql_query(text("SELECT * FROM dbo.TP2_SegmentacionRFM ORDER BY id_cliente"), conexion)
            negocio = datos.drop(columns="fecha_proceso")
            if negocio["id_cliente"].duplicated().any() or negocio.empty:
                raise AssertionError("El destino está vacío o contiene clientes duplicados.")
            huella = hashlib.sha256(negocio.to_json(orient="records", double_precision=10).encode("utf-8")).hexdigest()
            registro = {"ejecucion": intento, "control_sql": control, "sha256_negocio": huella,
                        "fecha_proceso": str(datos["fecha_proceso"].iloc[0])}
            resumen["ejecuciones"].append(registro)
            log.write("CONTROL SQL: " + json.dumps(control, ensure_ascii=False, default=str) + "\n")
            log.write("SHA256 de negocio: " + huella + "\n")
            if anteriores is not None:
                assert_frame_equal(anteriores, negocio, check_exact=True)
                if resumen["ejecuciones"][0]["control_sql"] != control:
                    raise AssertionError("Cambió el conteo o una suma de control.")
            anteriores = negocio
        resumen["resultado"] = "Dos ejecuciones: conteos, sumas y todas las columnas de negocio idénticas."
        log.write("\nRESULTADO: " + resumen["resultado"] + "\n")
    (RAIZ / "pipeline" / "evidencia_idempotencia.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(resumen["resultado"])
    print("Evidencia:", evidencia)
    engine.dispose()


if __name__ == "__main__":
    verificar()

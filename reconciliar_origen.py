"""Cuenta las filas INSERT del archivo real de carga, sin ejecutarlo.

El lector reconoce INSERT INTO ... VALUES y respeta cadenas, comillas escapadas
y paréntesis internos. No pretende interpretar SQL arbitrario ni ejecutar DDL.
La población de film_text mediante trigger se acredita con el DDL adjunto.
"""

import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from esquema import MAPEO_TABLAS

RAIZ = Path(__file__).resolve().parent
ORIGEN = RAIZ / "sql" / "origen"
IDENT = r"(?:\[[^\]]+\]|`[^`]+`|[A-Za-z_][A-Za-z0-9_]*)"
TABLA = rf"{IDENT}(?:\s*\.\s*{IDENT}){{0,2}}"
INSERT = re.compile(rf"\bINSERT\s+INTO\s+({TABLA})\s*(?:\([^;]*?\))?\s+VALUES\s*", re.I)


def contar_tuplas(sql, inicio):
    """Devuelve cantidad e identificadores iniciales de un bloque VALUES."""
    profundidad, cadena, cantidad, ids = 0, False, 0, []
    i = inicio
    while i < len(sql):
        caracter = sql[i]
        if cadena:
            if caracter == "'":
                if i + 1 < len(sql) and sql[i + 1] == "'":
                    i += 2
                    continue
                cadena = False
        elif caracter == "'":
            cadena = True
        elif caracter == ";" and profundidad == 0:
            return cantidad, ids
        elif caracter == "(":
            if profundidad == 0:
                cantidad += 1
                primero = re.match(r"\s*(\d+)\s*,", sql[i + 1: i + 40])
                if primero:
                    ids.append(int(primero.group(1)))
            profundidad += 1
        elif caracter == ")":
            profundidad -= 1
            if profundidad < 0:
                raise ValueError("Paréntesis desbalanceados en VALUES.")
        i += 1
    raise ValueError("Bloque VALUES sin cierre de sentencia; revisar el origen.")


def contar_origen(ruta=None):
    ruta = Path(ruta or os.getenv("SAKILA_ORIGEN_SQL", ORIGEN / "sakila_carga_sql_server.sql"))
    contenido = ruta.read_bytes()
    sql = contenido.decode("utf-8-sig")
    # El origen archivado conserva sus nombres de TP1 aunque esquema.py se
    # adapte para consultar la base de otro equipo.
    mapeo_origen = json.loads((ORIGEN / "mapeo_carga.json").read_text(encoding="utf-8"))["tablas"]
    inverso = {local.lower(): canonica for canonica, local in mapeo_origen.items()}
    conteos, ids, metodos = defaultdict(int), defaultdict(list), {}
    for coincidencia in INSERT.finditer(sql):
        local = re.sub(r"[\[\]`\s]", "", coincidencia.group(1)).split(".")[-1].lower()
        canonica = local if local in MAPEO_TABLAS else inverso.get(local)
        if canonica is None:
            raise ValueError(f"Tabla del archivo no mapeada: {local}")
        cantidad, primeros = contar_tuplas(sql, coincidencia.end())
        conteos[canonica] += cantidad
        ids[canonica].extend(primeros)
        metodos[canonica] = "tuplas INSERT contadas en archivo"

    ddl = ORIGEN / "sakila_sql_server.sql"
    if "film_text" not in conteos and "film" in conteos:
        texto_ddl = re.sub(r"[\[\]]", "", ddl.read_text(encoding="utf-8-sig"))
        film = re.escape(mapeo_origen["film"])
        film_text = re.escape(mapeo_origen["film_text"])
        patron = rf"CREATE\s+TRIGGER\s+\S+\s+ON\s+(?:dbo\.)?{film}\s+AFTER\s+INSERT\s+AS\s+BEGIN.*?INSERT\s+INTO\s+(?:dbo\.)?{film_text}\s*\([^)]*\)\s*SELECT\s+[^;]+\s+FROM\s+inserted\s*;"
        if not re.search(patron, texto_ddl, re.I | re.S):
            raise ValueError("film_text no tiene INSERT directo ni trigger de carga acreditado.")
        conteos["film_text"] = conteos["film"]
        metodos["film_text"] = "derivado del INSERT de film por trigger AFTER INSERT acreditado en DDL"

    faltantes = set(MAPEO_TABLAS) - set(conteos)
    if faltantes:
        raise ValueError(f"No se pudo contar: {sorted(faltantes)}")
    pagos = ids["payment"]
    if len(pagos) != conteos["payment"] or len(pagos) != len(set(pagos)):
        raise ValueError("No se pudo verificar una clave única por pago en el archivo.")
    return {
        "archivo": ruta.name,
        "procedencia": "script de carga traducido a SQL Server utilizado por el equipo en TP1",
        "sha256": hashlib.sha256(contenido).hexdigest(),
        "ddl_sha256": hashlib.sha256(ddl.read_bytes()).hexdigest(),
        "mapeo_historico_sha256": hashlib.sha256((ORIGEN / "mapeo_carga.json").read_bytes()).hexdigest(),
        "conteos": dict(sorted(conteos.items())),
        "metodos": dict(sorted(metodos.items())),
        "pagos": {"filas": len(pagos), "max_id": max(pagos),
                   "huecos_id": sorted(set(range(min(pagos), max(pagos) + 1)) - set(pagos))},
    }


if __name__ == "__main__":
    print(json.dumps(contar_origen(), ensure_ascii=False, indent=2))

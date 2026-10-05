"""Traducción entre el esquema canónico de Sakila y la base migrada.

Este es el único módulo que conoce los nombres en español usados por el equipo.
El resto del proyecto debe pedir tablas y columnas mediante nombres canónicos.
"""

import re

# Tablas canónicas de Sakila -> nombres usados en SQL Server.
MAPEO_TABLAS = {
    "actor": "actor",
    "rental": "alquiler",
    "category": "categoria",
    "city": "ciudad",
    "customer": "cliente",
    "address": "direccion",
    "language": "idioma",
    "inventory": "inventario",
    "payment": "pago",
    "country": "pais",
    "film": "pelicula",
    "film_actor": "pelicula_actor",
    "film_category": "pelicula_categoria",
    "film_text": "pelicula_texto",
    "staff": "personal",
    "store": "tienda",
}

# Columnas necesarias para el análisis RFM, agrupadas por tabla canónica.
MAPEO_COLUMNAS = {
    "customer": {
        "customer_id": "id_cliente",
        "first_name": "nombre",
        "last_name": "apellido",
    },
    "rental": {
        "rental_id": "id_alquiler",
        "customer_id": "id_cliente",
        "rental_date": "fecha_alquiler",
    },
    "payment": {
        "payment_id": "id_pago",
        "customer_id": "id_cliente",
        "rental_id": "id_alquiler",
        "amount": "monto",
    },
}


# Los SQL usan tokens como {{customer}} o {{payment.amount}}.
_TOKEN_SQL = re.compile(r"\{\{([a-z_]+(?:\.[a-z_]+)?)\}\}")


def _identificador_sql(nombre: str) -> str:
    """Delimita un identificador SQL Server procedente de un mapeo confiable."""
    return f"[{nombre.replace(']', ']]')}]"


def get_tabla_espanol(tabla_canonica: str) -> str:
    """Devuelve el nombre local de una tabla canónica o informa un error claro."""
    try:
        return MAPEO_TABLAS[tabla_canonica.lower()]
    except KeyError as error:
        raise KeyError(f"Tabla canónica no mapeada: {tabla_canonica!r}") from error


def tabla_sql(tabla_canonica: str) -> str:
    """Devuelve una tabla calificada, por ejemplo ``[dbo].[cliente]``."""
    return f"[dbo].{_identificador_sql(get_tabla_espanol(tabla_canonica))}"


def get_columna_espanol(tabla_canonica: str, columna_canonica: str) -> str:
    """Devuelve el nombre local de una columna usada por el análisis RFM."""
    try:
        return MAPEO_COLUMNAS[tabla_canonica.lower()][columna_canonica.lower()]
    except KeyError as error:
        raise KeyError(
            f"Columna canónica no mapeada: {tabla_canonica!r}.{columna_canonica!r}"
        ) from error


def columna_sql(tabla_canonica: str, columna_canonica: str) -> str:
    """Devuelve un identificador de columna SQL Server delimitado."""
    return _identificador_sql(get_columna_espanol(tabla_canonica, columna_canonica))


def renderizar_sql(plantilla: str) -> str:
    """Sustituye tokens canónicos del SQL por identificadores locales seguros.

    Acepta ``{{tabla}}`` y ``{{tabla.columna}}``. Los tokens desconocidos
    fallan de forma explícita, para evitar ejecutar una consulta incompleta.
    """
    def reemplazar(coincidencia: re.Match[str]) -> str:
        partes = coincidencia.group(1).split(".")
        if len(partes) == 1:
            return tabla_sql(partes[0])
        return columna_sql(partes[0], partes[1])

    return _TOKEN_SQL.sub(reemplazar, plantilla)

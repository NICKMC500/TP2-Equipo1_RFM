"""Traducción entre el esquema canónico de Sakila y SQL Server.

Las claves utilizan los nombres originales de Sakila.
Los valores representan los nombres físicos de la base migrada.

Este módulo centraliza los nombres físicos de tablas y columnas.
El resto del proyecto debe trabajar con nombres canónicos.
"""

# Tablas canónicas de Sakila -> nombres físicos en SQL Server.
MAPEO_TABLAS = {
    "actor": "actor",
    "address": "direccion",
    "category": "categoria",
    "city": "ciudad",
    "country": "pais",
    "customer": "cliente",
    "film": "pelicula",
    "film_actor": "pelicula_actor",
    "film_category": "pelicula_categoria",
    "film_text": "pelicula_texto",
    "inventory": "inventario",
    "language": "idioma",
    "payment": "pago",
    "rental": "alquiler",
    "staff": "personal",
    "store": "tienda",
}


# Columnas canónicas de Sakila -> nombres físicos en SQL Server.
MAPEO_COLUMNAS = {
    "actor": {
        "actor_id": "id_actor",
        "first_name": "nombre",
        "last_name": "apellido",
        "last_update": "ultima_actualizacion",
    },

    "address": {
        "address_id": "id_direccion",
        "address": "direccion",
        "address2": "direccion2",
        "district": "distrito",
        "city_id": "id_ciudad",
        "postal_code": "codigo_postal",
        "phone": "telefono",
        "location": "ubicacion",
        "last_update": "ultima_actualizacion",
    },

    "category": {
        "category_id": "id_categoria",
        "name": "nombre",
        "last_update": "ultima_actualizacion",
    },

    "city": {
        "city_id": "id_ciudad",
        "city": "ciudad",
        "country_id": "id_pais",
        "last_update": "ultima_actualizacion",
    },

    "country": {
        "country_id": "id_pais",
        "country": "pais",
        "last_update": "ultima_actualizacion",
    },

    "customer": {
        "customer_id": "id_cliente",
        "store_id": "id_tienda",
        "first_name": "nombre",
        "last_name": "apellido",
        "email": "email",
        "address_id": "id_direccion",
        "active": "activo",
        "create_date": "fecha_creacion",
        "last_update": "ultima_actualizacion",
    },

    "film": {
        "film_id": "id_pelicula",
        "title": "titulo",
        "description": "descripcion",
        "release_year": "anio_lanzamiento",
        "language_id": "id_idioma",
        "original_language_id": "id_idioma_original",
        "rental_duration": "duracion_alquiler",
        "rental_rate": "tarifa_alquiler",
        "length": "duracion",
        "replacement_cost": "costo_reemplazo",
        "rating": "clasificacion",
        "special_features": "caracteristicas_especiales",
        "last_update": "ultima_actualizacion",
    },

    "film_actor": {
        "actor_id": "id_actor",
        "film_id": "id_pelicula",
        "last_update": "ultima_actualizacion",
    },

    "film_category": {
        "film_id": "id_pelicula",
        "category_id": "id_categoria",
        "last_update": "ultima_actualizacion",
    },

    "film_text": {
        "film_id": "id_pelicula",
        "title": "titulo",
        "description": "descripcion",
    },

    "inventory": {
        "inventory_id": "id_inventario",
        "film_id": "id_pelicula",
        "store_id": "id_tienda",
        "last_update": "ultima_actualizacion",
    },

    "language": {
        "language_id": "id_idioma",
        "name": "nombre",
        "last_update": "ultima_actualizacion",
    },

    "payment": {
        "payment_id": "id_pago",
        "customer_id": "id_cliente",
        "staff_id": "id_personal",
        "rental_id": "id_alquiler",
        "amount": "monto",
        "payment_date": "fecha_pago",
        "last_update": "ultima_actualizacion",
    },

    "rental": {
        "rental_id": "id_alquiler",
        "rental_date": "fecha_alquiler",
        "inventory_id": "id_inventario",
        "customer_id": "id_cliente",
        "return_date": "fecha_devolucion",
        "staff_id": "id_personal",
        "last_update": "ultima_actualizacion",
    },

    "staff": {
        "staff_id": "id_personal",
        "first_name": "nombre",
        "last_name": "apellido",
        "address_id": "id_direccion",
        "picture": "foto",
        "email": "email",
        "store_id": "id_tienda",
        "active": "activo",
        "username": "usuario",
        "password": "contrasena",
        "last_update": "ultima_actualizacion",
    },

    "store": {
        "store_id": "id_tienda",
        "manager_staff_id": "id_gerente",
        "address_id": "id_direccion",
        "last_update": "ultima_actualizacion",
    },
}

import re

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

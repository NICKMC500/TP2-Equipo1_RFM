# Diccionario de esquema - Equipo 1

Actualización posterior a la devolución del 30/10/2026.

## Tablas

| Canónica | Nombre físico |
| --- | --- |
| actor | actor |
| address | direccion |
| category | categoria |
| city | ciudad |
| country | pais |
| customer | cliente |
| film | pelicula |
| film_actor | pelicula_actor |
| film_category | pelicula_categoria |
| film_text | pelicula_texto |
| inventory | inventario |
| language | idioma |
| payment | pago |
| rental | alquiler |
| staff | personal |
| store | tienda |

## Columnas

| Tabla canónica | Columna canónica | Tabla física | Columna física |
| --- | --- | --- | --- |
| actor | actor_id | actor | id_actor |
| actor | first_name | actor | nombre |
| actor | last_name | actor | apellido |
| actor | last_update | actor | ultima_actualizacion |
| address | address_id | direccion | id_direccion |
| address | address | direccion | direccion |
| address | address2 | direccion | direccion2 |
| address | district | direccion | distrito |
| address | city_id | direccion | id_ciudad |
| address | postal_code | direccion | codigo_postal |
| address | phone | direccion | telefono |
| address | location | direccion | ubicacion |
| address | last_update | direccion | ultima_actualizacion |
| category | category_id | categoria | id_categoria |
| category | name | categoria | nombre |
| category | last_update | categoria | ultima_actualizacion |
| city | city_id | ciudad | id_ciudad |
| city | city | ciudad | ciudad |
| city | country_id | ciudad | id_pais |
| city | last_update | ciudad | ultima_actualizacion |
| country | country_id | pais | id_pais |
| country | country | pais | pais |
| country | last_update | pais | ultima_actualizacion |
| customer | customer_id | cliente | id_cliente |
| customer | store_id | cliente | id_tienda |
| customer | first_name | cliente | nombre |
| customer | last_name | cliente | apellido |
| customer | email | cliente | email |
| customer | address_id | cliente | id_direccion |
| customer | active | cliente | activo |
| customer | create_date | cliente | fecha_creacion |
| customer | last_update | cliente | ultima_actualizacion |
| film | film_id | pelicula | id_pelicula |
| film | title | pelicula | titulo |
| film | description | pelicula | descripcion |
| film | release_year | pelicula | anio_lanzamiento |
| film | language_id | pelicula | id_idioma |
| film | original_language_id | pelicula | id_idioma_original |
| film | rental_duration | pelicula | duracion_alquiler |
| film | rental_rate | pelicula | tarifa_alquiler |
| film | length | pelicula | duracion |
| film | replacement_cost | pelicula | costo_reemplazo |
| film | rating | pelicula | clasificacion |
| film | special_features | pelicula | caracteristicas_especiales |
| film | last_update | pelicula | ultima_actualizacion |
| film_actor | actor_id | pelicula_actor | id_actor |
| film_actor | film_id | pelicula_actor | id_pelicula |
| film_actor | last_update | pelicula_actor | ultima_actualizacion |
| film_category | film_id | pelicula_categoria | id_pelicula |
| film_category | category_id | pelicula_categoria | id_categoria |
| film_category | last_update | pelicula_categoria | ultima_actualizacion |
| film_text | film_id | pelicula_texto | id_pelicula |
| film_text | title | pelicula_texto | titulo |
| film_text | description | pelicula_texto | descripcion |
| inventory | inventory_id | inventario | id_inventario |
| inventory | film_id | inventario | id_pelicula |
| inventory | store_id | inventario | id_tienda |
| inventory | last_update | inventario | ultima_actualizacion |
| language | language_id | idioma | id_idioma |
| language | name | idioma | nombre |
| language | last_update | idioma | ultima_actualizacion |
| payment | payment_id | pago | id_pago |
| payment | customer_id | pago | id_cliente |
| payment | staff_id | pago | id_personal |
| payment | rental_id | pago | id_alquiler |
| payment | amount | pago | monto |
| payment | payment_date | pago | fecha_pago |
| payment | last_update | pago | ultima_actualizacion |
| rental | rental_id | alquiler | id_alquiler |
| rental | rental_date | alquiler | fecha_alquiler |
| rental | inventory_id | alquiler | id_inventario |
| rental | customer_id | alquiler | id_cliente |
| rental | return_date | alquiler | fecha_devolucion |
| rental | staff_id | alquiler | id_personal |
| rental | last_update | alquiler | ultima_actualizacion |
| staff | staff_id | personal | id_personal |
| staff | first_name | personal | nombre |
| staff | last_name | personal | apellido |
| staff | address_id | personal | id_direccion |
| staff | picture | personal | foto |
| staff | email | personal | email |
| staff | store_id | personal | id_tienda |
| staff | active | personal | activo |
| staff | username | personal | usuario |
| staff | password | personal | contrasena |
| staff | last_update | personal | ultima_actualizacion |
| store | store_id | tienda | id_tienda |
| store | manager_staff_id | tienda | id_gerente |
| store | address_id | tienda | id_direccion |
| store | last_update | tienda | ultima_actualizacion |

## Reconciliación contra el archivo de carga utilizado en TP1

El archivo es la traducción a SQL Server facilitada por el equipo. Se contaron INSERT; film_text se deriva por un trigger acreditado en el DDL. No son cantidades escritas a mano ni un conteo independiente de un volcado MySQL.

| Tabla | Filas del archivo de carga | Filas SQL Server | Diferencia |
| --- | ---: | ---: | ---: |
| actor | 200 | 200 | 0 |
| address | 603 | 603 | 0 |
| category | 16 | 16 | 0 |
| city | 600 | 600 | 0 |
| country | 109 | 109 | 0 |
| customer | 599 | 599 | 0 |
| film | 1000 | 1000 | 0 |
| film_actor | 5462 | 5462 | 0 |
| film_category | 1000 | 1000 | 0 |
| film_text | 1000 | 1000 | 0 |
| inventory | 4581 | 4581 | 0 |
| language | 6 | 6 | 0 |
| payment | 16044 | 16044 | 0 |
| rental | 16044 | 16044 | 0 |
| staff | 2 | 2 | 0 |
| store | 2 | 2 | 0 |

Pagos: 16.044 filas, máximo ID 16.049 y cinco huecos de identificador. No representan cinco pagos perdidos en la migración.

SHA-256 carga: bed2046d87835b7bc3b9555467bf2d5294765187fe2ee8b54ffb225975d5835d

SHA-256 DDL: 67f0d88401d6331128d6beacf713b7ee92f73427e20b036e11b28b8f771e3f62

Métodos y evidencia completa: informe/evidencia_reconciliacion.json.

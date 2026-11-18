/* Conteos reales del destino. reconciliar_origen.py cuenta las tuplas del
   archivo de carga y pandas une ambos resultados por tabla canónica.
   No hay cantidades de origen escritas a mano ni se usa MAX(id) como COUNT. */
SELECT 'actor' AS canonical_table, COUNT_BIG(*) AS sql_server_rows FROM {{actor}} UNION ALL
SELECT 'address', COUNT_BIG(*) FROM {{address}} UNION ALL
SELECT 'category', COUNT_BIG(*) FROM {{category}} UNION ALL
SELECT 'city', COUNT_BIG(*) FROM {{city}} UNION ALL
SELECT 'country', COUNT_BIG(*) FROM {{country}} UNION ALL
SELECT 'customer', COUNT_BIG(*) FROM {{customer}} UNION ALL
SELECT 'film', COUNT_BIG(*) FROM {{film}} UNION ALL
SELECT 'film_actor', COUNT_BIG(*) FROM {{film_actor}} UNION ALL
SELECT 'film_category', COUNT_BIG(*) FROM {{film_category}} UNION ALL
SELECT 'film_text', COUNT_BIG(*) FROM {{film_text}} UNION ALL
SELECT 'inventory', COUNT_BIG(*) FROM {{inventory}} UNION ALL
SELECT 'language', COUNT_BIG(*) FROM {{language}} UNION ALL
SELECT 'payment', COUNT_BIG(*) FROM {{payment}} UNION ALL
SELECT 'rental', COUNT_BIG(*) FROM {{rental}} UNION ALL
SELECT 'staff', COUNT_BIG(*) FROM {{staff}} UNION ALL
SELECT 'store', COUNT_BIG(*) FROM {{store}}
ORDER BY canonical_table;

/*
Reconciliación contra el volcado estándar de Sakila.
Los nombres físicos se resuelven desde esquema.py al cargar esta plantilla.
La difference de payment se documenta en el diagnóstico del notebook.
*/
WITH Origen AS (
    SELECT * FROM (VALUES
        ('actor',          200),
        ('address',        603),
        ('category',        16),
        ('city',          600),
        ('country',       109),
        ('customer',      599),
        ('film',         1000),
        ('film_actor',   5462),
        ('film_category',1000),
        ('film_text',    1000),
        ('inventory',    4581),
        ('language',        6),
        ('payment',     16049),
        ('rental',      16044),
        ('staff',          2),
        ('store',          2)
    ) AS o(canonical_table, source_mysql_rows)
), SqlServer AS (
    SELECT 'actor' AS canonical_table, COUNT(*) AS sql_server_rows FROM {{actor}} UNION ALL
    SELECT 'address', COUNT(*) FROM {{address}} UNION ALL
    SELECT 'category', COUNT(*) FROM {{category}} UNION ALL
    SELECT 'city', COUNT(*) FROM {{city}} UNION ALL
    SELECT 'country', COUNT(*) FROM {{country}} UNION ALL
    SELECT 'customer', COUNT(*) FROM {{customer}} UNION ALL
    SELECT 'film', COUNT(*) FROM {{film}} UNION ALL
    SELECT 'film_actor', COUNT(*) FROM {{film_actor}} UNION ALL
    SELECT 'film_category', COUNT(*) FROM {{film_category}} UNION ALL
    SELECT 'film_text', COUNT(*) FROM {{film_text}} UNION ALL
    SELECT 'inventory', COUNT(*) FROM {{inventory}} UNION ALL
    SELECT 'language', COUNT(*) FROM {{language}} UNION ALL
    SELECT 'payment', COUNT(*) FROM {{payment}} UNION ALL
    SELECT 'rental', COUNT(*) FROM {{rental}} UNION ALL
    SELECT 'staff', COUNT(*) FROM {{staff}} UNION ALL
    SELECT 'store', COUNT(*) FROM {{store}}
)
SELECT
    o.canonical_table,
    o.source_mysql_rows,
    s.sql_server_rows,
    s.sql_server_rows - o.source_mysql_rows AS difference
FROM Origen AS o
INNER JOIN SqlServer AS s
    ON s.canonical_table = o.canonical_table
ORDER BY o.canonical_table;

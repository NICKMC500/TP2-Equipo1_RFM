
SELECT 'actor' AS tabla_canonica, 'actor' AS tabla_espanol, COUNT(*) AS filas_sql_server FROM dbo.actor UNION ALL 
SELECT 'rental', 'alquiler', COUNT(*) FROM dbo.alquiler UNION ALL 
SELECT 'category', 'categoria', COUNT(*) FROM dbo.categoria UNION ALL 
SELECT 'city', 'ciudad', COUNT(*) FROM dbo.ciudad UNION ALL 
SELECT 'customer', 'cliente', COUNT(*) FROM dbo.cliente UNION ALL 
SELECT 'address', 'direccion', COUNT(*) FROM dbo.direccion UNION ALL 
SELECT 'language', 'idioma', COUNT(*) FROM dbo.idioma UNION ALL 
SELECT 'inventory', 'inventario', COUNT(*) FROM dbo.inventario UNION ALL 
SELECT 'payment', 'pago', COUNT(*) FROM dbo.pago UNION ALL 
SELECT 'country', 'pais', COUNT(*) FROM dbo.pais UNION ALL 
SELECT 'film', 'pelicula', COUNT(*) FROM dbo.pelicula UNION ALL 
SELECT 'film_actor', 'pelicula_actor', COUNT(*) FROM dbo.pelicula_actor UNION ALL 
SELECT 'film_category', 'pelicula_categoria', COUNT(*) FROM dbo.pelicula_categoria UNION ALL 
SELECT 'film_text', 'pelicula_texto', COUNT(*) FROM dbo.pelicula_texto UNION ALL 
SELECT 'staff', 'personal', COUNT(*) FROM dbo.personal UNION ALL 
SELECT 'store', 'tienda', COUNT(*) FROM dbo.tienda;
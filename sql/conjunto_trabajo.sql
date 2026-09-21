WITH FechaMax AS(
	SELECT MAX(fecha_alquiler) AS max_fecha FROM dbo.alquiler
)

SELECT 
	c.id_cliente,
	CONCAT(c.nombre,' ',c.apellido) AS nombre_completo,
	DATEDIFF(day, MAX(a.fecha_alquiler), (SELECT max_fecha FROM FechaMax)) AS recencia_dias,
	COUNT(DISTINCT a.id_alquiler) AS frecuencia_alquileres,
	ISNULL(SUM(p.monto), 0) AS monto_total
FROM dbo.cliente c
LEFT JOIN dbo.alquiler a ON c.id_cliente = a.id_cliente
LEFT JOIN dbo.pago p ON a.id_alquiler = p.id_alquiler
GROUP BY c.id_cliente ,c.nombre,c.apellido;
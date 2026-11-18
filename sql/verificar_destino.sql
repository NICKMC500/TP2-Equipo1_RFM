/* Ejecutar sobre el destino después de cada corrida del pipeline.
   fecha_proceso es auditoría y se excluye de los controles de negocio.
   Las sumas no prueban por sí solas igualdad total: verificar_idempotencia.py
   además compara todas las columnas de negocio y calcula una huella SHA-256. */
SELECT COUNT_BIG(*) AS filas,
       COUNT_BIG(DISTINCT id_cliente) AS clientes_distintos,
       COALESCE(SUM(CAST(id_cliente AS BIGINT)), 0) AS suma_id_cliente,
       COALESCE(SUM(CAST(frecuencia AS BIGINT)), 0) AS suma_frecuencia,
       COALESCE(SUM(CAST(monto_total AS DECIMAL(20,2))), 0) AS suma_monto,
       COALESCE(SUM(CAST(score_recencia AS BIGINT)), 0) AS suma_score_recencia,
       COALESCE(SUM(CAST(score_frecuencia AS BIGINT)), 0) AS suma_score_frecuencia,
       COALESCE(SUM(CAST(score_monto AS BIGINT)), 0) AS suma_score_monto
FROM dbo.TP2_SegmentacionRFM;

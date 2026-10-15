IF OBJECT_ID(N'dbo.TP2_SegmentacionRFM', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.TP2_SegmentacionRFM (
        id_cliente SMALLINT NOT NULL PRIMARY KEY,
        nombre VARCHAR(45) NOT NULL,
        apellido VARCHAR(45) NOT NULL,
        recencia_dias INT NOT NULL,
        frecuencia INT NOT NULL,
        monto_total DECIMAL(12,2) NOT NULL,
        score_recencia TINYINT NOT NULL,
        score_frecuencia TINYINT NOT NULL,
        score_monto TINYINT NOT NULL,
        segmento_rfm CHAR(3) NOT NULL,
        perfil_comercial VARCHAR(40) NOT NULL,
        canal_preferido VARCHAR(30) NOT NULL,
        descuento_sugerido_pct DECIMAL(5,2) NOT NULL,
        fecha_proceso DATETIME2 NOT NULL
    );
END;

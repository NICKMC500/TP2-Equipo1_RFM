USE [master]; 
GO 
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'sakila') 
BEGIN 
CREATE DATABASE [sakila]; 
END 
GO 
USE [sakila]; 
GO 
-- Tabla 1: ACTOR (Original: actor)
IF OBJECT_ID('[dbo].tr_actor_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_actor_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].[actor];
GO

CREATE TABLE [dbo].[actor] (
    id_actor SMALLINT IDENTITY(1,1) NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_actor PRIMARY KEY CLUSTERED (id_actor ASC)
);
GO


CREATE NONCLUSTERED INDEX idx_actor_apellido
ON [dbo].actor (apellido ASC);
GO

CREATE TRIGGER [dbo].tr_actor_ultima_actualizacion
ON [dbo].actor
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].actor
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].actor t
    INNER JOIN inserted i ON t.id_actor = i.id_actor;
END;
GO
-- Tabla 2: CATEGORIA (Original: category)
IF OBJECT_ID('[dbo].tr_categoria_ultima_actualizacion','TR') IS NOT NULL
	DROP TRIGGER [dbo].tr_categoria_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].categoria;

CREATE TABLE [dbo].categoria(
	id_categoria TINYINT IDENTITY(1,1) NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_categoria PRIMARY KEY CLUSTERED (id_categoria ASC)
    );
    GO
    
    CREATE TRIGGER [dbo].tr_categoria_ultima_actualizacion
    ON [dbo].categoria
    AFTER UPDATE
    AS
    BEGIN
		SET NOCOUNT ON;
        UPDATE [dbo].categoria
        SET ultima_actualizacion = GETDATE()
        FROM [dbo].categoria t
        INNER JOIN inserted i ON t.id_categoria =i.id_categoria;
        END;
        GO
-- Tabla 5: PAIS (Original: country)

IF OBJECT_ID('[dbo].tr_pais_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_pais_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].pais;
GO

CREATE TABLE [dbo].pais (
    id_pais SMALLINT IDENTITY(1,1) NOT NULL,
    pais VARCHAR(50) NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_pais PRIMARY KEY CLUSTERED (id_pais ASC)
);
GO

CREATE TRIGGER [dbo].tr_pais_ultima_actualizacion
ON [dbo].pais
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].pais
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].pais t
    INNER JOIN inserted i ON t.id_pais = i.id_pais;
END;
GO        
	-- Tabla 3: CIUDAD (Original: city)
	IF OBJECT_ID('[dbo].tr_ciudad_ultima_actualizacion','TR') IS NOT NULL
		DROP TRIGGER [dbo].tr_ciudad_ultima_actualizacion;
	GO
        
	DROP TABLE IF EXISTS [dbo].ciudad;
	GO
        
	CREATE TABLE [dbo].ciudad (
		id_ciudad SMALLINT IDENTITY(1,1) NOT NULL,
		ciudad VARCHAR(50) NOT NULL,
		id_pais SMALLINT NOT NULL,
		ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
            
		CONSTRAINT PK_ciudad PRIMARY KEY CLUSTERED (id_ciudad ASC),
        CONSTRAINT FK_ciudad_pais FOREIGN KEY (id_pais) REFERENCES [dbo].pais(id_pais) ON UPDATE CASCADE
		);
            
	CREATE NONCLUSTERED INDEX idx_fk_id_pais
	ON [dbo].ciudad (id_pais ASC);
	GO
            
	CREATE TRIGGER [dbo].tr_ciudad_ultima_actualizacion 
	ON [dbo].ciudad
	AFTER UPDATE
	AS 
	BEGIN
		SET NOCOUNT ON;
		UPDATE [dbo].ciudad
		SET ultima_actualizacion = GETDATE()
		FROM [dbo].ciudad t
		INNER JOIN inserted i ON t.id_ciudad = i.id_ciudad;
	END;
	GO
-- Tabla 4: DIRECCION (Original: address)          
IF OBJECT_ID ('[dbo].tr_direccion_ultima_actualizacion','TR') IS NOT NULL
	DROP TRIGGER [dbo].tr_direccion_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].direccion;
GO

CREATE TABLE [dbo].direccion (
    id_direccion SMALLINT IDENTITY(1,1) NOT NULL,
    direccion  VARCHAR(50) NOT NULL,
    direccion2 VARCHAR(50) NULL,
    distrito VARCHAR(20) NOT NULL,
	id_ciudad SMALLINT NOT NULL,
    codigo_postal VARCHAR(10) NULL,
    telefono VARCHAR(20) NOT NULL,
    ubicacion GEOMETRY NOT NULL, 
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_direccion PRIMARY KEY CLUSTERED (id_direccion ASC),
    CONSTRAINT FK_direccion_ciudad FOREIGN KEY (id_ciudad) REFERENCES [dbo].ciudad (id_ciudad) ON UPDATE CASCADE
);
GO

CREATE NONCLUSTERED INDEX idx_fk_id_ciudad 
ON [dbo].direccion (id_ciudad ASC);
GO


CREATE SPATIAL INDEX idx_ubicacion 
ON [dbo].direccion (ubicacion)
USING GEOMETRY_GRID
WITH (BOUNDING_BOX = (XMIN=-180, YMIN=-90, XMAX=180, YMAX=90));
GO

CREATE TRIGGER [dbo].tr_direccion_ultima_actualizacion
ON [dbo].direccion
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].direccion
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].direccion t
    INNER JOIN inserted i ON t.id_direccion = i.id_direccion;
END;
GO
-- Tabla 6: CLIENTE (Original: customer)


IF OBJECT_ID('[dbo].tr_cliente_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_cliente_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].cliente;
GO

CREATE TABLE [dbo].cliente (
    id_cliente SMALLINT IDENTITY(1,1) NOT NULL,
    id_tienda TINYINT NOT NULL, 
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    email VARCHAR(50) NULL,
    id_direccion SMALLINT NOT NULL,
    activo BIT NOT NULL DEFAULT 1, 
    fecha_creacion DATETIME NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_cliente PRIMARY KEY CLUSTERED (id_cliente ASC),
    CONSTRAINT FK_cliente_direccion FOREIGN KEY (id_direccion) REFERENCES [dbo].direccion (id_direccion) ON UPDATE CASCADE
    
);
GO


CREATE NONCLUSTERED INDEX idx_fk_id_tienda
ON [dbo].cliente (id_tienda ASC);
GO

CREATE NONCLUSTERED INDEX [idx_fk_id_direccion] 
ON [dbo].cliente (id_direccion ASC);
GO

CREATE NONCLUSTERED INDEX idx_cliente_apellido
ON [dbo].cliente (apellido ASC);
GO

CREATE TRIGGER [dbo].tr_cliente_ultima_actualizacion
ON [dbo].cliente
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].cliente
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].cliente t
    INNER JOIN inserted i ON t.id_cliente = i.id_cliente;
END;
GO


-- Tabla 10: IDIOMA (Original: language)

-- ====================================================================
IF OBJECT_ID('[dbo].tr_idioma_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_idioma_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].idioma;
GO

CREATE TABLE [dbo].idioma (
    id_idioma TINYINT IDENTITY(1,1) NOT NULL,
    nombre CHAR(20) NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_idioma PRIMARY KEY CLUSTERED (id_idioma ASC)
);
GO

CREATE TRIGGER [dbo].tr_idioma_ultima_actualizacion
ON [dbo].idioma
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].idioma
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].idioma t
    INNER JOIN inserted i ON t.id_idioma = i.id_idioma;
END;
GO

-- Tabla 7: PELICULA (Original: film)
-- ====================================================================
IF OBJECT_ID('[dbo].tr_pelicula_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_pelicula_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].pelicula;
GO

CREATE TABLE [dbo].pelicula (
    id_pelicula SMALLINT IDENTITY(1,1) NOT NULL,
    titulo VARCHAR(128) NOT NULL,
    descripcion VARCHAR(MAX) NULL,
    anio_lanzamiento SMALLINT NULL, 
    id_idioma TINYINT NOT NULL,
    id_idioma_original TINYINT NULL,
    duracion_alquiler TINYINT NOT NULL DEFAULT 3,
    tarifa_alquiler DECIMAL(4,2) NOT NULL DEFAULT 4.99,
    duracion SMALLINT NULL, 
    costo_reemplazo DECIMAL(5,2) NOT NULL DEFAULT 19.99,
    clasificacion VARCHAR(10) NOT NULL DEFAULT 'G', 
    caracteristicas_especiales VARCHAR(100) NULL, 
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_pelicula PRIMARY KEY CLUSTERED (id_pelicula ASC),
    CONSTRAINT CK_pelicula_anio_lanzamiento CHECK (anio_lanzamiento >= 1901 AND anio_lanzamiento <= 2150),
    CONSTRAINT CK_pelicula_clasificacion CHECK (clasificacion IN ('G','PG','PG-13','R','NC-17')),
    CONSTRAINT FK_pelicula_idioma FOREIGN KEY (id_idioma) REFERENCES [dbo].idioma (id_idioma) ON UPDATE CASCADE,
    CONSTRAINT FK_pelicula_idioma_original FOREIGN KEY (id_idioma_original) REFERENCES [dbo].idioma (id_idioma)
);
GO

CREATE NONCLUSTERED INDEX idx_pelicula_titulo ON [dbo].pelicula (titulo ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_id_idioma ON [dbo].pelicula (id_idioma ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_id_idioma_original ON [dbo].pelicula (id_idioma_original ASC);
GO

CREATE TRIGGER [dbo].tr_pelicula_ultima_actualizacion
ON [dbo].pelicula
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].pelicula
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].pelicula t
    INNER JOIN inserted i ON t.id_pelicula = i.id_pelicula;
END;
GO
-- Tabla 8: PELICULA_ACTOR (Original: film_actor)

IF OBJECT_ID('[dbo].tr_pelicula_actor_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_pelicula_actor_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].pelicula_actor;
GO

CREATE TABLE [dbo].pelicula_actor (
    id_actor SMALLINT NOT NULL,
    id_pelicula SMALLINT NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_pelicula_actor PRIMARY KEY CLUSTERED (id_actor ASC, id_pelicula ASC),
    CONSTRAINT FK_pelicula_actor_actor FOREIGN KEY (id_actor) REFERENCES [dbo].actor (id_actor) ON UPDATE CASCADE,
    CONSTRAINT FK_pelicula_actor_pelicula FOREIGN KEY (id_pelicula) REFERENCES [dbo].pelicula (id_pelicula) ON UPDATE CASCADE
);
GO

CREATE NONCLUSTERED INDEX idx_fk_pelicula_id ON [dbo].pelicula_actor (id_pelicula ASC);
GO

CREATE TRIGGER [dbo].tr_pelicula_actor_ultima_actualizacion
ON [dbo].pelicula_actor
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].pelicula_actor
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].pelicula_actor t
    INNER JOIN inserted i ON t.id_actor = i.id_actor AND t.id_pelicula = i.id_pelicula;
END;
GO
-- Tabla 9: PELICULA_CATEGORIA (Original: film_category)

IF OBJECT_ID('[dbo].tr_pelicula_categoria_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_pelicula_categoria_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].pelicula_categoria;
GO

CREATE TABLE [dbo].pelicula_categoria (
    id_pelicula SMALLINT NOT NULL,
    id_categoria TINYINT NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_pelicula_categoria PRIMARY KEY CLUSTERED (id_pelicula ASC, id_categoria ASC),
    CONSTRAINT FK_pelicula_categoria_pelicula FOREIGN KEY (id_pelicula) REFERENCES [dbo].pelicula (id_pelicula) ON UPDATE CASCADE,
    CONSTRAINT FK_pelicula_categoria_categoria FOREIGN KEY (id_categoria) REFERENCES [dbo].categoria (id_categoria) ON UPDATE CASCADE
);
GO

CREATE TRIGGER [dbo].tr_pelicula_categoria_ultima_actualizacion
ON [dbo].pelicula_categoria
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].pelicula_categoria
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].pelicula_categoria t
    INNER JOIN inserted i ON t.id_pelicula = i.id_pelicula AND t.id_categoria = i.id_categoria;
END;
GO
-- Tabla 11: INVENTARIO (Original: inventory)

IF OBJECT_ID('[dbo].tr_inventario_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_inventario_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].inventario;
GO

CREATE TABLE [dbo].inventario (
    id_inventario INT IDENTITY(1,1) NOT NULL, -- Mapeo de MEDIUMINT a INT
    id_pelicula SMALLINT NOT NULL,
    id_tienda TINYINT NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_inventario PRIMARY KEY CLUSTERED (id_inventario ASC),
    CONSTRAINT FK_inventario_pelicula FOREIGN KEY (id_pelicula) REFERENCES [dbo].pelicula (id_pelicula) ON UPDATE CASCADE
    -- NOTA: Descomentar la FK de tienda cuando la tabla [tienda] (store) esté creada:
    -- CONSTRAINT FK_inventario_tienda FOREIGN KEY (id_tienda) REFERENCES [dbo].tienda (id_tienda) ON UPDATE CASCADE
);
GO

CREATE NONCLUSTERED INDEX idx_fk_pelicula_id_inv ON [dbo].inventario (id_pelicula ASC);
GO
CREATE NONCLUSTERED INDEX idx_store_id_film_id ON [dbo].inventario (id_tienda ASC, id_pelicula ASC);
GO

CREATE TRIGGER [dbo].tr_inventario_ultima_actualizacion
ON [dbo].inventario
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].inventario
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].inventario t
    INNER JOIN inserted i ON t.id_inventario = i.id_inventario;
END;
GO

-- Tabla 12: PELICULA_TEXTO (Original: film_text) y su Búsqueda de Texto Completo
-- ====================================================================
DROP TABLE IF EXISTS [dbo].pelicula_texto;
GO

CREATE TABLE [dbo].pelicula_texto (
    id_pelicula SMALLINT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(MAX) NULL, -- CAMBIO CLAVE: VARCHAR(MAX) en lugar de TEXT
    
    CONSTRAINT PK_pelicula_texto PRIMARY KEY CLUSTERED (id_pelicula ASC)
);
GO
-- TRIGGERS EN [pelicula] PARA LA SINCRONIZACIÓN CON [pelicula_texto]
-- ====================================================================

-- Trigger para INSERT
IF OBJECT_ID('[dbo].tr_ins_pelicula_sincronizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_ins_pelicula_sincronizacion;
GO

CREATE TRIGGER [dbo].tr_ins_pelicula_sincronizacion
ON [dbo].pelicula
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO [dbo].pelicula_texto (id_pelicula, titulo, descripcion)
    SELECT id_pelicula, titulo, descripcion FROM inserted;
END;
GO

-- Trigger para UPDATE 
IF OBJECT_ID('[dbo].tr_upd_pelicula_sincronizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_upd_pelicula_sincronizacion;
GO

CREATE TRIGGER [dbo].tr_upd_pelicula_sincronizacion
ON [dbo].pelicula
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF UPDATE(titulo) OR UPDATE(descripcion) OR UPDATE(id_pelicula)
    BEGIN
        UPDATE pt
        SET pt.titulo = i.titulo,
            pt.descripcion = i.descripcion,
            pt.id_pelicula = i.id_pelicula
        FROM [dbo].pelicula_texto pt
        INNER JOIN deleted d ON pt.id_pelicula = d.id_pelicula
        INNER JOIN inserted i ON d.id_pelicula = i.id_pelicula; 
    END
END;
GO

-- Trigger para DELETE
IF OBJECT_ID('[dbo].tr_del_pelicula_sincronizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_del_pelicula_sincronizacion;
GO

CREATE TRIGGER [dbo].tr_del_pelicula_sincronizacion
ON [dbo].pelicula
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    DELETE pt
    FROM [dbo].pelicula_texto pt
    INNER JOIN deleted d ON pt.id_pelicula = d.id_pelicula;
END;
GO
-- Tabla 14: TIENDA (Original: store)
-- ====================================================================
IF OBJECT_ID('[dbo].tr_tienda_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_tienda_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].tienda;
GO

CREATE TABLE [dbo].tienda (
    id_tienda TINYINT IDENTITY(1,1) NOT NULL,
    id_gerente TINYINT NOT NULL,
    id_direccion SMALLINT NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_tienda PRIMARY KEY CLUSTERED (id_tienda ASC),
    CONSTRAINT FK_tienda_direccion FOREIGN KEY (id_direccion) REFERENCES [dbo].direccion (id_direccion) ON UPDATE CASCADE
    -- NOTA: La FK a personal (gerente) se agrega después por la dependencia circular
);
GO

CREATE UNIQUE NONCLUSTERED INDEX idx_fk_tienda_gerente ON [dbo].tienda (id_gerente ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_tienda_direccion ON [dbo].tienda (id_direccion ASC);
GO

CREATE TRIGGER [dbo].tr_tienda_ultima_actualizacion
ON [dbo].tienda
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].tienda
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].tienda t
    INNER JOIN inserted i ON t.id_tienda = i.id_tienda;
END;
GO

-- Tabla 15: PERSONAL (Original: staff)
-- ====================================================================
IF OBJECT_ID('[dbo].tr_personal_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_personal_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].personal;
GO

CREATE TABLE [dbo].personal (
    id_personal TINYINT IDENTITY(1,1) NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    id_direccion SMALLINT NOT NULL,
    foto VARBINARY(MAX) NULL, -- Reemplaza BLOB
    email VARCHAR(50) NULL,
    id_tienda TINYINT NOT NULL,
    activo BIT NOT NULL DEFAULT 1, -- Reemplaza BOOLEAN/TINYINT(1)
    usuario VARCHAR(16) NOT NULL,
    contrasena VARCHAR(40) NULL, 
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_personal PRIMARY KEY CLUSTERED (id_personal ASC),
    CONSTRAINT FK_personal_direccion FOREIGN KEY (id_direccion) REFERENCES [dbo].direccion (id_direccion) ON UPDATE CASCADE,
    CONSTRAINT FK_personal_tienda FOREIGN KEY (id_tienda) REFERENCES [dbo].tienda (id_tienda) ON UPDATE NO ACTION
);
GO

CREATE NONCLUSTERED INDEX idx_fk_personal_tienda ON [dbo].personal (id_tienda ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_personal_direccion ON [dbo].personal (id_direccion ASC);
GO

CREATE TRIGGER [dbo].tr_personal_ultima_actualizacion
ON [dbo].personal
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].personal
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].personal t
    INNER JOIN inserted i ON t.id_personal = i.id_personal;
END;
GO

-- ====================================================================
-- RESOLUCIÓN DE DEPENDENCIAS
-- ====================================================================

-- 1. Agregamos el gerente a la Tienda
ALTER TABLE [dbo].tienda
ADD CONSTRAINT FK_tienda_gerente FOREIGN KEY (id_gerente) REFERENCES [dbo].personal (id_personal) ON UPDATE NO ACTION;
GO

-- 2. Como en tu mensaje anterior ya creaste "inventario", ahora que "tienda" existe, 
-- debemos agregar la relación que había quedado comentada en tu script:
ALTER TABLE [dbo].inventario
ADD CONSTRAINT FK_inventario_tienda FOREIGN KEY (id_tienda) REFERENCES [dbo].tienda (id_tienda) ON UPDATE CASCADE;
GO

-- Tabla 16: ALQUILER (Original: rental)
-- ====================================================================
IF OBJECT_ID('[dbo].tr_alquiler_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_alquiler_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].alquiler;
GO

CREATE TABLE [dbo].alquiler (
    id_alquiler INT IDENTITY(1,1) NOT NULL,
    fecha_alquiler DATETIME NOT NULL,
    id_inventario INT NOT NULL, -- Se mantiene INT para coincidir con la tabla inventario
    id_cliente SMALLINT NOT NULL,
    fecha_devolucion DATETIME NULL,
    id_personal TINYINT NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_alquiler PRIMARY KEY CLUSTERED (id_alquiler ASC),
    CONSTRAINT UQ_alquiler_fecha_inventario_cliente UNIQUE (fecha_alquiler, id_inventario, id_cliente),
    
    -- Se utiliza NO ACTION para evitar el error de múltiples caminos de cascada de SQL Server
    CONSTRAINT FK_alquiler_personal FOREIGN KEY (id_personal) REFERENCES [dbo].personal (id_personal) ON UPDATE NO ACTION,
    CONSTRAINT FK_alquiler_inventario FOREIGN KEY (id_inventario) REFERENCES [dbo].inventario (id_inventario) ON UPDATE NO ACTION,
    CONSTRAINT FK_alquiler_cliente FOREIGN KEY (id_cliente) REFERENCES [dbo].cliente (id_cliente) ON UPDATE NO ACTION
);
GO

CREATE NONCLUSTERED INDEX idx_fk_alquiler_inventario ON [dbo].alquiler (id_inventario ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_alquiler_cliente ON [dbo].alquiler (id_cliente ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_alquiler_personal ON [dbo].alquiler (id_personal ASC);
GO

CREATE TRIGGER [dbo].tr_alquiler_ultima_actualizacion
ON [dbo].alquiler
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].alquiler
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].alquiler t
    INNER JOIN inserted i ON t.id_alquiler = i.id_alquiler;
END;
GO

-- Tabla 17: PAGO (Original: payment)
-- ====================================================================
IF OBJECT_ID('[dbo].tr_pago_ultima_actualizacion', 'TR') IS NOT NULL
    DROP TRIGGER [dbo].tr_pago_ultima_actualizacion;
GO

DROP TABLE IF EXISTS [dbo].pago;
GO

CREATE TABLE [dbo].pago (
    id_pago SMALLINT IDENTITY(1,1) NOT NULL,
    id_cliente SMALLINT NOT NULL,
    id_personal TINYINT NOT NULL,
    id_alquiler INT NULL,
    monto DECIMAL(5,2) NOT NULL,
    fecha_pago DATETIME NOT NULL,
    ultima_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT PK_pago PRIMARY KEY CLUSTERED (id_pago ASC),
    
    -- Mantenemos SET NULL en alquiler si se borra, pero el resto se protege con NO ACTION
    CONSTRAINT FK_pago_alquiler FOREIGN KEY (id_alquiler) REFERENCES [dbo].alquiler (id_alquiler) ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT FK_pago_cliente FOREIGN KEY (id_cliente) REFERENCES [dbo].cliente (id_cliente) ON UPDATE NO ACTION,
    CONSTRAINT FK_pago_personal FOREIGN KEY (id_personal) REFERENCES [dbo].personal (id_personal) ON UPDATE NO ACTION
);
GO

CREATE NONCLUSTERED INDEX idx_fk_pago_cliente ON [dbo].pago (id_cliente ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_pago_personal ON [dbo].pago (id_personal ASC);
GO
CREATE NONCLUSTERED INDEX idx_fk_pago_alquiler ON [dbo].pago (id_alquiler ASC);
GO

CREATE TRIGGER [dbo].tr_pago_ultima_actualizacion
ON [dbo].pago
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [dbo].pago
    SET ultima_actualizacion = GETDATE()
    FROM [dbo].pago t
    INNER JOIN inserted i ON t.id_pago = i.id_pago;
END;
GO
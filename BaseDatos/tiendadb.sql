-- Crear la base de datos con el conjunto de caracteres adecuado para español
CREATE DATABASE tiendadb CHARACTER
SET
    utf8mb4 COLLATE utf8mb4_spanish_ci;

-- Seleccionar la base de datos
USE tiendadb;

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS tbl_usuarios (
    id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    direccion_mac CHAR(17) NOT NULL,
    intentos TINYINT UNSIGNED DEFAULT 3,
    estado TINYINT UNSIGNED NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla para unidades
CREATE TABLE IF NOT EXISTS tbl_unidades (
    id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE,
    codigo CHAR(3) DEFAULT 'NIU'
);

-- Crear la tabla para las categorias
CREATE TABLE tbl_categorias (
    id tinyint unsigned auto_increment PRIMARY key,
    nombre varchar(100) UNIQUE
);

-- Crear la tabla para los productos
CREATE TABLE tbl_productos (
    id smallint unsigned auto_increment PRIMARY key,
    codigo_barras varchar(13) UNIQUE NOT NULL,
    id_unidad tinyint unsigned,
    id_categoria tinyint unsigned,
    descripcion varchar(100),
    precio_compra decimal(9, 2),
    precio_venta decimal(9, 2),
    stock decimal(9, 2),
    stock_minimo decimal(9, 2),
    estado tinyint unsigned,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN key (
        id_unidad
    ) REFERENCES tbl_unidades (id),
    FOREIGN key (
        id_categoria
    ) REFERENCES tbl_categorias (id),
    index idx_codigo_barras (
        codigo_barras
    ),
    index idx_descripcion (
        descripcion
    ),
    index idx_fecha_actualizacion (
        fecha_actualizacion
    )
);

-- Crear la tabla par alos clientes
CREATE TABLE tbl_clientes (
    id smallint unsigned auto_increment,
    documento varchar(15),
    Nombre varchar(1500),
    estado tinyint unsigned,
    PRIMARY key (
        id,
        documento
    )
);

-- Crear la tabla para los proveedores
CREATE TABLE tbl_proveedores (
    id smallint unsigned auto_increment,
    ruc varchar(15),
    Nombre varchar(1500),
    estado tinyint unsigned,
    PRIMARY key (
        id,
        ruc
    )
);

-- Crear la tabla para los estados
CREATE TABLE tbl_estados (
    nombre_tabla varchar(50),
    estado tinyint unsigned,
    descripcion varchar(100),
    PRIMARY key (
        nombre_tabla,
        estado
    )
);

-- Crear la tabla para las series de comprobantes
CREATE TABLE tbl_series (
    id tinyint unsigned auto_increment NOT NULL PRIMARY key,
    serie char(4),
    contador mediumint unsigned
);

-- Crear la tabla para las ventas
CREATE TABLE tbl_ventas (
    id mediumint unsigned auto_increment NOT NULL PRIMARY key,
    id_serie tinyint unsigned,
    contador_serie mediumint unsigned,
    id_usuario tinyint unsigned,
    id_cliente smallint unsigned,
    estado tinyint unsigned,
    fecha datetime NOT NULL,
    total decimal(9, 2) NOT NULL,
    FOREIGN key (
        id_serie
    ) REFERENCES tbl_series (id),
    FOREIGN key (
        id_usuario
    ) REFERENCES tbl_usuarios (id),
    FOREIGN key (
        id_cliente
    ) REFERENCES tbl_clientes (id)
);

-- Crear la tabla para los detalles de las ventas
CREATE TABLE tbl_venta_detalles (
    id_venta mediumint unsigned,
    id_producto smallint unsigned,
    cantidad decimal(9, 2),
    precio_venta decimal(9, 2),
    descuento decimal(9, 2),
    estado tinyint unsigned,
    FOREIGN key (
        id_venta
    ) REFERENCES tbl_ventas (id),
    FOREIGN key (
        id_producto
    ) REFERENCES tbl_productos (id),
    PRIMARY key (
        id_venta,
        id_producto
    )
);

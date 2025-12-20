USE tiendadb;

-- Procedimentos para la tabla de usuarios
CREATE PROCEDURE proc_obtener_contrasena (IN p_nombre_usuario varchar(50)) BEGIN
SELECT
    u.id,
    u.contrasena,
    u.intentos,
    e.descripcion as estado
FROM
    tbl_usuarios u
    JOIN tbl_estados e ON u.estado = e.estado
    AND e.nombre_tabla = "tbl_usuarios"
WHERE
    u.nombre_usuario = p_nombre_usuario;

END;

CREATE PROCEDURE proc_reducir_intento (IN p_nombre_usuario varchar(50)) BEGIN
UPDATE
    tbl_usuarios
SET
    intentos = GREATEST(0, intentos - 1)
WHERE
    nombre_usuario = p_nombre_usuario;

END;

CREATE PROCEDURE proc_Restablecer_Intento (IN p_nombre_usuario varchar(50)) BEGIN
UPDATE
    tbl_usuarios
SET
    intentos = 3
WHERE
    nombre_usuario = p_nombre_usuario;

END;

CREATE PROCEDURE proc_insertar_usuario (
    IN p_nombre_usuario varchar(50),
    IN p_contrasena varchar(255),
    IN p_correo varchar(100),
    IN p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            and nombre_tabla = 'tbl_usuarios'
    );

INSERT INTO
    tbl_usuarios (
        nombre_usuario,
        contrasena,
        correo,
        estado
    )
VALUES
    (
        p_nombre_usuario,
        p_contrasena,
        p_correo,
        p_estado
    );

-- Devolver el ID insertado directamente
SELECT
    LAST_INSERT_ID() AS id_usuario;

END;

CREATE PROCEDURE proc_actualizar_usuario (
    IN p_id tinyint UNSIGNED,
    p_nombre_usuario varchar(50),
    p_contrasena varchar(255),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
    );

UPDATE
    tbl_usuarios
SET
    nombre_usuario = p_nombre_usuario,
    contrasena = p_contrasena,
    estado = p_estado
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_eliminar_usuario (IN p_id tinyint UNSIGNED) BEGIN
UPDATE
    tbl_usuarios
SET
    estado = 255 - estado
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_mostrar_usuario () BEGIN
SELECT
    u.id,
    u.nombre_usuario,
    u.intentos,
    e.descripcion as estado
FROM
    tbl_usuarios u
    JOIN tbl_estados e ON e.estado = u.estado
    AND e.nombre_tabla = "tbl_usuarios";

END;

-- Procedimientos para la tabla de Categorias
CREATE PROCEDURE proc_mostrar_categoria () BEGIN
SELECT
    *
FROM
    tbl_categorias
ORDER BY
    id DESC;

END;

CREATE PROCEDURE proc_insertar_categoria (IN p_nombre varchar(100)) BEGIN
INSERT INTO
    tbl_categorias (nombre)
VALUES
    (p_nombre);

END;

CREATE PROCEDURE proc_actualizar_categoria (
    IN p_id tinyint UNSIGNED,
    p_nombre varchar(100)
) BEGIN
UPDATE
    tbl_categorias
SET
    nombre = p_nombre
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_obtener_fecha_actual () BEGIN
SELECT
    CURRENT_TIMESTAMP AS tiempo_actual;

END;

-- Procedimientos para la tabla de unidades
CREATE PROCEDURE proc_mostrar_unidad () BEGIN
SELECT
    *
FROM
    tbl_unidades
ORDER BY
    id DESC;

END;

CREATE PROCEDURE proc_insertar_unidad (IN p_nombre varchar(100)) BEGIN
INSERT INTO
    tbl_unidades (nombre)
VALUES
    (p_nombre);

END;

CREATE PROCEDURE proc_actualizar_unidad (
    IN p_id tinyint UNSIGNED,
    p_nombre varchar(100)
) BEGIN
UPDATE
    tbl_unidades
SET
    nombre = p_nombre
WHERE
    id = p_id;

END;

-- Procedimientos para la tabla de productos
CREATE PROCEDURE proc_obtener_productos_actualizados (IN p_tiempo_actualizacion TIMESTAMP) BEGIN
SELECT
    p.id,
    p.codigo_Barras,
    u.nombre AS unidad,
    c.nombre AS categoria,
    p.descripcion,
    p.precio_compra,
    p.precio_venta,
    p.stock,
    p.stock_minimo,
    e.descripcion as 'estado'
FROM
    tbl_productos p
    INNER JOIN tbl_unidades u ON u.id = p.id_unidad
    INNER JOIN tbl_categorias c ON c.id = p.id_categoria
    INNER JOIN tbl_estados e ON e.estado = p.estado
    AND e.nombre_tabla = 'tbl_productos'
WHERE
    p.fecha_actualizacion >= p_tiempo_actualizacion
ORDER BY
    p.id DESC;

END;

CREATE PROCEDURE proc_obtener_producto_por_id (IN p_id INT) BEGIN
SELECT
    p.id,
    p.codigo_Barras,
    u.nombre AS unidad,
    c.nombre AS categoria,
    p.descripcion,
    p.precio_compra,
    p.precio_venta,
    p.stock,
    p.stock_minimo,
    e.descripcion AS estado
FROM
    tbl_productos p
    INNER JOIN tbl_unidades u ON u.id = p.id_unidad
    INNER JOIN tbl_categorias c ON c.id = p.id_categoria
    INNER JOIN tbl_estados e ON e.estado = p.estado
    AND e.nombre_tabla = 'tbl_productos'
WHERE
    p.id = p_id
LIMIT
    1;

END;

CREATE PROCEDURE proc_obtener_productos_por_filtro (IN p_filtro VARCHAR(255)) BEGIN
SELECT
    p.id,
    p.codigo_Barras,
    u.nombre AS unidad,
    c.nombre AS categoria,
    p.descripcion,
    p.precio_compra,
    p.precio_venta,
    p.stock,
    p.stock_minimo,
    e.descripcion AS estado
FROM
    tbl_productos p
    INNER JOIN tbl_unidades u ON u.id = p.id_unidad
    INNER JOIN tbl_categorias c ON c.id = p.id_categoria
    INNER JOIN tbl_estados e ON e.estado = p.estado
    AND e.nombre_tabla = 'tbl_productos'
WHERE
    p.codigo_Barras LIKE CONCAT('%', p_filtro, '%')
    OR p.descripcion LIKE CONCAT('%', p_filtro, '%')
ORDER BY
    p.id DESC;

END;

CREATE PROCEDURE proc_mostrar_productos_paginado (IN p_limit INT, IN p_offset INT) BEGIN
SELECT
    p.id,
    p.codigo_Barras,
    u.nombre as unidad,
    c.nombre AS categoria,
    p.descripcion,
    p.precio_compra,
    p.precio_venta,
    p.stock,
    p.stock_minimo,
    e.descripcion as estado
FROM
    tbl_productos p
    INNER JOIN tbl_unidades u ON u.id = p.id_unidad
    INNER JOIN tbl_categorias c ON c.id = p.id_categoria
    INNER JOIN tbl_estados e ON e.estado = p.estado
    AND e.nombre_tabla = 'tbl_productos'
ORDER BY
    p.id DESC
LIMIT
    p_limit OFFSET p_offset;

END;

create procedure proc_productos_conteo() BEGIN
SELECT
    COUNT(*) AS conteo
FROM
    tbl_productos;

END;

CREATE PROCEDURE proc_Insertar_producto (
    IN p_Codigo_Barras varchar(13),
    p_Nombre_Unidad VARCHAR(100),
    p_Nombre_Categoria varchar(100),
    p_Descripcion varchar(100),
    p_Precio_Compra decimal(9, 2),
    p_Precio_Venta decimal(9, 2),
    p_Stock decimal(9, 2),
    p_Stock_Minimo decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

DECLARE p_Id_Unidad tinyint UNSIGNED;

DECLARE p_Id_Categoria tinyint UNSIGNED;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_productos"
    );

SET
    p_id_Categoria = (
        select
            Id
        FROM
            tbl_categorias
        where
            nombre = p_Nombre_Categoria
    );

SET
    p_id_Unidad = (
        select
            Id
        from
            tbl_unidades
        where
            nombre = p_Nombre_Unidad
    );

INSERT INTO
    tbl_productos (
        codigo_barras,
        id_unidad,
        id_Categoria,
        Descripcion,
        precio_compra,
        precio_venta,
        Stock,
        stock_minimo,
        Estado
    )
VALUES
    (
        p_Codigo_Barras,
        p_id_Unidad,
        p_id_Unidad,
        p_Descripcion,
        p_Precio_Compra,
        p_Precio_Venta,
        p_Stock,
        p_Stock_Minimo,
        p_estado
    );

END;

CREATE PROCEDURE proc_Actualizar_producto (
    IN p_id smallint UNSIGNED,
    p_Codigo_Barras varchar(13),
    p_Nombre_Unidad VARCHAR(100),
    p_Nombre_Categoria VARCHAR(100),
    p_Descripcion varchar(100),
    p_Precio_Compra decimal(9, 2),
    p_Precio_Venta decimal(9, 2),
    p_Stock decimal(9, 2),
    p_Stock_Minimo decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

DECLARE p_Id_Unidad tinyint UNSIGNED;

DECLARE p_Id_Categoria tinyint UNSIGNED;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_productos"
    );

SET
    p_id_Categoria = (
        select
            Id
        FROM
            tbl_categorias
        where
            nombre = p_Nombre_Categoria
    );

SET
    p_id_Unidad = (
        select
            Id
        from
            tbl_unidades
        where
            nombre = p_Nombre_Unidad
    );

UPDATE
    tbl_productos
SET
    codigo_barras = p_Codigo_Barras,
    id_unidad = p_Id_Unidad,
    id_Categoria = p_id_Categoria,
    Descripcion = p_Descripcion,
    precio_compra = p_Precio_Compra,
    precio_venta = p_Precio_Venta,
    Stock = p_Stock,
    stock_minimo = p_Stock_Minimo,
    Estado = p_estado
WHERE
    Id = p_id;

END;

CREATE PROCEDURE proc_eliminar_producto (IN p_id smallint UNSIGNED) BEGIN
UPDATE
    tbl_productos
SET
    estado = 255 - estado
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_buscar_codigo_barras (
    IN p_codigo_barras VARCHAR(13),
    OUT p_id SMALLINT UNSIGNED
) BEGIN DECLARE temp_id SMALLINT UNSIGNED DEFAULT 0;

SELECT
    id INTO temp_id
FROM
    tbl_productos
WHERE
    codigo_barras = p_codigo_barras
LIMIT
    1;

SET
    p_id = IFNULL (temp_id, 0);

END;

-- Procedimientos almacenados para la tabla de clientes
CREATE PROCEDURE proc_mostrar_clientes () BEGIN
SELECT
    c.id,
    c.documento,
    c.nombre,
    e.descripcion as estado
FROM
    tbl_clientes c
    JOIN tbl_estados e ON c.estado = e.estado
    AND e.nombre_tabla = "tbl_clientes";

END;

CREATE PROCEDURE proc_insertar_cliente (
    IN p_documento varchar(15),
    p_nombre varchar(1500),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_clientes"
    );

INSERT INTO
    tbl_clientes (
        documento,
        nombre,
        estado
    )
VALUES
    (
        p_documento,
        p_nombre,
        p_estado
    );

END;

CREATE PROCEDURE proc_actualizar_cliente (
    IN p_id smallint UNSIGNED,
    p_documento varchar(15),
    p_nombre varchar(1500),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_clientes"
    );

UPDATE
    tbl_clientes
SET
    documento = p_documento,
    nombre = p_nombre,
    estado = p_estado
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_eliminar_cliente (IN p_id smallint UNSIGNED) BEGIN
UPDATE
    tbl_clientes
SET
    estado = 255 - estado
WHERE
    id = p_id;

END;

-- Procedimientos para la tabla de proveedores
CREATE PROCEDURE proc_mostrar_proveedores () BEGIN
SELECT
    p.id,
    p.ruc,
    p.nombre,
    e.descripcion as estado
FROM
    tbl_proveedores p
    JOIN tbl_estados e ON p.estado = e.estado
    AND e.nombre_tabla = "tbl_proveedores";

END;

CREATE PROCEDURE proc_insertar_proveedor (
    IN p_ruc varchar(15),
    p_nombre varchar(1500),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_proveedores"
    );

INSERT INTO
    tbl_proveedores (ruc, nombre, estado)
VALUES
    (
        p_ruc,
        p_nombre,
        p_estado
    );

END;

CREATE PROCEDURE proc_actualizar_proveedor (
    IN p_id smallint UNSIGNED,
    p_ruc varchar(15),
    p_nombre varchar(1500),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_Estado tinyint unsigned;

SET
    p_Estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_proveedores"
    );

UPDATE
    tbl_proveedores
SET
    ruc = p_ruc,
    nombre = p_nombre,
    estado = p_estado
WHERE
    id = p_id;

END;

CREATE PROCEDURE proc_eliminar_proveedor (IN p_id smallint UNSIGNED) BEGIN
UPDATE
    tbl_proveedores
SET
    estado = 255 - estado
WHERE
    id = p_id;

END;

-- Procedimientos para la tabla de estados
CREATE PROCEDURE proc_insertar_estado (
    IN p_nombre_tabla varchar(50),
    p_estado tinyint UNSIGNED,
    p_descripcion varchar(100)
) BEGIN
INSERT INTO
    tbl_estados (
        nombre_tabla,
        estado,
        descripcion
    )
VALUES
    (
        p_nombre_tabla,
        p_estado,
        p_descripcion
    );

END;

CREATE PROCEDURE proc_actualizar_estado (
    IN p_nombre_tabla varchar(50),
    p_estado tinyint UNSIGNED,
    p_descripcion varchar(100)
) BEGIN
UPDATE
    tbl_estados
SET
    descripcion = p_descripcion
WHERE
    nombre_tabla = p_nombre_tabla
    AND estado = p_estado;

END;

CREATE PROCEDURE proc_mostrar_estado (IN p_nombre_tabla varchar(50)) BEGIN
SELECT
    *
FROM
    tbl_estados
WHERE
    nombre_tabla = p_nombre_tabla
ORDER BY
    estado ASC;

END;

-- Procedimientos para las ventas
CREATE PROCEDURE proc_mostrar_ventas () BEGIN
SELECT
    v.id,
    v.id_serie,
    v.contador_serie,
    v.id_usuario,
    v.id_cliente,
    e.descripcion as estado,
    v.fecha,
    v.total
FROM
    tbl_ventas v
    JOIN tbl_estados e ON v.estado = e.estado
    AND e.nombre_tabla = "tbl_ventas";

END;

CREATE PROCEDURE proc_insertar_venta (
    IN p_id_serie tinyint UNSIGNED,
    p_id_usuario tinyint UNSIGNED,
    p_id_cliente smallint UNSIGNED,
    p_descripcion_estado varchar(100),
    p_fecha timestamp,
    p_total decimal(9, 2)
) BEGIN DECLARE p_contador_serie mediumint UNSIGNED;

DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_contador_serie = (
        SELECT
            contador
        FROM
            tbl_series
        WHERE
            id = p_id_serie
    );

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_ventas"
    );

INSERT INTO
    tbl_ventas (
        id_serie,
        contador_serie,
        id_usuario,
        id_cliente,
        estado,
        fecha,
        total
    )
VALUES
    (
        p_id_serie,
        p_contador_serie,
        p_id_usuario,
        p_id_cliente,
        p_estado,
        p_fecha,
        p_total
    );

UPDATE
    tbl_series
SET
    contador = contador + 1
WHERE
    id = p_id_serie;

SELECT
    LAST_INSERT_ID() AS id_venta;

COMMIT;

END;

CREATE PROCEDURE proc_actualizar_venta (
    IN p_id mediumint UNSIGNED,
    p_id_cliente smallint UNSIGNED,
    p_descripcion_estado varchar(100),
    p_total decimal(9, 2)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_ventas"
    );

UPDATE
    tbl_ventas
SET
    id_cliente = p_id_cliente,
    estado = p_estado,
    total = p_total
WHERE
    id = p_id;

COMMIT;

END;

CREATE PROCEDURE proc_eliminar_venta (IN p_id mediumint UNSIGNED) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

UPDATE
    tbl_ventas
SET
    estado = 255 - estado
WHERE
    id = p_id;

COMMIT;

END;

-- Procedimientos para detalles de ventas
CREATE PROCEDURE proc_mostrar_venta_detalles (IN p_id_venta mediumint unsigned) BEGIN
SELECT
    vd.id_venta,
    vd.id_producto,
    vd.cantidad,
    vd.precio_venta,
    vd.descuento,
    e.descripcion as estado
FROM
    tbl_venta_detalles vd
    JOIN tbl_estados e ON vd.estado = e.estado
    AND e.nombre_tabla = "tbl_venta_detalles"
WHERE
    vd.id_venta = p_id_venta;

END;

CREATE PROCEDURE proc_insertar_venta_detalle (
    IN p_id_venta mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2),
    p_precio_Venta decimal(9, 2),
    p_descuento decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

select
    'funciono el procedimiento';

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_venta_detalles"
    );

INSERT INTO
    tbl_venta_detalles (
        id_venta,
        id_producto,
        cantidad,
        precio_venta,
        descuento,
        estado
    )
VALUES
    (
        p_id_venta,
        p_id_producto,
        p_cantidad,
        p_precio_Venta,
        p_descuento,
        p_estado
    );

COMMIT;

END;

CREATE PROCEDURE proc_actualizar_venta_detalle (
    IN p_id_venta mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2),
    p_precio_Venta decimal(9, 2),
    p_descuento decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado TINYINT UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_venta_detalles"
    );

UPDATE
    tbl_venta_detalles
SET
    cantidad = p_cantidad,
    precio_venta = p_Precio_Venta,
    descuento = p_descuento,
    estado = p_estado
WHERE
    id_producto = p_id_producto
    AND id_venta = p_id_venta;

COMMIT;

END;

CREATE PROCEDURE proc_eliminar_venta_detalle (
    IN p_id_venta mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

UPDATE
    tbl_venta_detalles
SET
    estado = 255 - estado
WHERE
    id_venta = p_id_venta
    AND id_producto = p_id_producto;

COMMIT;

END;

-- Mostrar todas las ventas individuales
CREATE PROCEDURE proc_mostrar_ventas_individuales (IN p_fecha DATE) BEGIN
SELECT
    vi.id,
    vi.id_producto,
    p.codigo_barras,
    p.descripcion,
    vi.id_usuario,
    u.nombre,
    vi.cantidad,
    vi.precio_venta,
    vi.fecha_hora
FROM
    tbl_venta_individual vi
    JOIN tbl_productos p ON vi.id_producto = p.id
    JOIN tbl_usuarios u ON vi.id_usuario = u.id
WHERE
    vi.fecha_hora >= p_fecha
    AND vi.fecha_hora < DATE_ADD(p_fecha, INTERVAL 1 DAY)
ORDER BY
    vi.fecha_hora DESC;

END;

CREATE PROCEDURE proc_insertar_venta_individual (
    IN p_id_producto smallint UNSIGNED,
    p_id_usuario tinyint unsigned,
    p_cantidad decimal(9, 2),
    p_precio_Venta decimal(9, 2),
    p_fecha_hora timestamp
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

select
    'funciono el procedimiento';

END;

START TRANSACTION;

INSERT INTO
    tbl_venta_individual (
        id_producto,
        id_usuario,
        cantidad,
        precio_venta,
        fecha_hora
    )
VALUES
    (
        p_id_producto,
        p_id_usuario,
        p_cantidad,
        p_precio_venta,
        p_fecha_hora
    );

COMMIT;

END;

CREATE PROCEDURE proc_actualizar_venta_individual (
    IN p_id mediumint UNSIGNED,
    IN p_id_producto smallint UNSIGNED,
    IN p_id_usuario tinyint UNSIGNED,
    IN p_cantidad decimal(9, 2),
    IN p_precio_venta decimal(9, 2),
    IN p_fecha_hora timestamp
) BEGIN DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

DECLARE EXIT HANDLER FOR SQLWARNING BEGIN ROLLBACK;

END;

START TRANSACTION;

-- Verificar si el registro existe
IF NOT EXISTS (
    SELECT
        1
    FROM
        tbl_venta_individual
    WHERE
        id = p_id
) THEN ROLLBACK;

ELSE -- Actualizar el registro
UPDATE
    tbl_venta_individual
SET
    id_producto = COALESCE(p_id_producto, id_producto),
    id_usuario = COALESCE(p_id_usuario, id_usuario),
    cantidad = COALESCE(p_cantidad, cantidad),
    precio_venta = COALESCE(p_precio_venta, precio_venta),
    fecha_hora = COALESCE(p_fecha_hora, fecha_hora)
WHERE
    id = p_id;

COMMIT;

END IF;

END;

CREATE PROCEDURE proc_eliminar_venta_individual(in p_id mediumint unsigned) BEGIN DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

DELETE FROM
    tbl_venta_individual
WHERE
    id = p_id;

COMMIT;

END;

-- Procedimiento para mostrar todas las compras
CREATE PROCEDURE proc_mostrar_compras () BEGIN
SELECT
    c.id,
    c.id_usuario,
    c.id_proveedor,
    e.descripcion as estado,
    c.fecha_hora,
    c.total
FROM
    tbl_compras c
    JOIN tbl_estados e ON c.estado = e.estado
    AND e.nombre_tabla = "tbl_compras";

END;

-- Procedimiento para insertar una nueva compra
CREATE PROCEDURE proc_insertar_compra (
    IN p_id_usuario tinyint UNSIGNED,
    p_id_proveedor smallint UNSIGNED,
    p_descripcion_estado varchar(100),
    p_fecha_hora timestamp,
    p_total decimal(9, 2)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_compras"
    );

INSERT INTO
    tbl_compras (
        id_usuario,
        id_proveedor,
        estado,
        fecha_hora,
        total
    )
VALUES
    (
        p_id_usuario,
        p_id_proveedor,
        p_estado,
        p_fecha_hora,
        p_total
    );

SELECT
    LAST_INSERT_ID() AS id_compra;

COMMIT;

END;

-- Procedimiento para actualizar una compra existente
CREATE PROCEDURE proc_actualizar_compra (
    IN p_id mediumint UNSIGNED,
    p_id_proveedor smallint UNSIGNED,
    p_descripcion_estado varchar(100),
    p_total decimal(9, 2)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_compras"
    );

UPDATE
    tbl_compras
SET
    id_proveedor = p_id_proveedor,
    estado = p_estado,
    total = p_total
WHERE
    id = p_id;

COMMIT;

END;

-- Procedimiento para eliminar (cambiar estado) de una compra
CREATE PROCEDURE proc_eliminar_compra (IN p_id_compra mediumint UNSIGNED) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

UPDATE
    tbl_compras
SET
    estado = 255 - estado
WHERE
    id = p_id;

COMMIT;

END;

-- Procedimiento para mostrar los detalles de una compra específica
CREATE PROCEDURE proc_mostrar_compra_detalles (IN p_id_compra mediumint unsigned) BEGIN
SELECT
    cd.id_compra,
    cd.id_producto,
    cd.cantidad,
    cd.precio_compra,
    cd.descuento,
    e.descripcion as estado
FROM
    tbl_compras_detalles cd
    JOIN tbl_estados e ON cd.estado = e.estado
    AND e.nombre_tabla = "tbl_compras_detalles"
WHERE
    cd.id_compra = p_id_compra;

END;

-- Procedimiento para insertar un detalle de compra
CREATE PROCEDURE proc_insertar_compra_detalle (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2),
    p_precio_compra decimal(9, 2),
    p_descuento decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_compras_detalles"
    );

INSERT INTO
    tbl_compras_detalles (
        id_compra,
        id_producto,
        cantidad,
        precio_compra,
        descuento,
        estado
    )
VALUES
    (
        p_id_compra,
        p_id_producto,
        p_cantidad,
        p_precio_compra,
        p_descuento,
        p_estado
    );

COMMIT;

END;

-- Procedimiento para actualizar un detalle de compra
CREATE PROCEDURE proc_actualizar_compra_detalle (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2),
    p_precio_compra decimal(9, 2),
    p_descuento decimal(9, 2),
    p_descripcion_estado varchar(100)
) BEGIN DECLARE p_estado tinyint UNSIGNED;

DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

SET
    p_estado = (
        SELECT
            estado
        FROM
            tbl_estados
        WHERE
            descripcion = p_descripcion_estado
            AND nombre_tabla = "tbl_compras_detalles"
    );

UPDATE
    tbl_compras_detalles
SET
    cantidad = p_cantidad,
    precio_compra = p_precio_compra,
    descuento = p_descuento,
    estado = p_estado
WHERE
    id_producto = p_id_producto
    AND id_compra = p_id_compra;

COMMIT;

END;

-- Procedimiento para eliminar (cambiar estado) de un detalle de compra
CREATE PROCEDURE proc_eliminar_compra_detalle (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

END;

START TRANSACTION;

UPDATE
    tbl_compras_detalles
SET
    estado = 255 - estado
WHERE
    id_compra = p_id_compra
    AND id_producto = p_id_producto;

COMMIT;

END;

-- Procedimiento para mostrar todas las bonificaciones de una compra
CREATE PROCEDURE proc_mostrar_bonificaciones (IN p_id_compra mediumint unsigned) BEGIN
SELECT
    b.id_compra,
    b.id_producto,
    p.descripcion,
    b.cantidad
FROM
    tbl_bonificaciones b
    JOIN tbl_productos p ON b.id_producto = p.id
WHERE
    b.id_compra = p_id_compra;

END;

-- Procedimiento para insertar una nueva bonificación
CREATE PROCEDURE proc_insertar_bonificacion (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2)
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

SELECT
    'Error al insertar la bonificación' AS mensaje;

END;

START TRANSACTION;

INSERT INTO
    tbl_bonificaciones (
        id_compra,
        id_producto,
        cantidad
    )
VALUES
    (
        p_id_compra,
        p_id_producto,
        p_cantidad
    );

SELECT
    'Bonificación agregada correctamente' AS mensaje;

COMMIT;

END;

-- Procedimiento para actualizar una bonificación existente
CREATE PROCEDURE proc_actualizar_bonificacion (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED,
    p_cantidad decimal(9, 2)
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

SELECT
    'Error al actualizar la bonificación' AS mensaje;

END;

START TRANSACTION;

UPDATE
    tbl_bonificaciones
SET
    cantidad = p_cantidad
WHERE
    id_compra = p_id_compra
    AND id_producto = p_id_producto;

IF ROW_COUNT() = 0 THEN
SELECT
    'No se encontró la bonificación para actualizar' AS mensaje;

ELSE
SELECT
    'Bonificación actualizada correctamente' AS mensaje;

END IF;

COMMIT;

END;

-- Procedimiento para eliminar una bonificación
CREATE PROCEDURE proc_eliminar_bonificacion (
    IN p_id_compra mediumint UNSIGNED,
    p_id_producto smallint UNSIGNED
) BEGIN DECLARE exit HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK;

SELECT
    'Error al eliminar la bonificación' AS mensaje;

END;

START TRANSACTION;

DELETE FROM
    tbl_bonificaciones
WHERE
    id_compra = p_id_compra
    AND id_producto = p_id_producto;

IF ROW_COUNT() = 0 THEN
SELECT
    'No se encontró la bonificación para eliminar' AS mensaje;

ELSE
SELECT
    'Bonificación eliminada correctamente' AS mensaje;

END IF;

COMMIT;

END;

-- Procedimientos para la tabla series
create procedure proc_mostrar_series() begin
select
    *
from
    tbl_series;

end;

CREATE PROCEDURE proc_insertar_serie(in p_serie char(4)) BEGIN
INSERT INTO
    tbl_series (serie, contador)
VALUES
    (p_serie, 1);

END;

CREATE PROCEDURE proc_actualizar_serie (
    IN p_id tinyint UNSIGNED,
    p_serie char(4),
    p_contador mediumint UNSIGNED
) BEGIN
UPDATE
    tbl_series
SET
    serie = p_serie,
    contador = p_contador
WHERE
    id = p_id;
END;
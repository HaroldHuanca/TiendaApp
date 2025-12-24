from sqlalchemy import text
from typing import List, Dict, Any
from database.connection import DatabaseManager

# Mostrar detalles de una compra específica
def mostrar_detalles_compra(id_compra: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_mostrar_compra_detalles", [id_compra])
            detalles = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    for row in results:
                        detalles.append(dict(zip(columns, row)))
                if not cursor.nextset():
                    break
            return detalles
        finally:
            cursor.close()

# Insertar un detalle de compra
def insertar_detalle_compra(
    id_compra: int,
    id_producto: int,
    cantidad: float,
    precio_compra: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_insertar_compra_detalle(
                    :p_id_compra,
                    :p_id_producto,
                    :p_cantidad,
                    :p_precio_compra,
                    :p_descuento,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id_compra": id_compra,
                "p_id_producto": id_producto,
                "p_cantidad": cantidad,
                "p_precio_compra": precio_compra,
                "p_descuento": descuento,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# Actualizar un detalle de compra
def actualizar_detalle_compra(
    id_compra: int,
    id_producto: int,
    cantidad: float,
    precio_compra: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_compra_detalle(
                    :p_id_compra,
                    :p_id_producto,
                    :p_cantidad,
                    :p_precio_compra,
                    :p_descuento,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id_compra": id_compra,
                "p_id_producto": id_producto,
                "p_cantidad": cantidad,
                "p_precio_compra": precio_compra,
                "p_descuento": descuento,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# Eliminar (anular) un detalle de compra
def eliminar_detalle_compra(id_compra: int, id_producto: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_eliminar_compra_detalle(
                    :p_id_compra,
                    :p_id_producto
                )
            """),
            {
                "p_id_compra": id_compra,
                "p_id_producto": id_producto
            }
        )
        db.commit()

# Obtener detalles con información de productos
def obtener_detalles_con_productos(id_compra: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_obtener_compra_detalles_con_productos", [id_compra])
            detalles = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    for row in results:
                        detalles.append(dict(zip(columns, row)))
                if not cursor.nextset():
                    break
            return detalles
        finally:
            cursor.close()
from sqlalchemy import text
from typing import List, Dict, Any
from database.connection import DatabaseManager

# ✅ Mostrar detalles de una venta específica
def mostrar_detalles_venta(id_venta: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_mostrar_venta_detalles(:p_id_venta)"),
            {"p_id_venta": id_venta}
        )
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar un detalle de venta
def insertar_detalle_venta(
    id_venta: int,
    id_producto: int,
    cantidad: float,
    precio_venta: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_insertar_venta_detalle(
                    :p_id_venta,
                    :p_id_producto,
                    :p_cantidad,
                    :p_precio_Venta,
                    :p_descuento,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id_venta": id_venta,
                "p_id_producto": id_producto,
                "p_cantidad": cantidad,
                "p_precio_Venta": precio_venta,
                "p_descuento": descuento,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Actualizar un detalle de venta
def actualizar_detalle_venta(
    id_venta: int,
    id_producto: int,
    cantidad: float,
    precio_venta: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_venta_detalle(
                    :p_id_venta,
                    :p_id_producto,
                    :p_cantidad,
                    :p_precio_Venta,
                    :p_descuento,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id_venta": id_venta,
                "p_id_producto": id_producto,
                "p_cantidad": cantidad,
                "p_precio_Venta": precio_venta,
                "p_descuento": descuento,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Eliminar (anular) un detalle de venta
def eliminar_detalle_venta(id_venta: int, id_producto: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_eliminar_venta_detalle(
                    :p_id_venta,
                    :p_id_producto
                )
            """),
            {
                "p_id_venta": id_venta,
                "p_id_producto": id_producto
            }
        )
        db.commit()

# ✅ Obtener detalles de venta con información del producto
def obtener_detalles_con_productos(id_venta: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_obtener_venta_detalles_con_productos", [id_venta])
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

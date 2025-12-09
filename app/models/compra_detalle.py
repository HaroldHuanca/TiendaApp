from sqlalchemy import text
from typing import List, Dict, Any
from database.connection import DatabaseManager

# Mostrar detalles de una compra específica
def mostrar_detalles_compra(id_compra: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_mostrar_compra_detalles(:p_id_compra)"),
            {"p_id_compra": id_compra}
        )
        return [dict(row._mapping) for row in result.fetchall()]

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
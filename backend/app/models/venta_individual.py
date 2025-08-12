from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.database import DatabaseManager

# Mostramos las ventas indidividuales
def mostrar_ventas_individuales(fecha: str) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("SELECT * FROM ventas_individuales(:p_fecha)"),
            {"p_fecha": fecha}
        )
        return [dict(row._mapping) for row in result.fetchall()]

# Insertar una venta individual
def insertar_venta_individual(
    id_produccto: int,
    id_usuario: int,
    cantidad: float,
    precio_venta: float,
    fecha_hora: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                 CALL proc_insertar_venta_individual(
                     :p_id_producto,
                     :p_id_usuario,
                     :p_cantidad,
                     :p_precio_venta,
                     :p_fecha_hora
                 )
            """),
            {
                "p_id_producto": id_produccto,
                "p_id_usuario": id_usuario,
                "p_cantidad": cantidad,
                "p_precio_venta": precio_venta,
                "p_fecha_hora": fecha_hora
            }
        
        )
        db.commit()
        
# Actualizar una venta individual

def actualizar_venta_individual(
    id: int,
    id_producto: int,
    id_usuario: int,
    cantidad: float,
    precio_venta: float,
    fecha_hora: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                 CALL proc_actualizar_venta_individual(
                     :p_id,
                     :p_id_producto,
                     :p_id_usuario,
                     :p_cantidad,
                     :p_precio_venta,
                     :p_fecha_hora
                 )
            """),
            {
                "p_id": id,
                "p_id_producto": id_producto,
                "p_id_usuario": id_usuario,
                "p_cantidad": cantidad,
                "p_precio_venta": precio_venta,
                "p_fecha_hora": fecha_hora
            }
        )
        db.commit()
        
# Eliminar una venta individual
def eliminar_venta_individual(id: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                 CALL proc_eliminar_venta_individual(:p_id)
            """),
            {
                "p_id": id
            }
        )
        db.commit()
from sqlalchemy import text
from typing import List, Dict, Any
from datetime import datetime
from database.connection import DatabaseManager

# Mostramos las ventas indidividuales
def mostrar_ventas_individuales(fecha: str) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("""
                SELECT
                    vi.id,
                    vi.id_producto,
                    p.codigo_barras,
                    p.descripcion,
                    vi.id_usuario,
                    u.nombre_usuario AS nombre_usuario,
                    vi.cantidad,
                    vi.precio_venta,
                    vi.fecha_hora
                FROM
                    tbl_venta_individual vi
                    JOIN tbl_productos p ON vi.id_producto = p.id
                    JOIN tbl_usuarios u ON vi.id_usuario = u.id
                WHERE
                    vi.fecha_hora >= :p_fecha
                    AND vi.fecha_hora < DATE_ADD(:p_fecha, INTERVAL 1 DAY)
                ORDER BY
                    vi.fecha_hora DESC
            """),
            {"p_fecha": fecha}
        )
        rows = [dict(row._mapping) for row in result.fetchall()]

    try:
        return sorted(
            rows,
            key=lambda row: datetime.strptime(row.get('fecha_hora', ''), '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )
    except Exception:
        return sorted(rows, key=lambda row: row.get('fecha_hora', ''), reverse=True)

# Insertar una venta individual
def insertar_venta_individual(
    id_producto: int,
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
                "p_id_producto": id_producto,
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
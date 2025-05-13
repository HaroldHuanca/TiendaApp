from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.database import DatabaseManager

# ✅ Mostrar todas las ventas
def mostrar_ventas() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_ventas()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar una venta (retorna el ID generado)
def insertar_venta(id_serie: int, id_usuario: int, id_cliente: int, descripcion_estado: str, fecha: str, total: float) -> Optional[int]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection  # conexión real de MariaDB
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_insertar_venta", [
                id_serie,
                id_usuario,
                id_cliente,
                descripcion_estado,
                fecha,
                total
            ])

            # Recorremos todos los resultsets hasta encontrar el resultado del SELECT
            while True:
                result = cursor.fetchall()
                if result:
                    return result[0][0]  # ID de la venta insertada
                if not cursor.nextset():
                    break

        finally:
            cursor.close()
            raw_connection.commit()
# ✅ Actualizar una venta
def actualizar_venta(
    id: int,
    id_cliente: int,
    descripcion_estado: str,
    total: float
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_venta(
                    :p_id,
                    :p_id_cliente,
                    :p_descripcion_estado,
                    :p_total
                )
            """),
            {
                "p_id": id,
                "p_id_cliente": id_cliente,
                "p_descripcion_estado": descripcion_estado,
                "p_total": total
            }
        )
        db.commit()

# ✅ Eliminar (anular) una venta
def eliminar_venta(id: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_venta(:p_id)"),
            {"p_id": id}
        )
        db.commit()
from sqlalchemy import text
from typing import List, Dict, Any
from app.database import DatabaseManager

# ✅ Mostrar todas las ventas
def mostrar_ventas() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_ventas()"))
        return [dict(row) for row in result.fetchall()]

# ✅ Insertar una venta (retorna el ID generado)
def insertar_venta(
    id_serie: int,
    id_usuario: int,
    id_cliente: int,
    descripcion_estado: str,
    fecha: str,  # formato: 'YYYY-MM-DD HH:MM:SS'
    total: float
) -> int:
    with DatabaseManager() as db:
        result = db.execute(
            text("""
                CALL proc_insertar_venta(
                    :p_id_serie,
                    :p_id_usuario,
                    :p_id_cliente,
                    :p_descripcion_estado,
                    :p_fecha,
                    :p_total,
                    @p_id
                );
                SELECT @p_id AS id;
            """),
            {
                "p_id_serie": id_serie,
                "p_id_usuario": id_usuario,
                "p_id_cliente": id_cliente,
                "p_descripcion_estado": descripcion_estado,
                "p_fecha": fecha,
                "p_total": total
            }
        )
        # El ID insertado está en el segundo result set
        result.nextset()
        row = result.fetchone()
        return row["id"] if row else None

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
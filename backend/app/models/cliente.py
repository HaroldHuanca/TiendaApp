from sqlalchemy import text
from typing import List, Dict, Any
from database import DatabaseManager

# ✅ Mostrar todos los clientes
def mostrar_clientes() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_clientes()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar un nuevo cliente
def insertar_cliente(documento: str, nombre: str, descripcion_estado: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_insertar_cliente(
                    :p_documento,
                    :p_nombre,
                    :p_descripcion_estado
                )
            """),
            {
                "p_documento": documento,
                "p_nombre": nombre,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Actualizar un cliente existente
def actualizar_cliente(id_cliente: int, documento: str, nombre: str, descripcion_estado: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_cliente(
                    :p_id,
                    :p_documento,
                    :p_nombre,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id": id_cliente,
                "p_documento": documento,
                "p_nombre": nombre,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Eliminar (alternar estado) de un cliente
def eliminar_cliente(id_cliente: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_cliente(:p_id)"),
            {"p_id": id_cliente}
        )
        db.commit()

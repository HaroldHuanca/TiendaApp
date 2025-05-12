from sqlalchemy import text
from typing import List, Dict, Any
from database import DatabaseManager

# ✅ Mostrar todos los proveedores
def mostrar_proveedores() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_proveedores()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar un nuevo proveedor
def insertar_proveedor(ruc: str, nombre: str, descripcion_estado: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_insertar_proveedor(
                    :p_ruc,
                    :p_nombre,
                    :p_descripcion_estado
                )
            """),
            {
                "p_ruc": ruc,
                "p_nombre": nombre,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Actualizar un proveedor existente
def actualizar_proveedor(id_proveedor: int, ruc: str, nombre: str, descripcion_estado: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_proveedor(
                    :p_id,
                    :p_ruc,
                    :p_nombre,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id": id_proveedor,
                "p_ruc": ruc,
                "p_nombre": nombre,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Eliminar (alternar estado) de un proveedor
def eliminar_proveedor(id_proveedor: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_proveedor(:p_id)"),
            {"p_id": id_proveedor}
        )
        db.commit()

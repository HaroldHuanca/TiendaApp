from sqlalchemy import text
from typing import List, Dict, Any
from database.connection import DatabaseManager

# ✅ Mostrar todas las unidades
def mostrar_unidades() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_unidad()"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]

# ✅ Insertar una nueva unidad
def insertar_unidad(nombre: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_insertar_unidad(:p_nombre)"),
            {"p_nombre": nombre}
        )
        db.commit()

# ✅ Actualizar el nombre de una unidad por ID
def actualizar_unidad(id: int, nombre: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_actualizar_unidad(:p_id, :p_nombre)"),
            {"p_id": id, "p_nombre": nombre}
        )
        db.commit()

# ✅ Eliminar (alternar estado) de una unidad
def eliminar_unidad(id_unidad: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_unidad(:p_id)"),
            {"p_id": id_unidad}
        )
        db.commit()

# ✅ Mostrar unidades eliminadas
def mostrar_unidades_eliminadas() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_unidades_eliminadas()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Restaurar una unidad
def restaurar_unidad(id_unidad: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_restaurar_unidad(:p_id)"),
            {"p_id": id_unidad}
        )
        db.commit()

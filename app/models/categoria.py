from sqlalchemy import text
from typing import List, Dict, Any
from database.connection import DatabaseManager

# ✅ Mostrar todas las categorías
def mostrar_categorias() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_categoria()"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]

# ✅ Insertar una nueva categoría
def insertar_categoria(nombre: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_insertar_categoria(:p_nombre)"),
            {"p_nombre": nombre}
        )
        db.commit()

# ✅ Actualizar el nombre de una categoría por ID
def actualizar_categoria(id: int, nombre: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_actualizar_categoria(:p_id, :p_nombre)"),
            {"p_id": id, "p_nombre": nombre}
        )
        db.commit()

# ✅ Eliminar (alternar estado) de una categoría
def eliminar_categoria(id_categoria: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_categoria(:p_id)"),
            {"p_id": id_categoria}
        )
        db.commit()

# ✅ Mostrar categorías eliminadas
def mostrar_categorias_eliminadas() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_categorias_eliminadas()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Restaurar una categoría
def restaurar_categoria(id_categoria: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_restaurar_categoria(:p_id)"),
            {"p_id": id_categoria}
        )
        db.commit()


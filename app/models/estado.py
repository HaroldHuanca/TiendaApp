from sqlalchemy import text
from typing import List, Dict, Any
from app.database import DatabaseManager

# ✅ Mostrar estados por nombre de tabla
def mostrar_estados(nombre_tabla: str) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_mostrar_estado(:p_nombre_tabla)"),
            {"p_nombre_tabla": nombre_tabla}
        )
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar nuevo estado
def insertar_estado(nombre_tabla: str, estado: int, descripcion: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_insertar_estado(
                    :p_nombre_tabla,
                    :p_estado,
                    :p_descripcion
                )
            """),
            {
                "p_nombre_tabla": nombre_tabla,
                "p_estado": estado,
                "p_descripcion": descripcion
            }
        )
        db.commit()

# ✅ Actualizar descripción de estado existente
def actualizar_estado(nombre_tabla: str, estado: int, descripcion: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_estado(
                    :p_nombre_tabla,
                    :p_estado,
                    :p_descripcion
                )
            """),
            {
                "p_nombre_tabla": nombre_tabla,
                "p_estado": estado,
                "p_descripcion": descripcion
            }
        )
        db.commit()

from sqlalchemy import text
from typing import List, Optional, Dict
from database.connection import DatabaseManager

def mostrar_series() -> List[Dict]:
    """Obtiene todas las series de comprobantes"""
    with DatabaseManager() as db:
        result = db.execute(text("SELECT id, serie, contador FROM tbl_series"))
        rows = result.fetchall()
        return [
            {
                "id": row[0],
                "serie": row[1],
                "contador": row[2]
            }
            for row in rows
        ]

def insertar_serie(serie: str, contador: int) -> None:
    """Inserta una nueva serie de comprobante"""
    with DatabaseManager() as db:
        db.execute(
            text("INSERT INTO tbl_series (serie, contador) VALUES (:serie, :contador)"),
            {"serie": serie, "contador": contador}
        )
        db.commit()

def actualizar_serie(id: int, serie: str, contador: int) -> None:
    """Actualiza una serie existente"""
    with DatabaseManager() as db:
        db.execute(
            text("UPDATE tbl_series SET serie = :serie, contador = :contador WHERE id = :id"),
            {"id": id, "serie": serie, "contador": contador}
        )
        db.commit()

def eliminar_serie(id: int) -> None:
    """Elimina una serie"""
    with DatabaseManager() as db:
        db.execute(
            text("DELETE FROM tbl_series WHERE id = :id"),
            {"id": id}
        )
        db.commit()

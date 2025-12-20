from sqlalchemy import text
from typing import List, Optional, Dict
from database.connection import DatabaseManager

def mostrar_series() -> List[Dict]:
    """Obtiene todas las series de comprobantes"""
    with DatabaseManager() as db:
        result = db.execute(text("CaLL proc_mostrar_series()"))
        rows = result.fetchall()
        return [
            {
                "id": row[0],
                "serie": row[1],
                "contador": row[2]
            }
            for row in rows
        ]

def insertar_serie(serie: str) -> None:
    """Inserta una nueva serie de comprobante"""
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_insertar_serie(:serie)"),
            {"serie": serie}
        )
        db.commit()

def actualizar_serie(id: int, serie: str, contador: int) -> None:
    """Actualiza una serie existente"""
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_actualizar_serie(:id, :serie, :contador)"),
            {"id": id, "serie": serie, "contador": contador}
        )
        db.commit()

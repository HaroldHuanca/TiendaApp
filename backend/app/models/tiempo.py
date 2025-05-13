from sqlalchemy import text
from typing import Optional
from app.database import DatabaseManager

# ✅ Obtener la fecha y hora actual del servidor
def obtener_fecha_actual() -> Optional[str]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_obtener_fecha_actual()"))
        row = result.fetchone()
        _ = result.fetchall()
        return row[0] if row else None
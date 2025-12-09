from sqlalchemy import text
from typing import Optional
from app.database import DatabaseManager
from datetime import datetime

# ✅ Obtener la fecha y hora actual del servidor
def obtener_fecha_actual() -> Optional[str]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_obtener_fecha_actual()"))
        row = result.fetchone()
        _ = result.fetchall()
        return row[0].strftime("%d/%m/%Y %H:%M:%S") if row else "1/1/1996 00:00:00"
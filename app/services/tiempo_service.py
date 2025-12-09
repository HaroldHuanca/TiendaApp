# backend/app/services/tiempo_service.py

from app.models.tiempo import obtener_fecha_actual

def obtener_fecha_actual_formateada() -> (str|None):
    """
    Lógica de negocio que obtiene la fecha actual del servidor y la devuelve formateada.
    """
    return obtener_fecha_actual()

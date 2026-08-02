# backend/app/services/tiempo_service.py

from app.models.tiempo import obtener_fecha_actual

def obtener_fecha_actual_formateada() -> (str|None):
    """
    Lógica de negocio que obtiene la fecha actual del servidor y la devuelve formateada.
    """
    return obtener_fecha_actual()

def obtener_fecha_actual_formateada_YYYYmmddHHMMSS() -> (str|None):
    """
    Lógica de negocio que obtiene la fecha actual del servidor y la devuelve formateada en el formato YYYY-mm-dd HH:MM:SS.
    """
    from app.models.tiempo import obtener_fecha_actual_formato_YYYYmmddHHMMSS
    return obtener_fecha_actual_formato_YYYYmmddHHMMSS()

# backend/app/services/tiempo_service.py

from app.models.tiempo import obtener_fecha_actual

def obtener_fecha_actual_formateada() -> str:
    """
    Lógica de negocio que obtiene la fecha actual del servidor y la devuelve formateada.
    """
    fecha = obtener_fecha_actual()
    if fecha is None:
        return "Fecha no disponible"
    
    # Aquí podrías aplicar formato adicional si quisieras
    return f"La fecha y hora actual es: {fecha}"

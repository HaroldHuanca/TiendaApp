from app.models import serie

def mostrar_series():
    """Obtiene todas las series de comprobantes"""
    return serie.mostrar_series()

def insertar_serie(serie_valor: str, contador: int) -> None:
    """Inserta una nueva serie de comprobante"""
    serie.insertar_serie(serie_valor, contador)

def actualizar_serie(id: int, serie_valor: str, contador: int) -> None:
    """Actualiza una serie existente"""
    serie.actualizar_serie(id, serie_valor, contador)

def eliminar_serie(id: int) -> None:
    """Elimina una serie"""
    serie.eliminar_serie(id)

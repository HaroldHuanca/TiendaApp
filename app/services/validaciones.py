import re
from datetime import datetime

def validar_id_tinyint(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0 or id_ > 255:
        raise ValueError(f"{nombre} debe ser un número entero positivo menor a 255.")
def validar_id_smallint(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0 or id_ > 65535:
        raise ValueError(f"{nombre} debe ser un número entero positivo menor a 65535.")
def validar_id_mediumint(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0 or id_ > 16777215:
        raise ValueError(f"{nombre} debe ser un número entero positivo menor a 16777215.")
def validar_descripcion(descripcion: str, nombre: str = "Descripcion") -> None:
    if not isinstance(descripcion, str):
        raise ValueError(f"{nombre} debe ser una cadena de texto.")
    if len(descripcion) == 0 or len(descripcion) > 100:
        raise ValueError(f"{nombre} debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ 0-9()]+", descripcion):
        raise ValueError(f"{nombre} contiene caracteres no permitidos.")
def validar_fecha(fecha: str) -> None:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha debe estar en formato AAAA-MM-DD.")

def validar_fecha_hora(fecha_hora: str) -> None:
    try:
        datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("La fecha y hora deben estar en formato AAAA-MM-DD HH:MM:SS.")
def validar_total(total: float) -> None:
    if not isinstance(total, (int, float)) or total < 0:
        raise ValueError("El total debe ser un número no negativo.")
# Validaciones

def validar_cantidad(cantidad: float) -> None:
    if not isinstance(cantidad, (int, float)) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un número positivo.")

def validar_precio(precio: float) -> None:
    if not isinstance(precio, (int, float)) or precio < 0:
        raise ValueError("El precio de venta debe ser un número no negativo.")

def validar_descuento(descuento: float) -> None:
    if not isinstance(descuento, (int, float)) or descuento < 0:
        raise ValueError("El descuento debe ser un numero positivo o cero.")

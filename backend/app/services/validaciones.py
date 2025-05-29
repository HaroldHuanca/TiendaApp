import re

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
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion):
        raise ValueError(f"{nombre} contiene caracteres no permitidos.")
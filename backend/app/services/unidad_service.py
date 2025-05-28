import re
from typing import List, Dict, Any
import app.models.unidad as unidad_model

# Validaciones

def validar_id(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0 or id > 255:
        raise ValueError(f"{nombre} debe ser un número entero positivo menor a 255.")

def validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")
    if len(nombre) == 0 or len(nombre) > 100:
        raise ValueError("El nombre debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 .,'\-()]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

# Lógica del servicio

def mostrar_unidades() -> List[Dict[str, Any]]:
    return unidad_model.mostrar_unidades()

def insertar_unidad(nombre: str) -> None:
    validar_nombre(nombre)
    unidad_model.insertar_unidad(nombre)

def actualizar_unidad(id_unidad: int, nombre: str) -> None:
    validar_id(id_unidad, "ID de la unidad")
    validar_nombre(nombre)
    unidad_model.actualizar_unidad(id_unidad, nombre)

from typing import List,Dict,Any
import re

import app.models.categoria as cat

# Validación para 'nombre': letras, números, espacios y guiones bajos, hasta 50 caracteres
def validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")
    if len(nombre) == 0 or len(nombre) > 100:
        raise ValueError("El nombre debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ'., -]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

# Validación para 'id': debe ser entero positivo
def validar_id(id: int) -> None:
    if not isinstance(id, int) or id <= 0 or id > 255:
        raise ValueError("El ID debe ser un número entero positivo menor o igual a 255.")

def mostrar_categorias() -> List[Dict[str, Any]]:
    return cat.mostrar_categorias()

def insertar_categoria(nombre: str) -> None:
    validar_nombre(nombre)
    cat.insertar_categoria(nombre)

def actualizar_categoria(id: int, nombre: str) -> None:
    validar_id(id)
    validar_nombre(nombre)
    cat.actualizar_categoria(id,nombre)

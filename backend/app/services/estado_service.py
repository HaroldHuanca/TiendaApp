from typing import List, Dict, Any
import re

import app.models.estado as estado_model
from app.services.validaciones import validar_descripcion, validar_id_tinyint

# Validación para 'nombre_tabla': letras y guiones bajos (ej. cliente, producto)
def validar_nombre_tabla(nombre_tabla: str) -> None:
    if not isinstance(nombre_tabla, str):
        raise ValueError("El nombre de la tabla debe ser una cadena de texto.")
    if len(nombre_tabla) == 0 or len(nombre_tabla) > 50:
        raise ValueError("El nombre de la tabla debe tener entre 1 y 50 caracteres.")
    if not re.fullmatch(r"[a-zA-Z_]+", nombre_tabla):
        raise ValueError("El nombre de la tabla contiene caracteres no permitidos.")
    
# Lógica de servicio
def mostrar_estados(nombre_tabla: str) -> List[Dict[str, Any]]:
    validar_nombre_tabla(nombre_tabla)
    return estado_model.mostrar_estados(nombre_tabla)

def insertar_estado(nombre_tabla: str, estado: int, descripcion: str) -> None:
    validar_nombre_tabla(nombre_tabla)
    validar_id_tinyint(estado,"Estado")
    validar_descripcion(descripcion, "Descripcion Estado")
    estado_model.insertar_estado(nombre_tabla, estado, descripcion)

def actualizar_estado(nombre_tabla: str, estado: int, descripcion: str) -> None:
    validar_nombre_tabla(nombre_tabla)
    validar_id_tinyint(estado,"Estado")
    validar_descripcion(descripcion,"Descripcion Estado")
    estado_model.actualizar_estado(nombre_tabla, estado, descripcion)

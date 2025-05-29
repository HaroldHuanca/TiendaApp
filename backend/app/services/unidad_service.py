import re
from typing import List, Dict, Any
import app.models.unidad as unidad_model

from app.services.validaciones import validar_descripcion, validar_id_tinyint

# Lógica del servicio

def mostrar_unidades() -> List[Dict[str, Any]]:
    return unidad_model.mostrar_unidades()

def insertar_unidad(nombre: str) -> None:
    validar_descripcion(nombre,"Nombre de Unidad")
    unidad_model.insertar_unidad(nombre)

def actualizar_unidad(id_unidad: int, nombre: str) -> None:
    validar_id_tinyint(id_unidad, "ID de la unidad")
    validar_descripcion(nombre, "Nombre de Unidad")
    unidad_model.actualizar_unidad(id_unidad, nombre)

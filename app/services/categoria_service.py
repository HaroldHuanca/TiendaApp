from typing import List,Dict,Any
import re

import app.models.categoria as cat
from app.services.validaciones import validar_descripcion, validar_id_tinyint

def mostrar_categorias() -> List[Dict[str, Any]]:
    return cat.mostrar_categorias()

def insertar_categoria(nombre: str) -> None:
    validar_descripcion(nombre, "Nombre Categoria")
    cat.insertar_categoria(nombre)

def actualizar_categoria(id: int, nombre: str) -> None:
    validar_id_tinyint(id, "ID Categoria")
    validar_descripcion(nombre, "Nombre Categoria")
    cat.actualizar_categoria(id,nombre)

def eliminar_categoria(id_categoria: int) -> None:
    validar_id_tinyint(id_categoria, "ID Categoria")
    cat.eliminar_categoria(id_categoria)

def mostrar_categorias_eliminadas() -> List[Dict[str, Any]]:
    return cat.mostrar_categorias_eliminadas()

def restaurar_categoria(id_categoria: int) -> None:
    validar_id_tinyint(id_categoria, "ID Categoria")
    cat.restaurar_categoria(id_categoria)

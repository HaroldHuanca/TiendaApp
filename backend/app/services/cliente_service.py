from typing import List, Dict, Any
import re

import app.models.cliente as cli
from app.services.validaciones import validar_descripcion, validar_id_smallint
# Validación para 'nombre': letras, espacios, guiones, tildes, hasta 50 caracteres
def validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")
    if len(nombre) == 0 or len(nombre) > 1500:
        raise ValueError("El nombre debe tener entre 1 y 1500 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ' -]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

# Validación para 'documento': alfanumérico, entre 1 y 20 caracteres
def validar_documento(documento: str) -> None:
    if not isinstance(documento, str):
        raise ValueError("El documento debe ser una cadena de texto.")
    if len(documento) == 0 or len(documento) > 15:
        raise ValueError("El documento debe tener entre 1 y 15 caracteres.")
    if not re.fullmatch(r"[a-zA-Z0-9]+", documento):
        raise ValueError("El documento solo puede contener letras y números.")
# Lógica de servicio
def mostrar_clientes() -> List[Dict[str, Any]]:
    return cli.mostrar_clientes()

def insertar_cliente(documento: str, nombre: str, descripcion_estado: str) -> None:
    validar_documento(documento)
    validar_nombre(nombre)
    validar_descripcion(descripcion_estado,"Descripcion Estado")
    cli.insertar_cliente(documento, nombre, descripcion_estado)

def actualizar_cliente(id_cliente: int, documento: str, nombre: str, descripcion_estado: str) -> None:
    validar_id_smallint(id_cliente,"ID Cliente")
    validar_documento(documento)
    validar_nombre(nombre)
    validar_descripcion(descripcion_estado,"Descripcion Estado")
    cli.actualizar_cliente(id_cliente, documento, nombre, descripcion_estado)

def eliminar_cliente(id_cliente: int) -> None:
    validar_id_smallint(id_cliente,"ID Cliente")
    cli.eliminar_cliente(id_cliente)

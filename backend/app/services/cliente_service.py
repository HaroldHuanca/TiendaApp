from typing import List, Dict, Any
import re

import app.models.cliente as cli

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

# Validación para 'descripcion_estado': letras y espacios, hasta 30 caracteres
def validar_descripcion_estado(descripcion_estado: str) -> None:
    if not isinstance(descripcion_estado, str):
        raise ValueError("La descripción del estado debe ser una cadena de texto.")
    if len(descripcion_estado) == 0 or len(descripcion_estado) > 100:
        raise ValueError("La descripción del estado debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion_estado):
        raise ValueError("La descripción del estado contiene caracteres no permitidos.")

# Validación para 'id_cliente': entero positivo
def validar_id(id_cliente: int) -> None:
    if not isinstance(id_cliente, int) or id_cliente <= 0 or id_cliente >65535:
        raise ValueError("El ID debe ser un número entero positivo menor o igual que 65535.")

# Lógica de servicio
def mostrar_clientes() -> List[Dict[str, Any]]:
    return cli.mostrar_clientes()

def insertar_cliente(documento: str, nombre: str, descripcion_estado: str) -> None:
    validar_documento(documento)
    validar_nombre(nombre)
    validar_descripcion_estado(descripcion_estado)
    cli.insertar_cliente(documento, nombre, descripcion_estado)

def actualizar_cliente(id_cliente: int, documento: str, nombre: str, descripcion_estado: str) -> None:
    validar_id(id_cliente)
    validar_documento(documento)
    validar_nombre(nombre)
    validar_descripcion_estado(descripcion_estado)
    cli.actualizar_cliente(id_cliente, documento, nombre, descripcion_estado)

def eliminar_cliente(id_cliente: int) -> None:
    validar_id(id_cliente)
    cli.eliminar_cliente(id_cliente)

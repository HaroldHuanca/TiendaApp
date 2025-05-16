import re
from typing import List, Dict, Any
import app.models.proveedor as proveedor_model

# Validaciones

def validar_id(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0:
        raise ValueError(f"{nombre} debe ser un número entero positivo.")

def validar_ruc(ruc: str) -> None:
    if not isinstance(ruc, str):
        raise ValueError("El RUC debe ser una cadena de texto.")
    if not re.fullmatch(r"\d{11}", ruc):
        raise ValueError("El RUC debe contener exactamente 11 dígitos numéricos.")

def validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")
    if len(nombre) == 0 or len(nombre) > 100:
        raise ValueError("El nombre debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 .,'\-&()]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

def validar_descripcion_estado(descripcion_estado: str) -> None:
    if not isinstance(descripcion_estado, str):
        raise ValueError("La descripción del estado debe ser una cadena de texto.")
    if len(descripcion_estado) == 0 or len(descripcion_estado) > 30:
        raise ValueError("La descripción del estado debe tener entre 1 y 30 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion_estado):
        raise ValueError("La descripción del estado contiene caracteres no permitidos.")

# Lógica del servicio

def mostrar_proveedores() -> List[Dict[str, Any]]:
    return proveedor_model.mostrar_proveedores()

def insertar_proveedor(ruc: str, nombre: str, descripcion_estado: str) -> None:
    validar_ruc(ruc)
    validar_nombre(nombre)
    validar_descripcion_estado(descripcion_estado)

    proveedor_model.insertar_proveedor(ruc, nombre, descripcion_estado)

def actualizar_proveedor(id_proveedor: int, ruc: str, nombre: str, descripcion_estado: str) -> None:
    validar_id(id_proveedor, "ID del proveedor")
    insertar_proveedor(ruc, nombre, descripcion_estado)  # Reutiliza validaciones
    proveedor_model.actualizar_proveedor(id_proveedor, ruc, nombre, descripcion_estado)

def eliminar_proveedor(id_proveedor: int) -> None:
    validar_id(id_proveedor, "ID del proveedor")
    proveedor_model.eliminar_proveedor(id_proveedor)

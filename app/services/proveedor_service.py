import re
from typing import List, Dict, Any
import app.models.proveedor as proveedor_model
from app.services.validaciones import validar_descripcion, validar_id_smallint
# Validaciones

def validar_ruc(ruc: str) -> None:
    if not isinstance(ruc, str):
        raise ValueError("El RUC debe ser una cadena de texto.")
    if ruc != "" and not re.fullmatch(r"\d{11}", ruc):
        raise ValueError("El RUC debe contener exactamente 11 dígitos numéricos o no tener digitos.")

def validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")
    if len(nombre) == 0 or len(nombre) > 1500:
        raise ValueError("El nombre debe tener entre 1 y 1500 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 .,'\-&()]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

# Lógica del servicio

def mostrar_proveedores() -> List[Dict[str, Any]]:
    return proveedor_model.mostrar_proveedores()

def insertar_proveedor(ruc: str, nombre: str, descripcion_estado: str) -> None:
    validar_ruc(ruc)
    validar_nombre(nombre)
    validar_descripcion(descripcion_estado, "Descripcion estado")

    proveedor_model.insertar_proveedor(ruc, nombre, descripcion_estado)

def actualizar_proveedor(id_proveedor: int, ruc: str, nombre: str, descripcion_estado: str) -> None:
    validar_id_smallint(id_proveedor, "ID del proveedor")
    validar_ruc(ruc)
    validar_nombre(nombre)
    validar_descripcion(descripcion_estado)
    proveedor_model.actualizar_proveedor(id_proveedor, ruc, nombre, descripcion_estado)

def eliminar_proveedor(id_proveedor: int) -> None:
    validar_id_smallint(id_proveedor, "ID del proveedor")
    proveedor_model.eliminar_proveedor(id_proveedor)
"descripcion_estado"
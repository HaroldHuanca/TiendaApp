from typing import List, Dict, Any, Optional
import re
from datetime import datetime

import app.models.venta as venta_model

# Validaciones

def validar_id(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0:
        raise ValueError(f"{nombre} debe ser un número entero positivo.")

def validar_total(total: float) -> None:
    if not isinstance(total, (int, float)) or total < 0:
        raise ValueError("El total debe ser un número no negativo.")

def validar_descripcion_estado(descripcion_estado: str) -> None:
    if not isinstance(descripcion_estado, str) or not (1 <= len(descripcion_estado) <= 30):
        raise ValueError("La descripción del estado debe tener entre 1 y 30 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion_estado):
        raise ValueError("La descripción del estado contiene caracteres no permitidos.")

def validar_fecha(fecha: str) -> None:
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha debe estar en formato AAAA-MM-DD.")

# Lógica del servicio

def mostrar_ventas() -> List[Dict[str, Any]]:
    return venta_model.mostrar_ventas()

def insertar_venta(
    id_serie: int,
    id_usuario: int,
    id_cliente: int,
    descripcion_estado: str,
    fecha: str,
    total: float
) -> Optional[int]:
    validar_id(id_serie, "ID de serie")
    validar_id(id_usuario, "ID de usuario")
    validar_id(id_cliente, "ID de cliente")
    validar_descripcion_estado(descripcion_estado)
    validar_fecha(fecha)
    validar_total(total)

    return venta_model.insertar_venta(
        id_serie, id_usuario, id_cliente, descripcion_estado, fecha, total
    )

def actualizar_venta(
    id: int,
    id_cliente: int,
    descripcion_estado: str,
    total: float
) -> None:
    validar_id(id, "ID de venta")
    validar_id(id_cliente, "ID de cliente")
    validar_descripcion_estado(descripcion_estado)
    validar_total(total)

    venta_model.actualizar_venta(
        id, id_cliente, descripcion_estado, total
    )

def eliminar_venta(id: int) -> None:
    validar_id(id, "ID de venta")
    venta_model.eliminar_venta(id)

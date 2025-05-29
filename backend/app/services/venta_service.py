from typing import List, Dict, Any, Optional
import re
from datetime import datetime

import app.models.venta as venta_model
from app.services.validaciones import validar_descripcion,validar_id_mediumint,validar_id_smallint,validar_id_tinyint

# Validaciones

def validar_total(total: float) -> None:
    if not isinstance(total, (int, float)) or total < 0:
        raise ValueError("El total debe ser un número no negativo.")

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
    validar_id_tinyint(id_serie, "ID de serie")
    validar_id_tinyint(id_usuario, "ID de usuario")
    validar_id_smallint(id_cliente, "ID de cliente")
    validar_descripcion(descripcion_estado, "Descripcion Estado")
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
    validar_id_mediumint(id, "ID de venta")
    validar_id_smallint(id_cliente, "ID de cliente")
    validar_descripcion(descripcion_estado,"Descripcion Estado")
    validar_total(total)

    venta_model.actualizar_venta(
        id, id_cliente, descripcion_estado, total
    )

def eliminar_venta(id: int) -> None:
    validar_id_mediumint(id, "ID de venta")
    venta_model.eliminar_venta(id)

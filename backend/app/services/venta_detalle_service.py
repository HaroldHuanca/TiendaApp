from typing import List, Dict, Any
import app.models.venta_detalle as venta_detalle_model
import re
from app.services.validaciones import validar_descripcion, validar_id_smallint, validar_id_mediumint
# Validaciones

def validar_cantidad(cantidad: float) -> None:
    if not isinstance(cantidad, (int, float)) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un número positivo.")

def validar_precio(precio: float) -> None:
    if not isinstance(precio, (int, float)) or precio < 0:
        raise ValueError("El precio de venta debe ser un número no negativo.")

def validar_descuento(descuento: float) -> None:
    if not isinstance(descuento, (int, float)) or descuento <= 0:
        raise ValueError("El descuento debe ser un numero positivo.")

# Lógica del servicio

def mostrar_detalles_venta(id_venta: int) -> List[Dict[str, Any]]:
    validar_id_mediumint(id_venta, "ID de venta")
    return venta_detalle_model.mostrar_detalles_venta(id_venta)

def insertar_detalle_venta(
    id_venta: int,
    id_producto: int,
    cantidad: float,
    precio_venta: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    validar_id_mediumint(id_venta, "ID de venta")
    validar_id_smallint(id_producto, "ID de producto")
    validar_cantidad(cantidad)
    validar_precio(precio_venta)
    validar_descuento(descuento)
    validar_descripcion(descripcion_estado, "Descripcion Estado")

    venta_detalle_model.insertar_detalle_venta(
        id_venta, id_producto, cantidad, precio_venta, descuento, descripcion_estado
    )

def actualizar_detalle_venta(
    id_venta: int,
    id_producto: int,
    cantidad: float,
    precio_venta: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    # Reutilizamos las validaciones
    insertar_detalle_venta(id_venta, id_producto, cantidad, precio_venta, descuento, descripcion_estado)
    venta_detalle_model.actualizar_detalle_venta(
        id_venta, id_producto, cantidad, precio_venta, descuento, descripcion_estado
    )

def eliminar_detalle_venta(id_venta: int, id_producto: int) -> None:
    validar_id_mediumint(id_venta, "ID de venta")
    validar_id_smallint(id_producto, "ID de producto")
    venta_detalle_model.eliminar_detalle_venta(id_venta, id_producto)

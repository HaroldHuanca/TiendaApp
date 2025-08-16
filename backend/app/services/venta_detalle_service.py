from typing import List, Dict, Any
import app.models.venta_detalle as venta_detalle_model
from app.services.validaciones import validar_descripcion, validar_id_smallint, validar_id_mediumint, validar_cantidad, validar_descuento, validar_precio

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

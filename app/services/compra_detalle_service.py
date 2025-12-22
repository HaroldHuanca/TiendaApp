from typing import List, Dict, Any
import app.models.compra_detalle as compra_detalle_model
from app.services.validaciones import validar_descripcion, validar_id_smallint, validar_id_mediumint, validar_cantidad, validar_descuento, validar_precio

# Lógica del servicio

def mostrar_detalles_venta(id_compra: int) -> List[Dict[str, Any]]:
    validar_id_mediumint(id_compra, "ID compra")
    return compra_detalle_model.mostrar_detalles_compra(id_compra)

def insertar_detalle_compra(
    id_compra: int,
    id_producto: int,
    cantidad: float,
    precio_compra: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    validar_id_mediumint(id_compra, "ID de Compra")
    validar_id_smallint(id_producto, "ID Producto")
    validar_cantidad(cantidad)
    validar_precio(precio_compra)
    validar_descuento(descuento)
    validar_descripcion(descripcion_estado, "Descripcion Estado")
    
    compra_detalle_model.insertar_detalle_compra(
        id_compra, id_producto, cantidad, precio_compra, descuento, descripcion_estado
    )

# Actualizar un detalle de compra
def actualizar_detalle_compra(
    id_compra: int,
    id_producto: int,
    cantidad: float,
    precio_compra: float,
    descuento: float,
    descripcion_estado: str
) -> None:
    validar_id_mediumint(id_compra, "ID de Compra")
    validar_id_smallint(id_producto, "ID Producto")
    validar_cantidad(cantidad)
    validar_precio(precio_compra)
    validar_descuento(descuento)
    validar_descripcion(descripcion_estado, "Descripcion Estado")
    
    compra_detalle_model.actualizar_detalle_compra(
        id_compra, id_producto, cantidad, precio_compra, descuento, descripcion_estado
    )
    
def eliminar_detalle_compra(id_compra: int, id_producto: int) -> None:
    validar_id_mediumint(id_compra, "ID de Compra")
    validar_id_smallint(id_producto, "ID de Producto")
    compra_detalle_model.eliminar_detalle_compra(id_compra, id_producto)

def obtener_detalles_con_productos(id_compra: int) -> List[Dict[str, Any]]:
    validar_id_mediumint(id_compra, "ID de compra")
    return compra_detalle_model.obtener_detalles_con_productos(id_compra)

    


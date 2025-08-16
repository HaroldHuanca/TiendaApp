from typing import List, Dict, Any
import app.models.venta_individual as venta_individual_model
from app.services.validaciones import validar_id_mediumint, validar_id_smallint, validar_id_tinyint, validar_precio, validar_cantidad, validar_fecha, validar_fecha_hora

#Lógica del servicio

def mostrar_ventas_individuales(fecha: str) -> List[Dict[str, Any]]:
    validar_fecha(fecha)
    return venta_individual_model.mostrar_ventas_individuales(fecha)

def insertar_venta_individual(
    id_producto: int,
    id_usuario: int,
    cantidad: float,
    precio_venta: float,
    fecha_hora: str
) -> None:
    validar_id_smallint(id_producto,"ID del producto")
    validar_id_tinyint(id_usuario, "ID del usuario")
    validar_cantidad(cantidad)
    validar_precio(precio_venta)
    validar_fecha_hora(fecha_hora)
    venta_individual_model.insertar_venta_individual(
        id_producto, id_usuario, cantidad, precio_venta, fecha_hora
    )
    
    
def actualizar_venta_individual(
    id: int,
    id_producto: int,
    id_usuario: int,
    cantidad: float,
    precio_venta: float,
    fecha_hora: str
) -> None:
    validar_id_mediumint(id, "ID de la Venta Individual")
    validar_id_smallint(id_producto,"ID del producto")
    validar_id_tinyint(id_usuario, "ID del usuario")
    validar_cantidad(cantidad)
    validar_precio(precio_venta)
    validar_fecha_hora(fecha_hora)
    venta_individual_model.actualizar_venta_individual(
        id, id_producto, id_usuario, cantidad, precio_venta, fecha_hora
    )
    
def eliminar_venta_individual(id: int) -> None:
    validar_id_mediumint(id, "ID de la Venta Individual")
    venta_individual_model.eliminar_venta_individual(id)
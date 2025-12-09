from typing import Optional, List, Dict, Any
from datetime import datetime

import app.models.compra as compra_model
from app.services.validaciones import validar_descripcion, validar_id_mediumint, validar_id_smallint, validar_id_tinyint, validar_fecha_hora, validar_total

#Lógica del servicio

def mostrar_compras() -> List[Dict[str,Any]]:
    return compra_model.mostrar_compras()

def insertar_compra(
    id_usuario: int,
    id_proveedor: int,
    descripcion_estado: str,
    fecha_hora: str,
    total: float
) -> Optional[int]:
    validar_id_tinyint(id_usuario, "ID de usuario")
    validar_id_smallint(id_proveedor, "ID de proveedor")
    validar_descripcion(descripcion_estado,"Descripcion Estado")
    validar_fecha_hora(fecha_hora)
    validar_total(total)
    
    return compra_model.insertar_compra(
        id_usuario,id_proveedor, descripcion_estado, fecha_hora, total
    )

def actualizar_compra(
    id: int,
    id_proveedor: int,
    descripcion_estado: str,
    total: float
) -> None:
    validar_id_mediumint(id,"ID de la compra")
    validar_id_smallint(id_proveedor,"ID del proveedor")
    validar_descripcion(descripcion_estado,"Descripcion Estado")
    validar_total(total)
    compra_model.actualizar_compra(
        id,id_proveedor, descripcion_estado, total
    )
    
def eliminar_compra(id: int) -> None:
    validar_id_mediumint(id,"ID de compra")
    compra_model.eliminar_compra(id)
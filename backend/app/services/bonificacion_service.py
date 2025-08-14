from typing import List, Dict, Any, Optional
import re

import app.models.bonificacion as bon
from app.services.validaciones import validar_id_mediumint,validar_id_smallint

#Mostrar bonificaciones por id de compra
def mostrar_bonificaciones(id_compra:int) -> List[Dict[str, Any]]:
    validar_id_mediumint(id_compra)
    return bon.mostrar_bonificaciones(id_compra)

#Insertar una bonificación
def insertar_bonificacion(id_compra:int, id_producto:int, cantidad :float) -> None:
    validar_id_mediumint(id_compra)
    validar_id_smallint(id_producto)
    bon.insertar_bonificacion(id_compra, id_producto, cantidad)
    
#Actualizar bonificación
def actualizar_bonificacion(
    id_compra: int,
    id_producto: int,
    cantidad: float
) -> Optional[str]:
    validar_id_mediumint(id_compra)
    validar_id_smallint(id_producto)
    return bon.actualizar_bonificacion(id_compra, id_producto, cantidad)
    
#Eliminar bonificación
def eliminar_bonificacion(id_compra: int, id_producto: int) -> Optional[str]:
    validar_id_mediumint(id_compra)
    validar_id_smallint(id_producto)
    return bon.eliminar_bonificacion(id_compra, id_producto)
    
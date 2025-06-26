from typing import List, Dict, Any
import re

import app.models.producto as producto_model
from app.services.validaciones import validar_descripcion, validar_id_smallint

# Validaciones

def validar_codigo_barras(codigo_barras: str) -> None:
    if not isinstance(codigo_barras, str):
        raise ValueError("El código de barras debe ser una cadena de texto.")
    if len(codigo_barras) == 0 or len(codigo_barras) > 13:
        raise ValueError("El código de barras debe tener entre 1 y 13 caracteres.")
    if not re.fullmatch(r"[a-zA-Z0-9\-]+", codigo_barras):
        raise ValueError("El código de barras contiene caracteres no permitidos.")

def validar_precios(valor1: float, campo1: str,valor2: float, campo2: str) -> None:
    if not isinstance(valor1, (float, int)) or valor1 < 0:
        raise ValueError(f"{campo1} debe ser un número positivo.")
    if not isinstance(valor2, (float, int)) or valor2 < 0:
        raise ValueError(f"{campo2} debe ser un número positivo.")
    if valor1 >= valor2:
        raise ValueError(f"El {campo1} debe ser menor al {campo2}")
    
def validar_stock(valor: float, campo: str) -> None:
    if not isinstance(valor, (float, int)) or valor < 0:
        raise ValueError(f"{campo} debe ser un número positivo.")

# Lógica del servicio

def obtener_productos_actualizados(tiempo_actualizacion: str) -> List[Dict[str, Any]]:
    # No se valida 'tiempo_actualizacion' aquí, asumiendo formato correcto desde la fuente (ej. ISO8601)
    return producto_model.obtener_productos_actualizados(tiempo_actualizacion)

def insertar_producto(
    codigo_barras: str,
    nombre_unidad: str,
    nombre_categoria: str,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    validar_codigo_barras(codigo_barras)
    validar_descripcion(nombre_categoria, "Categoria")
    validar_descripcion(nombre_unidad, "Unidad")
    validar_descripcion(descripcion, "Producto")
    validar_precios(precio_compra, "Precio de compra",precio_venta, "Precio de venta")
    validar_stock(stock, "Stock")
    validar_stock(stock_minimo, "Stock mínimo")
    validar_descripcion(descripcion_estado, "Estado")

    producto_model.insertar_producto(
        codigo_barras, nombre_unidad, nombre_categoria, descripcion,
        precio_compra, precio_venta, stock, stock_minimo, descripcion_estado
    )

def actualizar_producto(
    id_producto: int,
    codigo_barras: str,
    nombre_unidad: str,
    nombre_categoria: str,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    validar_id_smallint(id_producto,"ID Producto")
    validar_descripcion(nombre_categoria, "Categoria")
    validar_descripcion(nombre_unidad, "Unidad")
    validar_descripcion(descripcion, "DProducto")
    validar_precios(precio_compra, "Precio de compra", precio_venta, "Precio de venta")
    validar_stock(stock, "Stock")
    validar_stock(stock_minimo, "Stock mínimo")
    validar_descripcion(descripcion_estado,"Estado")
    producto_model.actualizar_producto(
        id_producto, codigo_barras, nombre_unidad, nombre_categoria, descripcion,
        precio_compra, precio_venta, stock, stock_minimo, descripcion_estado
    )

def eliminar_producto(id_producto: int) -> None:
    validar_id_smallint(id_producto, "ID de producto")
    producto_model.eliminar_producto(id_producto)

def buscar_id_por_codigo_barras(codigo_barras: str) -> int:
    validar_codigo_barras(codigo_barras)
    return producto_model.buscar_id_por_codigo_barras(codigo_barras)

def mostrar_productos_paginado(limit: int, offset: int) -> List[Dict[str, Any]]:
    return producto_model.mostrar_productos_paginado(limit, offset)

def obtener_conteo_productos() -> int:
    return producto_model.obtener_conteo_productos()

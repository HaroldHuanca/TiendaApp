from typing import List, Dict, Any
import re

import app.models.producto as producto_model

# Validaciones

def validar_id(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0:
        raise ValueError(f"{nombre} debe ser un número entero positivo.")

def validar_codigo_barras(codigo_barras: str) -> None:
    if not isinstance(codigo_barras, str):
        raise ValueError("El código de barras debe ser una cadena de texto.")
    if len(codigo_barras) == 0 or len(codigo_barras) > 30:
        raise ValueError("El código de barras debe tener entre 1 y 30 caracteres.")
    if not re.fullmatch(r"[a-zA-Z0-9\-]+", codigo_barras):
        raise ValueError("El código de barras contiene caracteres no permitidos.")

def validar_descripcion(descripcion: str) -> None:
    if not isinstance(descripcion, str):
        raise ValueError("La descripción debe ser una cadena de texto.")
    if len(descripcion) == 0 or len(descripcion) > 100:
        raise ValueError("La descripción debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ.,\-_/()]+", descripcion):
        raise ValueError("La descripción contiene caracteres no permitidos.")

def validar_precio(valor: float, campo: str) -> None:
    if not isinstance(valor, (float, int)) or valor < 0:
        raise ValueError(f"{campo} debe ser un número positivo.")

def validar_stock(valor: float, campo: str) -> None:
    if not isinstance(valor, (float, int)) or valor < 0:
        raise ValueError(f"{campo} debe ser un número positivo.")

def validar_descripcion_estado(descripcion_estado: str) -> None:
    if not isinstance(descripcion_estado, str):
        raise ValueError("La descripción del estado debe ser una cadena de texto.")
    if len(descripcion_estado) == 0 or len(descripcion_estado) > 30:
        raise ValueError("La descripción del estado debe tener entre 1 y 30 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion_estado):
        raise ValueError("La descripción del estado contiene caracteres no permitidos.")

# Lógica del servicio

def obtener_productos_actualizados(tiempo_actualizacion: str) -> List[Dict[str, Any]]:
    # No se valida 'tiempo_actualizacion' aquí, asumiendo formato correcto desde la fuente (ej. ISO8601)
    return producto_model.obtener_productos_actualizados(tiempo_actualizacion)

def insertar_producto(
    codigo_barras: str,
    id_unidad: int,
    id_categoria: int,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    validar_codigo_barras(codigo_barras)
    validar_id(id_unidad, "ID de unidad")
    validar_id(id_categoria, "ID de categoría")
    validar_descripcion(descripcion)
    validar_precio(precio_compra, "Precio de compra")
    validar_precio(precio_venta, "Precio de venta")
    validar_stock(stock, "Stock")
    validar_stock(stock_minimo, "Stock mínimo")
    validar_descripcion_estado(descripcion_estado)

    producto_model.insertar_producto(
        codigo_barras, id_unidad, id_categoria, descripcion,
        precio_compra, precio_venta, stock, stock_minimo, descripcion_estado
    )

def actualizar_producto(
    id_producto: int,
    codigo_barras: str,
    id_unidad: int,
    id_categoria: int,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    validar_id(id_producto, "ID de producto")
    insertar_producto(
        codigo_barras, id_unidad, id_categoria, descripcion,
        precio_compra, precio_venta, stock, stock_minimo, descripcion_estado
    )  # Reutiliza la validación
    producto_model.actualizar_producto(
        id_producto, codigo_barras, id_unidad, id_categoria, descripcion,
        precio_compra, precio_venta, stock, stock_minimo, descripcion_estado
    )

def eliminar_producto(id_producto: int) -> None:
    validar_id(id_producto, "ID de producto")
    producto_model.eliminar_producto(id_producto)

def buscar_id_por_codigo_barras(codigo_barras: str) -> int:
    validar_codigo_barras(codigo_barras)
    return producto_model.buscar_id_por_codigo_barras(codigo_barras)

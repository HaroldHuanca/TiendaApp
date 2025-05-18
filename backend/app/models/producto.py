from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.database import DatabaseManager

# ✅ Obtener productos actualizados desde una fecha
def obtener_productos_actualizados(tiempo_actualizacion: str) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_obtener_productos_actualizados(:p_tiempo_actualizacion)"),
            {"p_tiempo_actualizacion": tiempo_actualizacion}
        )
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar un nuevo producto
def insertar_producto(
    codigo_barras: str,
    p_nombre_unidad: str,
    p_nombre_categoria: str,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_Insertar_producto(
                    :p_Codigo_Barras,
                    :p_Nombre_Unidad,
                    :p_Nombre_Categoria,
                    :p_Descripcion,
                    :p_Precio_Compra,
                    :p_Precio_Venta,
                    :p_Stock,
                    :p_Stock_Minimo,
                    :p_descripcion_estado
                )
            """),
            {
                "p_Codigo_Barras": codigo_barras,
                "p_Nombre_Unidad": p_nombre_unidad,
                "p_Nombre_Categoria": p_nombre_categoria,
                "p_Descripcion": descripcion,
                "p_Precio_Compra": precio_compra,
                "p_Precio_Venta": precio_venta,
                "p_Stock": stock,
                "p_Stock_Minimo": stock_minimo,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Actualizar un producto existente
def actualizar_producto(
    id_producto: int,
    codigo_barras: str,
    p_nombre_unidad: int,
    p_nombre_categoria: int,
    descripcion: str,
    precio_compra: float,
    precio_venta: float,
    stock: float,
    stock_minimo: float,
    descripcion_estado: str
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_Actualizar_producto(
                    :p_id,
                    :p_Codigo_Barras,
                    :p_Nombre_Unidad,
                    :p_Nombre_Categoria,
                    :p_Descripcion,
                    :p_Precio_Compra,
                    :p_Precio_Venta,
                    :p_Stock,
                    :p_Stock_Minimo,
                    :p_descripcion_estado
                )
            """),
            {
                "p_id": id_producto,
                "p_Codigo_Barras": codigo_barras,
                "p_Nombre_Unidad": p_nombre_unidad,
                "p_Nombre_Categoria": p_nombre_categoria,
                "p_Descripcion": descripcion,
                "p_Precio_Compra": precio_compra,
                "p_Precio_Venta": precio_venta,
                "p_Stock": stock,
                "p_Stock_Minimo": stock_minimo,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Eliminar (alternar estado) de un producto
def eliminar_producto(id_producto: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_producto(:p_id)"),
            {"p_id": id_producto}
        )
        db.commit()

# ✅ Buscar producto por código de barras y obtener su ID
def buscar_id_por_codigo_barras(codigo_barras: str) -> int:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_buscar_codigo_barras(:p_codigo_barras, @p_id)"),
            {"p_codigo_barras": codigo_barras}
        )
        # Obtener el valor del parámetro OUT
        result = db.execute(text("SELECT @p_id"))
        id_encontrado = result.scalar()
        return id_encontrado if id_encontrado is not None else 0

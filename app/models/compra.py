from sqlalchemy import text
from typing import Optional, List, Dict, Any
from database.connection import DatabaseManager

# Mostrar todas las compras
def mostrar_compras() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_compras()"))
        return [dict(row._mapping) for row in result.fetchall()]

# Insertar una compra (retorna el ID generado)
def insertar_compra(
    id_usuario: int,
    id_proveedor: int,
    descripcion_estado: str,
    fecha_hora: str,
    total: float
) -> Optional[int]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection  # conexión real de MariaDB
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_insertar_compra", [
                id_usuario,
                id_proveedor,
                descripcion_estado,
                fecha_hora,
                total
            ])

            # Recorremos todos los resultsets hasta encontrar el resultado del SELECT
            while True:
                result = cursor.fetchall()
                if result:
                    return result[0][0]  # ID de la compra insertada
                if not cursor.nextset():
                    break

        finally:
            cursor.close()
            raw_connection.commit()

# Actualizar una compra
def actualizar_compra(
    id: int,
    id_proveedor: int,
    descripcion_estado: str,
    total: float
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_compra(
                    :p_id,
                    :p_id_proveedor,
                    :p_descripcion_estado,
                    :p_total
                )
            """),
            {
                "p_id": id,
                "p_id_proveedor": id_proveedor,
                "p_descripcion_estado": descripcion_estado,
                "p_total": total
            }
        )
        db.commit()

# Eliminar (anular) una compra
def eliminar_compra(id: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_compra(:p_id)"),
            {"p_id": id}
        )
        db.commit()

# Filtrar compras (para la lista con nombres)
def filtrar_compras(filtro_nombre: str = None, fecha_desde: str = None, fecha_hasta: str = None) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_filtrar_compras(:p_filtro_nombre, :p_fecha_desde, :p_fecha_hasta)"),
            {
                "p_filtro_nombre": filtro_nombre,
                "p_fecha_desde": fecha_desde,
                "p_fecha_hasta": fecha_hasta
            }
        )
        return [dict(row._mapping) for row in result.fetchall()]

# Obtener cabecera de compra por ID
def obtener_compra_por_id(id_compra: int) -> Optional[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_obtener_compra_por_id(:p_id_compra)"),
            {"p_id_compra": id_compra}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
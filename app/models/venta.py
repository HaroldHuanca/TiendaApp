from sqlalchemy import text
from typing import Optional, List, Dict, Any
from database.connection import DatabaseManager

# ✅ Mostrar todas las ventas
def mostrar_ventas() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_ventas()"))
        return [dict(row._mapping) for row in result.fetchall()]

# ✅ Insertar una venta (retorna el ID generado)
def insertar_venta(id_serie: int, id_usuario: int, id_cliente: int, descripcion_estado: str, fecha: str, total: float) -> Optional[int]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection  # conexión real de MariaDB
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_insertar_venta", [
                id_serie,
                id_usuario,
                id_cliente,
                descripcion_estado,
                fecha,
                total
            ])

            v_id = None
            # Recorremos todos los resultsets hasta agotar la respuesta del procedimiento
            while True:
                if cursor.description:
                    results = cursor.fetchall()
                    if results and v_id is None:
                        v_id = results[0][0]  # Capturamos el ID si se encuentra
                if not cursor.nextset():
                    break
            return v_id

        finally:
            cursor.close()
            raw_connection.commit()
# ✅ Actualizar una venta
def actualizar_venta(
    id: int,
    id_cliente: int,
    descripcion_estado: str,
    total: float
) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("""
                CALL proc_actualizar_venta(
                    :p_id,
                    :p_id_cliente,
                    :p_descripcion_estado,
                    :p_total
                )
            """),
            {
                "p_id": id,
                "p_id_cliente": id_cliente,
                "p_descripcion_estado": descripcion_estado,
                "p_total": total
            }
        )
        db.commit()

# ✅ Filtrar ventas por nombre (usuario/cliente) y rango de fechas
def filtrar_ventas(filtro_nombre: Optional[str], fecha_desde: Optional[str], fecha_hasta: Optional[str]) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_filtrar_ventas", [filtro_nombre, fecha_desde, fecha_hasta])
            ventas = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    for row in results:
                        ventas.append(dict(zip(columns, row)))
                if not cursor.nextset():
                    break
            return ventas
        finally:
            cursor.close()

# ✅ Obtener cabecera de venta por ID con nombres
def obtener_venta_por_id(id_venta: int) -> Optional[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_obtener_venta_por_id", [id_venta])
            venta = None
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    if results and venta is None:
                        venta = dict(zip(columns, results[0]))
                if not cursor.nextset():
                    break
            return venta
        finally:
            cursor.close()

# ✅ Eliminar (anular) una venta
def eliminar_venta(id: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_venta(:p_id)"),
            {"p_id": id}
        )
        db.commit()
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from database.connection import DatabaseManager

# Mostrar todas las compras
def mostrar_compras() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_mostrar_compras")
            compras = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    for row in results:
                        compras.append(dict(zip(columns, row)))
                if not cursor.nextset():
                    break
            return compras
        finally:
            cursor.close()

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
        raw_connection = connection.connection
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_insertar_compra", [
                id_usuario,
                id_proveedor,
                descripcion_estado,
                fecha_hora,
                total
            ])

            id_compra = None
            while True:
                if cursor.description:
                    results = cursor.fetchall()
                    if results and id_compra is None:
                        id_compra = results[0][0]
                if not cursor.nextset():
                    break
            return id_compra

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
            text("CALL proc_actualizar_compra(:p_id, :p_id_proveedor, :p_descripcion_estado, :p_total)"),
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
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_filtrar_compras", [filtro_nombre, fecha_desde, fecha_hasta])
            compras = []
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    for row in results:
                        compras.append(dict(zip(columns, row)))
                if not cursor.nextset():
                    break
            return compras
        finally:
            cursor.close()

# Obtener cabecera de compra por ID
def obtener_compra_por_id(id_compra: int) -> Optional[Dict[str, Any]]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()
        try:
            cursor.callproc("proc_obtener_compra_por_id", [id_compra])
            compra = None
            while True:
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    if results and compra is None:
                        compra = dict(zip(columns, results[0]))
                if not cursor.nextset():
                    break
            return compra
        finally:
            cursor.close()
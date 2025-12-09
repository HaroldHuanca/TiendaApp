from sqlalchemy import text
from typing import List, Dict, Any, Optional
from database.connection import DatabaseManager

# Mostrar bonificaciones de una compra
def mostrar_bonificaciones(id_compra: int) -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_mostrar_bonificaciones(:p_id_compra)"),
            {"p_id_compra": id_compra}
        )
        return [dict(row._mapping) for row in result.fetchall()]

# Insertar una bonificación
def insertar_bonificacion(
    id_compra: int,
    id_producto: int,
    cantidad: float
) -> Optional[str]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_insertar_bonificacion", [
                id_compra,
                id_producto,
                cantidad
            ])

            # Obtener el mensaje de retorno
            while True:
                result = cursor.fetchall()
                if result:
                    return result[0][0]  # Mensaje del procedimiento
                if not cursor.nextset():
                    break
            return None

        finally:
            cursor.close()
            raw_connection.commit()

# Actualizar una bonificación
def actualizar_bonificacion(
    id_compra: int,
    id_producto: int,
    cantidad: float
) -> Optional[str]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_actualizar_bonificacion", [
                id_compra,
                id_producto,
                cantidad
            ])

            # Obtener el mensaje de retorno
            while True:
                result = cursor.fetchall()
                if result:
                    return result[0][0]  # Mensaje del procedimiento
                if not cursor.nextset():
                    break
            return None

        finally:
            cursor.close()
            raw_connection.commit()

# Eliminar una bonificación
def eliminar_bonificacion(
    id_compra: int,
    id_producto: int
) -> Optional[str]:
    with DatabaseManager() as db:
        connection = db.connection()
        raw_connection = connection.connection
        cursor = raw_connection.cursor()

        try:
            cursor.callproc("proc_eliminar_bonificacion", [
                id_compra,
                id_producto
            ])

            # Obtener el mensaje de retorno
            while True:
                result = cursor.fetchall()
                if result:
                    return result[0][0]  # Mensaje del procedimiento
                if not cursor.nextset():
                    break
            return None

        finally:
            cursor.close()
            raw_connection.commit()
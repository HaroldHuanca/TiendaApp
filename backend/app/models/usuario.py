from sqlalchemy import text
from typing import Optional, List, Dict, Any, Tuple
from app.database import DatabaseManager

# ✅ Obtener contraseña y estado
def obtener_contrasena(nombre_usuario: str) -> Optional[Tuple]:
    with DatabaseManager() as db:
        result = db.execute(
            text("CALL proc_obtener_contrasena(:p_nombre_usuario)"),
            {"p_nombre_usuario": nombre_usuario}
        )
        return result.fetchone()

# ✅ Reducir intentos
def reducir_intento(nombre_usuario: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_reducir_intento(:p_nombre_usuario)"),
            {"p_nombre_usuario": nombre_usuario}
        )
        db.commit()

# ✅ Restablecer intentos
def restablecer_intento(nombre_usuario: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_Restablecer_Intento(:p_nombre_usuario)"),
            {"p_nombre_usuario": nombre_usuario}
        )
        db.commit()

# ✅ Insertar usuario
def insertar_usuario(nombre_usuario: str, contrasena: str, correo: str, direccion_mac: str, descripcion_estado: str) -> Optional[int]:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_insertar_usuario(:p_nombre_usuario, :p_contrasena, :p_correo, :p_direccion_mac, :p_descripcion_estado, @p_id)"),
            {
                "p_nombre_usuario": nombre_usuario,
                "p_contrasena": contrasena,
                "p_correo": correo,
                "p_direccion_mac": direccion_mac,
                "p_descripcion_estado": descripcion_estado
            }
        )
        result = db.execute(text("SELECT @p_id"))
        return result.scalar()

# ✅ Actualizar usuario
def actualizar_usuario(id: int, nombre_usuario: str, contrasena: str, descripcion_estado: str) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_actualizar_usuario(:p_id, :p_nombre_usuario, :p_contrasena, :p_descripcion_estado)"),
            {
                "p_id": id,
                "p_nombre_usuario": nombre_usuario,
                "p_contrasena": contrasena,
                "p_descripcion_estado": descripcion_estado
            }
        )
        db.commit()

# ✅ Eliminar usuario (cambia el estado)
def eliminar_usuario(id: int) -> None:
    with DatabaseManager() as db:
        db.execute(
            text("CALL proc_eliminar_usuario(:p_id)"),
            {"p_id": id}
        )
        db.commit()

# ✅ Mostrar todos los usuarios
def mostrar_usuarios() -> List[Dict[str, Any]]:
    with DatabaseManager() as db:
        result = db.execute(text("CALL proc_mostrar_usuario()"))
        rows = result.fetchall()
        return [dict(row) for row in rows]

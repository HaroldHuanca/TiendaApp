import re
from typing import List, Dict, Any, Optional
import app.models.usuario as usuario_model

# Validaciones

def validar_id(id_: int, nombre: str = "ID") -> None:
    if not isinstance(id_, int) or id_ <= 0 > 255:
        raise ValueError(f"{nombre} debe ser un número entero positivo menor a 255.")

def validar_nombre_usuario(nombre_usuario: str) -> None:
    if not isinstance(nombre_usuario, str) or not (5 <= len(nombre_usuario) <= 50):
        raise ValueError("El nombre de usuario debe tener entre 5 y 50 caracteres.")
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", nombre_usuario):
        raise ValueError("El nombre de usuario contiene caracteres no válidos.")

def validar_contrasena(contrasena: str) -> None:
    if len(contrasena) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")

def validar_correo(correo: str) -> None:
    if not re.fullmatch(r"([^@]+@[^@]+\.[^@]+)?", correo):
        raise ValueError("El correo electrónico no es válido.")

def validar_mac(mac: str) -> None:
    if not re.fullmatch(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", mac):
        raise ValueError("La dirección MAC no es válida.")

def validar_descripcion_estado(descripcion_estado: str) -> None:
    if len(descripcion_estado) == 0 or len(descripcion_estado) > 100:
        raise ValueError("La descripción del estado debe tener entre 1 y 100 caracteres.")
    if not re.fullmatch(r"[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ ]+", descripcion_estado):
        raise ValueError("La descripción del estado contiene caracteres no permitidos.")

# Lógica del servicio

def mostrar_usuarios() -> List[Dict[str, Any]]:
    return usuario_model.mostrar_usuarios()

def obtener_contrasena(nombre_usuario: str) -> Optional[tuple]:
    validar_nombre_usuario(nombre_usuario)
    return usuario_model.obtener_contrasena(nombre_usuario)

def reducir_intento(nombre_usuario: str) -> None:
    validar_nombre_usuario(nombre_usuario)
    usuario_model.reducir_intento(nombre_usuario)

def restablecer_intento(nombre_usuario: str) -> None:
    validar_nombre_usuario(nombre_usuario)
    usuario_model.restablecer_intento(nombre_usuario)

def insertar_usuario(nombre_usuario: str, contrasena: str, correo: str, direccion_mac: str, descripcion_estado: str) -> Optional[int]:
    validar_nombre_usuario(nombre_usuario)
    validar_contrasena(contrasena)
    validar_correo(correo)
    validar_mac(direccion_mac)
    validar_descripcion_estado(descripcion_estado)
    
    return usuario_model.insertar_usuario(nombre_usuario, contrasena, correo, direccion_mac, descripcion_estado)

def actualizar_usuario(id_usuario: int, nombre_usuario: str, contrasena: str, descripcion_estado: str) -> None:
    validar_id(id_usuario)
    validar_nombre_usuario(nombre_usuario)
    validar_contrasena(contrasena)
    validar_descripcion_estado(descripcion_estado) 
    usuario_model.actualizar_usuario(id_usuario, nombre_usuario, contrasena, descripcion_estado)

def eliminar_usuario(id_usuario: int) -> None:
    validar_id(id_usuario)
    usuario_model.eliminar_usuario(id_usuario)

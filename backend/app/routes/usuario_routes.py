from flask import Blueprint, request, jsonify
from app.services import usuario_service
import bcrypt

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/mostrar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = usuario_service.mostrar_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/insetar_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    try:
        id_insertado = usuario_service.insertar_usuario(
            datos.get("nombre_usuario"),
            datos.get("contrasena"),
            datos.get("correo"),
            datos.get("direccion_mac"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Usuario creado exitosamente", "id_usuario": id_insertado}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/actualizar_usuario/<int:id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    datos = request.get_json()
    try:
        usuario_service.actualizar_usuario(
            id_usuario,
            datos.get("nombre_usuario"),
            datos.get("contrasena"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/eliminar_usuario/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        usuario_service.eliminar_usuario(id_usuario)
        return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/obtener_contrasena/<string:nombre_usuario>', methods=['GET'])
def obtener_contrasena(nombre_usuario):
    try:
        resultado = usuario_service.obtener_contrasena(nombre_usuario)
        if resultado:
            return jsonify(resultado[0]), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/reducir_intento/<string:nombre_usuario>', methods=['POST'])
def reducir_intento(nombre_usuario):
    try:
        usuario_service.reducir_intento(nombre_usuario)
        return jsonify({"mensaje": "Intento reducido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/restablecer_intento/<string:nombre_usuario>', methods=['POST'])
def restablecer_intento(nombre_usuario):
    try:
        usuario_service.restablecer_intento(nombre_usuario)
        return jsonify({"mensaje": "Intentos restablecidos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route('/verificar_login', methods=['POST'])
def verificar_login():
    datos = request.get_json()
    try:
        # 1. Obtener usuario de la base de datos
        usuario = usuario_service.obtener_contrasena(datos['usuario'])[0]
        if not usuario:
            return jsonify({
                "exito": False,
                "mensaje": "Usuario no encontrado"
            }), 404
        
        # 2. Verificar contraseña con bcrypt
        if bcrypt.checkpw(datos['contrasena'].encode('utf-8'), usuario['Contrasena'].encode('utf-8')):
            # 3. Restablecer intentos si es necesario
            usuario_service.restablecer_intento(datos['usuario'])
            
            # 4. Generar nueva MAC (opcional)
            nueva_mac = generar_mac_aleatoria()
            usuario_service.actualizar_mac(datos['usuario'], nueva_mac)
            
            return jsonify({
                "exito": True,
                "mensaje": "Login exitoso",
                "id_usuario": usuario['Id'],
                "estado": usuario['Estado'],
                "MAC": nueva_mac
            })
        else:
            # Reducir intentos fallidos
            usuario_service.reducir_intento(datos['usuario'])
            
            return jsonify({
                "exito": False,
                "mensaje": "Contraseña incorrecta"
            }), 401
            
    except Exception as e:
        return jsonify({
            "exito": False,
            "mensaje": str(e)
        }), 500

def generar_mac_aleatoria():
    import random
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
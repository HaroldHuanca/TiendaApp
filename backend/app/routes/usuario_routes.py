from flask import Blueprint, request, jsonify
from app.services import usuario_service

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
            return jsonify({"contrasena": resultado[0]}), 200
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

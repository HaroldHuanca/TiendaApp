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
        # Validar input básico
        if not datos or 'usuario' not in datos or 'contrasena' not in datos:
            return jsonify({"exito": False, "mensaje": "Se requiere usuario y contraseña"}), 400

        # 1. Obtener usuario de la base de datos (proc devuelve una lista)
        resultado = usuario_service.obtener_contrasena(datos['usuario'])
        if not resultado or len(resultado) == 0:
            return jsonify({"exito": False, "mensaje": "Usuario no encontrado"}), 404

        usuario = resultado[0]

        # Helper: obtener campo sin importar mayúsculas/minúsculas
        def field_ci(obj: dict, field_name: str):
            for k, v in obj.items():
                if k.lower() == field_name.lower():
                    return v
            return None

        # 1.5. Verificar intentos disponibles ANTES de validar contraseña
        intentos = field_ci(usuario, 'intentos')
        if intentos is not None and intentos <= 0:
            return jsonify({
                "exito": False,
                "mensaje": "Ya no tiene más intentos disponibles, contacte a su administrador."
            }), 403

        # 2. Verificar contraseña con bcrypt (buscar el campo 'contrasena' de forma case-insensitive)
        stored_hash = field_ci(usuario, 'contrasena')
        if not stored_hash:
            return jsonify({"exito": False, "mensaje": "Registro de usuario inválido (hash no encontrado)"}), 500

        if bcrypt.checkpw(datos['contrasena'].encode('utf-8'), stored_hash.encode('utf-8')):
            # 3. Restablecer intentos si es necesario
            usuario_service.restablecer_intento(datos['usuario'])
            
            # Obtener id y estado de forma case-insensitive
            id_usuario = field_ci(usuario, 'id') or field_ci(usuario, 'Id')
            estado = field_ci(usuario, 'estado') or field_ci(usuario, 'Estado')

            # 4. Establecer sesión
            from flask import session
            session['usuario'] = datos['usuario']
            session['id'] = id_usuario
            session['estado'] = estado

            return jsonify({
                "exito": True,
                "mensaje": "Login exitoso",
                "id_usuario": id_usuario,
                "estado": estado
            })
        else:
            # Reducir intentos fallidos solo si tiene intentos disponibles
            if intentos is not None and intentos > 0:
                usuario_service.reducir_intento(datos['usuario'])
                intentos_restantes = intentos - 1
                
                if intentos_restantes > 0:
                    mensaje = f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos."
                else:
                    mensaje = "Contraseña incorrecta. Este fue su último intento. Contacte a su administrador."
            else:
                mensaje = "Contraseña incorrecta."
            
            return jsonify({
                "exito": False,
                "mensaje": mensaje
            }), 401
            
    except Exception as e:
        return jsonify({
            "exito": False,
            "mensaje": str(e)
        }), 500
from flask import Blueprint, request, jsonify
from app.services import estado_service

estado_bp = Blueprint('estado_bp', __name__)

@estado_bp.route('/mostrar_estados/<string:nombre_tabla>', methods=['GET'])
def obtener_estados(nombre_tabla):
    try:
        estados = estado_service.mostrar_estados(nombre_tabla)
        return jsonify(estados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@estado_bp.route('/insertar_estado/<string:nombre_tabla>', methods=['POST'])
def crear_estado(nombre_tabla):
    datos = request.get_json()
    try:
        estado = datos.get("estado")
        descripcion = datos.get("descripcion")
        if estado is None or descripcion is None:
            return jsonify({"error": "Faltan campos requeridos: 'estado' y/o 'descripcion'"}), 400
        estado_service.insertar_estado(nombre_tabla, estado, descripcion)
        return jsonify({"mensaje": "Estado creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@estado_bp.route('/actualizar_estado/<string:nombre_tabla>', methods=['PUT'])
def modificar_estado(nombre_tabla):
    datos = request.get_json()
    try:
        estado = datos.get("estado")
        descripcion = datos.get("descripcion")
        if estado is None or descripcion is None:
            return jsonify({"error": "Faltan campos requeridos: 'estado' y/o 'descripcion'"}), 400
        estado_service.actualizar_estado(nombre_tabla, estado, descripcion)
        return jsonify({"mensaje": "Estado actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

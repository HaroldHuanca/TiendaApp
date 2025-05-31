from flask import Blueprint, request, jsonify
from app.services import unidad_service

unidad_bp = Blueprint('unidad_bp', __name__)

@unidad_bp.route('/unidades', methods=['GET'])
def listar_unidades():
    try:
        unidades = unidad_service.mostrar_unidades()
        return jsonify(unidades), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unidad_bp.route('/unidades', methods=['POST'])
def crear_unidad():
    datos = request.get_json()
    try:
        unidad_service.insertar_unidad(datos.get("nombre"))
        return jsonify({"mensaje": "Unidad creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unidad_bp.route('/unidades/<int:id_unidad>', methods=['PUT'])
def modificar_unidad(id_unidad):
    datos = request.get_json()
    try:
        unidad_service.actualizar_unidad(id_unidad, datos.get("nombre"))
        return jsonify({"mensaje": "Unidad actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

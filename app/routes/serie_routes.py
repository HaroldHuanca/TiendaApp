from flask import Blueprint, request, jsonify
from app.services import serie_service

serie_bp = Blueprint('serie_bp', __name__)

@serie_bp.route('/mostrar_series', methods=['GET'])
def obtener_series():
    try:
        series = serie_service.mostrar_series()
        return jsonify(series), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@serie_bp.route('/insertar_serie', methods=['POST'])
def crear_serie():
    datos = request.get_json()
    try:
        serie_service.insertar_serie(
            datos.get("serie")
        )
        return jsonify({"mensaje": "Serie creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@serie_bp.route('/actualizar_serie/<int:id>', methods=['PUT'])
def actualizar_serie(id):
    datos = request.get_json()
    try:
        serie_service.actualizar_serie(
            id,
            datos.get("serie"),
            datos.get("contador")
        )
        return jsonify({"mensaje": "Serie actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

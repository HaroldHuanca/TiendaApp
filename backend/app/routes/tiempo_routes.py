from flask import Blueprint, jsonify
from app.services import tiempo_service

tiempo_bp = Blueprint('tiempo_bp', __name__)

@tiempo_bp.route('/fecha_actual', methods=['GET'])
def obtener_fecha_actual():
    try:
        fecha = tiempo_service.obtener_fecha_actual_formateada()
        return jsonify({"fecha":fecha}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

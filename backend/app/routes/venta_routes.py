from flask import Blueprint, request, jsonify
from app.services import venta_service

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.route('/ventas', methods=['GET'])
def obtener_ventas():
    try:
        ventas = venta_service.mostrar_ventas()
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/ventas', methods=['POST'])
def crear_venta():
    datos = request.get_json()
    try:
        id_nueva_venta = venta_service.insertar_venta(
            datos.get("id_serie"),
            datos.get("id_usuario"),
            datos.get("id_cliente"),
            datos.get("descripcion_estado"),
            datos.get("fecha"),
            datos.get("total")
        )
        return jsonify({"mensaje": "Venta registrada exitosamente", "id": id_nueva_venta}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/ventas', methods=['PUT'])
def modificar_venta():
    datos = request.get_json()
    try:
        venta_service.actualizar_venta(
            datos.get("id"),
            datos.get("id_cliente"),
            datos.get("descripcion_estado"),
            datos.get("total")
        )
        return jsonify({"mensaje": "Venta actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    try:
        venta_service.eliminar_venta(id)
        return jsonify({"mensaje": "Venta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

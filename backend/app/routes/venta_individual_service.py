from flask import Blueprint, request, jsonify
from app.services import venta_individual_service

venta_individual_bp = Blueprint('venta_individual_bp', __name__)

@venta_individual_bp.route('/mostrar_ventas_individuales/<string:fecha>', methods=['GET'])
def mostrar_ventas_individuales(fecha):
    try:
        ventas = venta_individual_service.mostrar_ventas_individuales(fecha)
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_individual_bp.route('/insertar_venta_individual', methods=['POST'])
def insertar_venta_individual():
    datos = request.get_json()
    try:
        venta_individual_service.insertar_venta_individual(
            datos.get("id_producto"),
            datos.get("id_usuario"),
            datos.get("cantidad"),
            datos.get("precio_venta"),
            datos.get("fecha_hora")
        )
        return jsonify({"mensaje": "Venta individual insertada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_individual_bp.route('/actualizar_venta_individual/<int:id>', methods=['PUT'])
def actualizar_venta_individual(id):
    datos = request.get_json()
    try:
        venta_individual_service.actualizar_venta_individual(
            id,
            datos.get("id_producto"),
            datos.get("id_usuario"),
            datos.get("cantidad"),
            datos.get("precio_venta"),
            datos.get("fecha_hora")
        )
        return jsonify({"mensaje": "Venta individual actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_individual_bp.route('/eliminar_venta_individual/<int:id>', methods=['DELETE'])
def eliminar_venta_individual(id):
    try:
        venta_individual_service.eliminar_venta_individual(id)
        return jsonify({"mensaje": "Venta individual eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
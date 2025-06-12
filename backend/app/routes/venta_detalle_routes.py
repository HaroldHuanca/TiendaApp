from flask import Blueprint, request, jsonify
from app.services import venta_detalle_service

venta_detalle_bp = Blueprint('venta_detalle_bp', __name__)

@venta_detalle_bp.route('/mostrar_venta_detalles/<int:id_venta>', methods=['GET'])
def obtener_detalles_venta(id_venta):
    try:
        detalles = venta_detalle_service.mostrar_detalles_venta(id_venta)
        return jsonify(detalles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_detalle_bp.route('/insertar_venta_detalle', methods=['POST'])
def crear_detalle_venta():
    datos = request.get_json()
    try:
        venta_detalle_service.insertar_detalle_venta(
            datos.get("id_venta"),
            datos.get("id_producto"),
            datos.get("cantidad"),
            datos.get("precio_venta"),
            datos.get("descuento"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Detalle de venta insertado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_detalle_bp.route('/actualizar_venta_detalle', methods=['PUT'])
def modificar_detalle_venta():
    datos = request.get_json()
    try:
        venta_detalle_service.actualizar_detalle_venta(
            datos.get("id_venta"),
            datos.get("id_producto"),
            datos.get("cantidad"),
            datos.get("precio_venta"),
            datos.get("descuento"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Detalle de venta actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_detalle_bp.route('/eliminar_venta_detalle/<int:id_venta>/<int:id_producto>', methods=['DELETE'])
def eliminar_detalle_venta(id_venta, id_producto):
    try:
        venta_detalle_service.eliminar_detalle_venta(id_venta, id_producto)
        return jsonify({"mensaje": "Detalle de venta eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

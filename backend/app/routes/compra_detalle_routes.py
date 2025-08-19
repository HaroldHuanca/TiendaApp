from flask import Blueprint, request, jsonify
from app.services import compra_detalle_service

compra_detalle_bp = Blueprint('compra_detalle_bp', __name__)

@compra_detalle_bp.route('/mostrar_detalles_compra/<int:id_compra>', methods=['GET'])
def mostrar_detalles_compra(id_compra):
    try:
        detalles = compra_detalle_service.mostrar_detalles_venta(id_compra)
        return jsonify(detalles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_detalle_bp.route('/insertar_detalle_compra', methods=['POST'])
def insertar_detalle_compra():
    datos = request.get_json()
    try:
        compra_detalle_service.insertar_detalle_compra(
            datos.get("id_compra"),
            datos.get("id_producto"),
            datos.get("cantidad"),
            datos.get("precio_compra"),
            datos.get("descuento"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Detalle de compra insertado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_detalle_bp.route('/actualizar_detalle_compra/<int:id_compra>/<int:id_producto>', methods=['PUT'])
def actualizar_detalle_compra(id_compra, id_producto):
    datos = request.get_json()
    try:
        compra_detalle_service.actualizar_detalle_compra(
            id_compra,
            id_producto,
            datos.get("cantidad"),
            datos.get("precio_compra"),
            datos.get("descuento"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Detalle de compra actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_detalle_bp.route('/eliminar_detalle_compra/<int:id_compra>/<int:id_producto>', methods=['DELETE'])
def eliminar_detalle_compra(id_compra, id_producto):
    try:
        compra_detalle_service.eliminar_detalle_compra(id_compra, id_producto)
        return jsonify({"mensaje": "Detalle de compra eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
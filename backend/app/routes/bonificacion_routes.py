from flask import Blueprint, request, jsonify
from app.services import bonificacion_service

bonificacion_bp = Blueprint('bonificacion_bp', __name__)

@bonificacion_bp.route('/mostrar_bonificaciones/<int:id_compra>', methods=['GET'])
def mostrar_bonificaciones(id_compra):
    try:
        bonificaciones = bonificacion_service.mostrar_bonificaciones(id_compra)
        return jsonify(bonificaciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@bonificacion_bp.route('/insertar_bonificacion', methods=['POST'])
def insertar_bonificacion():
    datos = request.get_json()
    try:
        bonificacion_service.insertar_bonificacion(
            datos.get("id_compra"),
            datos.get("id_producto"),
            datos.get("cantidad")
        )
        return jsonify({"mensaje": "Bonificacion insertada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@bonificacion_bp.route('/actualizar_bonificacion/<int:id_compra>/<int:id_producto>', methods=['PUT'])
def actualizar_bonificacion(id_compra,id_producto):
    datos = request.get_json()
    try:
        bonificacion_service.actualizar_bonificacion(
            id_compra,
            id_producto,
            datos.get("cantidad")
        )
        return jsonify({"mensaje": "Bonificacion actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@bonificacion_bp.route('/eliminar_bonificacion/<int:id_compra>/<int:id_producto>', methods=['DELETE'])
def eliminar_bonificacion(id_compra,id_producto):
    try:
        bonificacion_service.eliminar_bonificacion(id_compra,id_producto)
        return jsonify({"mensaje": "Bonificacion eliminada exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
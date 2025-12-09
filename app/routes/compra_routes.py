from flask import Blueprint, request, jsonify
from app.services import compra_service

compra_bp = Blueprint('compra_bp', __name__)

@compra_bp.route('/mostrar_compras', methods=['GET'])
def mostrar_compras():
    try:
        compras = compra_service.mostrar_compras()
        return jsonify(compras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route('/insertar_compra', methods=['POST'])
def insertar_compra():
    datos = request.get_json()
    try:
        id_compra = compra_service.insertar_compra(
            datos.get("id_usuario"),
            datos.get("id_proveedor"),
            datos.get("descripcion_estado"),
            datos.get("fecha_hora"),
            datos.get("total")
        )
        return jsonify({
            "mensaje": "Compra insertada exitosamente",
            "id_compra": id_compra
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route('/actualizar_compra/<int:id>', methods=['PUT'])
def actualizar_compra(id):
    datos = request.get_json()
    try:
        compra_service.actualizar_compra(
            id,
            datos.get("id_proveedor"),
            datos.get("descripcion_estado"),
            datos.get("total")
        )
        return jsonify({"mensaje": "Compra actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route('/eliminar_compra/<int:id>', methods=['DELETE'])
def eliminar_compra(id):
    try:
        compra_service.eliminar_compra(id)
        return jsonify({"mensaje": "Compra eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
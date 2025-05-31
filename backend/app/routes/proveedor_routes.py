from flask import Blueprint, request, jsonify
from app.services import proveedor_service

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/proveedores', methods=['GET'])
def listar_proveedores():
    try:
        proveedores = proveedor_service.mostrar_proveedores()
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@proveedor_bp.route('/proveedores', methods=['POST'])
def crear_proveedor():
    datos = request.get_json()
    try:
        proveedor_service.insertar_proveedor(
            datos.get("ruc"),
            datos.get("nombre"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Proveedor creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@proveedor_bp.route('/proveedores/<int:id_proveedor>', methods=['PUT'])
def modificar_proveedor(id_proveedor):
    datos = request.get_json()
    try:
        proveedor_service.actualizar_proveedor(
            id_proveedor,
            datos.get("ruc"),
            datos.get("nombre"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Proveedor actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@proveedor_bp.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
def borrar_proveedor(id_proveedor):
    try:
        proveedor_service.eliminar_proveedor(id_proveedor)
        return jsonify({"mensaje": "Proveedor eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

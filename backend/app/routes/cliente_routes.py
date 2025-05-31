# routes/cliente_routes.py

from flask import Blueprint, request, jsonify
from app.services import cliente_service

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = cliente_service.mostrar_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    datos = request.get_json()
    try:
        documento = datos.get("documento")
        nombre = datos.get("nombre")
        descripcion_estado = datos.get("descripcion_estado")
        cliente_service.insertar_cliente(documento, nombre, descripcion_estado)
        return jsonify({"mensaje": "Cliente creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['PUT'])
def modificar_cliente(id_cliente):
    datos = request.get_json()
    try:
        documento = datos.get("documento")
        nombre = datos.get("nombre")
        descripcion_estado = datos.get("descripcion_estado")
        cliente_service.actualizar_cliente(id_cliente, documento, nombre, descripcion_estado)
        return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def borrar_cliente(id_cliente):
    try:
        cliente_service.eliminar_cliente(id_cliente)
        return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

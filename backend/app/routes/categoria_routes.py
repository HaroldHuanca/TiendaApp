from flask import Blueprint, request, jsonify
from app.services import categoria_service

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/mostrar_categorias', methods=['GET'])
def obtener_categorias():
    try:
        categorias = categoria_service.mostrar_categorias()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@categoria_bp.route('/insertar_categoria', methods=['POST'])
def crear_categoria():
    datos = request.get_json()
    try:
        nombre = datos.get("nombre")
        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'"}), 400
        categoria_service.insertar_categoria(nombre)
        return jsonify({"mensaje": "Categoría creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@categoria_bp.route('/actualizar_categoria/<int:id>', methods=['PUT'])
def modificar_categoria(id):
    datos = request.get_json()
    try:
        nombre = datos.get("nombre")
        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'"}), 400
        categoria_service.actualizar_categoria(id, nombre)
        return jsonify({"mensaje": "Categoría actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

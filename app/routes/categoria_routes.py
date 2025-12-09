from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
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

@categoria_bp.route('/api/eliminar_categoria/<int:id_categoria>', methods=['DELETE'])
def eliminar_categoria_api(id_categoria):
    try:
        categoria_service.eliminar_categoria(id_categoria)
        return jsonify({"mensaje": "Categoría eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@categoria_bp.route('/categorias', methods=['GET'])
def categorias_lista():
    """Renderiza la página principal con la lista de categorías"""
    try:
        categorias = categoria_service.mostrar_categorias()
        return render_template('categorias_lista.html', categorias=categorias)
    except Exception as e:
        flash(f"Error al cargar categorías: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@categoria_bp.route('/categorias/crear', methods=['GET'])
def categorias_crear():
    """Renderiza el formulario de creación de categoría"""
    return render_template('categorias_crear.html')

@categoria_bp.route('/categorias/editar/<int:id_categoria>', methods=['GET'])
def categorias_editar(id_categoria):
    """Renderiza el formulario de edición de categoría"""
    try:
        categorias = categoria_service.mostrar_categorias()
        categoria = next((c for c in categorias if c.get('ID_Categoria') == id_categoria), None)
        
        if not categoria:
            flash("Categoría no encontrada", "danger")
            return redirect(url_for('categoria_bp.categorias_lista'))
        
        return render_template('categorias_editar.html', categoria=categoria)
    except Exception as e:
        flash(f"Error al cargar la categoría: {str(e)}", "danger")
        return redirect(url_for('categoria_bp.categorias_lista'))

@categoria_bp.route('/categorias/eliminados', methods=['GET'])
def categorias_eliminados():
    """Renderiza la lista de categorías eliminadas"""
    try:
        categorias = categoria_service.mostrar_categorias_eliminadas()
        return render_template('categorias_eliminados.html', categorias=categorias)
    except Exception as e:
        flash(f"Error al cargar categorías eliminadas: {str(e)}", "danger")
        return redirect(url_for('categoria_bp.categorias_lista'))

@categoria_bp.route('/categorias/restaurar/<int:id_categoria>', methods=['POST'])
def categorias_restaurar(id_categoria):
    """Restaura una categoría eliminada"""
    try:
        categoria_service.restaurar_categoria(id_categoria)
        flash("Categoría restaurada exitosamente", "success")
    except Exception as e:
        flash(f"Error al restaurar la categoría: {str(e)}", "danger")
    return redirect(url_for('categoria_bp.categorias_eliminados'))

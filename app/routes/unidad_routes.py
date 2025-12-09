from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services import unidad_service

unidad_bp = Blueprint('unidad_bp', __name__)

@unidad_bp.route('/mostrar_unidades', methods=['GET'])
def listar_unidades():
    try:
        unidades = unidad_service.mostrar_unidades()
        return jsonify(unidades), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unidad_bp.route('/insertar_unidad', methods=['POST'])
def crear_unidad():
    datos = request.get_json()
    try:
        unidad_service.insertar_unidad(datos.get("nombre"))
        return jsonify({"mensaje": "Unidad creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unidad_bp.route('/actualizar_unidad/<int:id_unidad>', methods=['PUT'])
def modificar_unidad(id_unidad):
    datos = request.get_json()
    try:
        unidad_service.actualizar_unidad(id_unidad, datos.get("nombre"))
        return jsonify({"mensaje": "Unidad actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unidad_bp.route('/api/eliminar_unidad/<int:id_unidad>', methods=['DELETE'])
def eliminar_unidad_api(id_unidad):
    try:
        unidad_service.eliminar_unidad(id_unidad)
        return jsonify({"mensaje": "Unidad eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@unidad_bp.route('/unidades', methods=['GET'])
def unidades_lista():
    """Renderiza la página principal con la lista de unidades"""
    try:
        unidades = unidad_service.mostrar_unidades()
        return render_template('unidades_lista.html', unidades=unidades)
    except Exception as e:
        flash(f"Error al cargar unidades: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@unidad_bp.route('/unidades/crear', methods=['GET'])
def unidades_crear():
    """Renderiza el formulario de creación de unidad"""
    return render_template('unidades_crear.html')

@unidad_bp.route('/unidades/editar/<int:id_unidad>', methods=['GET'])
def unidades_editar(id_unidad):
    """Renderiza el formulario de edición de unidad"""
    try:
        unidades = unidad_service.mostrar_unidades()
        unidad = next((u for u in unidades if u.get('ID_Unidad') == id_unidad), None)
        
        if not unidad:
            flash("Unidad no encontrada", "danger")
            return redirect(url_for('unidad_bp.unidades_lista'))
        
        return render_template('unidades_editar.html', unidad=unidad)
    except Exception as e:
        flash(f"Error al cargar la unidad: {str(e)}", "danger")
        return redirect(url_for('unidad_bp.unidades_lista'))

@unidad_bp.route('/unidades/eliminados', methods=['GET'])
def unidades_eliminados():
    """Renderiza la lista de unidades eliminadas"""
    try:
        unidades = unidad_service.mostrar_unidades_eliminadas()
        return render_template('unidades_eliminados.html', unidades=unidades)
    except Exception as e:
        flash(f"Error al cargar unidades eliminadas: {str(e)}", "danger")
        return redirect(url_for('unidad_bp.unidades_lista'))

@unidad_bp.route('/unidades/restaurar/<int:id_unidad>', methods=['POST'])
def unidades_restaurar(id_unidad):
    """Restaura una unidad eliminada"""
    try:
        unidad_service.restaurar_unidad(id_unidad)
        flash("Unidad restaurada exitosamente", "success")
    except Exception as e:
        flash(f"Error al restaurar la unidad: {str(e)}", "danger")
    return redirect(url_for('unidad_bp.unidades_eliminados'))

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services import proveedor_service

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/mostrar_proveedores', methods=['GET'])
def listar_proveedores():
    try:
        proveedores = proveedor_service.mostrar_proveedores()
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@proveedor_bp.route('/insertar_proveedor', methods=['POST'])
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

@proveedor_bp.route('/actualizar_proveedor/<int:id_proveedor>', methods=['PUT'])
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

@proveedor_bp.route('/eliminar_proveedor/<int:id_proveedor>', methods=['DELETE'])
def borrar_proveedor(id_proveedor):
    try:
        proveedor_service.eliminar_proveedor(id_proveedor)
        return jsonify({"mensaje": "Proveedor eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@proveedor_bp.route('/proveedores', methods=['GET'])
def proveedores_lista():
    """Renderiza la página principal con la lista de proveedores"""
    try:
        proveedores = proveedor_service.mostrar_proveedores()
        return render_template('proveedores_lista.html', proveedores=proveedores)
    except Exception as e:
        flash(f"Error al cargar proveedores: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@proveedor_bp.route('/proveedores/crear', methods=['GET'])
def proveedores_crear():
    """Renderiza el formulario de creación de proveedor"""
    return render_template('proveedores_crear.html')

@proveedor_bp.route('/proveedores/editar/<int:id_proveedor>', methods=['GET'])
def proveedores_editar(id_proveedor):
    """Renderiza el formulario de edición de proveedor"""
    try:
        proveedores = proveedor_service.mostrar_proveedores()
        proveedor = next((p for p in proveedores if p.get('ID_Proveedor') == id_proveedor), None)
        
        if not proveedor:
            flash("Proveedor no encontrado", "danger")
            return redirect(url_for('proveedor_bp.proveedores_lista'))
        
        return render_template('proveedores_editar.html', proveedor=proveedor)
    except Exception as e:
        flash(f"Error al cargar el proveedor: {str(e)}", "danger")
        return redirect(url_for('proveedor_bp.proveedores_lista'))

@proveedor_bp.route('/proveedores/eliminados', methods=['GET'])
def proveedores_eliminados():
    """Renderiza la lista de proveedores eliminados"""
    try:
        proveedores = proveedor_service.mostrar_proveedores_eliminados()
        return render_template('proveedores_eliminados.html', proveedores=proveedores)
    except Exception as e:
        flash(f"Error al cargar proveedores eliminados: {str(e)}", "danger")
        return redirect(url_for('proveedor_bp.proveedores_lista'))

@proveedor_bp.route('/proveedores/restaurar/<int:id_proveedor>', methods=['POST'])
def proveedores_restaurar(id_proveedor):
    """Restaura un proveedor eliminado"""
    try:
        proveedor_service.restaurar_proveedor(id_proveedor)
        flash("Proveedor restaurado exitosamente", "success")
    except Exception as e:
        flash(f"Error al restaurar el proveedor: {str(e)}", "danger")
    return redirect(url_for('proveedor_bp.proveedores_eliminados'))

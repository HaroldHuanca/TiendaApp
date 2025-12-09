# routes/cliente_routes.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services import cliente_service

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/mostrar_clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = cliente_service.mostrar_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/insertar_cliente', methods=['POST'])
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

@cliente_bp.route('/actualizar_cliente/<int:id_cliente>', methods=['PUT'])
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

@cliente_bp.route('/eliminar_cliente/<int:id_cliente>', methods=['DELETE'])
def borrar_cliente(id_cliente):
    try:
        cliente_service.eliminar_cliente(id_cliente)
        return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@cliente_bp.route('/clientes', methods=['GET'])
def clientes_lista():
    """Renderiza la página principal con la lista de clientes"""
    try:
        clientes = cliente_service.mostrar_clientes()
        return render_template('clientes_lista.html', clientes=clientes)
    except Exception as e:
        flash(f"Error al cargar clientes: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@cliente_bp.route('/clientes/crear', methods=['GET'])
def clientes_crear():
    """Renderiza el formulario de creación de cliente"""
    return render_template('clientes_crear.html')

@cliente_bp.route('/clientes/editar/<int:id_cliente>', methods=['GET'])
def clientes_editar(id_cliente):
    """Renderiza el formulario de edición de cliente"""
    try:
        clientes = cliente_service.mostrar_clientes()
        cliente = next((c for c in clientes if c.get('ID_Cliente') == id_cliente), None)
        
        if not cliente:
            flash("Cliente no encontrado", "danger")
            return redirect(url_for('cliente_bp.clientes_lista'))
        
        return render_template('clientes_editar.html', cliente=cliente)
    except Exception as e:
        flash(f"Error al cargar el cliente: {str(e)}", "danger")
        return redirect(url_for('cliente_bp.clientes_lista'))

@cliente_bp.route('/clientes/eliminados', methods=['GET'])
def clientes_eliminados():
    """Renderiza la lista de clientes eliminados"""
    try:
        clientes = cliente_service.mostrar_clientes_eliminados()
        return render_template('clientes_eliminados.html', clientes=clientes)
    except Exception as e:
        flash(f"Error al cargar clientes eliminados: {str(e)}", "danger")
        return redirect(url_for('cliente_bp.clientes_lista'))

@cliente_bp.route('/clientes/restaurar/<int:id_cliente>', methods=['POST'])
def clientes_restaurar(id_cliente):
    """Restaura un cliente eliminado"""
    try:
        cliente_service.restaurar_cliente(id_cliente)
        flash("Cliente restaurado exitosamente", "success")
    except Exception as e:
        flash(f"Error al restaurar el cliente: {str(e)}", "danger")
    return redirect(url_for('cliente_bp.clientes_eliminados'))

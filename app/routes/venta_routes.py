from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from app.services import venta_service, venta_detalle_service

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.route('/mostrar_ventas', methods=['GET'])
def obtener_ventas():
    try:
        ventas = venta_service.mostrar_ventas()
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/insertar_venta', methods=['POST'])
def crear_venta():
    datos = request.get_json()
    try:
        id_nueva_venta = venta_service.insertar_venta(
            datos.get("id_serie"),
            datos.get("id_usuario"),
            datos.get("id_cliente"),
            datos.get("descripcion_estado"),
            datos.get("fecha"),
            datos.get("total")
        )
        return jsonify({"mensaje": "Venta registrada exitosamente", "id": id_nueva_venta}), 201
    except Exception as e:
        print("ESTE ES EL ERROR QUE NO ME DEJA DORMIR")
        print(str(e))
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/actualizar_venta', methods=['PUT'])
def modificar_venta():
    datos = request.get_json()
    try:
        venta_service.actualizar_venta(
            datos.get("id"),
            datos.get("id_cliente"),
            datos.get("descripcion_estado"),
            datos.get("total")
        )
        return jsonify({"mensaje": "Venta actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/eliminar_venta/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    try:
        venta_service.eliminar_venta(id)
        return jsonify({"mensaje": "Venta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/filtrar_ventas', methods=['POST'])
def filtrar_ventas_api():
    datos = request.get_json()
    try:
        filtro_nombre = datos.get("filtro_nombre")
        fecha_desde = datos.get("fecha_desde")
        fecha_hasta = datos.get("fecha_hasta")
        
        ventas = venta_service.filtrar_ventas(filtro_nombre, fecha_desde, fecha_hasta)
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@venta_bp.route('/obtener_venta_completa/<int:id>', methods=['GET'])
def obtener_venta_completa_api(id):
    try:
        cabecera = venta_service.obtener_venta_por_id(id)
        if not cabecera:
            return jsonify({"error": "Venta no encontrada"}), 404
            
        detalles = venta_detalle_service.obtener_detalles_con_productos(id)
        
        return jsonify({
            "cabecera": cabecera,
            "detalles": detalles
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@venta_bp.route('/ventas_lista', methods=['GET'])
def ventas_lista_web():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        "ventas_lista.html",
        usuario=session.get('usuario'),
        id=session.get('id'),
        estado=session.get('estado')
    )

@venta_bp.route('/venta_vista/<int:id>', methods=['GET'])
def venta_vista_web(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        "venta_vista.html",
        id_venta=id,
        usuario=session.get('usuario'),
        id=session.get('id'),
        estado=session.get('estado')
    )

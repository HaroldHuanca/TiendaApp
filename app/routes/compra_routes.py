from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.services import compra_service, compra_detalle_service

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

@compra_bp.route('/filtrar_compras', methods=['POST'])
def filtrar_compras_api():
    datos = request.get_json()
    try:
        filtro_nombre = datos.get("filtro_nombre")
        fecha_desde = datos.get("fecha_desde")
        fecha_hasta = datos.get("fecha_hasta")
        
        compras = compra_service.filtrar_compras(filtro_nombre, fecha_desde, fecha_hasta)
        return jsonify(compras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route('/obtener_compra_completa/<int:id>', methods=['GET'])
def obtener_compra_completa_api(id):
    try:
        cabecera = compra_service.obtener_compra_por_id(id)
        if not cabecera:
            return jsonify({"error": "Compra no encontrada"}), 404
            
        detalles = compra_detalle_service.obtener_detalles_con_productos(id)
        
        return jsonify({
            "cabecera": cabecera,
            "detalles": detalles
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@compra_bp.route('/compras_lista', methods=['GET'])
def compras_lista_web():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        "compras_lista.html",
        usuario=session.get('usuario'),
        id=session.get('id'),
        estado=session.get('estado')
    )

@compra_bp.route('/compras_vista/<int:id>', methods=['GET'])
def compras_vista_web(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template(
        "compras_vista.html",
        id_compra=id,
        usuario=session.get('usuario'),
        id=session.get('id'),
        estado=session.get('estado')
    )
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services import producto_service

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/productos_actualizados/<string:tiempo_actualizacion>', methods=['GET'])
def obtener_productos_actualizados(tiempo_actualizacion):
    try:
        productos = producto_service.obtener_productos_actualizados(tiempo_actualizacion)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/insertar_producto', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    try:
        producto_service.insertar_producto(
            datos.get("codigo_barras"),
            datos.get("nombre_unidad"),
            datos.get("nombre_categoria"),
            datos.get("descripcion"),
            datos.get("precio_compra"),
            datos.get("precio_venta"),
            datos.get("stock"),
            datos.get("stock_minimo"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Producto creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/actualizar_producto/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    datos = request.get_json()
    try:
        producto_service.actualizar_producto(
            id_producto,
            datos.get("codigo_barras"),
            datos.get("nombre_unidad"),
            datos.get("nombre_categoria"),
            datos.get("descripcion"),
            datos.get("precio_compra"),
            datos.get("precio_venta"),
            datos.get("stock"),
            datos.get("stock_minimo"),
            datos.get("descripcion_estado")
        )
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/eliminar_producto/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    try:
        producto_service.eliminar_producto(id_producto)
        return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/buscar_id_producto/<string:codigo_barras>', methods=['GET'])
def buscar_id_producto(codigo_barras):
    try:
        id_producto = producto_service.buscar_id_por_codigo_barras(codigo_barras)
        return jsonify({"id_producto": id_producto}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/mostrar_productos_paginado', methods=['GET'])
def obtener_productos_paginado():
    try:
        # Obtener parámetros de consulta (ej. /obtener_productos_paginados?limit=20&offset=40)
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        productos = producto_service.mostrar_productos_paginado(limit, offset)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/conteo', methods=['GET'])
def obtener_conteo_productos():
    try:
        conteo = producto_service.obtener_conteo_productos()
        return jsonify({"total": conteo}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# RUTAS PARA RENDERIZAR TEMPLATES
# ============================================

@producto_bp.route('/productos', methods=['GET'])
def productos_lista():
    """Renderiza la página principal con la lista de productos"""
    try:
        productos = producto_service.mostrar_productos_paginado(100, 0)
        from app.services import categoria_service, unidad_service
        categorias = categoria_service.mostrar_categorias()
        unidades = unidad_service.mostrar_unidades()
        return render_template('productos_lista.html', 
                             productos=productos,
                             categorias=categorias,
                             unidades=unidades)
    except Exception as e:
        flash(f"Error al cargar productos: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

@producto_bp.route('/productos/crear', methods=['GET'])
def productos_crear():
    """Renderiza el formulario de creación de producto"""
    try:
        from app.services import categoria_service, unidad_service
        categorias = categoria_service.mostrar_categorias()
        unidades = unidad_service.mostrar_unidades()
        return render_template('productos_crear.html',
                             categorias=categorias,
                             unidades=unidades)
    except Exception as e:
        flash(f"Error al cargar el formulario: {str(e)}", "danger")
        return redirect(url_for('producto_bp.productos_lista'))

@producto_bp.route('/productos/editar/<int:id_producto>', methods=['GET'])
def productos_editar(id_producto):
    """Renderiza el formulario de edición de producto"""
    try:
        productos = producto_service.mostrar_productos_paginado(1000, 0)
        producto = next((p for p in productos if p.get('ID_Producto') == id_producto), None)
        
        if not producto:
            flash("Producto no encontrado", "danger")
            return redirect(url_for('producto_bp.productos_lista'))
        
        from app.services import categoria_service, unidad_service
        categorias = categoria_service.mostrar_categorias()
        unidades = unidad_service.mostrar_unidades()
        
        return render_template('productos_editar.html',
                             producto=producto,
                             categorias=categorias,
                             unidades=unidades)
    except Exception as e:
        flash(f"Error al cargar el producto: {str(e)}", "danger")
        return redirect(url_for('producto_bp.productos_lista'))

@producto_bp.route('/productos/eliminados', methods=['GET'])
def productos_eliminados():
    """Renderiza la lista de productos eliminados"""
    try:
        productos = producto_service.mostrar_productos_eliminados()
        return render_template('productos_eliminados.html', productos=productos)
    except Exception as e:
        flash(f"Error al cargar productos eliminados: {str(e)}", "danger")
        return redirect(url_for('producto_bp.productos_lista'))

@producto_bp.route('/productos/restaurar/<int:id_producto>', methods=['POST'])
def productos_restaurar(id_producto):
    """Restaura un producto eliminado"""
    try:
        producto_service.restaurar_producto(id_producto)
        flash("Producto restaurado exitosamente", "success")
    except Exception as e:
        flash(f"Error al restaurar el producto: {str(e)}", "danger")
    return redirect(url_for('producto_bp.productos_eliminados'))

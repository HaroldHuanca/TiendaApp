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

@producto_bp.route('/obtener_productos_por_filtro/<string:filtro>', methods=['GET'])
def obtener_productos_por_filtro(filtro):
    try:
        productos = producto_service.obtener_productos_por_filtro(filtro)
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/mostrar_productos_paginado', methods=['GET'])
def obtener_productos_paginado():
    try:
        # Parámetros
        limit = int(request.args.get('limit', 20))
        pagina = int(request.args.get('pagina', 1))

        # Calcular offset automáticamente
        offset = (pagina - 1) * limit
        
        productos = producto_service.mostrar_productos_paginado(limit, offset)
        
        return jsonify({
            "pagina": pagina,
            "limit": limit,
            "offset": offset,
            "productos": productos
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@producto_bp.route('/conteo', methods=['GET'])
def obtener_conteo_productos():
    try:
        conteo = producto_service.obtener_conteo_productos()
        return jsonify({"total": conteo}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@producto_bp.route('/obtener_producto/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto):
    try:
        producto = producto_service.obtener_producto_por_id(id_producto)
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


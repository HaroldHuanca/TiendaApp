from flask import Flask, render_template, request, make_response
from flask_cors import CORS

# Importación de blueprints
from app.routes.categoria_routes import categoria_bp
from app.routes.cliente_routes import cliente_bp
from app.routes.estado_routes import estado_bp
from app.routes.producto_routes import producto_bp
from app.routes.proveedor_routes import proveedor_bp
from app.routes.tiempo_routes import tiempo_bp
from app.routes.unidad_routes import unidad_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.venta_routes import venta_bp
from app.routes.venta_detalle_routes import venta_detalle_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registro de blueprints
    app.register_blueprint(categoria_bp, url_prefix="/categorias")
    app.register_blueprint(cliente_bp, url_prefix="/clientes")
    app.register_blueprint(estado_bp, url_prefix="/estados")
    app.register_blueprint(producto_bp, url_prefix="/productos")
    app.register_blueprint(proveedor_bp, url_prefix="/proveedores")
    app.register_blueprint(tiempo_bp, url_prefix="/tiempo")
    app.register_blueprint(unidad_bp, url_prefix="/unidades")
    app.register_blueprint(usuario_bp, url_prefix="/usuarios")
    app.register_blueprint(venta_bp, url_prefix="/ventas")
    app.register_blueprint(venta_detalle_bp, url_prefix="/venta_detalles")

    def render_con_cookie(template):
        usuario_cookie = request.cookies.get("usuario")
        if usuario_cookie:
            return render_template(template, usuario=usuario_cookie)
        else:
            resp = make_response(render_template(template, usuario="admin"))
            resp.set_cookie("usuario", "admin")
            return resp

    @app.route("/")
    def index():
        return render_con_cookie("index.html")

    @app.route('/clientes')
    def clientes_web():
        return render_con_cookie("clientes.html")

    @app.route('/proveedores')
    def proveedores_web():
        return render_con_cookie("proveedores.html")

    @app.route('/categorias')
    def categorias_web():
        return render_con_cookie("categorias.html")

    @app.route('/unidades')
    def unidades_web():
        return render_con_cookie("unidades.html")
    @app.route('/usuarios')
    def usuarios_web():
        return render_con_cookie("usuarios.html")
    @app.route('/about')
    def about_web():
        return render_con_cookie("about.html")
    @app.route('/productos')
    def productos_web():
        return render_con_cookie("productos.html")
    @app.route('/ventas')
    def ventas_web():
        return render_con_cookie("ventas.html")
            
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

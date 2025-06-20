from flask import Flask
from flask_cors import CORS
from flask import render_template

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
    CORS(app)  # Permite solicitudes desde otros orígenes

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

    @app.route("/")
    def index():
        return render_template("inicio.html")
    
    @app.route('/clientes-web')
    def clientes_web():
        return render_template('clientes.html')
    @app.route('/proveedores-web')
    def proveedores_web():
        return render_template('proveedores.html')
    @app.route('/categorias-web')
    def categorias_web():
        return render_template('categorias.html')
    @app.route('/unidades-web')
    def unidades_web():
        return render_template('unidades.html')
    @app.route('/usuarios-web')
    def usuarios_web():
        return render_template('usuarios.html')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0' ,port=5000)
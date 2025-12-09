from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import app.services.usuario_service as usuario_service
import os

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
from app.routes.bonificacion_routes import bonificacion_bp
from app.routes.compra_detalle_routes import compra_detalle_bp
from app.routes.compra_routes import compra_bp
from app.routes.venta_individual_routes import venta_individual_bp

def create_app():
    # Rutas absolutas para templates y static
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'app', 'templates')
    static_dir = os.path.join(base_dir, 'app', 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = 'super-clave-123456'  # cámbiala por una segura
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora
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
    app.register_blueprint(bonificacion_bp, url_prefix="/bonificaciones")
    app.register_blueprint(compra_detalle_bp, url_prefix="/compra_detalles")
    app.register_blueprint(compra_bp, url_prefix="/compras")
    app.register_blueprint(venta_individual_bp, url_prefix="/venta_individuales")

    def render_con_session(template):
        """Renderiza un template verificando que el usuario tenga una sesión activa."""
        # Verificar si hay un usuario en la sesión
        if 'usuario' not in session:
            return redirect(url_for('login'))
        
        # Verificar que el usuario existe en la base de datos
        try:
            resultado = usuario_service.obtener_contrasena(session['usuario'])
            if not resultado or len(resultado) == 0:
                # Usuario no encontrado, limpiar sesión
                session.clear()
                return redirect(url_for('login'))
        except Exception:
            # Error al verificar usuario, limpiar sesión
            session.clear()
            return redirect(url_for('login'))
        
        # Renderizar template con los datos de la sesión
        return render_template(
            template,
            usuario=session.get('usuario'),
            id=session.get('id'),
            estado=session.get('estado')
        )

    @app.route("/login")
    def login():
        return render_template('login.html')
    
    @app.route("/logout")
    def logout():
        """Cierra la sesión del usuario."""
        session.clear()
        return redirect(url_for('login'))

    @app.route("/")
    def index():
        return render_con_session("dashboard.html")

    @app.route('/clientes')
    def clientes_web():
        return render_con_session("clientes.html")

    @app.route('/proveedores')
    def proveedores_web():
        return render_con_session("proveedores.html")

    @app.route('/categorias')
    def categorias_web():
        return render_con_session("categorias.html")

    @app.route('/unidades')
    def unidades_web():
        return render_con_session("unidades.html")

    @app.route('/productos')
    def productos_web():
        return render_con_session("productos.html")

    @app.route('/ventas')
    def ventas_web():
        return render_con_session("ventas.html")
            
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
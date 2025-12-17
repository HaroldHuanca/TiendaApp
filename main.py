from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_cors import CORS
import app.services.usuario_service as usuario_service
import os
from config import LANConfig

# Importación de blueprints
from app.routes.categoria_routes import categoria_bp
from app.routes.cliente_routes import cliente_bp
from app.routes.estado_routes import estado_bp
from app.routes.producto_routes import producto_bp
from app.routes.proveedor_routes import proveedor_bp
from app.routes.serie_routes import serie_bp
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

    # Cargar configuración para LAN
    app.config.from_object(LANConfig)

    # Habilitar CORS para permitir peticiones desde la LAN (preflight incluida)
    # Se permite cualquier origen para facilitar el uso en red local; si necesitas
    # credenciales (cookies/sesión) reemplaza '*' por orígenes específicos.
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Middleware para evitar cacheo de páginas autenticadas
    @app.after_request
    def set_cache_headers(response):
        """Previene el cacheo de páginas para evitar problemas de sesión stale"""
        if request.path.startswith(('/productos', '/categorias', '/unidades', '/clientes', '/proveedores')):
            response.cache_control.no_cache = True
            response.cache_control.no_store = True
            response.cache_control.max_age = 0
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    
    # Registro de blueprints
    app.register_blueprint(categoria_bp, url_prefix="/categorias")
    app.register_blueprint(cliente_bp, url_prefix="/clientes")
    app.register_blueprint(estado_bp, url_prefix="/estados")
    app.register_blueprint(producto_bp, url_prefix="/productos")
    app.register_blueprint(proveedor_bp, url_prefix="/proveedores")
    app.register_blueprint(serie_bp, url_prefix="/series")
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
    
    @app.route("/logout", methods=['GET', 'POST'], strict_slashes=False)
    def logout():
        """Cierra la sesión del usuario y limpia todas las cookies."""
        # Limpiar la sesión
        session.clear()
        
        # Crear respuesta de redirección
        response = make_response(redirect(url_for('login')))
        
        # Eliminar cookies específicamente
        response.delete_cookie('session', path='/')
        response.delete_cookie('session', path='/productos')
        response.delete_cookie('session', path='/categorias')
        response.delete_cookie('session', path='/unidades')
        response.delete_cookie('session', path='/clientes')
        response.delete_cookie('session', path='/proveedores')
        
        # Agregar headers para evitar cacheo
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.max_age = 0
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

    @app.route("/clear-session", strict_slashes=False)
    def clear_session():
        """Endpoint para limpiar sesión corrupta (útil para debugging)"""
        session.clear()
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('session', path='/')
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        return response

    @app.route("/test-sidebar")
    def test_sidebar():
        """Página de test para el sidebar móvil (sin requiere sesión)"""
        return render_template('test_sidebar.html', usuario='Test', id='0', estado='activo')

    @app.route('/', strict_slashes=False)
    def index():
        return render_con_session("dashboard.html")

    @app.route('/clientes', strict_slashes=False)
    def clientes_web():
        return render_con_session("clientes_lista.html")

    @app.route('/proveedores', strict_slashes=False)
    def proveedores_web():
        return render_con_session("proveedores_lista.html")

    @app.route('/categorias', strict_slashes=False)
    def categorias_web():
        return render_con_session("categorias_lista.html")

    @app.route('/unidades', strict_slashes=False)
    def unidades_web():
        return render_con_session("unidades_lista.html")

    @app.route('/productos', strict_slashes=False)
    def productos_web():
        # Verificar si hay sesión activa
        if 'usuario' not in session:
            return redirect(url_for('login'))
        
        try:
            resultado = usuario_service.obtener_contrasena(session['usuario'])
            if not resultado or len(resultado) == 0:
                # Usuario no existe en la BD, pero si hay sesión activa, permitir acceso
                print(f"Advertencia: Usuario {session['usuario']} en sesión pero no en BD")
        except Exception as e:
            # Si hay error pero hay sesión, permitir acceso (para desarrollo)
            print(f"Error verificando usuario: {e}")
        
        return render_template(
            "productos_listar.html",
            usuario=session.get('usuario'),
            id=session.get('id'),
            estado=session.get('estado')
        )

    @app.route('/ventas', strict_slashes=False)
    def ventas_web():
        return render_con_session("ventas.html")
            
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
import bcrypt
from app.routes.usuario_routes import usuario_bp

class TestUsuarioRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(usuario_bp)
        self.client = self.app.test_client()

    @patch('app.routes.usuario_routes.usuario_service')
    def test_listar_usuarios(self, mock_service):
        mock_service.mostrar_usuarios.return_value = []
        response = self.client.get('/mostrar_usuarios')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.usuario_routes.usuario_service')
    def test_crear_usuario(self, mock_service):
        mock_service.insertar_usuario.return_value = 1
        response = self.client.post('/insetar_usuario', json={
            "nombre_usuario": "user", "contrasena": "pass", "correo": "mail", 
            "direccion_mac": "mac", "descripcion_estado": "estado"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.usuario_routes.usuario_service')
    def test_verificar_login_success(self, mock_service):
        # Mocking password verification
        hashed = bcrypt.hashpw(b"pass", bcrypt.gensalt()).decode('utf-8')
        mock_service.obtener_contrasena.return_value = [{'contrasena': hashed, 'id': 1, 'estado': 'Activo'}]
        
        with patch('bcrypt.checkpw') as mock_checkpw, \
             patch('app.routes.usuario_routes.generar_mac_aleatoria', return_value="new_mac"):
            mock_checkpw.return_value = True
            
            response = self.client.post('/verificar_login', json={
                "usuario": "user", "contrasena": "pass"
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['exito'])

if __name__ == '__main__':
    unittest.main()

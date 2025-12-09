import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.cliente_routes import cliente_bp

class TestClienteRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(cliente_bp)
        self.client = self.app.test_client()

    @patch('app.routes.cliente_routes.cliente_service')
    def test_obtener_clientes(self, mock_service):
        mock_service.mostrar_clientes.return_value = []
        response = self.client.get('/mostrar_clientes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.routes.cliente_routes.cliente_service')
    def test_crear_cliente(self, mock_service):
        mock_service.insertar_cliente.return_value = None
        response = self.client.post('/insertar_cliente', json={
            "documento": "123", "nombre": "Juan", "descripcion_estado": "Activo"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.cliente_routes.cliente_service')
    def test_modificar_cliente(self, mock_service):
        mock_service.actualizar_cliente.return_value = None
        response = self.client.put('/actualizar_cliente/1', json={
            "documento": "123", "nombre": "Juan", "descripcion_estado": "Activo"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.cliente_routes.cliente_service')
    def test_borrar_cliente(self, mock_service):
        mock_service.eliminar_cliente.return_value = None
        response = self.client.delete('/eliminar_cliente/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

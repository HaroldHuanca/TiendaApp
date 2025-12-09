import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.compra_routes import compra_bp

class TestCompraRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(compra_bp)
        self.client = self.app.test_client()

    @patch('app.routes.compra_routes.compra_service')
    def test_mostrar_compras(self, mock_service):
        mock_service.mostrar_compras.return_value = []
        response = self.client.get('/mostrar_compras')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.routes.compra_routes.compra_service')
    def test_insertar_compra(self, mock_service):
        mock_service.insertar_compra.return_value = 1
        response = self.client.post('/insertar_compra', json={
            "id_usuario": 1, "id_proveedor": 1, "descripcion_estado": "Pendiente",
            "fecha_hora": "2023-01-01", "total": 100
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.compra_routes.compra_service')
    def test_actualizar_compra(self, mock_service):
        mock_service.actualizar_compra.return_value = None
        response = self.client.put('/actualizar_compra/1', json={
            "id_proveedor": 1, "descripcion_estado": "Completada", "total": 150
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.compra_routes.compra_service')
    def test_eliminar_compra(self, mock_service):
        mock_service.eliminar_compra.return_value = None
        response = self.client.delete('/eliminar_compra/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

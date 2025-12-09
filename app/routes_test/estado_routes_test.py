import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.estado_routes import estado_bp

class TestEstadoRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(estado_bp)
        self.client = self.app.test_client()

    @patch('app.routes.estado_routes.estado_service')
    def test_obtener_estados(self, mock_service):
        mock_service.mostrar_estados.return_value = []
        response = self.client.get('/mostrar_estados/tabla')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.estado_routes.estado_service')
    def test_crear_estado(self, mock_service):
        mock_service.insertar_estado.return_value = None
        response = self.client.post('/insertar_estado/tabla', json={
            "estado": 1, "descripcion": "desc"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.estado_routes.estado_service')
    def test_modificar_estado(self, mock_service):
        mock_service.actualizar_estado.return_value = None
        response = self.client.put('/actualizar_estado/tabla', json={
            "estado": 1, "descripcion": "desc"
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

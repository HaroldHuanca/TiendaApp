import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.unidad_routes import unidad_bp

class TestUnidadRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(unidad_bp)
        self.client = self.app.test_client()

    @patch('app.routes.unidad_routes.unidad_service')
    def test_listar_unidades(self, mock_service):
        mock_service.mostrar_unidades.return_value = []
        response = self.client.get('/mostrar_unidades')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.unidad_routes.unidad_service')
    def test_crear_unidad(self, mock_service):
        mock_service.insertar_unidad.return_value = None
        response = self.client.post('/insertar_unidad', json={"nombre": "U"})
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.unidad_routes.unidad_service')
    def test_modificar_unidad(self, mock_service):
        mock_service.actualizar_unidad.return_value = None
        response = self.client.put('/actualizar_unidad/1', json={"nombre": "U"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

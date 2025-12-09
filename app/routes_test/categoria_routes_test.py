import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.categoria_routes import categoria_bp

class TestCategoriaRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(categoria_bp)
        self.client = self.app.test_client()

    @patch('app.routes.categoria_routes.categoria_service')
    def test_obtener_categorias(self, mock_service):
        mock_service.mostrar_categorias.return_value = []
        response = self.client.get('/mostrar_categorias')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.routes.categoria_routes.categoria_service')
    def test_crear_categoria(self, mock_service):
        mock_service.insertar_categoria.return_value = None
        response = self.client.post('/insertar_categoria', json={"nombre": "Nueva"})
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.categoria_routes.categoria_service')
    def test_modificar_categoria(self, mock_service):
        mock_service.actualizar_categoria.return_value = None
        response = self.client.put('/actualizar_categoria/1', json={"nombre": "Actualizada"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

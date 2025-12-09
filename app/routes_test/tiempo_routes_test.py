import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.tiempo_routes import tiempo_bp

class TestTiempoRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(tiempo_bp)
        self.client = self.app.test_client()

    @patch('app.routes.tiempo_routes.tiempo_service')
    def test_obtener_fecha_actual(self, mock_service):
        mock_service.obtener_fecha_actual_formateada.return_value = "01/01/2023"
        response = self.client.get('/fecha_actual')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"fecha": "01/01/2023"})

if __name__ == '__main__':
    unittest.main()

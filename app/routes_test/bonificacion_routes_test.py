import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.bonificacion_routes import bonificacion_bp

class TestBonificacionRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(bonificacion_bp)
        self.client = self.app.test_client()

    @patch('app.routes.bonificacion_routes.bonificacion_service')
    def test_mostrar_bonificaciones(self, mock_service):
        mock_service.mostrar_bonificaciones.return_value = []
        response = self.client.get('/mostrar_bonificaciones/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.routes.bonificacion_routes.bonificacion_service')
    def test_insertar_bonificacion(self, mock_service):
        mock_service.insertar_bonificacion.return_value = None
        response = self.client.post('/insertar_bonificacion', json={
            "id_compra": 1,
            "id_producto": 1,
            "cantidad": 10
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.bonificacion_routes.bonificacion_service')
    def test_actualizar_bonificacion(self, mock_service):
        mock_service.actualizar_bonificacion.return_value = None
        response = self.client.put('/actualizar_bonificacion/1/1', json={
            "cantidad": 20
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.bonificacion_routes.bonificacion_service')
    def test_eliminar_bonificacion(self, mock_service):
        mock_service.eliminar_bonificacion.return_value = None
        response = self.client.delete('/eliminar_bonificacion/1/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

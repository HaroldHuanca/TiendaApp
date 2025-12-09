import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.venta_individual_routes import venta_individual_bp

class TestVentaIndividualRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(venta_individual_bp)
        self.client = self.app.test_client()

    @patch('app.routes.venta_individual_routes.venta_individual_service')
    def test_mostrar_ventas_individuales(self, mock_service):
        mock_service.mostrar_ventas_individuales.return_value = []
        response = self.client.get('/mostrar_ventas_individuales/2023-01-01')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_individual_routes.venta_individual_service')
    def test_insertar_venta_individual(self, mock_service):
        mock_service.insertar_venta_individual.return_value = None
        response = self.client.post('/insertar_venta_individual', json={
            "id_producto": 1, "id_usuario": 1, "cantidad": 1, 
            "precio_venta": 10, "fecha_hora": "F"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.venta_individual_routes.venta_individual_service')
    def test_actualizar_venta_individual(self, mock_service):
        mock_service.actualizar_venta_individual.return_value = None
        response = self.client.put('/actualizar_venta_individual/1', json={
            "id_producto": 1, "id_usuario": 1, "cantidad": 1, 
            "precio_venta": 10, "fecha_hora": "F"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_individual_routes.venta_individual_service')
    def test_eliminar_venta_individual(self, mock_service):
        mock_service.eliminar_venta_individual.return_value = None
        response = self.client.delete('/eliminar_venta_individual/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

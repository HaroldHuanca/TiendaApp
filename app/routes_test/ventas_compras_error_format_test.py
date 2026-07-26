import unittest
from flask import Flask
from unittest.mock import patch

from app.routes.venta_routes import venta_bp
from app.routes.compra_routes import compra_bp


class TestErrorResponseFormat(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(venta_bp)
        self.app.register_blueprint(compra_bp)
        self.client = self.app.test_client()

    @patch('app.routes.venta_routes.venta_service.insertar_venta')
    def test_venta_error_response_format(self, mock_insertar_venta):
        mock_insertar_venta.side_effect = RuntimeError('Stock insuficiente')

        response = self.client.post('/insertar_venta', json={
            'id_serie': 1,
            'id_usuario': 1,
            'id_cliente': 1,
            'descripcion_estado': 'Activo',
            'fecha': '2026-07-25',
            'total': 100.0
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(response.json['error'], 'Stock insuficiente')

    @patch('app.routes.compra_routes.compra_service.insertar_compra')
    def test_compra_error_response_format(self, mock_insertar_compra):
        mock_insertar_compra.side_effect = RuntimeError('No se pudo registrar la compra')

        response = self.client.post('/insertar_compra', json={
            'id_usuario': 1,
            'id_proveedor': 1,
            'descripcion_estado': 'Activo',
            'fecha_hora': '2026-07-25 10:00:00',
            'total': 200.0
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(response.json['error'], 'No se pudo registrar la compra')


if __name__ == '__main__':
    unittest.main()

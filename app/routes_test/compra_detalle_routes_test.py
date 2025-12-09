import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.compra_detalle_routes import compra_detalle_bp

class TestCompraDetalleRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(compra_detalle_bp)
        self.client = self.app.test_client()

    @patch('app.routes.compra_detalle_routes.compra_detalle_service')
    def test_mostrar_detalles_compra(self, mock_service):
        mock_service.mostrar_detalles_venta.return_value = []
        response = self.client.get('/mostrar_detalles_compra/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.routes.compra_detalle_routes.compra_detalle_service')
    def test_insertar_detalle_compra(self, mock_service):
        mock_service.insertar_detalle_compra.return_value = None
        response = self.client.post('/insertar_detalle_compra', json={
            "id_compra": 1, "id_producto": 1, "cantidad": 5,
            "precio_compra": 10, "descuento": 0, "descripcion_estado": "Ok"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.compra_detalle_routes.compra_detalle_service')
    def test_actualizar_detalle_compra(self, mock_service):
        mock_service.actualizar_detalle_compra.return_value = None
        response = self.client.put('/actualizar_detalle_compra/1/1', json={
            "cantidad": 10, "precio_compra": 10, "descuento": 0, "descripcion_estado": "Ok"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.compra_detalle_routes.compra_detalle_service')
    def test_eliminar_detalle_compra(self, mock_service):
        mock_service.eliminar_detalle_compra.return_value = None
        response = self.client.delete('/eliminar_detalle_compra/1/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

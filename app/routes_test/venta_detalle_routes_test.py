import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.venta_detalle_routes import venta_detalle_bp

class TestVentaDetalleRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(venta_detalle_bp)
        self.client = self.app.test_client()

    @patch('app.routes.venta_detalle_routes.venta_detalle_service')
    def test_obtener_detalles_venta(self, mock_service):
        mock_service.mostrar_detalles_venta.return_value = []
        response = self.client.get('/mostrar_venta_detalles/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_detalle_routes.venta_detalle_service')
    def test_crear_detalle_venta(self, mock_service):
        mock_service.insertar_detalle_venta.return_value = None
        response = self.client.post('/insertar_venta_detalle', json={
            "id_venta": 1, "id_producto": 1, "cantidad": 1, 
            "precio_venta": 10, "descuento": 0, "descripcion_estado": "E"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.venta_detalle_routes.venta_detalle_service')
    def test_modificar_detalle_venta(self, mock_service):
        mock_service.actualizar_detalle_venta.return_value = None
        response = self.client.put('/actualizar_venta_detalle', json={
            "id_venta": 1, "id_producto": 1, "cantidad": 1, 
            "precio_venta": 10, "descuento": 0, "descripcion_estado": "E"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_detalle_routes.venta_detalle_service')
    def test_eliminar_detalle_venta(self, mock_service):
        mock_service.eliminar_detalle_venta.return_value = None
        response = self.client.delete('/eliminar_venta_detalle/1/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

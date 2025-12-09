import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.venta_routes import venta_bp

class TestVentaRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(venta_bp)
        self.client = self.app.test_client()

    @patch('app.routes.venta_routes.venta_service')
    def test_obtener_ventas(self, mock_service):
        mock_service.mostrar_ventas.return_value = []
        response = self.client.get('/mostrar_ventas')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_routes.venta_service')
    def test_crear_venta(self, mock_service):
        mock_service.insertar_venta.return_value = 1
        response = self.client.post('/insertar_venta', json={
            "id_serie": 1, "id_usuario": 1, "id_cliente": 1, 
            "descripcion_estado": "E", "fecha": "F", "total": 100
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.venta_routes.venta_service')
    def test_modificar_venta(self, mock_service):
        mock_service.actualizar_venta.return_value = None
        response = self.client.put('/actualizar_venta', json={
            "id": 1, "id_cliente": 1, "descripcion_estado": "E", "total": 100
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.venta_routes.venta_service')
    def test_eliminar_venta(self, mock_service):
        mock_service.eliminar_venta.return_value = None
        response = self.client.delete('/eliminar_venta/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

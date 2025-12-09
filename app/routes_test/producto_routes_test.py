import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.producto_routes import producto_bp

class TestProductoRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(producto_bp)
        self.client = self.app.test_client()

    @patch('app.routes.producto_routes.producto_service')
    def test_obtener_productos_actualizados(self, mock_service):
        mock_service.obtener_productos_actualizados.return_value = []
        response = self.client.get('/productos_actualizados/2023-01-01')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.producto_routes.producto_service')
    def test_crear_producto(self, mock_service):
        mock_service.insertar_producto.return_value = None
        response = self.client.post('/insertar_producto', json={
            "codigo_barras": "123", "nombre_unidad": "U", "nombre_categoria": "C",
            "descripcion": "D", "precio_compra": 10, "precio_venta": 20,
            "stock": 100, "stock_minimo": 10, "descripcion_estado": "E"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.producto_routes.producto_service')
    def test_actualizar_producto(self, mock_service):
        mock_service.actualizar_producto.return_value = None
        response = self.client.put('/actualizar_producto/1', json={
            "codigo_barras": "123", "nombre_unidad": "U", "nombre_categoria": "C",
            "descripcion": "D", "precio_compra": 10, "precio_venta": 20,
            "stock": 100, "stock_minimo": 10, "descripcion_estado": "E"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.producto_routes.producto_service')
    def test_eliminar_producto(self, mock_service):
        mock_service.eliminar_producto.return_value = None
        response = self.client.delete('/eliminar_producto/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.producto_routes.producto_service')
    def test_buscar_id_producto(self, mock_service):
        mock_service.buscar_id_por_codigo_barras.return_value = 1
        response = self.client.get('/buscar_id_producto/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id_producto': 1})

    @patch('app.routes.producto_routes.producto_service')
    def test_obtener_productos_paginado(self, mock_service):
        mock_service.mostrar_productos_paginado.return_value = []
        response = self.client.get('/mostrar_productos_paginado?limit=10&offset=0')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.producto_routes.producto_service')
    def test_obtener_conteo_productos(self, mock_service):
        mock_service.obtener_conteo_productos.return_value = 100
        response = self.client.get('/conteo')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

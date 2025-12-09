import unittest
from flask import Flask
from unittest.mock import MagicMock, patch
from app.routes.proveedor_routes import proveedor_bp

class TestProveedorRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(proveedor_bp)
        self.client = self.app.test_client()

    @patch('app.routes.proveedor_routes.proveedor_service')
    def test_listar_proveedores(self, mock_service):
        mock_service.mostrar_proveedores.return_value = []
        response = self.client.get('/mostrar_proveedores')
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.proveedor_routes.proveedor_service')
    def test_crear_proveedor(self, mock_service):
        mock_service.insertar_proveedor.return_value = None
        response = self.client.post('/insertar_proveedor', json={
            "ruc": "123", "nombre": "Prov", "descripcion_estado": "Act"
        })
        self.assertEqual(response.status_code, 201)

    @patch('app.routes.proveedor_routes.proveedor_service')
    def test_modificar_proveedor(self, mock_service):
        mock_service.actualizar_proveedor.return_value = None
        response = self.client.put('/actualizar_proveedor/1', json={
            "ruc": "123", "nombre": "Prov", "descripcion_estado": "Act"
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.proveedor_routes.proveedor_service')
    def test_borrar_proveedor(self, mock_service):
        mock_service.eliminar_proveedor.return_value = None
        response = self.client.delete('/eliminar_proveedor/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

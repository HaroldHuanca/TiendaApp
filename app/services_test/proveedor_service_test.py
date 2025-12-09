import unittest
from unittest.mock import MagicMock, patch
from app.services.proveedor_service import mostrar_proveedores, insertar_proveedor, actualizar_proveedor, eliminar_proveedor

class TestProveedorService(unittest.TestCase):

    @patch('app.services.proveedor_service.proveedor_model.mostrar_proveedores')
    def test_mostrar_proveedores(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_proveedores()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.proveedor_service.proveedor_model.insertar_proveedor')
    def test_insertar_proveedor(self, mock_insertar):
        insertar_proveedor("12345678901", "Proveedor", "Activo")
        mock_insertar.assert_called()

    @patch('app.services.proveedor_service.proveedor_model.actualizar_proveedor')
    def test_actualizar_proveedor(self, mock_actualizar):
        actualizar_proveedor(1, "12345678901", "Proveedor", "Activo")
        mock_actualizar.assert_called()

    @patch('app.services.proveedor_service.proveedor_model.eliminar_proveedor')
    def test_eliminar_proveedor(self, mock_eliminar):
        # 0 is not valid smallint > 0, so using 1
        eliminar_proveedor(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

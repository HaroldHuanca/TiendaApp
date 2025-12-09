import unittest
from unittest.mock import MagicMock, patch
from app.services.venta_service import mostrar_ventas, insertar_venta, actualizar_venta, eliminar_venta

class TestVentaService(unittest.TestCase):

    @patch('app.services.venta_service.venta_model.mostrar_ventas')
    def test_mostrar_ventas(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_ventas()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.venta_service.venta_model.insertar_venta')
    def test_insertar_venta(self, mock_insertar):
        mock_insertar.return_value = 1
        result = insertar_venta(1, 1, 1, "Estado", "2023-01-01 12:00:00", 100.0)
        self.assertEqual(result, 1)
        mock_insertar.assert_called()

    @patch('app.services.venta_service.venta_model.actualizar_venta')
    def test_actualizar_venta(self, mock_actualizar):
        actualizar_venta(1, 1, "Estado", 100.0)
        mock_actualizar.assert_called()

    @patch('app.services.venta_service.venta_model.eliminar_venta')
    def test_eliminar_venta(self, mock_eliminar):
        eliminar_venta(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

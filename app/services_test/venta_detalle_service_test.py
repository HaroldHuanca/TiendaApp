import unittest
from unittest.mock import MagicMock, patch
from app.services.venta_detalle_service import mostrar_detalles_venta, insertar_detalle_venta, actualizar_detalle_venta, eliminar_detalle_venta

class TestVentaDetalleService(unittest.TestCase):

    @patch('app.services.venta_detalle_service.venta_detalle_model.mostrar_detalles_venta')
    def test_mostrar_detalles_venta(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_detalles_venta(1)
        self.assertEqual(result, [])
        mock_mostrar.assert_called_with(1)

    @patch('app.services.venta_detalle_service.venta_detalle_model.insertar_detalle_venta')
    def test_insertar_detalle_venta(self, mock_insertar):
        insertar_detalle_venta(1, 1, 5.0, 10.0, 0.0, "Estado")
        mock_insertar.assert_called()

    @patch('app.services.venta_detalle_service.venta_detalle_model.actualizar_detalle_venta')
    def test_actualizar_detalle_venta(self, mock_actualizar):
        actualizar_detalle_venta(1, 1, 5.0, 10.0, 0.0, "Estado")
        mock_actualizar.assert_called()

    @patch('app.services.venta_detalle_service.venta_detalle_model.eliminar_detalle_venta')
    def test_eliminar_detalle_venta(self, mock_eliminar):
        eliminar_detalle_venta(1, 1)
        mock_eliminar.assert_called_with(1, 1)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
from app.services.compra_detalle_service import mostrar_detalles_venta, insertar_detalle_compra, actualizar_detalle_compra, eliminar_detalle_compra

class TestCompraDetalleService(unittest.TestCase):

    @patch('app.services.compra_detalle_service.compra_detalle_model.mostrar_detalles_compra')
    def test_mostrar_detalles_venta(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_detalles_venta(1)
        self.assertEqual(result, [])
        mock_mostrar.assert_called_with(1)

    @patch('app.services.compra_detalle_service.compra_detalle_model.insertar_detalle_compra')
    def test_insertar_detalle_compra(self, mock_insertar):
        insertar_detalle_compra(1, 1, 5.0, 10.0, 0.0, "Activo")
        mock_insertar.assert_called()

    @patch('app.services.compra_detalle_service.compra_detalle_model.actualizar_detalle_compra')
    def test_actualizar_detalle_compra(self, mock_actualizar):
        actualizar_detalle_compra(1, 1, 10.0, 10.0, 2.0, "Activo")
        mock_actualizar.assert_called()

    @patch('app.services.compra_detalle_service.compra_detalle_model.eliminar_detalle_compra')
    def test_eliminar_detalle_compra(self, mock_eliminar):
        eliminar_detalle_compra(1, 1)
        mock_eliminar.assert_called_with(1, 1)

if __name__ == '__main__':
    unittest.main()

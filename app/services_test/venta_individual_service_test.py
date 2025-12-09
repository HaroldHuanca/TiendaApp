import unittest
from unittest.mock import MagicMock, patch
from app.services.venta_individual_service import mostrar_ventas_individuales, insertar_venta_individual, actualizar_venta_individual, eliminar_venta_individual

class TestVentaIndividualService(unittest.TestCase):

    @patch('app.services.venta_individual_service.venta_individual_model.mostrar_ventas_individuales')
    def test_mostrar_ventas_individuales(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_ventas_individuales("2023-01-01")
        self.assertEqual(result, [])
        mock_mostrar.assert_called_with("2023-01-01")

    @patch('app.services.venta_individual_service.venta_individual_model.insertar_venta_individual')
    def test_insertar_venta_individual(self, mock_insertar):
        insertar_venta_individual(1, 1, 10.0, 20.0, "2023-01-01 12:00:00")
        mock_insertar.assert_called()

    @patch('app.services.venta_individual_service.venta_individual_model.actualizar_venta_individual')
    def test_actualizar_venta_individual(self, mock_actualizar):
        actualizar_venta_individual(1, 1, 1, 10.0, 20.0, "2023-01-01 12:00:00")
        mock_actualizar.assert_called()

    @patch('app.services.venta_individual_service.venta_individual_model.eliminar_venta_individual')
    def test_eliminar_venta_individual(self, mock_eliminar):
        eliminar_venta_individual(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

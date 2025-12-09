import unittest
from unittest.mock import MagicMock, patch
from app.services.compra_service import mostrar_compras, insertar_compra, actualizar_compra, eliminar_compra

class TestCompraService(unittest.TestCase):

    @patch('app.services.compra_service.compra_model.mostrar_compras')
    def test_mostrar_compras(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_compras()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.compra_service.compra_model.insertar_compra')
    def test_insertar_compra(self, mock_insertar):
        mock_insertar.return_value = 1
        result = insertar_compra(1, 1, "Pendiente", "2023-01-01 12:00:00", 100.0)
        self.assertEqual(result, 1)
        # Assuming validation passes
        mock_insertar.assert_called()

    @patch('app.services.compra_service.compra_model.actualizar_compra')
    def test_actualizar_compra(self, mock_actualizar):
        actualizar_compra(1, 1, "Completada", 150.0)
        mock_actualizar.assert_called()

    @patch('app.services.compra_service.compra_model.eliminar_compra')
    def test_eliminar_compra(self, mock_eliminar):
        eliminar_compra(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

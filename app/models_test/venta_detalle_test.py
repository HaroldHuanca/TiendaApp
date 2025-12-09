import unittest
from unittest.mock import MagicMock, patch
from app.models.venta_detalle import mostrar_detalles_venta, insertar_detalle_venta, actualizar_detalle_venta, eliminar_detalle_venta

class TestVentaDetalleModel(unittest.TestCase):

    @patch('app.models.venta_detalle.DatabaseManager')
    def test_mostrar_detalles_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_detalles_venta(1)
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.venta_detalle.DatabaseManager')
    def test_insertar_detalle_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_detalle_venta(1, 1, 5.0, 10.0, 0.0, "Estado")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.venta_detalle.DatabaseManager')
    def test_actualizar_detalle_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_detalle_venta(1, 1, 10.0, 10.0, 0.0, "Estado")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.venta_detalle.DatabaseManager')
    def test_eliminar_detalle_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_detalle_venta(1, 1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

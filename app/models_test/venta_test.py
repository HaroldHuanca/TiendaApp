import unittest
from unittest.mock import MagicMock, patch
from app.models.venta import mostrar_ventas, insertar_venta, actualizar_venta, eliminar_venta

class TestVentaModel(unittest.TestCase):

    @patch('app.models.venta.DatabaseManager')
    def test_mostrar_ventas(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_ventas()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.venta.DatabaseManager')
    def test_insertar_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.side_effect = [[(1,)], []]
        mock_cursor.nextset.return_value = False

        result = insertar_venta(1, 1, 1, "Estado", "2023-01-01", 100.0)
        self.assertEqual(result, 1)
        mock_cursor.callproc.assert_called()

    @patch('app.models.venta.DatabaseManager')
    def test_actualizar_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_venta(1, 1, "Estado", 150.0)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.venta.DatabaseManager')
    def test_eliminar_venta(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_venta(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

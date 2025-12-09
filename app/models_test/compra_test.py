import unittest
from unittest.mock import MagicMock, patch
from app.models.compra import mostrar_compras, insertar_compra, actualizar_compra, eliminar_compra

class TestCompraModel(unittest.TestCase):

    @patch('app.models.compra.DatabaseManager')
    def test_mostrar_compras(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_compras()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.compra.DatabaseManager')
    def test_insertar_compra(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.side_effect = [[(1,)], []] # Returns ID 1
        mock_cursor.nextset.return_value = False

        result = insertar_compra(1, 1, "Pendiente", "2023-01-01", 100.0)
        self.assertEqual(result, 1)
        mock_cursor.callproc.assert_called()

    @patch('app.models.compra.DatabaseManager')
    def test_actualizar_compra(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_compra(1, 2, "Completada", 150.0)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.compra.DatabaseManager')
    def test_eliminar_compra(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_compra(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

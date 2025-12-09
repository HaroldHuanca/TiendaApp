import unittest
from unittest.mock import MagicMock, patch
from app.models.bonificacion import mostrar_bonificaciones, insertar_bonificacion, actualizar_bonificacion, eliminar_bonificacion

class TestBonificacionModel(unittest.TestCase):

    @patch('app.models.bonificacion.DatabaseManager')
    def test_mostrar_bonificaciones(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_bonificaciones(1)
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.bonificacion.DatabaseManager')
    def test_insertar_bonificacion(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        # Mocking fetchall to return a result then nothing (to break loop)
        mock_cursor.fetchall.side_effect = [[('Success',)], []]
        mock_cursor.nextset.return_value = False

        result = insertar_bonificacion(1, 1, 10.0)
        self.assertEqual(result, 'Success')
        mock_cursor.callproc.assert_called()

    @patch('app.models.bonificacion.DatabaseManager')
    def test_actualizar_bonificacion(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.side_effect = [[('Updated',)], []]
        mock_cursor.nextset.return_value = False

        result = actualizar_bonificacion(1, 1, 20.0)
        self.assertEqual(result, 'Updated')
        mock_cursor.callproc.assert_called()

    @patch('app.models.bonificacion.DatabaseManager')
    def test_eliminar_bonificacion(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.side_effect = [[('Deleted',)], []]
        mock_cursor.nextset.return_value = False

        result = eliminar_bonificacion(1, 1)
        self.assertEqual(result, 'Deleted')
        mock_cursor.callproc.assert_called()

if __name__ == '__main__':
    unittest.main()

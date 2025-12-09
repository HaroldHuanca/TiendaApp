import unittest
from unittest.mock import MagicMock, patch
from app.models.usuario import mostrar_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario, obtener_contrasena, reducir_intento, restablecer_intento, actualizar_mac

class TestUsuarioModel(unittest.TestCase):

    @patch('app.models.usuario.DatabaseManager')
    def test_mostrar_usuarios(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_usuarios()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_insertar_usuario(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db.connection.return_value = mock_connection
        mock_connection.connection.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.side_effect = [[(123,)], []]
        mock_cursor.nextset.return_value = False

        result = insertar_usuario("user", "pass", "mail", "mac", "estado")
        self.assertEqual(result, 123)
        mock_cursor.callproc.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_actualizar_usuario(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_usuario(1, "user", "pass", "estado")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_eliminar_usuario(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_usuario(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_obtener_contrasena(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = obtener_contrasena("user")
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_reducir_intento(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        reducir_intento("user")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_restablecer_intento(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        restablecer_intento("user")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.usuario.DatabaseManager')
    def test_actualizar_mac(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_mac("user", "new_mac")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

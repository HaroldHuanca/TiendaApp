import unittest
from unittest.mock import MagicMock, patch
from app.models.cliente import mostrar_clientes, insertar_cliente, actualizar_cliente, eliminar_cliente

class TestClienteModel(unittest.TestCase):

    @patch('app.models.cliente.DatabaseManager')
    def test_mostrar_clientes(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_clientes()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.cliente.DatabaseManager')
    def test_insertar_cliente(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_cliente("12345678", "Juan Perez", "Activo")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.cliente.DatabaseManager')
    def test_actualizar_cliente(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_cliente(1, "87654321", "Pedro Gomez", "Inactivo")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.cliente.DatabaseManager')
    def test_eliminar_cliente(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_cliente(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

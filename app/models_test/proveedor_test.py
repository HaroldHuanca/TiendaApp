import unittest
from unittest.mock import MagicMock, patch
from app.models.proveedor import mostrar_proveedores, insertar_proveedor, actualizar_proveedor, eliminar_proveedor

class TestProveedorModel(unittest.TestCase):

    @patch('app.models.proveedor.DatabaseManager')
    def test_mostrar_proveedores(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_proveedores()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.proveedor.DatabaseManager')
    def test_insertar_proveedor(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_proveedor("12345678901", "Proveedor", "Activo")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.proveedor.DatabaseManager')
    def test_actualizar_proveedor(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_proveedor(1, "10987654321", "Proveedor Modificado", "Activo")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.proveedor.DatabaseManager')
    def test_eliminar_proveedor(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_proveedor(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
from app.models.categoria import mostrar_categorias, insertar_categoria, actualizar_categoria

class TestCategoriaModel(unittest.TestCase):

    @patch('app.models.categoria.DatabaseManager')
    def test_mostrar_categorias(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_categorias()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.categoria.DatabaseManager')
    def test_insertar_categoria(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_categoria("Nueva Categoria")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.categoria.DatabaseManager')
    def test_actualizar_categoria(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_categoria(1, "Categoria Actualizada")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
from app.models.estado import mostrar_estados, insertar_estado, actualizar_estado

class TestEstadoModel(unittest.TestCase):

    @patch('app.models.estado.DatabaseManager')
    def test_mostrar_estados(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_estados("tabla")
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.estado.DatabaseManager')
    def test_insertar_estado(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_estado("tabla", 1, "descripcion")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.estado.DatabaseManager')
    def test_actualizar_estado(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_estado("tabla", 1, "descripcion")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

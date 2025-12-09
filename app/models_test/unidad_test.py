import unittest
from unittest.mock import MagicMock, patch
from app.models.unidad import mostrar_unidades, insertar_unidad, actualizar_unidad

class TestUnidadModel(unittest.TestCase):

    @patch('app.models.unidad.DatabaseManager')
    def test_mostrar_unidades(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_unidades()
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.unidad.DatabaseManager')
    def test_insertar_unidad(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_unidad("Unidad")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.unidad.DatabaseManager')
    def test_actualizar_unidad(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_unidad(1, "Unidad Modificada")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

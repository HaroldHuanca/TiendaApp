import unittest
from unittest.mock import MagicMock, patch
from app.models.venta_individual import mostrar_ventas_individuales, insertar_venta_individual, actualizar_venta_individual, eliminar_venta_individual

class TestVentaIndividualModel(unittest.TestCase):

    @patch('app.models.venta_individual.DatabaseManager')
    def test_mostrar_ventas_individuales(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_ventas_individuales("2023-01-01")
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.venta_individual.DatabaseManager')
    def test_insertar_venta_individual(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_venta_individual(1, 1, 5.0, 10.0, "2023-01-01")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.venta_individual.DatabaseManager')
    def test_actualizar_venta_individual(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_venta_individual(1, 1, 1, 10.0, 10.0, "2023-01-01")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.venta_individual.DatabaseManager')
    def test_eliminar_venta_individual(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_venta_individual(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

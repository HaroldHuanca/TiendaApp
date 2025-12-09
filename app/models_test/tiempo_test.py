import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.models.tiempo import obtener_fecha_actual

class TestTiempoModel(unittest.TestCase):

    @patch('app.models.tiempo.DatabaseManager')
    def test_obtener_fecha_actual(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        # Mocking fetchone to return a datetime object
        mock_date = datetime(2023, 1, 1, 12, 0, 0)
        mock_result.fetchone.return_value = (mock_date,)
        mock_db.execute.return_value = mock_result

        result = obtener_fecha_actual()
        self.assertEqual(result, "01/01/2023 12:00:00")
        mock_db.execute.assert_called()

if __name__ == '__main__':
    unittest.main()

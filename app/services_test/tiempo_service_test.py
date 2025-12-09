import unittest
from unittest.mock import MagicMock, patch
from app.services.tiempo_service import obtener_fecha_actual_formateada

class TestTiempoService(unittest.TestCase):

    @patch('app.services.tiempo_service.obtener_fecha_actual')
    def test_obtener_fecha_actual(self, mock_obtener):
        mock_obtener.return_value = "01/01/2023"
        result = obtener_fecha_actual_formateada()
        self.assertEqual(result, "01/01/2023")
        mock_obtener.assert_called()

if __name__ == '__main__':
    unittest.main()

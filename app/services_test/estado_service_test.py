import unittest
from unittest.mock import MagicMock, patch
from app.services.estado_service import mostrar_estados, insertar_estado, actualizar_estado

class TestEstadoService(unittest.TestCase):

    @patch('app.services.estado_service.estado_model.mostrar_estados')
    def test_mostrar_estados(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_estados("tabla")
        self.assertEqual(result, [])
        mock_mostrar.assert_called_with("tabla")

    @patch('app.services.estado_service.estado_model.insertar_estado')
    def test_insertar_estado(self, mock_insertar):
        insertar_estado("tabla", 1, "desc")
        mock_insertar.assert_called_with("tabla", 1, "desc")

    @patch('app.services.estado_service.estado_model.actualizar_estado')
    def test_actualizar_estado(self, mock_actualizar):
        actualizar_estado("tabla", 1, "desc")
        mock_actualizar.assert_called_with("tabla", 1, "desc")

if __name__ == '__main__':
    unittest.main()

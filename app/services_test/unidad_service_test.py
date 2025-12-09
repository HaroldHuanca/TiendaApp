import unittest
from unittest.mock import MagicMock, patch
from app.services.unidad_service import mostrar_unidades, insertar_unidad, actualizar_unidad

class TestUnidadService(unittest.TestCase):

    @patch('app.services.unidad_service.unidad_model.mostrar_unidades')
    def test_mostrar_unidades(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_unidades()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.unidad_service.unidad_model.insertar_unidad')
    def test_insertar_unidad(self, mock_insertar):
        insertar_unidad("Unidad")
        mock_insertar.assert_called_with("Unidad")

    @patch('app.services.unidad_service.unidad_model.actualizar_unidad')
    def test_actualizar_unidad(self, mock_actualizar):
        actualizar_unidad(1, "Unidad")
        mock_actualizar.assert_called_with(1, "Unidad")

if __name__ == '__main__':
    unittest.main()

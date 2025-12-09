import unittest
from unittest.mock import MagicMock, patch
from app.services.bonificacion_service import mostrar_bonificaciones, insertar_bonificacion, actualizar_bonificacion, eliminar_bonificacion

class TestBonificacionService(unittest.TestCase):

    @patch('app.services.bonificacion_service.bon.mostrar_bonificaciones')
    def test_mostrar_bonificaciones(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_bonificaciones(1)
        self.assertEqual(result, [])
        mock_mostrar.assert_called_with(1)

    @patch('app.services.bonificacion_service.bon.insertar_bonificacion')
    def test_insertar_bonificacion(self, mock_insertar):
        insertar_bonificacion(1, 1, 10.0)
        mock_insertar.assert_called_with(1, 1, 10.0)

    @patch('app.services.bonificacion_service.bon.actualizar_bonificacion')
    def test_actualizar_bonificacion(self, mock_actualizar):
        mock_actualizar.return_value = "Ok"
        result = actualizar_bonificacion(1, 1, 20.0)
        self.assertEqual(result, "Ok")
        mock_actualizar.assert_called_with(1, 1, 20.0)

    @patch('app.services.bonificacion_service.bon.eliminar_bonificacion')
    def test_eliminar_bonificacion(self, mock_eliminar):
        mock_eliminar.return_value = "Ok"
        result = eliminar_bonificacion(1, 1)
        self.assertEqual(result, "Ok")
        mock_eliminar.assert_called_with(1, 1)

if __name__ == '__main__':
    unittest.main()

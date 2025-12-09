import unittest
from unittest.mock import MagicMock, patch
from app.services.usuario_service import (
    mostrar_usuarios, insertar_usuario, actualizar_usuario, eliminar_usuario,
    obtener_contrasena, reducir_intento, restablecer_intento, actualizar_mac
)

class TestUsuarioService(unittest.TestCase):

    @patch('app.services.usuario_service.usuario_model.mostrar_usuarios')
    def test_mostrar_usuarios(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_usuarios()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.usuario_service.usuario_model.insertar_usuario')
    def test_insertar_usuario(self, mock_insertar):
        mock_insertar.return_value = 1
        # Provide valid data to pass validation
        result = insertar_usuario("usuario", "password123", "test@test.com", "00:00:00:00:00:00", "Activo")
        self.assertEqual(result, 1)
        mock_insertar.assert_called()

    @patch('app.services.usuario_service.usuario_model.actualizar_usuario')
    def test_actualizar_usuario(self, mock_actualizar):
        actualizar_usuario(1, "usuario", "password123", "Activo")
        mock_actualizar.assert_called()

    @patch('app.services.usuario_service.usuario_model.eliminar_usuario')
    def test_eliminar_usuario(self, mock_eliminar):
        eliminar_usuario(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

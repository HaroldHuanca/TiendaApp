import unittest
from unittest.mock import MagicMock, patch
from app.services.cliente_service import mostrar_clientes, insertar_cliente, actualizar_cliente, eliminar_cliente

class TestClienteService(unittest.TestCase):

    @patch('app.services.cliente_service.cli.mostrar_clientes')
    def test_mostrar_clientes(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_clientes()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.cliente_service.cli.insertar_cliente')
    def test_insertar_cliente(self, mock_insertar):
        insertar_cliente("123", "Juan", "Activo")
        mock_insertar.assert_called_with("123", "Juan", "Activo")

    @patch('app.services.cliente_service.cli.actualizar_cliente')
    def test_actualizar_cliente(self, mock_actualizar):
        actualizar_cliente(1, "123", "Juan", "Activo")
        mock_actualizar.assert_called_with(1, "123", "Juan", "Activo")

    @patch('app.services.cliente_service.cli.eliminar_cliente')
    def test_eliminar_cliente(self, mock_eliminar):
        eliminar_cliente(1)
        mock_eliminar.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()

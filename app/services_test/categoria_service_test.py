import unittest
from unittest.mock import MagicMock, patch
from app.services.categoria_service import mostrar_categorias, insertar_categoria, actualizar_categoria

class TestCategoriaService(unittest.TestCase):

    @patch('app.services.categoria_service.cat.mostrar_categorias')
    def test_mostrar_categorias(self, mock_mostrar):
        mock_mostrar.return_value = []
        result = mostrar_categorias()
        self.assertEqual(result, [])
        mock_mostrar.assert_called()

    @patch('app.services.categoria_service.cat.insertar_categoria')
    def test_insertar_categoria(self, mock_insertar):
        insertar_categoria("Categoria")
        mock_insertar.assert_called_with("Categoria")

    @patch('app.services.categoria_service.cat.actualizar_categoria')
    def test_actualizar_categoria(self, mock_actualizar):
        actualizar_categoria(1, "Categoria")
        mock_actualizar.assert_called_with(1, "Categoria")

if __name__ == '__main__':
    unittest.main()

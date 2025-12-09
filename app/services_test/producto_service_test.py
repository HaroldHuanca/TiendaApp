import unittest
from unittest.mock import MagicMock, patch
from app.services.producto_service import (
    obtener_productos_actualizados, insertar_producto, actualizar_producto,
    eliminar_producto, buscar_id_por_codigo_barras, mostrar_productos_paginado,
    obtener_conteo_productos
)

class TestProductoService(unittest.TestCase):

    @patch('app.services.producto_service.producto_model.obtener_productos_actualizados')
    def test_obtener_productos_actualizados(self, mock_obtener):
        mock_obtener.return_value = []
        result = obtener_productos_actualizados("2023-01-01")
        self.assertEqual(result, [])
        mock_obtener.assert_called_with("2023-01-01")

    @patch('app.services.producto_service.producto_model.insertar_producto')
    def test_insertar_producto(self, mock_insertar):
        # Providing valid data
        insertar_producto("CODE-123", "Unidad", "Categoria", "Desc", 10.0, 20.0, 100.0, 10.0, "Estado")
        mock_insertar.assert_called()

    @patch('app.services.producto_service.producto_model.actualizar_producto')
    def test_actualizar_producto(self, mock_actualizar):
        actualizar_producto(1, "CODE-123", "Unidad", "Categoria", "Desc", 10.0, 20.0, 100.0, 10.0, "Estado")
        mock_actualizar.assert_called()

    @patch('app.services.producto_service.producto_model.eliminar_producto')
    def test_eliminar_producto(self, mock_eliminar):
        eliminar_producto(1)
        mock_eliminar.assert_called_with(1)

    @patch('app.services.producto_service.producto_model.buscar_id_por_codigo_barras')
    def test_buscar_id_por_codigo_barras(self, mock_buscar):
        mock_buscar.return_value = 1
        result = buscar_id_por_codigo_barras("CODE-123")
        self.assertEqual(result, 1)
        mock_buscar.assert_called_with("CODE-123")

if __name__ == '__main__':
    unittest.main()

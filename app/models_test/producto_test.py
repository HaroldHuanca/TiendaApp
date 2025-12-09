import unittest
from unittest.mock import MagicMock, patch
from app.models.producto import (
    obtener_productos_actualizados, insertar_producto, actualizar_producto,
    eliminar_producto, buscar_id_por_codigo_barras, mostrar_productos_paginado,
    obtener_conteo_productos
)

class TestProductoModel(unittest.TestCase):

    @patch('app.models.producto.DatabaseManager')
    def test_obtener_productos_actualizados(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = obtener_productos_actualizados("2023-01-01")
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.producto.DatabaseManager')
    def test_insertar_producto(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        insertar_producto("123", "Unidad", "Cat", "Desc", 10.0, 15.0, 100.0, 10.0, "Estado")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.producto.DatabaseManager')
    def test_actualizar_producto(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        actualizar_producto(1, "123", 1, 1, "Desc", 10.0, 15.0, 100.0, 10.0, "Estado")
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.producto.DatabaseManager')
    def test_eliminar_producto(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        
        eliminar_producto(1)
        mock_db.execute.assert_called()
        mock_db.commit.assert_called()

    @patch('app.models.producto.DatabaseManager')
    def test_buscar_id_por_codigo_barras(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1
        # Second execute return value (SELECT @p_id)
        mock_db.execute.side_effect = [None, mock_result]

        result = buscar_id_por_codigo_barras("123")
        self.assertEqual(result, 1)

    @patch('app.models.producto.DatabaseManager')
    def test_mostrar_productos_paginado(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_db.execute.return_value = mock_result

        result = mostrar_productos_paginado(10, 0)
        self.assertEqual(result, [])
        mock_db.execute.assert_called()

    @patch('app.models.producto.DatabaseManager')
    def test_obtener_conteo_productos(self, MockDatabaseManager):
        mock_db = MockDatabaseManager.return_value.__enter__.return_value
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (50,)
        mock_db.execute.return_value = mock_result

        result = obtener_conteo_productos()
        self.assertEqual(result, 50)
        mock_db.execute.assert_called()

if __name__ == '__main__':
    unittest.main()

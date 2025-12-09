import unittest
from app.services.validaciones import validar_id_tinyint, validar_descripcion, validar_fecha

class TestValidaciones(unittest.TestCase):
    def test_validar_id(self):
        validar_id_tinyint(1)
        with self.assertRaises(ValueError):
            validar_id_tinyint(0)
        with self.assertRaises(ValueError):
            validar_id_tinyint(300)

    def test_validar_descripcion(self):
        validar_descripcion("Valid")
        with self.assertRaises(ValueError):
            validar_descripcion("")
        with self.assertRaises(ValueError):
            validar_descripcion("Invalid@Char")

    def test_validar_fecha(self):
        validar_fecha("2023-01-01")
        with self.assertRaises(ValueError):
            validar_fecha("01-01-2023")

if __name__ == '__main__':
    unittest.main()

# test_conteo_productos.py

from app.models.producto import obtener_conteo_productos

def main():
    try:
        total = obtener_conteo_productos()
        print(f"✅ Total de productos: {total}")
    except Exception as e:
        print(f"❌ Error al obtener el conteo de productos: {e}")

if __name__ == "__main__":
    main()

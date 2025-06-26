# test_conteo_productos.py

from producto import obtener_conteo_productos

def main():
    total = obtener_conteo_productos()
    print(f"✅ Total de productos: {total}")
    
if __name__ == "__main__":
    main()

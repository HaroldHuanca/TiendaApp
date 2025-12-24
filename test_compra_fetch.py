from app.services import compra_service, compra_detalle_service
import json

def test_fetch_compra():
    id_compra = 1
    print(f"Testing fetch for compra ID: {id_compra}")
    try:
        cabecera = compra_service.obtener_compra_por_id(id_compra)
        print("Cabecera fetched:", json.dumps(cabecera, indent=2, default=str))
        
        if not cabecera:
            print("Error: Compra not found")
            return

        detalles = compra_detalle_service.obtener_detalles_con_productos(id_compra)
        print(f"Detalles fetched: {len(detalles)} items")
        print(json.dumps(detalles, indent=2, default=str))

        print("\nSuccess: Fetch completed without errors.")
    except Exception as e:
        print(f"\nFailed: {str(e)}")

if __name__ == "__main__":
    test_fetch_compra()

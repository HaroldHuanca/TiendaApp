from datetime import datetime
from app.services.venta_service import (
    mostrar_ventas,
    insertar_venta,
    actualizar_venta,
    eliminar_venta
)

def menu_ventas():
    while True:
        print("\n--- Menú de Ventas ---")
        print("1. Mostrar todas las ventas")
        print("2. Insertar nueva venta")
        print("3. Actualizar una venta")
        print("4. Eliminar (anular) una venta")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            try:
                ventas = mostrar_ventas()
                if ventas:
                    print("\nVentas registradas:")
                    for venta in ventas:
                        print(venta)
                else:
                    print("No hay ventas registradas.")
            except Exception as e:
                print("❌ Error al mostrar ventas:", e)

        elif opcion == "2":
            try:
                id_serie = int(input("ID de serie: "))
                id_usuario = int(input("ID de usuario: "))
                id_cliente = int(input("ID del cliente: "))
                descripcion_estado = input("Estado (ej. ACTIVO): ")
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                total = float(input("Total: "))

                nuevo_id = insertar_venta(id_serie, id_usuario, id_cliente, descripcion_estado, fecha, total)
                print(f"✅ Venta insertada con ID: {nuevo_id}")
            except Exception as e:
                print("❌ Error al insertar venta:", e)

        elif opcion == "3":
            try:
                id = int(input("ID de la venta a actualizar: "))
                id_cliente = int(input("Nuevo ID de cliente: "))
                descripcion_estado = input("Nuevo estado: ")
                total = float(input("Nuevo total: "))

                actualizar_venta(id, id_cliente, descripcion_estado, total)
                print("✅ Venta actualizada correctamente.")
            except Exception as e:
                print("❌ Error al actualizar venta:", e)

        elif opcion == "4":
            try:
                id = int(input("ID de la venta a eliminar: "))
                eliminar_venta(id)
                print("✅ Venta eliminada (anulada) correctamente.")
            except Exception as e:
                print("❌ Error al eliminar venta:", e)

        elif opcion == "0":
            print("Saliendo del menú de ventas...")
            break

        else:
            print("⚠️ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_ventas()

from app.services.venta_detalle_service import (
    mostrar_detalles_venta,
    insertar_detalle_venta,
    actualizar_detalle_venta,
    eliminar_detalle_venta
)

def menu_detalles_venta():
    while True:
        print("\n--- Menú Detalle de Venta ---")
        print("1. Mostrar detalles de venta")
        print("2. Insertar detalle de venta")
        print("3. Actualizar detalle de venta")
        print("4. Eliminar (anular) detalle de venta")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            try:
                id_venta = int(input("ID de venta: "))
                detalles = mostrar_detalles_venta(id_venta)
                if detalles:
                    print("\nDetalles de la venta:")
                    for d in detalles:
                        print(d)
                else:
                    print("No se encontraron detalles.")
            except Exception as e:
                print("❌ Error al mostrar detalles:", e)

        elif opcion == "2":
            try:
                id_venta = int(input("ID de venta: "))
                id_producto = int(input("ID del producto: "))
                cantidad = float(input("Cantidad: "))
                precio_venta = float(input("Precio de venta: "))
                descuento = float(input("Descuento: "))
                descripcion_estado = input("Estado (ej. ACTIVO): ")

                insertar_detalle_venta(id_venta, id_producto, cantidad, precio_venta, descuento, descripcion_estado)
                print("✅ Detalle de venta insertado correctamente.")
            except Exception as e:
                print("❌ Error al insertar:", e)

        elif opcion == "3":
            try:
                id_venta = int(input("ID de venta: "))
                id_producto = int(input("ID del producto: "))
                cantidad = float(input("Cantidad nueva: "))
                precio_venta = float(input("Precio de venta nuevo: "))
                descuento = float(input("Descuento nuevo: "))
                descripcion_estado = input("Estado nuevo (ej. ACTIVO): ")

                actualizar_detalle_venta(id_venta, id_producto, cantidad, precio_venta, descuento, descripcion_estado)
                print("✅ Detalle de venta actualizado correctamente.")
            except Exception as e:
                print("❌ Error al actualizar:", e)

        elif opcion == "4":
            try:
                id_venta = int(input("ID de venta: "))
                id_producto = int(input("ID del producto: "))
                eliminar_detalle_venta(id_venta, id_producto)
                print("✅ Detalle de venta eliminado (anulado) correctamente.")
            except Exception as e:
                print("❌ Error al eliminar:", e)

        elif opcion == "0":
            print("Saliendo del menú...")
            break

        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_detalles_venta()

from models.producto import (
    obtener_productos_actualizados,
    insertar_producto,
    actualizar_producto,
    eliminar_producto,
    buscar_id_por_codigo_barras
)

def menu_productos():
    while True:
        print("\n--- MENÚ DE PRODUCTOS ---")
        print("1. Obtener productos actualizados desde una fecha")
        print("2. Insertar nuevo producto")
        print("3. Actualizar producto")
        print("4. Eliminar (alternar estado) producto")
        print("5. Buscar ID por código de barras")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            fecha = input("Ingresa la fecha y hora (formato 'YYYY-MM-DD HH:MM:SS'): ")
            productos = obtener_productos_actualizados(fecha)
            if productos:
                for p in productos:
                    print(f"ID: {p['Id']} | Descripcion: {p['Descripcion']} | Stock: {p['Stock']} | Estado: {p['Estado']}")
            else:
                print("No hay productos actualizados desde esa fecha.")

        elif opcion == "2":
            cb = input("Código de barras: ")
            id_unidad = int(input("ID unidad: "))
            id_categoria = int(input("ID categoría: "))
            descripcion = input("Descripción: ")
            precio_compra = float(input("Precio de compra: "))
            precio_venta = float(input("Precio de venta: "))
            stock = float(input("Stock: "))
            stock_minimo = float(input("Stock mínimo: "))
            estado = input("Estado (activo/inactivo): ")
            insertar_producto(cb, id_unidad, id_categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, estado)
            print("✅ Producto insertado.")

        elif opcion == "3":
            id_producto = int(input("ID del producto a actualizar: "))
            cb = input("Nuevo código de barras: ")
            id_unidad = int(input("Nuevo ID unidad: "))
            id_categoria = int(input("Nuevo ID categoría: "))
            descripcion = input("Nueva descripción: ")
            precio_compra = float(input("Nuevo precio de compra: "))
            precio_venta = float(input("Nuevo precio de venta: "))
            stock = float(input("Nuevo stock: "))
            stock_minimo = float(input("Nuevo stock mínimo: "))
            estado = input("Nuevo estado (activo/inactivo): ")
            actualizar_producto(id_producto, cb, id_unidad, id_categoria, descripcion, precio_compra, precio_venta, stock, stock_minimo, estado)
            print("✅ Producto actualizado.")

        elif opcion == "4":
            id_producto = int(input("ID del producto a eliminar (alternar estado): "))
            eliminar_producto(id_producto)
            print("✅ Producto eliminado (estado alternado).")

        elif opcion == "5":
            cb = input("Código de barras: ")
            id_encontrado = buscar_id_por_codigo_barras(cb)
            print(f"ID encontrado: {id_encontrado}")

        elif opcion == "6":
            print("Saliendo del menú.")
            break

        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_productos()

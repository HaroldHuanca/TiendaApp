from app.services.cliente_service import (
    mostrar_clientes,
    insertar_cliente,
    actualizar_cliente,
    eliminar_cliente
)

def menu_clientes():
    while True:
        print("\n--- MENÚ DE CLIENTES ---")
        print("1. Mostrar todos los clientes")
        print("2. Insertar nuevo cliente")
        print("3. Actualizar cliente existente")
        print("4. Eliminar (alternar estado) cliente")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            clientes = mostrar_clientes()
            if clientes:
                for c in clientes:
                    print(f"ID: {c['Id']} | Documento: {c['Documento']} | Nombre: {c['Nombre']} | Estado: {c['Estado']}")
            else:
                print("No hay clientes registrados.")
        
        elif opcion == "2":
            doc = input("Documento: ")
            nombre = input("Nombre: ")
            estado = input("Estado (activo/inactivo): ")
            insertar_cliente(doc, nombre, estado)
            print("✅ Cliente insertado.")
        
        elif opcion == "3":
            id_cliente = int(input("ID del cliente a actualizar: "))
            doc = input("Nuevo documento: ")
            nombre = input("Nuevo nombre: ")
            estado = input("Nuevo estado (activo/inactivo): ")
            actualizar_cliente(id_cliente, doc, nombre, estado)
            print("✅ Cliente actualizado.")
        
        elif opcion == "4":
            id_cliente = int(input("ID del cliente a eliminar (alternar estado): "))
            eliminar_cliente(id_cliente)
            print("✅ Cliente eliminado (estado alternado).")
        
        elif opcion == "5":
            print("Saliendo del menú.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_clientes()

from models.estado import (
    mostrar_estados,
    insertar_estado,
    actualizar_estado
)

def menu_estados():
    while True:
        print("\n--- MENÚ DE ESTADOS ---")
        print("1. Mostrar estados por nombre de tabla")
        print("2. Insertar nuevo estado")
        print("3. Actualizar descripción de estado")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            tabla = input("Nombre de la tabla: ")
            estados = mostrar_estados(tabla)
            if estados:
                for est in estados:
                    print(f"Estado: {est['estado']} | Descripción: {est['descripcion']}")
            else:
                print("No se encontraron estados.")

        elif opcion == "2":
            tabla = input("Nombre de la tabla: ")
            estado = int(input("Código del estado (entero): "))
            descripcion = input("Descripción del estado: ")
            insertar_estado(tabla, estado, descripcion)
            print("✅ Estado insertado correctamente.")

        elif opcion == "3":
            tabla = input("Nombre de la tabla: ")
            estado = int(input("Código del estado a actualizar: "))
            descripcion = input("Nueva descripción: ")
            actualizar_estado(tabla, estado, descripcion)
            print("✅ Estado actualizado correctamente.")

        elif opcion == "4":
            print("Saliendo del menú.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_estados()

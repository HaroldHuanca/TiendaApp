from app.models.unidad import (
    mostrar_unidades,
    insertar_unidad,
    actualizar_unidad
)

def menu_unidades():
    while True:
        print("\n--- MENÚ DE UNIDADES ---")
        print("1. Mostrar todas las unidades")
        print("2. Insertar nueva unidad")
        print("3. Actualizar unidad")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            unidades = mostrar_unidades()
            if unidades:
                for u in unidades:
                    print(f"ID: {u['id']} | Nombre: {u['nombre']}")
            else:
                print("No hay unidades registradas.")
        elif opcion == "2":
            nombre = input("Ingrese el nombre de la unidad: ")
            try:
                insertar_unidad(nombre)
                print("✅ Unidad insertada exitosamente.")
            except Exception as e:
                print(f"❌ Error al insertar unidad: {e}")
        elif opcion == "3":
            try:
                id_unidad = int(input("ID de la unidad a actualizar: "))
                nombre = input("Nuevo nombre de la unidad: ")
                actualizar_unidad(id_unidad, nombre)
                print("✅ Unidad actualizada correctamente.")
            except Exception as e:
                print(f"❌ Error al actualizar unidad: {e}")
        elif opcion == "4":
            print("Saliendo del menú de unidades.")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu_unidades()

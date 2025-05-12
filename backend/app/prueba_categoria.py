# main.py
from models.categoria import (
    mostrar_categorias,
    insertar_categoria,
    actualizar_categoria,
    obtener_fecha_actual,
)

def menu():
    while True:
        print("\n--- MENÚ DE CATEGORÍAS ---")
        print("1. Mostrar todas las categorías")
        print("2. Insertar una nueva categoría")
        print("3. Actualizar una categoría")
        print("4. Obtener fecha actual del servidor")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            categorias = mostrar_categorias()
            if categorias:
                print("\nCategorías:")
                for cat in categorias:
                    print(f"ID: {cat['id']} | Nombre: {cat['nombre']}")
            else:
                print("No hay categorías registradas.")
        
        elif opcion == "2":
            nombre = input("Ingresa el nombre de la nueva categoría: ")
            insertar_categoria(nombre)
            print("✅ Categoría insertada con éxito.")
        
        elif opcion == "3":
            try:
                id_categoria = int(input("Ingresa el ID de la categoría a actualizar: "))
                nuevo_nombre = input("Ingresa el nuevo nombre de la categoría: ")
                actualizar_categoria(id_categoria, nuevo_nombre)
                print("✅ Categoría actualizada con éxito.")
            except ValueError:
                print("⚠️ ID inválido.")
        
        elif opcion == "4":
            fecha = obtener_fecha_actual()
            if fecha:
                print(f"🕒 Fecha y hora actual del servidor: {fecha}")
            else:
                print("⚠️ No se pudo obtener la fecha.")
        
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        
        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    menu()

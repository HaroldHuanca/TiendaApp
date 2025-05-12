from typing import Any
from models.proveedor import (
    mostrar_proveedores,
    insertar_proveedor,
    actualizar_proveedor,
    eliminar_proveedor
)

def menu_proveedores():
    while True:
        print("\n--- MENÚ DE PROVEEDORES ---")
        print("1. Mostrar todos los proveedores")
        print("2. Insertar nuevo proveedor")
        print("3. Actualizar proveedor")
        print("4. Eliminar (alternar estado) de proveedor")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            proveedores = mostrar_proveedores()
            if proveedores:
                for p in proveedores:
                    print(f"ID: {p['Id']} | RUC: {p['RUC']} | Nombre: {p['Nombre']} | Estado: {p['Estado']}")
            else:
                print("No hay proveedores registrados.")
        elif opcion == "2":
            ruc = input("Ingrese RUC: ")
            nombre = input("Ingrese nombre del proveedor: ")
            estado = input("Ingrese descripción del estado (por ejemplo: activo, inactivo): ")
            try:
                insertar_proveedor(ruc, nombre, estado)
                print("✅ Proveedor insertado exitosamente.")
            except Exception as e:
                print(f"❌ Error al insertar: {e}")
        elif opcion == "3":
            try:
                id_proveedor = int(input("ID del proveedor a actualizar: "))
                ruc = input("Nuevo RUC: ")
                nombre = input("Nuevo nombre: ")
                estado = input("Nueva descripción del estado: ")
                actualizar_proveedor(id_proveedor, ruc, nombre, estado)
                print("✅ Proveedor actualizado correctamente.")
            except Exception as e:
                print(f"❌ Error al actualizar: {e}")
        elif opcion == "4":
            try:
                id_proveedor = int(input("ID del proveedor a eliminar (alternar estado): "))
                eliminar_proveedor(id_proveedor)
                print("✅ Proveedor eliminado (estado alternado).")
            except Exception as e:
                print(f"❌ Error al eliminar: {e}")
        elif opcion == "5":
            print("Saliendo del menú de proveedores.")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu_proveedores()

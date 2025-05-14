from app.models.usuario import (
    mostrar_usuarios,
    insertar_usuario,
    actualizar_usuario,
    eliminar_usuario,
    obtener_contrasena,
    reducir_intento,
    restablecer_intento
)

def menu_usuarios():
    while True:
        print("\n--- MENÚ DE USUARIOS ---")
        print("1. Mostrar todos los usuarios")
        print("2. Insertar nuevo usuario")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Obtener contraseña y estado")
        print("6. Reducir intento")
        print("7. Restablecer intentos")
        print("8. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            usuarios = mostrar_usuarios()
            if usuarios:
                for u in usuarios:
                    print(f"ID: {u['Id']} | Usuario: {u['Nombre Usuario']} | Estado: {u['Descripcion']}")            
            else:
                print("No hay usuarios registrados.")
        
        elif opcion == "2":
            nombre = input("Nombre de usuario: ")
            contrasena = input("Contraseña: ")
            correo = input("Correo: ")
            mac = input("Dirección MAC: ")
            estado = input("Descripción del estado: ")
            #try:
            nuevo_id = insertar_usuario(nombre, contrasena, correo, mac, estado)
            print(f"✅ Usuario insertado exitosamente con ID: {nuevo_id}")
            #except Exception as e:
             #   print(f"❌ Error al insertar usuario: {e}")

        elif opcion == "3":
            try:
                id_usuario = int(input("ID del usuario a actualizar: "))
                nombre = input("Nuevo nombre de usuario: ")
                contrasena = input("Nueva contraseña: ")
                estado = input("Nueva descripción del estado: ")
                actualizar_usuario(id_usuario, nombre, contrasena, estado)
                print("✅ Usuario actualizado exitosamente.")
            except Exception as e:
                print(f"❌ Error al actualizar usuario: {e}")
        
        elif opcion == "4":
            try:
                id_usuario = int(input("ID del usuario a eliminar (cambiar estado): "))
                eliminar_usuario(id_usuario)
                print("✅ Usuario eliminado (estado cambiado).")
            except Exception as e:
                print(f"❌ Error al eliminar usuario: {e}")

        elif opcion == "5":
            nombre = input("Nombre del usuario: ")
            resultado = obtener_contrasena(nombre)
            if resultado:
                for u in resultado:
                    print(f"ID: {u['Id']} | Contraseña: {u['Contraseña']} | Estado: {u['Estado']}")            
            else:
                print("No hay usuarios registrados.")

        elif opcion == "6":
            nombre = input("Nombre del usuario: ")
            try:
                reducir_intento(nombre)
                print("✅ Intento reducido correctamente.")
            except Exception as e:
                print(f"❌ Error al reducir intento: {e}")
        
        elif opcion == "7":
            nombre = input("Nombre del usuario: ")
            try:
                restablecer_intento(nombre)
                print("✅ Intentos restablecidos correctamente.")
            except Exception as e:
                print(f"❌ Error al restablecer intentos: {e}")
        
        elif opcion == "8":
            print("Saliendo del menú de usuarios.")
            break
        
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu_usuarios()
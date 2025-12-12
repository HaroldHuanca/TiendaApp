# Configuración de Sesiones para LAN - TiendaApp

## Cambios Realizados

Se han modificado las configuraciones de sesiones de Flask para que la aplicación funcione correctamente cuando se accede desde múltiples dispositivos en la misma red local (LAN).

### Cambios principales:

1. **SESSION_COOKIE_SECURE = False**
   - Permite que las cookies de sesión funcionen con HTTP (no requiere HTTPS)
   - Necesario para redes LAN internas

2. **SESSION_COOKIE_SAMESITE = 'Lax'**
   - Permite que las cookies se envíen en peticiones desde otros dispositivos
   - Proporciona protección contra CSRF mientras permite el acceso desde la LAN

3. **session.permanent = True**
   - Las sesiones ahora persisten durante toda la duración configurada (1 hora por defecto)
   - Evita que el usuario sea redirigido al login después de cada petición

4. **Archivo config.py**
   - Nueva configuración centralizada que permite cambiar entre LAN y Production fácilmente
   - LANConfig: Para desarrollo local (HTTP)
   - ProductionConfig: Para producción (HTTPS requerido)

## Cómo acceder desde otros dispositivos

### Paso 1: Obtener la IP del servidor
En la máquina del servidor, ejecuta:
```bash
hostname -I
```
O en Windows:
```cmd
ipconfig
```

Busca la IP de la red local (generalmente empieza con 192.168 o 10.)

### Paso 2: Acceder desde otro dispositivo
Desde cualquier dispositivo en la LAN, abre un navegador y ve a:
```
http://TU_IP_SERVIDOR:5000
```

Ejemplo:
```
http://192.168.1.100:5000
```

### Paso 3: Iniciar sesión
- Usa las credenciales normales
- La sesión se mantendrá activa durante 1 hora
- Podrás navegar sin ser redirigido al login

## Troubleshooting

### Si aún así se redirige al login:
1. **Borra las cookies del navegador**
   - Abre DevTools (F12)
   - Vete a Application → Cookies
   - Elimina todas las cookies de tu sitio

2. **Verifica que estés usando la IP correcta**
   - No uses localhost o 127.0.0.1 desde otros dispositivos
   - Usa la IP real de la red

3. **Reinicia el servidor**
   - Detén Flask (Ctrl+C)
   - Ejecuta nuevamente: `python main.py`

4. **Verifica el firewall**
   - Asegúrate que el puerto 5000 no esté bloqueado
   - Intenta acceder desde otro dispositivo en la red

## Configuración de Producción

Si necesitas cambiar a configuración de producción con HTTPS, modifica el inicio en `main.py`:

```python
if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
    # Y cambia en create_app(): app.config.from_object(ProductionConfig)
```

## Duración de Sesión

La sesión dura 1 hora por defecto. Para cambiar esto, modifica en `config.py`:

```python
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Cambiar a 2 horas
```

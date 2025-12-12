# 🔧 Sidebar Mobile - Troubleshooting

## ¿Por qué no funciona el toggle?

Si el botón hamburguesa no funciona en tu teléfono, sigue estos pasos:

### Paso 1: Verificar en el navegador (DevTools)

1. Abre DevTools (F12)
2. Activa el modo móvil (Ctrl+Shift+M o Cmd+Shift+M)
3. Selecciona un dispositivo móvil
4. Abre la consola (pestaña Console)
5. Debería ver un log así:
   ```
   Sidebar inicializado: {
     sidebar: true,
     sidebarToggle: true,
     sidebarOverlay: true,
     linksCount: 7
   }
   ```

### Paso 2: Si ves `false` en algún campo

Significa que ese elemento no existe en el DOM. Posibles causas:

- **sidebar: false** → El componente sidebar.html no se incluyó
- **sidebarToggle: false** → El botón hamburguesa en header.html no tiene `id="sidebarToggle"`
- **sidebarOverlay: false** → El overlay no se agregó al sidebar.html

### Paso 3: Prueba manual en DevTools

En la consola, ejecuta:
```javascript
// Ver si los elementos existen
document.getElementById('sidebarToggle')
document.getElementById('sidebar')
document.getElementById('sidebarOverlay')

// Probar el toggle manualmente
document.getElementById('sidebar').classList.toggle('active')
document.getElementById('sidebarOverlay').classList.toggle('active')
```

### Paso 4: Verificar el CSS

En DevTools, selecciona el sidebar y verifica en Styles:
- `position: fixed` ✓
- `z-index: 1040` ✓
- `transform: translateX(-100%)` (móvil)
- `transform: translateX(0)` (cuando está activo)

## Pasos para Fijar

### Si el problema persiste:

1. **Limpia el caché del navegador**
   - Ctrl+Shift+Delete
   - Borra todo
   - Actualiza la página

2. **Reinicia el servidor Flask**
   ```bash
   # En terminal, presiona Ctrl+C
   Ctrl+C
   # Luego inicia de nuevo
   python main.py
   ```

3. **Verifica que los archivos estén guardados**
   - Revisa que sidebar.html tenga el `id="sidebarOverlay"`
   - Revisa que header.html tenga `id="sidebarToggle"`
   - Revisa que estilos.css tenga `.sidebar-overlay`

4. **Usa mode Device Emulation real**
   - En DevTools: Device Emulation
   - Selecciona "iPhone 12" o "Pixel 5"
   - Recarga la página

5. **Prueba en un teléfono real**
   - Abre http://TU_IP:5000 en el navegador del teléfono
   - Verifica que el puerto sea accesible (firewall)

## Debug en Producción (Teléfono Real)

1. En tu teléfono, abre DevTools (varía según navegador)
   - Chrome: Menu → More tools → Developer tools
   - Firefox: Menu → More → Developer tools

2. Abre la pestaña Console

3. Debería ver los logs del JavaScript

4. Si hay error, anótalo y revisa los pasos anteriores

## Solución Nuclear 💣

Si nada funciona:

```bash
# 1. Para el servidor
Ctrl+C

# 2. Limpia caché de Python
rm -rf app/__pycache__ app/*/__pycache__

# 3. Inicia nuevamente
python main.py
```

Luego en el navegador:
- Abre DevTools (F12)
- Pestaña Network
- Marca "Disable cache"
- Ctrl+Shift+R (reload sin caché)

## Archivos Involucrados

Asegúrate que estos archivos estén correctamente:

- `/app/templates/components/sidebar.html` → Contiene el script
- `/app/templates/components/header.html` → Debe tener `id="sidebarToggle"`
- `/app/static/css/estilos.css` → Contiene `.sidebar-overlay` y media queries
- `/app/templates/base.html` → Incluye sidebar y header

## Verificación Rápida

Copia y pega esto en la consola del navegador:

```javascript
const sidebar = document.getElementById('sidebar');
const toggle = document.getElementById('sidebarToggle');
const overlay = document.getElementById('sidebarOverlay');

console.table({
  'Sidebar existe': !!sidebar,
  'Toggle existe': !!toggle,
  'Overlay existe': !!overlay,
  'Ancho pantalla': window.innerWidth,
  'Es móvil (≤768px)': window.innerWidth <= 768,
  'Sidebar active': sidebar?.classList.contains('active'),
  'Overlay active': overlay?.classList.contains('active')
});
```

Esto mostrará una tabla con el estado actual.

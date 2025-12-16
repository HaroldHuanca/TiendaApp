# Migración a Librerías Locales - TiendaApp

## Resumen
Se han descargado y migrado todas las librerías externas (CDN) a versiones locales para permitir el funcionamiento sin conexión a internet.

## Librerías Descargadas

### 1. SweetAlert2 (v11.10.0)
- **CSS**: `/app/static/css/sweetalert2.min.css` (24KB)
- **JS**: `/app/static/js/sweetalert2.all.min.js` (75KB)
- **Origen**: https://cdn.jsdelivr.net/npm/sweetalert2@11.10.0/

### 2. Google Fonts - Inter
- **CSS**: `/app/static/fonts/inter-font.css` (815B)
- **Fuentes TTF**: 
  - `inter-300.ttf` (319KB) - Light
  - `inter-400.ttf` (318KB) - Regular
  - `inter-500.ttf` (318KB) - Medium
  - `inter-600.ttf` (319KB) - SemiBold
  - `inter-700.ttf` (319KB) - Bold
- **Origen**: https://fonts.googleapis.com/

## Cambios Realizados

### Archivos Modificados

#### 1. **Head Component** (`app/templates/components/head.html`)
- Reemplazó referencias a Google Fonts CDN por referencia local
- Agregó referencia a `sweetalert2.min.css`
- Removió preconnect headers a fonts.googleapis.com y fonts.gstatic.com

#### 2. **Login Template** (`app/templates/login.html`)
- Removió preconnect headers
- Reemplazó referencia de Google Fonts CDN por referencia local

#### 3. **Templates de Listas** (removidas referencias CDN redundantes)
- `clientes_lista.html`
- `proveedores_lista.html`
- `categorias_lista.html`
- `unidades_lista.html`
- `productos_listar.html`

Removidas las referencias a CDN de SweetAlert2 ya que ahora se cargan desde el `head.html` centralizado.

### Verificación
✅ No hay referencias a URLs externas en los archivos HTML
✅ Todas las librerías CSS están en `head.html`
✅ Todos los scripts JS están en `footer.html`
✅ Las fuentes están alojadas localmente

## Estructura Final de Carpetas

```
app/static/
├── css/
│   ├── bootstrap.min.css (existente)
│   ├── estilos.css (existente)
│   └── sweetalert2.min.css (nuevo)
├── js/
│   ├── bootstrap.bundle.min.js (existente)
│   └── sweetalert2.all.min.js (nuevo)
└── fonts/
    ├── inter-font.css (nuevo)
    ├── inter-300.ttf (nuevo)
    ├── inter-400.ttf (nuevo)
    ├── inter-500.ttf (nuevo)
    ├── inter-600.ttf (nuevo)
    └── inter-700.ttf (nuevo)
```

## Notas
- El proyecto ahora es completamente independiente de conexiones a internet
- Todas las librerías son versiones minificadas para optimizar tamaño
- Bootstrap ya estaba descargado localmente, se mantiene sin cambios

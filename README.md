# TiendaApp

Sistema de gestión de tienda desarrollado con Flask y MariaDB.

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd TiendaApp
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Descargar assets de frontend
```bash
./descargar_assets.sh  # En Linux/Mac
# bash descargar_assets.sh  # En Windows con Git Bash
```

Este script descarga:
- Bootstrap 5.3.2 (CSS y JS)
- SweetAlert2

### 5. Configurar base de datos
```bash
# Crear base de datos
mariadb -u root -p < BaseDatos/tiendadb.sql

# Crear procedimientos almacenados
mariadb -u root -p tiendadb < BaseDatos/tiendadb_proc.sql
```

### 6. Ejecutar la aplicación
```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📁 Estructura del Proyecto

```
TiendaApp/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── descargar_assets.sh    # Script para descargar Bootstrap y SweetAlert2
├── database/              # Módulo de conexión a base de datos
│   ├── __init__.py
│   └── connection.py
├── app/
│   ├── models/           # Modelos de datos
│   ├── routes/           # Rutas/Endpoints de la API
│   ├── services/         # Lógica de negocio
│   ├── templates/        # Templates HTML
│   │   ├── components/   # Componentes reutilizables
│   │   ├── base.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static/           # Archivos estáticos
│       ├── css/
│       │   └── estilos.css
│       ├── js/
│       └── img/
└── BaseDatos/            # Scripts SQL
    ├── tiendadb.sql
    └── tiendadb_proc.sql
```

## 🎨 Personalización de Colores

Los colores del sitio se controlan mediante variables CSS en `app/static/css/estilos.css`:

```css
:root {
  --primary-color: #4F46E5;      /* Color principal */
  --secondary-color: #10B981;    /* Color secundario */
  --success-color: #10B981;      /* Color de éxito */
  /* ... más variables ... */
}
```

Modifica estas variables para cambiar toda la paleta de colores del sitio.

## 🔐 Características

- ✅ Sistema de autenticación con sesiones Flask
- ✅ Dashboard interactivo
- ✅ Gestión de productos, clientes, proveedores
- ✅ Sistema de ventas
- ✅ Diseño responsive con Bootstrap 5
- ✅ Notificaciones con SweetAlert2
- ✅ Paleta de colores personalizable

## 📝 Credenciales por Defecto

Ver en la base de datos los usuarios creados.

## 🛠️ Tecnologías

- **Backend**: Flask
- **Base de datos**: MariaDB con SQLAlchemy
- **Frontend**: Bootstrap 5.3.2, SweetAlert2
- **Fuentes**: Inter (Google Fonts)

## 📄 Licencia

[Especifica tu licencia aquí]

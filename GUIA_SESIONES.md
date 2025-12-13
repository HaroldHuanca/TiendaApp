# 🧹 Guía de Limpieza de Sesiones Corruptas

## 📌 Problema Resuelto

El error **"Not Found"** al acceder a `/productos` desde `127.0.0.1:5000` fue causado por **sesiones corruptas** almacenadas en el navegador. El problema NO ocurría desde otros dispositivos porque no tenían esa sesión corrupta.

---

## ✅ Soluciones Implementadas

### 1. **Mejorado el Endpoint de Logout**
- Ahora limpia correctamente:
  - La sesión de Flask
  - Las cookies de sesión en múltiples rutas
  - Headers de caché para evitar servir páginas stale
- **Ruta mejorada**: `GET /logout` o `POST /logout`

### 2. **Nuevo Endpoint de Limpieza de Emergencia**
- Ruta especial para debugging: `GET /clear-session`
- Solo úsalo si `logout` no funciona
- Limpia completamente la sesión corrupta

### 3. **Middleware Anti-Cacheo**
- Agregado a todas las rutas de autenticación
- Previene que el navegador sirva páginas viejas en caché
- Headers de Cache-Control configurados automáticamente

### 4. **Botón de Cerrar Sesión en el Sidebar**
- Nuevo botón rojo "Cerrar Sesión" en el menú
- Incluye confirmación antes de logout
- Limpia automáticamente la sesión

### 5. **Script de Limpieza Manual**
- Archivo: `clean_sessions.sh`
- Elimina todos los archivos de sesión del servidor
- Úsalo solo si nada más funciona

---

## 🚀 Cómo Usar

### **Opción 1: Usar el Botón del Sidebar (Recomendado)**
1. Abre la aplicación
2. Haz login normalmente
3. En el sidebar, haz clic en **"Cerrar Sesión"**
4. Confirma el mensaje
5. Serás redirigido a login

### **Opción 2: Acceder Directamente a Logout**
- Ve a: `http://127.0.0.1:5000/logout`
- Tu sesión se limpiará automáticamente
- Serás redirigido a login

### **Opción 3: Usar el Endpoint de Emergencia (Solo Desarrollo)**
- Ve a: `http://127.0.0.1:5000/clear-session`
- Limpia la sesión completamente
- Serás redirigido a login

### **Opción 4: Limpiar del Servidor (Nuclear)**
```bash
cd /home/HaroldUser/Tienda/TiendaApp
bash clean_sessions.sh
```

O directamente:
```bash
rm -rf /home/HaroldUser/Tienda/TiendaApp/flask_session/*
```

---

## 🔍 Cómo Verificar que Funciona

1. **Abre DevTools del navegador** (F12)
2. Ve a **Application → Cookies → http://127.0.0.1:5000**
3. Busca la cookie llamada **"session"**
4. Luego haz logout y recarga la página
5. La cookie debería haber desaparecido

---

## 💡 Prevenir el Problema en el Futuro

1. **Siempre usa el botón "Cerrar Sesión"** en lugar de cerrar el navegador
2. **Limpia caché regularmente** si trabajas en desarrollo
3. **Usa modo incógnito** para testear cambios de sesión
4. **En producción**, configura:
   - `SESSION_COOKIE_SECURE = True` (requiere HTTPS)
   - `SESSION_COOKIE_HTTPONLY = True` (ya está configurado)
   - `SESSION_COOKIE_SAMESITE = 'Strict'` (más seguro)

---

## 📋 Cambios Realizados en main.py

### Nuevo Middleware
```python
@app.after_request
def set_cache_headers(response):
    """Previene el cacheo de páginas para evitar problemas de sesión stale"""
    if request.path.startswith(('/productos', '/categorias', '/unidades', '/clientes', '/proveedores')):
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.max_age = 0
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response
```

### Logout Mejorado
```python
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """Cierra la sesión del usuario y limpia todas las cookies."""
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('session', path='/')
    response.delete_cookie('session', path='/productos')
    response.delete_cookie('session', path='/categorias')
    response.delete_cookie('session', path='/unidades')
    response.delete_cookie('session', path='/clientes')
    response.delete_cookie('session', path='/proveedores')
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
```

### Clear-Session (Emergencia)
```python
@app.route("/clear-session")
def clear_session():
    """Endpoint para limpiar sesión corrupta (útil para debugging)"""
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('session', path='/')
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    return response
```

---

## ✨ Resumen

| Problema | Solución | Ruta |
|----------|----------|------|
| Sesión corrupta | Botón Logout en sidebar | Integrado en UI |
| Necesitas limpiar rápido | Endpoint de logout | `GET /logout` |
| Emergencia | Endpoint de clearing | `GET /clear-session` |
| Servidor completo | Script de limpieza | `bash clean_sessions.sh` |

**¡Ahora debería funcionar correctamente en todos los navegadores!** 🎉

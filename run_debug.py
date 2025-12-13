#!/usr/bin/env python3
"""
Script para iniciar Flask con debug de rutas
"""

import sys
import os

# Agregar el proyecto al path
sys.path.insert(0, '/home/HaroldUser/Tienda/TiendaApp')

from main import create_app

# Crear la app
app = create_app()

print("\n" + "=" * 80)
print("🚀 INICIANDO TIENDAAPP")
print("=" * 80 + "\n")

# Listar rutas importantes
print("📋 RUTAS REGISTRADAS:\n")

importante_routes = [
    '/login',
    '/logout', 
    '/clear-session',
    '/',
    '/productos',
    '/categorias',
    '/unidades',
]

for rule in app.url_map.iter_rules():
    if str(rule).split('/')[1:2][0] in ['', 'productos', 'login', 'logout', 'clear-session'] or any(r in str(rule) for r in importante_routes):
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        print(f"   ✓ {str(rule):50} [{methods}]")

print("\n" + "=" * 80)
print("🌐 Servidor ejecutándose en: http://0.0.0.0:5000")
print("💻 Accede desde: http://127.0.0.1:5000")
print("📱 Desde red:    http://<tu_ip_local>:5000")
print("=" * 80 + "\n")

# Iniciar el servidor
app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

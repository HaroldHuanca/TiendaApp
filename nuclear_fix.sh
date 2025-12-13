#!/bin/bash
# 🧹 SOLUCIÓN NUCLEAR PARA SESIONES CORRUPTAS

echo "🧹 LIMPIEZA NUCLEAR DE SESIONES"
echo "================================"
echo ""

# 1. Limpiar sesiones del servidor
echo "1️⃣  Limpiando sesiones del servidor..."
rm -rf /home/HaroldUser/Tienda/TiendaApp/flask_session/*
echo "   ✅ Hecho"

# 2. Limpiar caché de Python
echo ""
echo "2️⃣  Limpiando caché de Python..."
find /home/HaroldUser/Tienda/TiendaApp -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find /home/HaroldUser/Tienda/TiendaApp -type f -name "*.pyc" -delete
echo "   ✅ Hecho"

# 3. Matar servidor anterior
echo ""
echo "3️⃣  Matando servidores Flask anteriores..."
pkill -f "python.*main.py" || true
pkill -f "run_debug.py" || true
sleep 1
echo "   ✅ Hecho"

# 4. Instrucciones finales
echo ""
echo "================================"
echo "✅ LIMPIEZA COMPLETADA"
echo "================================"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo ""
echo "1️⃣  EN TU NAVEGADOR BRAVE:"
echo "   a) Abre DevTools (F12)"
echo "   b) Ve a: Application → Cookies → http://127.0.0.1:5000"
echo "   c) Busca la cookie 'session' y ELIMÍNALA"
echo "   d) Cierra DevTools"
echo ""
echo "2️⃣  RECARGA LA PÁGINA:"
echo "   - Presiona Ctrl+Shift+R (recarga forzada)"
echo "   - O accede a: http://127.0.0.1:5000/login"
echo ""
echo "3️⃣  INICIA SESIÓN:"
echo "   - Username: admin (o tu usuario)"
echo "   - Password: (tu contraseña)"
echo ""
echo "4️⃣  INTENTA ACCEDER A /productos"
echo "   - http://127.0.0.1:5000/productos"
echo ""
echo "Si aún no funciona, usa:"
echo "   - Modo incógnito de Brave"
echo "   - O desde tu teléfono nuevamente"
echo ""

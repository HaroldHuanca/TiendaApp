#!/bin/bash
# Script para limpiar sesiones corruptas de Flask

echo "🧹 Limpiando sesiones de Flask..."

# Eliminar todos los archivos de sesión
rm -rf flask_session/*

echo "✅ Sesiones eliminadas correctamente"
echo ""
echo "📝 Próximas acciones:"
echo "1. Reinicia el servidor Flask"
echo "2. Accede a 127.0.0.1:5000/login"
echo "3. Hace login nuevamente"
echo "4. Intenta acceder a /productos"
echo ""
echo "Si el problema persiste, intenta:"
echo "- Abrir en navegador incógnito"
echo "- Limpiar cookies del navegador"
echo "- Acceder a 127.0.0.1:5000/clear-session (solo en desarrollo)"

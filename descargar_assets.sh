#!/bin/bash
# Script para descargar dependencias de frontend (Bootstrap y SweetAlert2)

set -e
echo "📦 Preparando directorios en app/static..."
mkdir -p app/static/css app/static/js

echo "📦 Descargando Bootstrap 5.3.2..."
curl -fL -o app/static/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css
curl -fL -o app/static/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js

echo "📦 Descargando SweetAlert2..."
curl -fL -o app/static/js/sweetalert2.all.min.js https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.all.min.js

echo "✅ Todas las dependencias han sido descargadas correctamente!"

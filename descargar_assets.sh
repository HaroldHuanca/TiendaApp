#!/bin/bash
# Script para descargar dependencias de frontend (Bootstrap, SweetAlert2 y Google Fonts)

set -e
echo "📦 Preparando directorios en app/static..."
mkdir -p app/static/css app/static/js app/static/fonts

echo "📦 Descargando Bootstrap 5.3.2..."
curl -fL -o app/static/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css
curl -fL -o app/static/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js

echo "📦 Descargando SweetAlert2 11.10.0..."
curl -fL -o app/static/css/sweetalert2.min.css https://cdn.jsdelivr.net/npm/sweetalert2@11.10.0/dist/sweetalert2.min.css
curl -fL -o app/static/js/sweetalert2.all.min.js https://cdn.jsdelivr.net/npm/sweetalert2@11.10.0/dist/sweetalert2.all.min.js

echo "📦 Descargando Google Fonts - Inter..."
curl -fL -o app/static/fonts/inter-font.css 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'

echo "📦 Descargando fuentes TTF de Inter..."
curl -fL -o app/static/fonts/inter-300.ttf 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuOKfMZg.ttf'
curl -fL -o app/static/fonts/inter-400.ttf 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf'
curl -fL -o app/static/fonts/inter-500.ttf 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuI6fMZg.ttf'
curl -fL -o app/static/fonts/inter-600.ttf 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf'
curl -fL -o app/static/fonts/inter-700.ttf 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf'

echo "✅ Actualizando CSS de fuentes para rutas locales..."
# Reemplazar URLs remotas por rutas locales en el CSS de fuentes
sed -i 's|https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuOKfMZg.ttf|/static/fonts/inter-300.ttf|g' app/static/fonts/inter-font.css
sed -i 's|https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf|/static/fonts/inter-400.ttf|g' app/static/fonts/inter-font.css
sed -i 's|https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuI6fMZg.ttf|/static/fonts/inter-500.ttf|g' app/static/fonts/inter-font.css
sed -i 's|https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf|/static/fonts/inter-600.ttf|g' app/static/fonts/inter-font.css
sed -i 's|https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf|/static/fonts/inter-700.ttf|g' app/static/fonts/inter-font.css

echo "✅ Todas las dependencias han sido descargadas correctamente!"
echo ""
echo "📋 Librerías instaladas:"
echo "  ✓ Bootstrap 5.3.2 (CSS y JS)"
echo "  ✓ SweetAlert2 11.10.0 (CSS y JS)"
echo "  ✓ Google Fonts - Inter (CSS y 5 variantes TTF)"
echo ""
echo "💡 Todas las librerías están en app/static/ y listas para usar sin conexión a internet."

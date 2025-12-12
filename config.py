"""
Configuración de Flask para la aplicación TiendaApp
"""
import os
from datetime import timedelta

class Config:
    """Configuración base para todos los entornos"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-clave-123456'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)


class LANConfig(Config):
    """Configuración para entorno LAN (desarrollo local)
    
    Esta configuración permite que la aplicación funcione correctamente
    cuando se accede desde múltiples dispositivos en la misma red local.
    """
    # Desactivar SECURE para HTTP (LAN)
    SESSION_COOKIE_SECURE = False
    
    # Proteger contra CSRF pero permitir acceso desde otros dispositivos
    SESSION_COOKIE_HTTPONLY = True
    
    # Permitir cookies en peticiones cross-site pero de forma segura
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Permitir headers de CORS
    CORS_HEADERS = 'Content-Type'
    
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción (HTTPS requierido)"""
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    DEBUG = False


# Seleccionar configuración según el entorno
config = {
    'lan': LANConfig,
    'production': ProductionConfig,
    'default': LANConfig
}

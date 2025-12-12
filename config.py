"""
Módulo de configuración para la aplicación Flask de TiendaApp.
Contiene diferentes configuraciones para distintos entornos.
"""

import os
from datetime import timedelta


class Config:
    """Configuración base para todos los entornos."""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-muy-segura-2025'
    
    # Configuración de sesión
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    
    # Configuración de CORS
    CORS_ORIGINS = "*"
    
    # Configuración de aplicación
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    DEBUG = True


class LANConfig(Config):
    """Configuración para uso en red local (LAN).
    
    Esta configuración está optimizada para que la aplicación
    funcione correctamente en una red local con múltiples dispositivos.
    """
    DEBUG = True
    
    # Permitir acceso desde cualquier dispositivo en la red local
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS permisivo para uso en LAN
    CORS_ORIGINS = "*"
    
    # Configuración de sesión más flexible para desarrollo
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_HTTPONLY = True
    
    # Base de datos
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'echo': False,  # Cambiar a True para ver queries SQL en desarrollo
    }


# Seleccionar la configuración según el entorno
config_env = os.environ.get('FLASK_ENV', 'lan')

if config_env == 'production':
    config = ProductionConfig
elif config_env == 'testing':
    config = TestingConfig
elif config_env == 'development':
    config = DevelopmentConfig
else:
    config = LANConfig

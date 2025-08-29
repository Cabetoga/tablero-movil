"""
Módulo de gestión de configuración general
"""

import json
import os
from datetime import datetime
from cryptography.fernet import Fernet


class ConfigManager:
    """Gestor de configuración general de la aplicación"""

    def __init__(self):
        self.config_file = "app_config.json"
        self.app_name = "PowerBI Mobile Dashboard"
        self.version = "1.0.0"
        self.config = self._load_default_config()

        self._load_config()

    def _load_default_config(self):
        """Carga configuración por defecto"""
        return {
            "app": {
                "name": self.app_name,
                "version": self.version,
                "debug": False,
                "auto_refresh": True,
                "refresh_interval": 300,  # 5 minutos
                "cache_timeout": 3600     # 1 hora
            },
            "ui": {
                "theme": "Light",
                "primary_color": "Blue",
                "language": "es",
                "show_splash": True,
                "animation_duration": 0.3
            },
            "security": {
                "session_timeout": 7200,  # 2 horas
                "max_login_attempts": 3,
                "require_strong_password": False,
                "encrypt_local_data": True
            },
            "powerbi": {
                "auto_login": False,
                "full_screen": False,
                "show_filters": True,
                "show_toolbar": False,
                "mobile_optimized": True
            },
            "network": {
                "timeout": 30,
                "retry_attempts": 3,
                "offline_mode": False
            },
            "logging": {
                "enabled": True,
                "level": "INFO",
                "max_file_size": 1048576,  # 1MB
                "backup_count": 3
            }
        }

    def _load_config(self):
        """Carga configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Merger configuración guardada con defaults
                    self.config = self._merge_configs(self.config, saved_config)
        except Exception as e:
            print(f"Error cargando configuración: {e}")

    def _merge_configs(self, default_config, saved_config):
        """Combina configuración por defecto con la guardada"""
        result = default_config.copy()

        for section, values in saved_config.items():
            if section in result and isinstance(values, dict):
                result[section].update(values)
            else:
                result[section] = values

        return result

    def save_config(self):
        """Guarda configuración en archivo"""
        try:
            # Agregar metadata de guardado
            self.config["_metadata"] = {
                "last_saved": datetime.now().isoformat(),
                "version": self.version
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")

    def get(self, section, key=None, default=None):
        """Obtiene valor de configuración"""
        try:
            if key is None:
                return self.config.get(section, default)
            else:
                return self.config.get(section, {}).get(key, default)
        except Exception:
            return default

    def set(self, section, key, value):
        """Establece valor de configuración"""
        if section not in self.config:
            self.config[section] = {}

        if isinstance(self.config[section], dict):
            self.config[section][key] = value
        else:
            self.config[section] = {key: value}

    def set_section(self, section, values):
        """Establece sección completa de configuración"""
        self.config[section] = values

    def get_app_info(self):
        """Obtiene información de la aplicación"""
        return {
            "name": self.get("app", "name"),
            "version": self.get("app", "version"),
            "debug": self.get("app", "debug"),
            "build_date": self.get("_metadata", "last_saved", "Unknown")
        }

    def get_ui_config(self):
        """Obtiene configuración de UI"""
        return self.get("ui", default={})

    def get_security_config(self):
        """Obtiene configuración de seguridad"""
        return self.get("security", default={})

    def get_powerbi_config(self):
        """Obtiene configuración de Power BI"""
        return self.get("powerbi", default={})

    def get_network_config(self):
        """Obtiene configuración de red"""
        return self.get("network", default={})

    def is_debug_enabled(self):
        """Verifica si el modo debug está habilitado"""
        return self.get("app", "debug", False)

    def get_theme_settings(self):
        """Obtiene configuración de tema"""
        ui_config = self.get_ui_config()
        return {
            "theme_style": ui_config.get("theme", "Light"),
            "primary_palette": ui_config.get("primary_color", "Blue"),
            "language": ui_config.get("language", "es")
        }

    def update_theme(self, theme_style=None, primary_color=None):
        """Actualiza configuración de tema"""
        if theme_style:
            self.set("ui", "theme", theme_style)
        if primary_color:
            self.set("ui", "primary_color", primary_color)

        self.save_config()

    def reset_to_defaults(self):
        """Restaura configuración por defecto"""
        self.config = self._load_default_config()
        self.save_config()

    def export_config(self, file_path):
        """Exporta configuración a archivo"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exportando configuración: {e}")
            return False

    def import_config(self, file_path):
        """Importa configuración desde archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                self.config = self._merge_configs(self._load_default_config(), imported_config)
                self.save_config()
            return True
        except Exception as e:
            print(f"Error importando configuración: {e}")
            return False

    def validate_config(self):
        """Valida la configuración actual"""
        errors = []

        # Validar secciones requeridas
        required_sections = ["app", "ui", "security", "powerbi", "network"]
        for section in required_sections:
            if section not in self.config:
                errors.append(f"Sección requerida '{section}' no encontrada")

        # Validar valores específicos
        if self.get("security", "session_timeout", 0) <= 0:
            errors.append("Timeout de sesión debe ser mayor a 0")

        if self.get("network", "timeout", 0) <= 0:
            errors.append("Timeout de red debe ser mayor a 0")

        return len(errors) == 0, errors


class AppConstants:
    """Constantes de la aplicación"""

    # Información de la app
    APP_NAME = "PowerBI Mobile Dashboard"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Comunicación Celular S.A."

    # Rutas y archivos
    CONFIG_DIR = "config"
    CACHE_DIR = "cache"
    LOGS_DIR = "logs"

    # Límites
    MAX_LOGIN_ATTEMPTS = 3
    SESSION_TIMEOUT = 7200  # 2 horas
    CACHE_TIMEOUT = 3600    # 1 hora

    # URLs y endpoints
    POWERBI_DOMAINS = [
        "app.powerbi.com",
        "powerbi.microsoft.com",
        "powerbi.com"
    ]

    # Configuración de UI
    DEFAULT_THEME = "Light"
    DEFAULT_PRIMARY_COLOR = "Blue"
    DEFAULT_LANGUAGE = "es"

    # Mensajes
    MESSAGES = {
        "es": {
            "login_required": "Debe iniciar sesión para continuar",
            "invalid_credentials": "Credenciales inválidas",
            "session_expired": "La sesión ha expirado",
            "network_error": "Error de conexión de red",
            "config_error": "Error en la configuración",
            "access_denied": "Acceso denegado",
            "loading": "Cargando...",
            "success": "Operación exitosa",
            "error": "Error"
        },
        "en": {
            "login_required": "Login required to continue",
            "invalid_credentials": "Invalid credentials",
            "session_expired": "Session has expired",
            "network_error": "Network connection error",
            "config_error": "Configuration error",
            "access_denied": "Access denied",
            "loading": "Loading...",
            "success": "Operation successful",
            "error": "Error"
        }
    }

    @classmethod
    def get_message(cls, key, language="es"):
        """Obtiene mensaje localizado"""
        return cls.MESSAGES.get(language, cls.MESSAGES["es"]).get(key, key)


# Instancia global de configuración
config_manager = ConfigManager()


def get_config():
    """Obtiene instancia global de configuración"""
    return config_manager


def setup_app_config():
    """Configuración inicial de la aplicación"""
    print("=== Configuración Inicial de la Aplicación ===")

    config = get_config()

    # Configuración básica
    debug_mode = input("¿Habilitar modo debug? (s/n) [n]: ").strip().lower()
    config.set("app", "debug", debug_mode == 's')

    # Configuración de tema
    print("\nTemas disponibles: Light, Dark")
    theme = input("Seleccionar tema [Light]: ").strip() or "Light"
    config.set("ui", "theme", theme)

    print("\nColores disponibles: Blue, Red, Green, Purple, Orange")
    color = input("Seleccionar color primario [Blue]: ").strip() or "Blue"
    config.set("ui", "primary_color", color)

    # Configuración de seguridad
    timeout = input("Timeout de sesión en minutos [120]: ").strip()
    try:
        timeout_seconds = int(timeout or 120) * 60
        config.set("security", "session_timeout", timeout_seconds)
    except ValueError:
        print("Valor inválido, usando 120 minutos")
        config.set("security", "session_timeout", 7200)

    # Guardar configuración
    config.save_config()

    print("\n✓ Configuración inicial completada")
    print(f"Archivo de configuración: {config.config_file}")

    return True


if __name__ == "__main__":
    setup_app_config()

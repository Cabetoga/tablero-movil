"""
Módulo de gestión de Power BI
Maneja la URL del tablero de forma segura
"""

import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import base64


class PowerBIManager:
    """Gestor de tableros Power BI"""

    def __init__(self):
        self.config_file = "powerbi_config.json"
        self.encrypted_config_file = "powerbi_secure.dat"
        self.encryption_key = self._get_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self.dashboard_url = None
        self.dashboard_config = {}

        self._load_config()

    def _get_encryption_key(self):
        """Obtiene clave de encriptación para URLs"""
        key_file = "powerbi_encryption.key"

        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

    def _load_config(self):
        """Carga configuración de Power BI"""
        try:
            # Intentar cargar configuración encriptada primero
            if os.path.exists(self.encrypted_config_file):
                self._load_encrypted_config()
            elif os.path.exists(self.config_file):
                self._load_plain_config()
                # Migrar a configuración encriptada
                self._save_encrypted_config()
        except Exception as e:
            print(f"Error cargando configuración Power BI: {e}")

    def _load_encrypted_config(self):
        """Carga configuración encriptada"""
        try:
            with open(self.encrypted_config_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                config = json.loads(decrypted_data.decode())

                self.dashboard_url = config.get('dashboard_url')
                self.dashboard_config = config.get('config', {})
        except Exception as e:
            raise Exception(f"Error cargando configuración encriptada: {e}")

    def _load_plain_config(self):
        """Carga configuración en texto plano (legacy)"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.dashboard_url = config.get('dashboard_url')
                self.dashboard_config = config.get('config', {})
        except Exception as e:
            raise Exception(f"Error cargando configuración plana: {e}")

    def _save_encrypted_config(self):
        """Guarda configuración encriptada"""
        try:
            config = {
                'dashboard_url': self.dashboard_url,
                'config': self.dashboard_config,
                'last_updated': datetime.now().isoformat()
            }

            config_json = json.dumps(config, ensure_ascii=False)
            encrypted_data = self.fernet.encrypt(config_json.encode())

            with open(self.encrypted_config_file, 'wb') as f:
                f.write(encrypted_data)

            # Eliminar archivo de configuración plana si existe
            if os.path.exists(self.config_file):
                os.remove(self.config_file)

        except Exception as e:
            print(f"Error guardando configuración encriptada: {e}")

    def set_dashboard_url(self, url, title="", description=""):
        """Establece la URL del tablero Power BI"""
        if not url:
            raise ValueError("URL del tablero no puede estar vacía")

        # Validar que sea una URL de Power BI válida
        if not self._validate_powerbi_url(url):
            raise ValueError("URL no es un tablero válido de Power BI")

        self.dashboard_url = url
        self.dashboard_config = {
            'title': title or "Tablero Power BI",
            'description': description or "Tablero corporativo",
            'configured_date': datetime.now().isoformat(),
            'embed_type': self._detect_embed_type(url)
        }

        self._save_encrypted_config()

    def _validate_powerbi_url(self, url):
        """Valida que la URL sea de Power BI"""
        powerbi_domains = [
            'app.powerbi.com',
            'powerbi.microsoft.com',
            'powerbi.com'
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in powerbi_domains)

    def _detect_embed_type(self, url):
        """Detecta el tipo de embed de Power BI"""
        url_lower = url.lower()

        if '/reportembed' in url_lower:
            return 'report'
        elif '/dashboardembed' in url_lower:
            return 'dashboard'
        elif '/tileeembed' in url_lower:
            return 'tile'
        else:
            return 'unknown'

    def get_dashboard_url(self):
        """Obtiene la URL del tablero Power BI"""
        if not self.dashboard_url:
            raise ValueError("URL del tablero no configurada")

        return self.dashboard_url

    def get_dashboard_config(self):
        """Obtiene configuración del tablero"""
        return self.dashboard_config

    def get_embed_url(self, width=800, height=600):
        """Genera URL de embed para iframe"""
        if not self.dashboard_url:
            return None

        base_url = self.dashboard_url

        # Agregar parámetros de embed si no están presentes
        if '?' in base_url:
            separator = '&'
        else:
            separator = '?'

        embed_params = [
            f"rs:embed=true",
            f"pageName=ReportSection",
            f"autoAuth=true",
            f"ctid=common"
        ]

        embed_url = base_url + separator + "&".join(embed_params)

        return embed_url

    def get_dashboard_info(self):
        """Obtiene información del tablero"""
        if not self.dashboard_url:
            return None

        return {
            'url': self.dashboard_url[:50] + "..." if len(self.dashboard_url) > 50 else self.dashboard_url,
            'title': self.dashboard_config.get('title', 'Tablero Power BI'),
            'description': self.dashboard_config.get('description', ''),
            'embed_type': self.dashboard_config.get('embed_type', 'unknown'),
            'configured_date': self.dashboard_config.get('configured_date'),
            'is_configured': bool(self.dashboard_url)
        }

    def create_mobile_friendly_url(self):
        """Crea URL optimizada para móviles"""
        if not self.dashboard_url:
            return None

        base_url = self.dashboard_url

        # Parámetros para optimización móvil
        mobile_params = [
            "rs:embed=true",
            "autoAuth=true",
            "navContentPaneEnabled=false",
            "filterPaneEnabled=false",
            "toolbarEnabled=false"
        ]

        if '?' in base_url:
            separator = '&'
        else:
            separator = '?'

        mobile_url = base_url + separator + "&".join(mobile_params)

        return mobile_url

    def is_configured(self):
        """Verifica si el tablero está configurado"""
        return bool(self.dashboard_url)

    def clear_configuration(self):
        """Limpia la configuración del tablero"""
        self.dashboard_url = None
        self.dashboard_config = {}

        # Eliminar archivos de configuración
        for file_path in [self.config_file, self.encrypted_config_file]:
            if os.path.exists(file_path):
                os.remove(file_path)


class PowerBIEmbedHelper:
    """Helper para embed de Power BI"""

    @staticmethod
    def create_iframe_html(embed_url, width="100%", height="600px"):
        """Crea HTML para iframe de Power BI"""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Power BI Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}
                .powerbi-frame {{
                    width: {width};
                    height: {height};
                    border: none;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <iframe
                class="powerbi-frame"
                src="{embed_url}"
                allowfullscreen="true"
                webkitallowfullscreen="true"
                mozallowfullscreen="true">
            </iframe>
        </body>
        </html>
        """
        return html_template

    @staticmethod
    def get_mobile_css():
        """CSS optimizado para móviles"""
        return """
        <style>
            @media (max-width: 768px) {
                .powerbi-frame {
                    width: 100vw !important;
                    height: 100vh !important;
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                }
                body {
                    overflow: hidden !important;
                }
            }
        </style>
        """


# Función para configurar Power BI
def setup_powerbi():
    """Función de utilidad para configurar Power BI"""
    print("=== Configuración de Power BI ===")
    print("Por favor, proporciona la URL pública del tablero Power BI")
    print("Ejemplo: https://app.powerbi.com/view?r=...")

    url = input("\nIngresa la URL del tablero: ").strip()
    title = input("Título del tablero (opcional): ").strip()
    description = input("Descripción (opcional): ").strip()

    if url:
        try:
            powerbi_manager = PowerBIManager()
            powerbi_manager.set_dashboard_url(url, title, description)
            print(f"\nTablero configurado exitosamente:")
            print(f"URL: {url[:50]}...")
            print(f"Título: {title or 'Tablero Power BI'}")
            return True
        except Exception as e:
            print(f"Error configurando tablero: {e}")
            return False
    else:
        print("URL no válida")
        return False


if __name__ == "__main__":
    setup_powerbi()

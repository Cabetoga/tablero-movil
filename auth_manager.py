"""
Módulo de gestión de autenticación y autorización
Lee permisos desde archivo CSV en OneDrive
"""


import requests
import hashlib
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import pandas as pd


class AuthManager:
    """Gestor de autenticación y autorización de usuarios"""

    def __init__(self):
        self.config_file = "auth_config.json"
        self.cache_file = "auth_cache.json"
        self.encryption_key = self._get_or_create_key()
        self.fernet = Fernet(self.encryption_key)
        self.csv_url = None
        self.current_user = None
        self.permissions_cache = {}
        self.cache_expiry = None

        self._load_config()

    def _get_or_create_key(self):
        """Obtiene o crea clave de encriptación"""
        key_file = "encryption.key"

        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

    def _load_config(self):
        """Carga configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.csv_url = config.get('csv_url')
        except Exception as e:
            print(f"Error cargando configuración: {e}")

    def set_csv_url(self, url):
        """Establece la URL del archivo CSV en OneDrive"""
        self.csv_url = url
        self._save_config()

    def _save_config(self):
        """Guarda configuración en archivo"""
        try:
            config = {
                'csv_url': self.csv_url,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")

    def _encrypt_password(self, password):
        """Encripta contraseña"""
        return self.fernet.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted_password):
        """Desencripta contraseña"""
        return self.fernet.decrypt(encrypted_password.encode()).decode()

    def _hash_password(self, password):
        """Genera hash de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _download_csv_data(self):
        """Descarga datos del CSV desde OneDrive"""
        if not self.csv_url:
            raise ValueError("URL del CSV no configurada")

        try:
            # Convertir URL de OneDrive para descarga directa
            if "onedrive.live.com" in self.csv_url or "1drv.ms" in self.csv_url:
                # Convertir URL de compartir a URL de descarga directa
                if "1drv.ms" in self.csv_url:
                    # Expandir URL corta primero
                    response = requests.head(self.csv_url, allow_redirects=True)
                    self.csv_url = response.url

                # Convertir a URL de descarga directa
                if "view.aspx" in self.csv_url:
                    download_url = self.csv_url.replace("view.aspx", "download.aspx")
                else:
                    download_url = self.csv_url + "&download=1"
            else:
                download_url = self.csv_url

            # Descargar el archivo
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()

            # Leer CSV desde el contenido descargado
            from io import StringIO
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)

            return df

        except Exception as e:
            raise Exception(f"Error descargando CSV: {str(e)}")

    def _load_permissions_from_cache(self):
        """Carga permisos desde caché"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                    # Verificar si el caché no ha expirado
                    cache_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
                    if datetime.now() - cache_time < timedelta(hours=1):
                        self.permissions_cache = cache_data.get('permissions', {})
                        self.cache_expiry = cache_time + timedelta(hours=1)
                        return True
            return False
        except Exception as e:
            print(f"Error cargando caché: {e}")
            return False

    def _save_permissions_to_cache(self):
        """Guarda permisos en caché"""
        try:
            cache_data = {
                'permissions': self.permissions_cache,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando caché: {e}")

    def _load_permissions(self):
        """Carga permisos desde CSV o caché"""
        # Intentar cargar desde caché primero
        if self._load_permissions_from_cache():
            return

        # Si no hay caché válido, descargar desde OneDrive
        try:
            df = self._download_csv_data()

            # Procesar datos del CSV
            self.permissions_cache = {}

            # Normalizar nombres de columnas (soportar mayúsculas/minúsculas)
            df.columns = df.columns.str.lower().str.strip()

            # Esperamos columnas: nombre, cedula (flexible con mayúsculas/minúsculas)
            for _, row in df.iterrows():
                nombre = str(row.get('nombre', '')).strip()
                cedula = str(row.get('cedula', '')).strip()

                if nombre and cedula:
                    # Usar el nombre como username (en minúsculas para consistencia)
                    username = nombre.lower()
                    # Usar la cédula como contraseña (generar hash)
                    cedula_hash = self._hash_password(cedula)

                    self.permissions_cache[username] = {
                        'password_hash': cedula_hash,
                        'active': True,  # Todos los usuarios en el CSV están activos
                        'expiry_date': '',  # Sin fecha de expiración
                        'permissions': 'dashboard',  # Permiso básico para todos
                        'full_name': nombre,  # Nombre completo
                        'department': '',  # Sin departamento específico
                        'role': 'usuario',  # Rol básico para todos
                        'cedula': cedula  # Guardar cédula original
                    }

            # Guardar en caché
            self._save_permissions_to_cache()
            self.cache_expiry = datetime.now() + timedelta(hours=1)

        except Exception as e:
            raise Exception(f"Error cargando permisos: {str(e)}")

    def authenticate(self, username, password):
        """Autentica usuario usando nombre y cédula"""
        try:
            # Cargar permisos
            self._load_permissions()

            username_lower = username.strip().lower()

            # Verificar si el usuario existe
            if username_lower not in self.permissions_cache:
                return False

            user_data = self.permissions_cache[username_lower]

            # Verificar contraseña (cédula)
            password_hash = self._hash_password(password)
            stored_hash = user_data.get('password_hash', '')

            if password_hash == stored_hash:
                # Autenticación exitosa
                self.current_user = {
                    'username': username_lower,
                    'full_name': user_data.get('full_name', username),
                    'department': user_data.get('department', ''),
                    'role': user_data.get('role', 'usuario'),
                    'permissions': user_data.get('permissions', 'dashboard'),
                    'cedula': user_data.get('cedula', ''),
                    'login_time': datetime.now().isoformat()
                }
                return True

            return False

        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False

    def is_authenticated(self):
        """Verifica si hay un usuario autenticado"""
        return self.current_user is not None

    def get_current_user(self):
        """Obtiene información del usuario actual"""
        return self.current_user

    def has_permission(self, permission):
        """Verifica si el usuario actual tiene un permiso específico"""
        if not self.current_user:
            return False

        user_permissions = self.current_user.get('permissions', '').lower()
        return permission.lower() in user_permissions or 'admin' in user_permissions

    def logout(self):
        """Cierra sesión del usuario actual"""
        self.current_user = None

    def refresh_permissions(self):
        """Actualiza permisos forzando descarga desde OneDrive"""
        try:
            # Eliminar caché
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)

            # Recargar permisos
            self._load_permissions()
            return True

        except Exception as e:
            print(f"Error actualizando permisos: {e}")
            return False

    def create_sample_csv_structure(self):
        """Crea estructura de ejemplo para el CSV simplificado"""
        sample_data = {
            'nombre': ['Juan Pérez', 'María García', 'Carlos López', 'Ana Rodríguez'],
            'cedula': ['12345678', '23456789', '34567890', '45678901']
        }

        df = pd.DataFrame(sample_data)
        df.to_csv('usuarios_sistema.csv', index=False, encoding='utf-8')

        print("📋 CSV de ejemplo creado con estructura simplificada:")
        print("   📄 Archivo: usuarios_sistema.csv")
        print("   📊 Columnas: nombre, cedula")
        print("   👥 Usuarios de prueba incluidos")
        print()
        print("🔐 Credenciales de prueba:")
        for _, row in df.iterrows():
            print(f"   Usuario: {row['nombre']} | Contraseña: {row['cedula']}")

        return df


# Función para configurar la URL del CSV
def setup_csv_url():
    """Función de utilidad para configurar la URL del CSV"""
    print("=== Configuración de URL del CSV ===")
    print("Por favor, proporciona la URL pública del archivo CSV en OneDrive")
    print()
    print("📋 El archivo CSV debe contener SOLO estas columnas:")
    print("   1. nombre - Nombre completo del usuario")
    print("   2. cedula - Número de cédula (usado como contraseña)")
    print()
    print("📝 Ejemplo de estructura:")
    print("   nombre,cedula")
    print("   Juan Pérez,12345678")
    print("   María García,23456789")
    print()

    url = input("Ingresa la URL del CSV: ").strip()

    if url:
        auth_manager = AuthManager()
        auth_manager.set_csv_url(url)
        print(f"✅ URL configurada: {url}")
        print("💾 Configuración guardada en auth_config.json")
        return True
    else:
        print("❌ URL no válida")
        return False


if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN AUTH MANAGER - ESTRUCTURA SIMPLIFICADA")
    print("=" * 60)

    # Crear estructura de ejemplo
    auth_manager = AuthManager()
    sample_df = auth_manager.create_sample_csv_structure()

    print()
    print("📋 Estructura del CSV creado:")
    print(sample_df.to_string(index=False))
    print()

    # Configurar URL
    print("🔧 CONFIGURACIÓN DE ONEDRIVE:")
    setup_csv_url()

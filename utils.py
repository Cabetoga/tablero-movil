"""
Utilidades adicionales para la aplicación PowerBI Mobile Dashboard
"""

import hashlib
import json
import os
import logging
from datetime import datetime, timedelta
import pandas as pd
from cryptography.fernet import Fernet


class PasswordUtils:
    """Utilidades para manejo de contraseñas"""

    @staticmethod
    def generate_hash(password):
        """Genera hash SHA256 de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password, hash_value):
        """Verifica contraseña contra hash"""
        return PasswordUtils.generate_hash(password) == hash_value

    @staticmethod
    def generate_password_batch(passwords):
        """Genera hashes para múltiples contraseñas"""
        return {pwd: PasswordUtils.generate_hash(pwd) for pwd in passwords}


class CSVGenerator:
    """Generador de archivos CSV para usuarios"""

    def __init__(self):
        self.template_data = {
            'usuario': [],
            'password_hash': [],
            'activo': [],
            'fecha_expiracion': [],
            'permisos': [],
            'nombre_completo': [],
            'departamento': [],
            'rol': []
        }

    def add_user(self, username, password, full_name, department="",
                 role="usuario", permissions="dashboard", active=True,
                 expiry_date=None):
        """Agrega usuario al CSV"""
        if expiry_date is None:
            expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

        self.template_data['usuario'].append(username)
        self.template_data['password_hash'].append(PasswordUtils.generate_hash(password))
        self.template_data['activo'].append(active)
        self.template_data['fecha_expiracion'].append(expiry_date)
        self.template_data['permisos'].append(permissions)
        self.template_data['nombre_completo'].append(full_name)
        self.template_data['departamento'].append(department)
        self.template_data['rol'].append(role)

    def add_admin(self, username, password, full_name):
        """Agrega usuario administrador"""
        self.add_user(
            username=username,
            password=password,
            full_name=full_name,
            department="IT",
            role="administrador",
            permissions="admin,dashboard,reports,users",
            expiry_date="2030-12-31"
        )

    def generate_csv(self, filename="users.csv"):
        """Genera archivo CSV"""
        df = pd.DataFrame(self.template_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        return df

    def preview(self):
        """Muestra preview de los datos"""
        df = pd.DataFrame(self.template_data)
        return df


class LogManager:
    """Gestor de logs para la aplicación"""

    def __init__(self, log_dir="logs", log_level=logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        """Configura el sistema de logging"""
        os.makedirs(self.log_dir, exist_ok=True)

        # Configurar logger
        self.logger = logging.getLogger('PowerBI_App')
        self.logger.setLevel(self.log_level)

        # Evitar duplicar handlers
        if self.logger.handlers:
            return

        # Handler para archivo
        log_file = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Formato de logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Agregar handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """Log nivel info"""
        self.logger.info(message)

    def warning(self, message):
        """Log nivel warning"""
        self.logger.warning(message)

    def error(self, message):
        """Log nivel error"""
        self.logger.error(message)

    def debug(self, message):
        """Log nivel debug"""
        self.logger.debug(message)

    def log_user_action(self, username, action, details=""):
        """Log específico para acciones de usuario"""
        message = f"Usuario: {username} | Acción: {action}"
        if details:
            message += f" | Detalles: {details}"
        self.info(message)

    def log_auth_attempt(self, username, success, ip_address="unknown"):
        """Log específico para intentos de autenticación"""
        status = "EXITOSO" if success else "FALLIDO"
        self.info(f"Intento de login {status} - Usuario: {username} - IP: {ip_address}")

    def log_powerbi_access(self, username, dashboard_url, success):
        """Log específico para acceso a Power BI"""
        status = "EXITOSO" if success else "FALLIDO"
        url_preview = dashboard_url[:50] + "..." if len(dashboard_url) > 50 else dashboard_url
        self.info(f"Acceso Power BI {status} - Usuario: {username} - URL: {url_preview}")


class DataValidator:
    """Validador de datos para CSV y configuraciones"""

    @staticmethod
    def validate_csv_structure(df):
        """Valida estructura del CSV de usuarios"""
        required_columns = [
            'usuario', 'password_hash', 'activo', 'fecha_expiracion',
            'permisos', 'nombre_completo', 'departamento', 'rol'
        ]

        errors = []

        # Verificar columnas
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            errors.append(f"Columnas faltantes: {missing_columns}")

        # Verificar datos
        for index, row in df.iterrows():
            # Usuario no vacío
            if pd.isna(row.get('usuario')) or str(row.get('usuario')).strip() == '':
                errors.append(f"Fila {index + 1}: Usuario vacío")

            # Hash de contraseña válido
            password_hash = str(row.get('password_hash', ''))
            if len(password_hash) != 64:  # SHA256 tiene 64 caracteres
                errors.append(f"Fila {index + 1}: Hash de contraseña inválido")

            # Valor de activo válido
            active_value = str(row.get('activo', '')).lower()
            if active_value not in ['true', 'false']:
                errors.append(f"Fila {index + 1}: Valor 'activo' debe ser true/false")

            # Fecha de expiración válida
            try:
                datetime.strptime(str(row.get('fecha_expiracion', '')), '%Y-%m-%d')
            except ValueError:
                errors.append(f"Fila {index + 1}: Fecha de expiración inválida (usar YYYY-MM-DD)")

        return len(errors) == 0, errors

    @staticmethod
    def validate_powerbi_url(url):
        """Valida URL de Power BI"""
        if not url:
            return False, "URL vacía"

        powerbi_domains = ['app.powerbi.com', 'powerbi.microsoft.com', 'powerbi.com']
        url_lower = url.lower()

        if not any(domain in url_lower for domain in powerbi_domains):
            return False, "URL no es de Power BI"

        if not url.startswith(('http://', 'https://')):
            return False, "URL debe comenzar con http:// o https://"

        return True, "URL válida"

    @staticmethod
    def validate_onedrive_url(url):
        """Valida URL de OneDrive"""
        if not url:
            return False, "URL vacía"

        onedrive_indicators = ['onedrive.live.com', '1drv.ms', 'sharepoint.com']
        url_lower = url.lower()

        if not any(indicator in url_lower for indicator in onedrive_indicators):
            return False, "URL no es de OneDrive/SharePoint"

        return True, "URL válida"


class SecurityUtils:
    """Utilidades de seguridad"""

    @staticmethod
    def generate_session_token():
        """Genera token de sesión único"""
        return hashlib.sha256(
            f"{datetime.now().isoformat()}{os.urandom(32)}".encode()
        ).hexdigest()

    @staticmethod
    def is_session_expired(session_start, timeout_seconds=7200):
        """Verifica si la sesión ha expirado"""
        if isinstance(session_start, str):
            session_start = datetime.fromisoformat(session_start)

        return datetime.now() - session_start > timedelta(seconds=timeout_seconds)

    @staticmethod
    def sanitize_input(text, max_length=255):
        """Sanitiza entrada de usuario"""
        if not text:
            return ""

        # Remover caracteres potencialmente peligrosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = str(text)

        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')

        return sanitized[:max_length].strip()


class MaintenanceUtils:
    """Utilidades de mantenimiento"""

    @staticmethod
    def cleanup_cache(cache_dir="cache", max_age_hours=24):
        """Limpia archivos de caché antiguos"""
        if not os.path.exists(cache_dir):
            return 0

        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        removed_count = 0

        for filename in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except OSError:
                        pass

        return removed_count

    @staticmethod
    def cleanup_logs(log_dir="logs", max_files=10):
        """Limpia archivos de log antiguos"""
        if not os.path.exists(log_dir):
            return 0

        log_files = [
            f for f in os.listdir(log_dir)
            if f.endswith('.log') and os.path.isfile(os.path.join(log_dir, f))
        ]

        if len(log_files) <= max_files:
            return 0

        # Ordenar por fecha de modificación
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)))

        # Eliminar archivos más antiguos
        files_to_remove = log_files[:-max_files]
        removed_count = 0

        for filename in files_to_remove:
            try:
                os.remove(os.path.join(log_dir, filename))
                removed_count += 1
            except OSError:
                pass

        return removed_count

    @staticmethod
    def get_app_statistics(cache_dir="cache", log_dir="logs"):
        """Obtiene estadísticas de la aplicación"""
        stats = {
            'cache_files': 0,
            'cache_size_mb': 0,
            'log_files': 0,
            'log_size_mb': 0,
            'last_cleanup': None
        }

        # Estadísticas de caché
        if os.path.exists(cache_dir):
            cache_files = os.listdir(cache_dir)
            stats['cache_files'] = len(cache_files)

            total_size = sum(
                os.path.getsize(os.path.join(cache_dir, f))
                for f in cache_files
                if os.path.isfile(os.path.join(cache_dir, f))
            )
            stats['cache_size_mb'] = round(total_size / (1024 * 1024), 2)

        # Estadísticas de logs
        if os.path.exists(log_dir):
            log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
            stats['log_files'] = len(log_files)

            total_size = sum(
                os.path.getsize(os.path.join(log_dir, f))
                for f in log_files
                if os.path.isfile(os.path.join(log_dir, f))
            )
            stats['log_size_mb'] = round(total_size / (1024 * 1024), 2)

        return stats


# Instancias globales
log_manager = LogManager()
password_utils = PasswordUtils()
data_validator = DataValidator()
security_utils = SecurityUtils()
maintenance_utils = MaintenanceUtils()


def quick_user_setup():
    """Configuración rápida de usuarios"""
    print("=== Configuración Rápida de Usuarios ===")

    csv_gen = CSVGenerator()

    # Agregar administrador
    csv_gen.add_admin("admin", "admin123", "Administrador del Sistema")

    # Agregar usuarios de ejemplo
    csv_gen.add_user("usuario1", "pass123", "Juan Pérez", "Ventas", "usuario", "dashboard")
    csv_gen.add_user("usuario2", "user456", "María García", "Marketing", "usuario", "dashboard")
    csv_gen.add_user("gerente1", "ger789", "Carlos López", "Gerencia", "gerente", "dashboard,reports")

    # Generar CSV
    df = csv_gen.generate_csv("users_setup.csv")

    print("✓ Archivo users_setup.csv generado")
    print("\nUsuarios creados:")
    print(df[['usuario', 'nombre_completo', 'departamento', 'rol', 'permisos']].to_string(index=False))

    print("\nCredenciales:")
    print("admin / admin123")
    print("usuario1 / pass123")
    print("usuario2 / user456")
    print("gerente1 / ger789")

    return True


if __name__ == "__main__":
    quick_user_setup()

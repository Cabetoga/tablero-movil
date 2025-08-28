# PowerBI Mobile Dashboard

Aplicación móvil desarrollada con Kivy y KivyMD para acceder a tableros de Power BI de manera segura, con autenticación basada en archivo CSV alojado en OneDrive.

## 🚀 Características

- **Interfaz móvil nativa** con Material Design (KivyMD)
- **Autenticación segura** mediante CSV en OneDrive
- **URLs encriptadas** para ocultar direcciones de tableros
- **Gestión de permisos** granular por usuario
- **Caché local** para mejor rendimiento
- **Soporte offline** limitado
- **Compatible con Android** via Buildozer

## 📋 Requisitos

### Sistema
- Python 3.8+
- Windows/Linux/macOS para desarrollo
- Android SDK (para compilación Android)

### Dependencias Python
```
kivy>=2.1.0
kivymd>=1.1.1
pandas>=1.5.0
requests>=2.28.0
cryptography>=3.4.8
buildozer>=1.4.0 (para Android)
```

## 🛠️ Instalación

### 1. Clonar/Descargar el proyecto
```bash
# Si tienes el código, navega al directorio
cd "Proyecto Tablero Movil"
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS
```

### 3. Instalar dependencias
```bash
pip install kivy kivymd pandas requests cryptography buildozer
```

### 4. Configuración inicial
```bash
python setup.py
```

## ⚙️ Configuración

### 1. Archivo CSV de Usuarios

Crea un archivo CSV con la siguiente estructura y súbelo a OneDrive:

```csv
usuario,password_hash,activo,fecha_expiracion,permisos,nombre_completo,departamento,rol
admin,ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f,true,2025-12-31,admin,Administrador,IT,administrador
usuario1,9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05,true,2025-06-30,dashboard,Juan Pérez,Ventas,usuario
```

**Columnas requeridas:**
- `usuario`: Nombre de usuario único
- `password_hash`: Hash SHA256 de la contraseña
- `activo`: true/false para habilitar/deshabilitar
- `fecha_expiracion`: Fecha en formato YYYY-MM-DD
- `permisos`: Permisos separados por comas (dashboard,admin,reports)
- `nombre_completo`: Nombre completo del usuario
- `departamento`: Departamento del usuario
- `rol`: Rol del usuario (administrador/usuario)

### 2. Generar Hashes de Contraseñas

```python
import hashlib

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ejemplo
print(generate_password_hash("admin123"))
```

### 3. Configurar OneDrive

1. Sube el archivo CSV a OneDrive
2. Comparte el archivo y obtén el enlace público
3. Ejecuta la configuración:
   ```bash
   python auth_manager.py
   ```

### 4. Configurar Power BI

1. Obtén la URL pública de tu tablero Power BI
2. Ejecuta la configuración:
   ```bash
   python powerbi_manager.py
   ```

## 🚀 Ejecución

### Desarrollo (Desktop)
```bash
python main.py
```

### Compilación para Android

1. **Instalar Buildozer** (Linux recomendado):
   ```bash
   pip install buildozer
   ```

2. **Generar APK**:
   ```bash
   buildozer android debug
   ```

3. **El APK se generará en**: `bin/`

## 📱 Uso de la Aplicación

### Pantalla de Login
- Ingresa usuario y contraseña
- Las credenciales se validan contra el CSV de OneDrive
- Sesiones con timeout configurable

### Pantalla Principal
- Visualización del tablero Power BI
- Menú lateral con opciones
- Actualización de datos
- Configuraciones

### Funciones del Menú
- **Actualizar Datos**: Refresca el CSV de usuarios
- **Configuración**: Ajustes de la aplicación
- **Cerrar Sesión**: Vuelve al login

## 🔐 Seguridad

### Encriptación
- URLs de Power BI encriptadas localmente
- Configuraciones sensibles protegidas
- Hashes SHA256 para contraseñas

### Autenticación
- Validación contra CSV en OneDrive
- Control de permisos granular
- Expiración de cuentas
- Límite de intentos de login

### Datos Locales
- Caché temporal encriptado
- Limpieza automática de datos
- No persistencia de credenciales

## 📂 Estructura del Proyecto

```
Proyecto Tablero Movil/
├── main.py                 # Aplicación principal
├── auth_manager.py         # Gestión de autenticación
├── powerbi_manager.py      # Gestión de Power BI
├── config_manager.py       # Configuración general
├── setup.py               # Script de configuración
├── buildozer.spec         # Configuración Android
├── README.md              # Este archivo
├── sample_users.csv       # Ejemplo de usuarios
├── config/                # Archivos de configuración
├── cache/                 # Caché temporal
├── logs/                  # Logs de la aplicación
└── assets/                # Recursos (imágenes, etc.)
```

## 🔧 Configuraciones Avanzadas

### Variables de Entorno
```bash
# Opcional: configuración via variables
export POWERBI_URL="https://app.powerbi.com/view?r=..."
export CSV_URL="https://onedrive.live.com/..."
export DEBUG_MODE="true"
```

### Archivo de Configuración
El archivo `app_config.json` permite personalizar:
- Timeouts de sesión
- Configuración de UI
- Parámetros de red
- Opciones de logging

### Personalización de Tema
```python
from config_manager import get_config

config = get_config()
config.update_theme("Dark", "Purple")
```

## 🐛 Solución de Problemas

### Error de Conexión
- Verifica conectividad a internet
- Confirma URLs de OneDrive y Power BI
- Revisa permisos de archivos

### Error de Autenticación
- Verifica formato del CSV
- Confirma hashes de contraseñas
- Revisa fechas de expiración

### Error de Compilación Android
- Instala Android SDK
- Verifica buildozer.spec
- Revisa logs de compilación

### Error de Dependencias
```bash
pip install --upgrade kivy kivymd pandas requests cryptography
```

## 📊 Monitoreo y Logs

### Activar Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Ubicación de Logs
- Desarrollo: Consola
- Producción: `logs/app.log`

## 🔄 Actualizaciones

### Actualizar CSV de Usuarios
1. Modifica el archivo CSV en OneDrive
2. En la app: Menú → Actualizar Datos

### Actualizar URL de Power BI
```bash
python powerbi_manager.py
```

### Actualizar Aplicación
1. Modifica el código
2. Incrementa versión en `buildozer.spec`
3. Recompila: `buildozer android debug`

## 📞 Soporte

### Credenciales de Ejemplo
- **Usuario**: admin | **Contraseña**: admin123
- **Usuario**: usuario1 | **Contraseña**: pass123

### Archivos de Ejemplo
- `sample_users.csv`: Plantilla de usuarios
- `app_config.json`: Configuración de ejemplo

### Comandos Útiles
```bash
# Limpiar caché
rm -rf cache/*

# Regenerar configuración
python setup.py

# Ver logs en tiempo real
tail -f logs/app.log

# Limpiar build Android
buildozer android clean
```

## 📄 Licencia

Este proyecto es para uso interno de Comunicación Celular S.A. (Comcel S.A.)

## 🚀 Próximas Funciones

- [ ] Modo offline completo
- [ ] Sincronización automática
- [ ] Notificaciones push
- [ ] Múltiples tableros
- [ ] Exportación de reportes
- [ ] Autenticación biométrica

---

**Desarrollado para Comunicación Celular S.A. - Comcel S.A.**

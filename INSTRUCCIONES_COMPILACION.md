# 📱 INSTRUCCIONES COMPLETAS DE COMPILACIÓN ANDROID

## 🎯 OPCIONES DISPONIBLES

### OPCIÓN 1: USANDO WSL EN WINDOWS (Recomendado)

#### 1️⃣ Instalar WSL
```powershell
# Como administrador en PowerShell:
wsl --install Ubuntu
# Reiniciar Windows cuando termine
```

#### 2️⃣ Configurar WSL Ubuntu
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias Python
sudo apt install python3-pip python3-venv python3-dev -y
sudo apt install build-essential libssl-dev libffi-dev -y

# Instalar Java (requerido para Android)
sudo apt install openjdk-11-jdk -y

# Instalar herramientas de desarrollo
sudo apt install git zip unzip -y
sudo apt install autoconf libtool -y
```

#### 3️⃣ Transferir proyecto
```bash
# Crear directorio proyecto
mkdir ~/tablero_movil
cd ~/tablero_movil

# Copiar archivos desde Windows
cp /mnt/d/OneDrive\ -\ Comunicacion\ Celular\ S.A.-\ Comcel\ S.A/Escritorio/Proyecto\ Tablero\ Movil/*.py .
cp /mnt/d/OneDrive\ -\ Comunicacion\ Celular\ S.A.-\ Comcel\ S.A/Escritorio/Proyecto\ Tablero\ Movil/*.spec .
cp /mnt/d/OneDrive\ -\ Comunicacion\ Celular\ S.A.-\ Comcel\ S.A/Escritorio/Proyecto\ Tablero\ Movil/*.json .
cp /mnt/d/OneDrive\ -\ Comunicacion\ Celular\ S.A.-\ Comcel\ S.A/Escritorio/Proyecto\ Tablero\ Movil/*.key .
cp /mnt/d/OneDrive\ -\ Comunicacion\ Celular\ S.A.-\ Comcel\ S.A/Escritorio/Proyecto\ Tablero\ Movil/*.dat .
```

#### 4️⃣ Configurar entorno virtual
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install kivy kivymd pandas requests cryptography
pip install buildozer cython
```

#### 5️⃣ Compilar APK
```bash
# Primera compilación (toma tiempo - descarga SDK)
buildozer android debug

# El APK estará en: bin/main-0.1-arm64-v8a-debug.apk
```

### OPCIÓN 2: USANDO LINUX NATIVO (Más rápido)

Si tienes acceso a una máquina Linux (Ubuntu/Debian):

```bash
# Clonar proyecto
git clone [repositorio] o copiar archivos

# Instalar dependencias
sudo apt update
sudo apt install python3-pip python3-venv python3-dev
sudo apt install build-essential libssl-dev libffi-dev
sudo apt install openjdk-11-jdk
sudo apt install git zip unzip autoconf libtool

# Configurar proyecto
cd proyecto
python3 -m venv venv
source venv/bin/activate
pip install kivy kivymd pandas requests cryptography buildozer cython

# Compilar
buildozer android debug
```

### OPCIÓN 3: GITHUB ACTIONS (Automático)

Subir proyecto a GitHub y usar GitHub Actions para compilar automáticamente.

## 📲 TRANSFERIR APK AL CELULAR

### Método 1: USB
1. Conectar celular por USB
2. Habilitar "Depuración USB" en opciones de desarrollador
3. Copiar APK desde `bin/` al celular
4. Instalar desde archivo APK

### Método 2: Email/Drive
1. Enviar APK por email o subir a Google Drive
2. Descargar en celular
3. Permitir "Instalar apps desconocidas"
4. Instalar APK

### Método 3: ADB (Avanzado)
```bash
# Instalar ADB
sudo apt install android-tools-adb

# Conectar celular e instalar
adb install bin/main-0.1-arm64-v8a-debug.apk
```

## ⚙️ CONFIGURACIÓN DEL CELULAR

### Habilitar instalación de APKs:
1. Ir a Configuración > Seguridad
2. Activar "Fuentes desconocidas"
3. O permitir instalación por aplicación específica

### Habilitar modo desarrollador:
1. Ir a Configuración > Acerca del teléfono
2. Tocar "Número de compilación" 7 veces
3. Ir a Configuración > Opciones de desarrollador
4. Activar "Depuración USB"

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error de compilación:
- Verificar todas las dependencias instaladas
- Limpiar cache: `buildozer android clean`
- Intentar de nuevo: `buildozer android debug`

### APK no instala:
- Verificar permisos de instalación
- Probar en modo desarrollador
- Verificar arquitectura del procesador

### App no ejecuta:
- Verificar logs: `adb logcat | grep python`
- Revisar permisos de internet en AndroidManifest.xml

## 📊 TIEMPO ESTIMADO

- Primera compilación: 30-60 minutos (descarga SDK)
- Compilaciones posteriores: 5-15 minutos
- Transferencia e instalación: 2-5 minutos

## 🎯 RESULTADO FINAL

Tendrás una APK funcional con:
- ✅ Interfaz nativa Android
- ✅ Autenticación con OneDrive
- ✅ Dashboard Power BI integrado
- ✅ 6,336+ usuarios soportados
- ✅ Encriptación de seguridad

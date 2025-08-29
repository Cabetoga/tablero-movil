# 📱 GUÍA COMPLETA: CREAR APK DEL TABLERO MÓVIL

Esta guía te explica **todas las formas** de generar el APK de la aplicación móvil Power BI Dashboard.

## 🎯 OPCIONES DISPONIBLES

### 1️⃣ GITHUB ACTIONS (RECOMENDADO - AUTOMÁTICO)

**✅ Ventajas:**
- Completamente automático
- Sin instalaciones locales
- Gratis para repositorios públicos
- APK optimizado para producción

**📋 Pasos:**
1. El APK se genera automáticamente al hacer push al repositorio
2. Ir a la pestaña "Actions" en GitHub
3. Buscar la ejecución completada (con ✅)
4. Descargar "PowerBI-Dashboard-APK" desde Artifacts
5. Extraer el archivo ZIP para obtener el APK

**⏱️ Tiempo:** 15-30 minutos

---

### 2️⃣ SCRIPT AUTOMÁTICO LOCAL

**✅ Ventajas:**
- Script que automatiza todo el proceso
- Verifica dependencias automáticamente
- Instrucciones paso a paso

**📋 Pasos:**
```bash
# 1. Ejecutar el script automático
./generate_apk.sh

# El script hará todo automáticamente:
# - Verificar dependencias
# - Instalar lo que falte
# - Generar el APK
```

**⏱️ Tiempo:** 20-45 minutos (primera vez)

---

### 3️⃣ BUILDOZER MANUAL

**📋 Pasos:**
```bash
# 1. Instalar dependencias del sistema
sudo apt install openjdk-11-jdk python3-dev build-essential

# 2. Instalar dependencias Python
pip3 install buildozer kivy kivymd pandas requests cryptography

# 3. Generar APK
buildozer android debug
```

**⏱️ Tiempo:** 30-60 minutos (primera vez)

---

### 4️⃣ WSL EN WINDOWS

Si estás en Windows, usa WSL (Windows Subsystem for Linux):

```powershell
# 1. Instalar WSL
wsl --install

# 2. Abrir Ubuntu en WSL
# 3. Seguir pasos de "BUILDOZER MANUAL" dentro de WSL
```

---

## 🔧 REQUISITOS PREVIOS

### Para cualquier método LOCAL:
- **Sistema Operativo:** Linux Ubuntu/Debian (recomendado) o WSL en Windows
- **RAM:** Mínimo 4GB, recomendado 8GB
- **Espacio:** 5-10GB libres
- **Internet:** Conexión estable (descarga Android SDK ~2GB)

### Para GitHub Actions:
- Solo tener el código en GitHub (¡Ya está listo!)

---

## 📂 ARCHIVOS GENERADOS

El APK se genera en la carpeta `bin/` con nombres como:
- `main-0.1-arm64-v8a-debug.apk` (ARM 64-bit)
- `main-0.1-armeabi-v7a-debug.apk` (ARM 32-bit)

---

## 📱 INSTALACIÓN EN EL CELULAR

### Método 1: USB
1. Conectar celular por USB
2. Habilitar "Depuración USB"
3. Copiar APK al celular
4. Instalar desde el archivo

### Método 2: Email/Drive
1. Enviar APK por email o Google Drive
2. Descargar en el celular
3. Permitir "Instalar apps desconocidas"
4. Instalar APK

### Método 3: ADB (Avanzado)
```bash
# Instalar automáticamente
adb install bin/main-0.1-arm64-v8a-debug.apk
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error de compilación:
```bash
# Limpiar y reintentar
buildozer android clean
buildozer android debug
```

### Falta Java:
```bash
sudo apt install openjdk-11-jdk
```

### Falta buildozer:
```bash
pip3 install --user buildozer
export PATH=$HOME/.local/bin:$PATH
```

### APK no instala:
- Verificar que sea la arquitectura correcta (ARM64 para dispositivos modernos)
- Habilitar "Fuentes desconocidas" en configuración
- Intentar en modo desarrollador

---

## ⏱️ TIEMPOS ESTIMADOS

| Método | Primera vez | Siguientes |
|--------|-------------|------------|
| GitHub Actions | 15-30 min | 10-20 min |
| Script automático | 20-45 min | 5-15 min |
| Buildozer manual | 30-60 min | 5-15 min |

---

## 🎯 RESULTADO FINAL

Tu APK tendrá:
- ✅ Interfaz nativa Android con KivyMD
- ✅ Autenticación con OneDrive (6,336+ usuarios)
- ✅ Dashboard Power BI integrado
- ✅ Encriptación de seguridad
- ✅ Funcionamiento offline para credenciales cacheadas

---

## 📞 MÉTODOS ORDENADOS POR FACILIDAD

1. **🥇 GitHub Actions:** Más fácil, automático
2. **🥈 Script automático:** Fácil, local
3. **🥉 Buildozer manual:** Intermedio
4. **🏆 WSL en Windows:** Para usuarios Windows

**💡 Recomendación:** Usar GitHub Actions para la primera APK, luego el script automático para desarrollo local.

---

**Desarrollado para Comunicación Celular S.A. - Comcel S.A.**
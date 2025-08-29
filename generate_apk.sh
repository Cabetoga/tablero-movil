#!/bin/bash

# Script para generar APK del Tablero Móvil Power BI
# PowerBI Mobile Dashboard APK Generation Script
# Autor: Comcel S.A.

echo "🚀 Iniciando generación de APK - Tablero Móvil Power BI"
echo "=================================================="

# Verificar dependencias
echo "🔍 Verificando dependencias..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar Java
if ! command -v javac &> /dev/null; then
    echo "❌ Error: Java Development Kit (JDK) no está instalado"
    echo "   Instalar con: sudo apt install openjdk-11-jdk"
    exit 1
fi

# Verificar buildozer
if ! command -v buildozer &> /dev/null; then
    echo "⚠️  Buildozer no está instalado. Instalando..."
    pip3 install --user buildozer cython
    export PATH=$HOME/.local/bin:$PATH
    
    if ! command -v buildozer &> /dev/null; then
        echo "❌ Error: No se pudo instalar buildozer"
        exit 1
    fi
fi

echo "✅ Dependencias verificadas"

# Verificar archivos necesarios
echo "📁 Verificando archivos del proyecto..."

required_files=(
    "main.py"
    "buildozer.spec"
    "auth_manager.py"
    "powerbi_manager.py"
    "config_manager.py"
    "utils.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Archivo requerido no encontrado: $file"
        exit 1
    fi
done

echo "✅ Todos los archivos necesarios están presentes"

# Limpiar build anterior si existe
echo "🧹 Limpiando builds anteriores..."
buildozer android clean

# Instalar dependencias Python si no están
echo "📦 Verificando dependencias Python..."
pip3 install --user kivy kivymd pandas requests cryptography pillow

# Iniciar build del APK
echo "🔨 Iniciando compilación del APK..."
echo "   Este proceso puede tomar 15-45 minutos en la primera ejecución"
echo "   (debido a la descarga del Android SDK)"

# Ejecutar buildozer
if buildozer android debug; then
    echo ""
    echo "🎉 ¡APK generado exitosamente!"
    echo "📱 Archivo APK ubicado en: bin/"
    
    # Mostrar información del APK
    if [ -d "bin" ]; then
        echo "📊 Información del APK generado:"
        ls -lh bin/*.apk 2>/dev/null || echo "   Archivos APK en bin/:"
        find bin/ -name "*.apk" -exec ls -lh {} \; 2>/dev/null
    fi
    
    echo ""
    echo "🔄 Próximos pasos para instalación:"
    echo "   1. Transferir el APK a tu dispositivo Android"
    echo "   2. Habilitar 'Fuentes desconocidas' en configuración"
    echo "   3. Instalar el APK"
    echo ""
    echo "📖 Para más detalles, consulta:"
    echo "   - INSTRUCCIONES_COMPILACION.md"
    echo "   - INSTRUCCIONES_GITHUB_ACTIONS.md"
    
else
    echo ""
    echo "❌ Error en la compilación del APK"
    echo ""
    echo "🔧 Posibles soluciones:"
    echo "   1. Verificar conexión a internet"
    echo "   2. Ejecutar: buildozer android clean"
    echo "   3. Intentar nuevamente"
    echo "   4. Revisar logs para errores específicos"
    echo ""
    echo "💡 Alternativa: Usar GitHub Actions para compilación automática"
    echo "   Consulta INSTRUCCIONES_GITHUB_ACTIONS.md"
    
    exit 1
fi
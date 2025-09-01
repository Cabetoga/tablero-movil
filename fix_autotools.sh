#!/bin/bash
# Script para corregir problemas de autotools y libtool en GitHub Actions

echo "🔧 Configurando autotools y libtool para compilación Android..."

# Actualizar sistema
sudo apt-get update -qq

# Instalar herramientas de autotools y libtool completas
sudo apt-get install -y \
    autoconf \
    automake \
    autotools-dev \
    libtool \
    libtool-bin \
    libltdl-dev \
    m4 \
    pkg-config \
    build-essential \
    patch \
    gettext \
    gettext-base \
    autopoint \
    texinfo \
    autoconf-archive

# Verificar que autopoint esté disponible
echo "🔍 Verificando autopoint:"
if command -v autopoint &> /dev/null; then
    echo "✅ autopoint disponible"
    autopoint --version
else
    echo "❌ autopoint NO disponible - instalando..."
    sudo apt-get install -y gettext autopoint
fi

# Configurar variables de entorno para autotools y libtool
export ACLOCAL_PATH="/usr/share/aclocal:/usr/local/share/aclocal:$ACLOCAL_PATH"
export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/share/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
export LIBTOOL_PATH="/usr/bin/libtool"
export M4PATH="/usr/share/aclocal"

# Verificar que las macros de libtool estén disponibles
echo "📋 Verificando macros de libtool disponibles:"
if ls /usr/share/aclocal/libtool.m4 2>/dev/null; then
    echo "✅ libtool.m4 encontrado"
else
    echo "❌ libtool.m4 NO encontrado"
fi

if ls /usr/share/aclocal/lt*.m4 2>/dev/null; then
    echo "✅ Macros lt*.m4 encontradas:"
    ls /usr/share/aclocal/lt*.m4
else
    echo "❌ Macros lt*.m4 NO encontradas"
fi

# Regenerar autotools con libtool
echo "🔄 Regenerando autotools con soporte completo de libtool..."
sudo autoreconf --install --force --verbose || true

# Verificar versiones instaladas
echo "📋 Versiones de herramientas instaladas:"
autoconf --version | head -1
automake --version | head -1
libtool --version | head -1
m4 --version | head -1

# Limpiar cache de autotools/buildozer si existe
if [ -d ~/.cache/buildozer ]; then
    echo "🧹 Limpiando cache de buildozer..."
    rm -rf ~/.cache/buildozer/autotools || true
    rm -rf ~/.cache/buildozer/android/platform/python-for-android || true
fi

if [ -d ~/.buildozer ]; then
    echo "🧹 Limpiando cache de .buildozer..."
    rm -rf ~/.buildozer/android/platform/python-for-android || true
fi

echo "✅ Configuración de autotools y libtool completada"
echo "🎯 Macros LT_SYS_SYMBOL_USCORE y similares deberían estar disponibles"

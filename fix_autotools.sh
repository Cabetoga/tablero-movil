#!/bin/bash
# Script para corregir problemas de autotools en GitHub Actions

echo "🔧 Configurando autotools para compilación Android..."

# Actualizar sistema
sudo apt-get update -qq

# Instalar herramientas de autotools más recientes
sudo apt-get install -y \
    autoconf \
    automake \
    autotools-dev \
    libtool \
    libtool-bin \
    m4 \
    pkg-config \
    build-essential \
    patch \
    gettext \
    texinfo

# Configurar variables de entorno para autotools
export ACLOCAL_PATH="/usr/share/aclocal:$ACLOCAL_PATH"
export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/share/pkgconfig:$PKG_CONFIG_PATH"
export AUTOCONF_VERSION="2.71"
export AUTOMAKE_VERSION="1.16"

# Verificar versiones instaladas
echo "📋 Versiones de autotools instaladas:"
autoconf --version | head -1
automake --version | head -1
libtool --version | head -1

# Limpiar cache de autotools si existe
if [ -d ~/.cache/buildozer ]; then
    echo "🧹 Limpiando cache de buildozer..."
    rm -rf ~/.cache/buildozer/autotools
fi

echo "✅ Configuración de autotools completada"

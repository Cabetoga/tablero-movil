"""
Script de configuración inicial para la aplicación PowerBI Mobile Dashboard
"""

import os
import sys
from auth_manager import AuthManager, setup_csv_url
from powerbi_manager import PowerBIManager, setup_powerbi
from config_manager import ConfigManager, setup_app_config


def create_directories():
    """Crea directorios necesarios"""
    directories = [
        "config",
        "cache",
        "logs",
        "assets",
        "assets/images"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("✓ Directorios creados")


def generate_sample_files():
    """Genera archivos de ejemplo"""
    print("\n=== Generando archivos de ejemplo ===")

    # Crear CSV de ejemplo para usuarios
    auth_manager = AuthManager()
    sample_df = auth_manager.create_sample_csv_structure()
    print(f"✓ Archivo de usuarios de ejemplo: sample_users.csv")

    # Mostrar estructura del CSV
    print("\nEstructura del CSV de usuarios:")
    print(sample_df.to_string(index=False))

    return True


def setup_configuration():
    """Configuración inicial completa"""
    print("\n" + "="*50)
    print("CONFIGURACIÓN INICIAL - POWERBI MOBILE DASHBOARD")
    print("="*50)

    # 1. Configuración general de la app
    print("\n1. Configuración General de la Aplicación")
    setup_app_config()

    # 2. Configuración de Power BI
    print("\n2. Configuración del Tablero Power BI")
    powerbi_configured = False
    while not powerbi_configured:
        try:
            powerbi_configured = setup_powerbi()
            if not powerbi_configured:
                retry = input("¿Reintentar configuración de Power BI? (s/n): ").strip().lower()
                if retry != 's':
                    print("⚠️  Configuración de Power BI omitida (se puede configurar después)")
                    break
        except KeyboardInterrupt:
            print("\n⚠️  Configuración de Power BI cancelada")
            break

    # 3. Configuración de autenticación CSV
    print("\n3. Configuración de Autenticación (CSV en OneDrive)")
    csv_configured = False
    while not csv_configured:
        try:
            csv_configured = setup_csv_url()
            if not csv_configured:
                retry = input("¿Reintentar configuración de CSV? (s/n): ").strip().lower()
                if retry != 's':
                    print("⚠️  Configuración de CSV omitida (se puede configurar después)")
                    break
        except KeyboardInterrupt:
            print("\n⚠️  Configuración de CSV cancelada")
            break

    return True


def verify_installation():
    """Verifica que todo esté correctamente instalado"""
    print("\n=== Verificando instalación ===")

    errors = []

    # Verificar archivos principales
    required_files = [
        "main.py",
        "auth_manager.py",
        "powerbi_manager.py",
        "config_manager.py",
        "buildozer.spec"
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            errors.append(f"✗ {file_path} no encontrado")

    # Verificar importaciones
    try:
        import kivy
        print("✓ Kivy instalado")
    except ImportError:
        errors.append("✗ Kivy no instalado")

    try:
        import kivymd
        print("✓ KivyMD instalado")
    except ImportError:
        errors.append("✗ KivyMD no instalado")

    try:
        import pandas
        print("✓ Pandas instalado")
    except ImportError:
        errors.append("✗ Pandas no instalado")

    try:
        import requests
        print("✓ Requests instalado")
    except ImportError:
        errors.append("✗ Requests no instalado")

    try:
        import cryptography
        print("✓ Cryptography instalado")
    except ImportError:
        errors.append("✗ Cryptography no instalado")

    if errors:
        print("\n❌ Errores encontrados:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ Verificación completada sin errores")
        return True


def show_next_steps():
    """Muestra los próximos pasos"""
    print("\n" + "="*50)
    print("CONFIGURACIÓN COMPLETADA")
    print("="*50)

    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1. Configurar OneDrive:")
    print("   - Sube el archivo 'sample_users.csv' a OneDrive")
    print("   - Genera un enlace público para compartir")
    print("   - Ejecuta: python auth_manager.py para configurar la URL")

    print("\n2. Configurar Power BI:")
    print("   - Obtén la URL pública de tu tablero Power BI")
    print("   - Ejecuta: python powerbi_manager.py para configurar")

    print("\n3. Ejecutar la aplicación:")
    print("   - Desarrollo: python main.py")
    print("   - Producción Android: buildozer android debug")

    print("\n4. Archivos importantes:")
    print("   - sample_users.csv: Plantilla de usuarios")
    print("   - main.py: Aplicación principal")
    print("   - buildozer.spec: Configuración para Android")

    print("\n5. Estructura del CSV de usuarios:")
    print("   Columnas requeridas:")
    print("   - usuario: nombre de usuario")
    print("   - password_hash: hash SHA256 de la contraseña")
    print("   - activo: true/false")
    print("   - fecha_expiracion: YYYY-MM-DD")
    print("   - permisos: dashboard,admin,reports")
    print("   - nombre_completo: nombre completo")
    print("   - departamento: departamento")
    print("   - rol: administrador/usuario")

    print("\n🔐 CREDENCIALES DE EJEMPLO:")
    print("   Usuario: admin | Contraseña: admin123")
    print("   Usuario: usuario1 | Contraseña: pass123")

    print("\n📱 GENERAR APK PARA ANDROID:")
    print("   1. Instalar buildozer: pip install buildozer")
    print("   2. Generar APK: buildozer android debug")
    print("   3. El APK estará en: bin/")

    print("\n⚠️  IMPORTANTE:")
    print("   - Mantén seguras las URLs y credenciales")
    print("   - Los archivos de configuración contienen datos encriptados")
    print("   - Actualiza regularmente el CSV de usuarios")


def main():
    """Función principal de configuración"""
    print("Iniciando configuración de PowerBI Mobile Dashboard...")

    try:
        # Crear directorios
        create_directories()

        # Generar archivos de ejemplo
        generate_sample_files()

        # Configuración interactiva
        setup_complete = input("\n¿Proceder con configuración interactiva? (s/n) [s]: ").strip().lower()
        if setup_complete != 'n':
            setup_configuration()

        # Verificar instalación
        if verify_installation():
            show_next_steps()
            print("\n🎉 ¡Configuración completada exitosamente!")
        else:
            print("\n❌ Configuración completada con errores. Revisa los mensajes anteriores.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")


if __name__ == "__main__":
    main()

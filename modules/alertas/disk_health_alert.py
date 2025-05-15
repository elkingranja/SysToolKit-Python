# -*- coding: utf-8 -*-
import platform
import os
import subprocess
import shutil  # Importar shutil para usar shutil.which

def verificar_sistema():
    """Verifica si el sistema es Linux y si smartctl está disponible."""
    if platform.system() != "Linux":
        print("Este modulo solo funciona en sistemas Linux.")
        return False
    if not shutil.which("smartctl"):
        print("El comando 'smartctl' no está disponible. Instálelo antes de continuar.")
        return False
    return True

def verificar_disco(disco):
    """Verifica si el disco especificado es válido."""
    if not os.path.exists(disco):
        print("El disco especificado no existe.")
        return False
    return True

def ejecutar_comando(comando):
    """Ejecuta un comando del sistema de forma segura y captura su salida."""
    try:
        resultado = subprocess.run(comando, shell=True, text=True, capture_output=True, check=True)
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e.stderr}")

def disk_health_alert():
    """Función principal para verificar el estado de salud del disco."""
    print("=== ESTADO DE SALUD DEL DISCO (SMART) ===\n")
    
    if not verificar_sistema():
        return

    disco = input("Ingrese el nombre del disco (por ejemplo: /dev/sda): ").strip()
    if not verificar_disco(disco):
        return

    print(f"\nRevisando estado SMART de {disco}...\n")
    print("Resultado del diagnóstico SMART (breve):\n")
    ejecutar_comando(f"sudo smartctl -H {disco}")

    print("\nInformación completa del disco:\n")
    ejecutar_comando(f"sudo smartctl -A {disco}")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    disk_health_alert()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para verificar el estado de salud del disco utilizando SMART.
    # Utiliza las bibliotecas os, platform y subprocess para manejar archivos y ejecutar comandos del sistema.
    # La función disk_health_alert() verifica si el programa se está ejecutando en Linux y si el comando smartctl está disponible.
    # Se asegura de que el disco especificado sea válido antes de proceder con la verificación.

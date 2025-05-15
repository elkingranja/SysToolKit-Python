#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import subprocess

# Configurar la consola para usar UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def obtener_ruta_log():
    """Determina la ruta del log de autenticación en Linux."""
    for ruta in ("/var/log/auth.log", "/var/log/secure"):
        if os.path.isfile(ruta):
            return ruta
    return None

def mostrar_intentos_fallidos(ruta_log, cantidad=20):
    """Imprime los últimos 'cantidad' intentos fallidos de autenticación."""
    try:
        resultado = subprocess.run(
            ["sudo", "grep", "Failed password", ruta_log],
            check=True,
            text=True,
            capture_output=True
        )
        lines = resultado.stdout.splitlines()[-cantidad:]
        if lines:
            print("\n".join(lines))
        else:
            print("No se encontraron intentos fallidos recientes.")
    except subprocess.CalledProcessError as e:
        print(f"Error al leer el log: {e.stderr or e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def auth_fail_monitor():
    print("MONITOR DE INTENTOS DE AUTENTICACIÓN FALLIDOS\n")

    if platform.system() != "Linux":
        print("Este módulo solo está disponible en sistemas Linux.")
        print("Saliendo del programa...")
        return

    if os.geteuid() != 0:
        print("Este script debe ejecutarse con permisos de administrador (sudo).")
        print("Intenta ejecutarlo nuevamente con: sudo python3 auth_fail_monitor.py")
        return

    ruta_log = obtener_ruta_log()
    if not ruta_log:
        print("No se encontró ningún archivo de log de autenticación. Asegúrate de estar en un sistema Linux con los logs habilitados.")
        return

    try:
        cantidad = int(input("¿Cuántos intentos mostrar? (por defecto 20): ").strip() or 20)
        if cantidad <= 0:
            raise ValueError("El número debe ser mayor que 0.")
    except ValueError:
        print("Entrada inválida. Usando el valor por defecto: 20.")
        cantidad = 20

    print(f"Revisando últimos {cantidad} intentos fallidos en: {ruta_log}\n")
    mostrar_intentos_fallidos(ruta_log, cantidad)
    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    auth_fail_monitor()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para monitorear los intentos de autenticación fallidos en sistemas Linux.
    # Utiliza las bibliotecas os, platform y subprocess para manejar archivos y ejecutar comandos del sistema.
    # La función auth_fail_monitor() verifica si el programa se está ejecutando como superusuario y si el sistema es Linux.
    # Si no se cumplen estas condiciones, informa al usuario y sale del programa.

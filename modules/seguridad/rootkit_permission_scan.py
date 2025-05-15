# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import logging
import sys

# Configurar la consola para usar UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if platform.system() == "Windows" else "clear")

def verificar_permisos():
    """Verifica si el programa se está ejecutando como superusuario en Linux."""
    if platform.system() == "Linux":
        try:
            if os.geteuid() != 0:
                print("Advertencia: se recomienda ejecutar como superusuario (sudo).")
        except AttributeError:
            # os.geteuid no está disponible en Windows
            pass

def escanear_linux():
    print("Escaneo de rootkits (requiere chkrootkit):")
    try:
        resultado = subprocess.run(["sudo", "chkrootkit"], capture_output=True, text=True)
        if resultado.returncode != 0:
            print("chkrootkit no está instalado o no se pudo ejecutar.")
        else:
            print(resultado.stdout)
    except Exception as e:
        logging.error(f"Error al ejecutar chkrootkit: {e}")

    print("\nArchivos con permisos 777:")
    try:
        resultado = subprocess.run(["find", "/", "-type", "f", "-perm", "0777"], capture_output=True, text=True)
        print("\n".join(resultado.stdout.splitlines()[:10]))
    except Exception as e:
        logging.error(f"Error al buscar archivos con permisos 777: {e}")

    print("\nArchivos con SUID:")
    try:
        resultado = subprocess.run(["find", "/", "-type", "f", "-perm", "-4000"], capture_output=True, text=True)
        print("\n".join(resultado.stdout.splitlines()[:10]))
    except Exception as e:
        logging.error(f"Error al buscar archivos con SUID: {e}")

    print("\nArchivos con SGID:")
    try:
        resultado = subprocess.run(["find", "/", "-type", "f", "-perm", "-2000"], capture_output=True, text=True)
        print("\n".join(resultado.stdout.splitlines()[:10]))
    except Exception as e:
        logging.error(f"Error al buscar archivos con SGID: {e}")

def escanear_windows():
    print("Archivos .exe/.bat con permisos totales para 'Everyone' en carpetas públicas:\n")
    carpetas = [
        "C:\\Users\\Public",
        "C:\\ProgramData",
        "C:\\Temp"
    ]

    encontrados = False  # Bandera para verificar si se encontraron archivos

    for carpeta in carpetas:
        if os.path.exists(carpeta):
            for raiz, _, archivos in os.walk(carpeta):
                for archivo in archivos:
                    if archivo.endswith(('.exe', '.bat', '.ps1')):
                        ruta = os.path.join(raiz, archivo)
                        try:
                            resultado = subprocess.run(["icacls", ruta], capture_output=True, text=True)
                            if "Everyone:(F)" in resultado.stdout:
                                print(f"Archivo con permiso total: {ruta}")
                                encontrados = True
                        except Exception as e:
                            logging.error(f"Error al revisar {ruta}: {e}")

    if not encontrados:
        print("No se encontraron archivos con permisos totales para 'Everyone'.")

def rootkit_permission_scan():
    """Función principal para escanear permisos y rootkits."""
    clear_screen()
    verificar_permisos()
    print("=== ESCANEO DE PERMISOS Y ROOTKITS ===\n")
    sistema = platform.system()

    if sistema == "Linux":
        escanear_linux()
    elif sistema == "Windows":
        escanear_windows()
    else:
        print("Sistema operativo no compatible.")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    rootkit_permission_scan()
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una herramienta para escanear permisos y rootkits en sistemas Linux y Windows.
# Utiliza las bibliotecas os, platform y subprocess para manejar archivos y ejecutar comandos del sistema.
# La función rootkit_permission_scan() verifica si el programa se está ejecutando como superusuario en Linux.
# Dependiendo del sistema operativo, ejecuta diferentes escaneos:
# En Linux, utiliza chkrootkit para buscar rootkits y encuentra archivos con permisos 777, SUID y SGID.
# En Windows, busca archivos .exe/.bat/.ps1 con permisos totales para 'Everyone' en carpetas públicas.
# El módulo también maneja errores y proporciona mensajes de advertencia según sea necesario.
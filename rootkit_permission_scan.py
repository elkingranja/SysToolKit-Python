# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import logging
import sys
import ctypes

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
    elif platform.system() == "Windows":
        if not es_administrador():
            print("Advertencia: se recomienda ejecutar como administrador en Windows.")

def es_administrador():
    """Verifica si el script se está ejecutando con privilegios de administrador en Windows."""
    try:
        return os.getuid() == 0  # Esto funciona en Linux
    except AttributeError:
        # En Windows, verifica permisos administrativos
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def comando_disponible(comando):
    """Verifica si un comando está disponible en el sistema."""
    return subprocess.run(["which", comando], capture_output=True, text=True).returncode == 0

def mostrar_resultados(resultado, limite=10):
    """Muestra los resultados de un comando con un límite opcional."""
    lineas = resultado.stdout.splitlines()
    print("\n".join(lineas[:limite]))
    if len(lineas) > limite:
        print(f"... y {len(lineas) - limite} más. Usa --ver-todo para mostrar todo.")

def escanear_linux():
    print("Escaneo de rootkits (requiere chkrootkit):")
    if not comando_disponible("chkrootkit"):
        print("chkrootkit no está instalado o no se pudo ejecutar.")
        print("Por favor, instala chkrootkit con el siguiente comando:")
        print("sudo apt install chkrootkit")
        return

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
        mostrar_resultados(resultado)
    except Exception as e:
        logging.error(f"Error al buscar archivos con permisos 777: {e}")

    print("\nArchivos con SUID:")
    try:
        resultado = subprocess.run(["find", "/", "-type", "f", "-perm", "-4000"], capture_output=True, text=True)
        mostrar_resultados(resultado)
    except Exception as e:
        logging.error(f"Error al buscar archivos con SUID: {e}")

    print("\nArchivos con SGID:")
    try:
        resultado = subprocess.run(["find", "/", "-type", "f", "-perm", "-2000"], capture_output=True, text=True)
        mostrar_resultados(resultado)
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

"""
Este módulo proporciona una herramienta para escanear permisos y rootkits en sistemas Linux y Windows.

Características:
- Verifica si el programa se ejecuta como superusuario en Linux.
- Escanea rootkits usando chkrootkit (Linux).
- Busca archivos con permisos 777, SUID y SGID (Linux).
- Busca archivos .exe/.bat/.ps1 con permisos totales para 'Everyone' en carpetas públicas (Windows).

Dependencias:
- Linux: chkrootkit, find
- Windows: icacls

Uso:
- Ejecuta el script directamente para iniciar el escaneo.
"""
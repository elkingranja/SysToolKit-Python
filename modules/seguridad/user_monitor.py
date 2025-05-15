# -*- coding: utf-8 -*-
import platform
import subprocess
import shutil
import os
import sys

# Configurar la consola para usar UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

# Constantes para mensajes
SEPARADOR = "=" * 30
MSG_NO_COMPATIBLE = "Sistema operativo no compatible."
MSG_PRESIONA_ENTER = "\nPresiona Enter para volver al menú..."

def comando_disponible(comando):
    """Verifica si un comando está disponible en el sistema."""
    return shutil.which(comando) is not None

def mostrar_usuarios_linux():
    """Muestra los usuarios conectados en sistemas Linux."""
    if not comando_disponible("who"):
        print("El comando 'who' no está disponible en este sistema.")
        return

    try:
        resultado = subprocess.check_output(["who"], text=True)
        print(resultado)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar 'who':", e.output.strip())
    except Exception as e:
        print(f"Error inesperado al ejecutar 'who': {e}")

def mostrar_usuarios_windows():
    """Muestra los usuarios conectados en sistemas Windows."""
    if not comando_disponible("query"):
        print("El comando 'query user' no está disponible en este sistema.")
        return

    try:
        resultado = subprocess.check_output("query user", shell=True, text=True, stderr=subprocess.STDOUT)
        print(resultado)
    except subprocess.CalledProcessError as e:
        print("Este comando requiere Windows Pro o superior o privilegios de administrador.")
        print("Detalles:", e.output.strip())
    except Exception as e:
        print(f"Error inesperado al ejecutar 'query user': {e}")

def user_monitor():
    """Función principal para mostrar usuarios conectados según el sistema operativo."""
    print(SEPARADOR)
    print("USUARIOS CONECTADOS")
    print(SEPARADOR)

    sistema = platform.system()

    if sistema == "Linux":
        mostrar_usuarios_linux()
    elif sistema == "Windows":
        mostrar_usuarios_windows()
    else:
        print(MSG_NO_COMPATIBLE)

    input(MSG_PRESIONA_ENTER)

if __name__ == "__main__":
    user_monitor()
    input("\nPresiona Enter para volver al menú...")

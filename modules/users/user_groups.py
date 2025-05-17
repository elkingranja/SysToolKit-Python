#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import subprocess

# Configurar consola Windows a UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

def obtener_comando(usuario):
    """Devuelve el comando adecuado según el sistema operativo."""
    so = platform.system()
    if so == "Linux":
        return ["groups", usuario]
    elif so == "Windows":
        if usuario.lower() != os.getlogin().lower():
            print("En Windows, solo se pueden consultar los grupos del usuario actual.")
            return None
        return ["whoami", "/groups"]
    else:
        print(f"Sistema operativo no soportado: {so}")
        return None

def ejecutar_comando(cmd):
    """Ejecuta un comando en el sistema y devuelve la salida."""
    try:
        salida = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return salida.strip()
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando:")
        print(e.output.strip())
    except FileNotFoundError:
        print("El comando no se encontró. Verifica que esté instalado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    return None

def user_groups():
    """Consulta los grupos de un usuario."""
    print("CONSULTA DE GRUPOS DE USUARIO\n")
    usuario = input("Ingrese el nombre del usuario: ").strip()
    if not usuario:
        print("Nombre de usuario inválido.")
        return

    cmd = obtener_comando(usuario)
    if not cmd:
        return

    salida = ejecutar_comando(cmd)
    if salida:
        print("\nGrupos del usuario:")
        print(salida)

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    user_groups()
    input("\nPresiona Enter para volver al menú...")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import re

# Asegurar UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

def validar_nombre_usuario(nombre):
    """Valida que el nombre del usuario cumpla con las reglas de Linux."""
    patron = r'^[a-z_][a-z0-9_-]*[$]?$'  # Patrón para nombres de usuario válidos
    return re.match(patron, nombre) is not None

def user_creator():
    print("CREACIÓN DE USUARIO (solo Linux)\n")

    if sys.platform != "linux":
        print("ERROR: Este módulo solo funciona en sistemas Linux.")
        print("Por favor, ejecuta este script en un sistema operativo basado en Linux.")
        input("Presiona Enter para salir...")
        return

    nombre = input("Nombre del nuevo usuario: ").strip()
    if not nombre:
        print("Nombre inválido. No puede estar vacío.")
        return

    if not validar_nombre_usuario(nombre):
        print("Nombre inválido. Asegúrate de usar solo caracteres permitidos (letras, números, guiones bajos o guiones).")
        return

    confirmar = input(f"¿Estás seguro de que deseas crear el usuario '{nombre}'? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operación cancelada.")
        return

    # Construir comando y ejecutarlo capturando salida y errores
    cmd = ["sudo", "useradd", "-m", nombre]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Usuario '{nombre}' creado correctamente.")
    except subprocess.CalledProcessError as e:
        print("Error al crear el usuario:")
        print(e.stderr or e.stdout or str(e))
    except Exception as e:
        print("Error inesperado:", str(e))

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    user_creator()
    input("\nPresiona Enter para volver al menú...")

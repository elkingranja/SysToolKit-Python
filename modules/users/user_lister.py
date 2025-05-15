#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import subprocess

def configurar_utf8_windows():
    """Configura la consola de Windows para usar UTF-8."""
    try:
        subprocess.run(["chcp", "65001"], shell=True, check=True, stdout=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception as e:
        print("Advertencia: No se pudo configurar UTF-8. Asegúrate de usar Python 3.7 o superior.")

def listar_usuarios_linux():
    passwd = "/etc/passwd"
    if not os.path.isfile(passwd):
        print("No se encontró /etc/passwd")
        return

    try:
        with open(passwd, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.split(":")
                nombre = partes[0]
                shell = partes[-1].strip()
                uid = int(partes[2])
                if uid >= 1000 and nombre != "nobody":
                    print(f"{nombre}\t{shell}")
    except Exception as e:
        print(f"Error leyendo /etc/passwd: {e}. Verifica que el archivo existe y tiene los permisos correctos.")

def listar_usuarios_windows():
    try:
        # Ejecutar el comando 'net user' para listar los usuarios
        result = subprocess.run(
            ["net", "user"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        usuarios = []
        for linea in result.stdout.splitlines():
            # Filtrar líneas que contienen nombres de usuarios
            if linea.strip() and not linea.startswith("Cuentas de usuario") and not linea.startswith("-----") and not linea.startswith("Se ha completado"):
                usuarios.extend(linea.split())

        print(f"\nNúmero total de usuarios locales: {len(usuarios)}")
        print("Usuarios locales y sus roles:")
        for usuario in usuarios:
            print(f"\nUsuario: {usuario}")
            # Obtener detalles del usuario con 'net user <usuario>'
            detalles = subprocess.run(
                ["net", "user", usuario],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            roles_encontrados = False
            for detalle in detalles.stdout.splitlines():
                if "Administradores" in detalle or "Usuarios" in detalle:
                    print(f"  Rol: {detalle.strip()}")
                    roles_encontrados = True
            if not roles_encontrados:
                print("  Rol: No se encontraron roles asociados.")
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando 'net user'. Asegúrate de tener permisos de administrador.")
        print(e.stderr or e.stdout)

def main():
    if sys.platform.startswith("win"):
        configurar_utf8_windows()

    so = platform.system()
    print(f"Sistema operativo: {so} {platform.release()}\n")

    if so == "Linux":
        print("Usuarios registrados (/etc/passwd):")
        listar_usuarios_linux()
    elif so == "Windows":
        print("Usuarios locales (net user):")
        listar_usuarios_windows()
    else:
        print(f"Sistema operativo no compatible: {so}. Este script solo soporta Linux y Windows.")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")
    # Si el script se importa como un módulo, no se ejecutará automáticamente.
    # Esto es útil para pruebas unitarias o para evitar la ejecución accidental.
    # El código se ejecuta directamente si se llama a este script
    # desde la línea de comandos. Si se importa como un módulo, no se ejecutará.

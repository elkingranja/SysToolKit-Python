#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import shutil

# Configurar UTF-8 en consola Windows
if sys.platform == "win32":
    try:
        subprocess.run(["chcp", "65001"], shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DESCRIPTION = """
SysToolKit – app_installer
Instala una o varias aplicaciones usando el gestor de paquetes disponible:
  * Linux: apt, dnf, pacman
  * Windows: winget
"""

def detect_linux_package_manager():
    if shutil.which("apt"):
        return "apt"
    elif shutil.which("dnf"):
        return "dnf"
    elif shutil.which("pacman"):
        return "pacman"
    return None

def install_linux(apps, manager):
    try:
        if manager == "apt":
            cmd = ["sudo", "apt", "install", "-y"] + apps
        elif manager == "dnf":
            cmd = ["sudo", "dnf", "install", "-y"] + apps
        elif manager == "pacman":
            cmd = ["sudo", "pacman", "-S", "--noconfirm"] + apps
        else:
            print("Gestor de paquetes no soportado.")
            return

        subprocess.run(cmd, check=True)
        print(f"[OK] Aplicaciones instaladas: {', '.join(apps)}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] No se pudieron instalar las aplicaciones: {e}")

def install_windows(apps):
    for app in apps:
        # Buscar el identificador usando winget search
        try:
            result = subprocess.run(
                ["winget", "search", "--name", app],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.splitlines()
            # Buscar líneas que tengan identificador (ID)
            opciones = []
            for line in lines:
                if "Id" in line and "Name" in line:
                    continue  # Saltar encabezado
                parts = line.split()
                if len(parts) >= 2:
                    opciones.append((parts[0], " ".join(parts[1:])))
            if not opciones:
                print(f"[ERROR] No se encontró ningún paquete para: {app}")
                continue
            # Si hay varias opciones, mostrar y pedir al usuario
            if len(opciones) > 1:
                print(f"Se encontraron varias opciones para '{app}':")
                for idx, (id_, name) in enumerate(opciones, 1):
                    print(f"{idx}. {name} ({id_})")
                print("0. No instalar ninguna de estas opciones")
                seleccion = input("Elige el número de la aplicación a instalar (o 0 para cancelar): ").strip()
                try:
                    seleccion = int(seleccion)
                    if seleccion == 0:
                        print(f"[INFO] No se instalará '{app}'.")
                        continue
                    seleccion -= 1
                    app_id = opciones[seleccion][0]
                except Exception:
                    print("[ERROR] Selección inválida.")
                    continue
            else:
                app_id = opciones[0][0]
            # Instalar usando el identificador encontrado
            subprocess.run([
                "winget", "install", "--silent", "--accept-source-agreements",
                "--accept-package-agreements", "--id", app_id
            ], check=True)
            print(f"[OK] Aplicación instalada: {app_id}")
        except subprocess.CalledProcessError:
            print(f"[ERROR] No se pudo instalar: {app}")

def main():
    parser = argparse.ArgumentParser(
        prog="app_installer",
        description="Instala una o varias aplicaciones usando el gestor de paquetes disponible:\n  * Linux: apt, dnf, pacman\n  * Windows: winget",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    parser.add_argument("apps", nargs="*", help="Aplicaciones a instalar")  # Cambia + por *
    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                        help="Muestra este mensaje de ayuda y sale")

    args = parser.parse_args()
    apps = args.apps

    # Si no se pasan apps por argumento, preguntar al usuario
    if not apps:
        entrada = input("¿Qué aplicación(es) deseas instalar? (separa por espacios): ").strip()
        if not entrada:
            print("[ERROR] No se proporcionaron aplicaciones para instalar.")
            sys.exit(1)
        apps = entrada.split()

    sistema = sys.platform

    if sistema.startswith("linux"):
        gestor = detect_linux_package_manager()
        if not gestor:
            print("[ERROR] No se detectó un gestor de paquetes compatible.")
            sys.exit(1)
        install_linux(apps, gestor)

    elif sistema in ("win32", "cygwin"):
        if shutil.which("winget"):
            install_windows(apps)
        else:
            print("[ERROR] winget no está disponible en este sistema.")

    elif sistema == "darwin":
        if shutil.which("brew"):
            try:
                for app in apps:
                    subprocess.run(["brew", "install", app], check=True)
                    print(f"[OK] Aplicación instalada: {app}")
            except subprocess.CalledProcessError:
                print(f"[ERROR] No se pudo instalar: {app}")
        else:
            print("[ERROR] Homebrew no está disponible en este sistema.")

    else:
        print("ERROR: Sistema operativo no compatible.")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")


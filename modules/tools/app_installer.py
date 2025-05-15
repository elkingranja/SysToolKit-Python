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
        try:
            subprocess.run(["winget", "install", "--silent", "--accept-source-agreements",
                            "--accept-package-agreements", "--id", app], check=True)
            print(f"[OK] Aplicación instalada: {app}")
        except subprocess.CalledProcessError:
            print(f"[ERROR] No se pudo instalar: {app}")

def main():
    parser = argparse.ArgumentParser(
        prog="app_installer",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("apps", nargs="+", help="Aplicaciones a instalar")

    args = parser.parse_args()
    apps = args.apps

    if not apps:
        print("[ERROR] No se proporcionaron aplicaciones para instalar.")
        sys.exit(1)

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

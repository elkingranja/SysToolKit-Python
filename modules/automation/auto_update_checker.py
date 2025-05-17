"""
Módulo: auto_update_checker.py
Descripción: Verifica e instala actualizaciones del sistema en Linux y verifica actualizaciones en Windows.
Compatibilidad: Linux (verificación + instalación), Windows (solo verificación).
Autor: [Tu Nombre]
Proyecto: SysToolKit
"""

import platform
import subprocess
import sys
import os
import ctypes
import shutil
import argparse

def configurar_utf8():
    if sys.platform == "win32":
        try:
            subprocess.run("chcp 65001", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError as e:
            print("Advertencia: no se pudo reconfigurar la consola en UTF-8:", e)
        except subprocess.SubprocessError as e:
            print("Advertencia: error al ejecutar el comando chcp:", e)
        except Exception as e:
            print("Advertencia: error inesperado al configurar UTF-8:", e)

def es_administrador():
    if os.name == 'nt':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def verificar_actualizaciones_linux():
    try:
        if shutil.which("apt"):
            resultado = subprocess.check_output(["apt", "list", "--upgradable"], stderr=subprocess.DEVNULL, text=True)
            lineas = resultado.splitlines()[1:]
            return lineas if lineas else []
        elif shutil.which("dnf"):
            resultado = subprocess.check_output(["dnf", "check-update"], stderr=subprocess.DEVNULL, text=True)
            return resultado.splitlines() if "No packages marked for update" not in resultado else []
        elif shutil.which("yum"):
            resultado = subprocess.check_output(["yum", "check-update"], stderr=subprocess.DEVNULL, text=True)
            return resultado.splitlines() if resultado else []
        elif shutil.which("zypper"):
            resultado = subprocess.check_output(["zypper", "list-updates"], stderr=subprocess.DEVNULL, text=True)
            return resultado.splitlines()[2:] if resultado else []
        else:
            return None  # No gestor compatible
    except Exception as e:
        return f"Error: {e}"

def instalar_actualizaciones_linux():
    print("\nInstalando actualizaciones...\n")
    try:
        if shutil.which("apt"):
            subprocess.run(["sudo", "apt", "update"])
            subprocess.run(["sudo", "apt", "upgrade", "-y"])
        elif shutil.which("dnf"):
            subprocess.run(["sudo", "dnf", "upgrade", "-y"])
        elif shutil.which("yum"):
            subprocess.run(["sudo", "yum", "update", "-y"])
        elif shutil.which("zypper"):
            subprocess.run(["sudo", "zypper", "refresh"])
            subprocess.run(["sudo", "zypper", "update", "-y"])
        else:
            print("No se encontró un gestor de paquetes compatible para instalar actualizaciones.")
            return
        print("Actualizaciones instaladas correctamente.")
    except Exception as e:
        print("Error al instalar actualizaciones:", e)

def verificar_actualizaciones_windows():
    print("Verificando actualizaciones en Windows...\n")
    try:
        script = """
        $Session = New-Object -ComObject Microsoft.Update.Session
        $Searcher = $Session.CreateUpdateSearcher()
        $Results = $Searcher.Search("IsInstalled=0 and Type='Software'")
        $Results.Updates | ForEach-Object { $_.Title }
        """
        salida = subprocess.check_output(["powershell", "-Command", script], text=True, stderr=subprocess.DEVNULL)
        if salida.strip():
            print("Actualizaciones disponibles:\n")
            print(salida)
        else:
            print("El sistema ya está actualizado.")
    except Exception as e:
        print("No se pudo verificar actualizaciones en Windows (requiere versión Pro o superior).")
        print("Detalle:", e)

def mostrar_resultados(actualizaciones):
    if isinstance(actualizaciones, str):
        print(actualizaciones)
    elif actualizaciones is None:
        print("No se encontró un gestor de paquetes compatible.")
    elif actualizaciones:
        print("Actualizaciones disponibles:\n")
        print("\n".join(actualizaciones))
    else:
        print("El sistema ya está actualizado.")

def auto_update_checker(auto_install=False, no_pause=False):
    configurar_utf8()
    print("=== VERIFICADOR DE ACTUALIZACIONES ===\n")
    sistema = platform.system()

    if sistema == "Linux":
        hay_actualizaciones = verificar_actualizaciones_linux()
        mostrar_resultados(hay_actualizaciones)
        if hay_actualizaciones:
            if auto_install:
                print("\nInstalando actualizaciones automáticamente...\n")
                instalar_actualizaciones_linux()
            else:
                while True:
                    opcion = input("\n¿Deseas instalar las actualizaciones ahora? (s/n): ").strip().lower()
                    if opcion in ["s", "n"]:
                        break
                    print("Entrada no válida. Por favor, ingresa 's' para sí o 'n' para no.")
                if opcion == "s":
                    instalar_actualizaciones_linux()
                else:
                    print("Actualizaciones no instaladas.")
    elif sistema == "Windows":
        verificar_actualizaciones_windows()
        print("Nota: la instalación automática no es compatible en esta versión.")
    else:
        print("Sistema operativo no compatible.")

    if not no_pause:
        input("\nPresiona Enter para volver al menú...")

def main():
    parser = argparse.ArgumentParser(description="Verifica e instala actualizaciones del sistema.")
    parser.add_argument('--auto', action='store_true', help='Instala actualizaciones automáticamente si hay.')
    parser.add_argument('--no-pause', action='store_true', help='No esperar input al finalizar.')
    args = parser.parse_args()

    if not es_administrador():
        print("Este script requiere permisos de administrador para ejecutarse.")
        input("Presiona Enter para salir...")
    else:
        try:
            auto_update_checker(args.auto, args.no_pause)
        except Exception as e:
            print(f"Error crítico: {e}")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception:
        sys.exit(1)


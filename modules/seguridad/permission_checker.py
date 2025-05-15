#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess
import ctypes  # Para verificar permisos de administrador en Windows

# Configurar consola Windows a UTF-8
if sys.platform == "win32":
    try:
        # Cambiar code page a UTF-8
        subprocess.run(["chcp", "65001"], shell=True, check=True, stdout=subprocess.DEVNULL)
        # Reconfigurar stdout a UTF-8
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_command(cmd):
    """
    Ejecuta cmd (lista para subprocess) y retorna (stdout, stderr, exitcode).
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform=="win32"))
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def revisar_linux():
    print("Permisos inseguros en Linux:\n")

    for desc, cmd in [
        ("Archivos con permisos 777", ["find", "/", "-type", "f", "-perm", "0777"]),
        ("Archivos con SUID",      ["find", "/", "-type", "f", "-perm", "-4000"]),
        ("Archivos con SGID",      ["find", "/", "-type", "f", "-perm", "-2000"])
    ]:
        print(f"== {desc} ==")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.DEVNULL)
            lines = result.stdout.strip().split("\n")[:10]  # Limitar a 10 resultados
            if lines:
                print("\n".join(lines))
            else:
                print("No se encontraron resultados.")
        except Exception as e:
            print(f"Error ejecutando el comando: {e}")
        print()

def es_administrador():
    """
    Verifica si el script se está ejecutando con privilegios de administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def revisar_windows():
    print("Revisión de permisos en Windows:\n")
    es_admin = es_administrador()
    if not es_admin:
        print("Advertencia: No estás ejecutando el script como administrador. Algunos archivos pueden ser ignorados.\n")

    carpetas = [
        r"C:\Users\Public",
        r"C:\ProgramData",
        r"C:\Temp"
    ]
    archivos_excluidos = ["McInst.exe"]
    for carpeta in carpetas:
        if not os.path.isdir(carpeta):
            continue
        print(f"Procesando carpeta: {carpeta}")
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.lower().endswith(('.exe', '.bat', '.ps1')):
                    ruta = os.path.join(root, file)
                    if os.path.basename(ruta) in archivos_excluidos:
                        print(f"Ignorando archivo excluido: {ruta} (archivo conocido o seguro)")
                        continue
                    cmd = f'icacls "{ruta}"'
                    out, err, code = run_command(cmd)
                    if code != 0 or not out:
                        razon = "requiere permisos elevados" if not es_admin else "no se pudo verificar permisos"
                        print(f"Ignorando archivo: {ruta} ({razon})")
                        if err:
                            print(f"Detalles del error: {err}")
                        continue
                    if "Everyone:(F)" in out:
                        print(f"PERMISO TOTAL para Everyone: {ruta}")
        print()

def permission_checker():
    print("=== Verificador de Permisos Peligrosos ===\n")
    sistema = platform.system()

    if sistema == "Linux":
        print(">>> Escaneando sistema Linux...\n")
        revisar_linux()
    elif sistema == "Windows":
        print(">>> Escaneando sistema Windows...\n")
        revisar_windows()
    else:
        print("Sistema operativo no compatible.")

    input("\nPresione Enter para terminar...")

if __name__ == "__main__":
    permission_checker()
    input("\nPresiona Enter para volver al menú...")
    # Este script verifica permisos inseguros en sistemas Linux y Windows.
    # En Linux, busca archivos con permisos 777, SUID y SGID.
    # En Windows, revisa permisos de carpetas públicas y temporales.
    # Se necesita ejecutar como administrador para evitar restricciones de permisos.

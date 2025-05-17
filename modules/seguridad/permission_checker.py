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

def revisar_linux(ruta=None, limite=10):
    print("Permisos inseguros en Linux:\n")

    for desc, cmd in [
        ("Archivos con permisos 777", ["find", ruta or "/", "-type", "f", "-perm", "0777"]),
        ("Archivos con SUID",      ["find", ruta or "/", "-type", "f", "-perm", "-4000"]),
        ("Archivos con SGID",      ["find", ruta or "/", "-type", "f", "-perm", "-2000"])
    ]:
        print(f"== {desc} ==")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.DEVNULL)
            lines = result.stdout.strip().split("\n")[:limite]  # Limitar a 'limite' resultados
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

def revisar_windows(ruta=None, limite=10, completo=False):
    print("Revisión de permisos en Windows:\n")
    es_admin = es_administrador()
    if not es_admin:
        print("Advertencia: No estás ejecutando el script como administrador. Algunos archivos pueden ser ignorados.\n")

    if completo or not ruta:
        carpetas = [
            r"C:\Users\Public",
            r"C:\ProgramData",
            r"C:\Temp",
            r"C:\\",  # Disco raíz
            r"C:\Windows",
            r"C:\Program Files",
            r"C:\Program Files (x86)"
        ]
    else:
        carpetas = [ruta]

    archivos_excluidos = ["McInst.exe"]
    revisados = 0
    encontrados = 0
    resultados = []
    for carpeta in carpetas:
        if not os.path.isdir(carpeta):
            continue
        print(f"Procesando carpeta: {carpeta}")
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.lower().endswith(('.exe', '.bat', '.ps1')):
                    ruta_archivo = os.path.join(root, file)
                    revisados += 1
                    if os.path.basename(ruta_archivo) in archivos_excluidos:
                        print(f"Ignorando archivo excluido: {ruta_archivo} (archivo conocido o seguro)")
                        continue
                    cmd = f'icacls "{ruta_archivo}"'
                    out, err, code = run_command(cmd)
                    if code != 0 or not out:
                        continue
                    if "Everyone:(F)" in out:
                        mensaje = f"PERMISO TOTAL para Everyone: {ruta_archivo}"
                        print(mensaje)
                        resultados.append(mensaje)
                        encontrados += 1
                        if limite and encontrados >= limite:
                            break
            if limite and encontrados >= limite:
                break
        print()
    print(f"Archivos revisados: {revisados}")
    print(f"Archivos con permisos peligrosos encontrados: {encontrados}")
    return resultados

def main():
    print("=== Verificador de Permisos Peligrosos ===\n")
    sistema = platform.system()

    if sistema == "Linux":
        print(">>> Escaneando sistema Linux...\n")
        ruta = input("¿Ruta específica a revisar? (deja vacío para todo el sistema): ").strip() or None
        try:
            limite = int(input("¿Cuántos resultados máximos mostrar por tipo? [10]: ") or "10")
        except ValueError:
            limite = 10
        revisar_linux(ruta=ruta, limite=limite)
    elif sistema == "Windows":
        print(">>> Escaneando sistema Windows...\n")
        eleccion = input("¿Quieres una revisión completa? (s/n): ").strip().lower()
        if eleccion == "s":
            completo = True
            ruta = None
        else:
            completo = False
            ruta = input("Introduce la ruta a revisar: ").strip()
            if not ruta:
                print("No se indicó ruta. Saliendo.")
                return
        try:
            limite = int(input("¿Cuántos resultados máximos mostrar? [10]: ") or "10")
        except ValueError:
            limite = 10
        revisar_windows(ruta=ruta, limite=limite, completo=completo)
    else:
        print("Sistema operativo no compatible.")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")
    # Este script verifica permisos inseguros en sistemas Linux y Windows.
    # En Linux, busca archivos con permisos 777, SUID y SGID.
    # En Windows, revisa permisos de carpetas públicas y temporales.
    # Se necesita ejecutar como administrador para evitar restricciones de permisos.

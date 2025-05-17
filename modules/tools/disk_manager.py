#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import hashlib
from collections import defaultdict
import psutil

# UTF‑8 en Windows
if sys.platform == "win32":
    try:
        subprocess.run(["chcp", "65001"], shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DESCRIPTION = """
SysToolKit – disk_manager
Gestión avanzada de disco:
  * list          Listar particiones y uso
  * topdirs       Carpetas más grandes
  * duplicates    Archivos duplicados en un directorio
"""

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def validate_path(path):
    if not os.path.isdir(path):
        print(f"ERROR: La ruta '{path}' no es válida o no es un directorio.")
        return False
    return True

def list_partitions():
    parts = psutil.disk_partitions(all=False)
    for p in parts:
        try:
            u = psutil.disk_usage(p.mountpoint)
            print(f"{p.device}  {p.mountpoint}")
            print(f"  Total: {format_size(u.total)}")
            print(f"  Usado: {format_size(u.used)} ({u.percent}%)\n")
        except PermissionError:
            print(f"{p.device}  {p.mountpoint}  (sin permisos)\n")

def top_directories(path, n):
    sizes = {}
    for root, dirs, files in os.walk(path):
        total = 0
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                continue
        sizes[root] = total
    top = sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:n]
    for folder, size in top:
        print(f"{folder} — {format_size(size)}")

def find_duplicates(path):
    size_map = defaultdict(list)
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                sz = os.path.getsize(fp)
                size_map[sz].append(fp)
            except OSError:
                continue
    dup = defaultdict(list)
    for sz, files in size_map.items():
        if len(files) < 2:
            continue
        hashes = {}
        for fp in files:
            try:
                h = hashlib.sha1()
                with open(fp, "rb") as f:
                    while chunk := f.read(8192):
                        h.update(chunk)
                digest = h.hexdigest()
                hashes.setdefault(digest, []).append(fp)
            except OSError:
                continue
        for group in hashes.values():
            if len(group) > 1:
                dup[sz].extend(group)
    if not dup:
        print("No se encontraron archivos duplicados.")
    for sz, files in dup.items():
        print(f"\nArchivos de {format_size(sz)} duplicados:")
        for fp in files:
            print(f"  {fp}")

def main():
    parser = argparse.ArgumentParser(
        prog="disk_manager",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=False)  # Cambia required a False

    sub.add_parser("list", help="Listar particiones y uso")

    p = sub.add_parser("topdirs", help="Mostrar N carpetas más grandes")
    p.add_argument("path", help="Ruta de carpeta a analizar")
    p.add_argument("--n", type=int, default=5, help="Número de carpetas (por defecto 5)")

    p = sub.add_parser("duplicates", help="Buscar archivos duplicados en un directorio")
    p.add_argument("path", help="Ruta de carpeta a escanear")

    # Si no hay argumentos, preguntar al usuario
    if len(sys.argv) == 1:
        print("¿Qué acción deseas realizar?")
        print("1. Listar particiones y uso")
        print("2. Mostrar N carpetas más grandes")
        print("3. Buscar archivos duplicados en un directorio")
        opcion = input("Elige una opción (1-3): ").strip()
        if opcion == "1":
            list_partitions()
        elif opcion == "2":
            ruta = input("Introduce la ruta de la carpeta a analizar: ").strip()
            if not validate_path(ruta):
                sys.exit(1)
            try:
                n = int(input("¿Cuántas carpetas quieres mostrar? [5]: ").strip() or "5")
            except ValueError:
                n = 5
            top_directories(ruta, n)
        elif opcion == "3":
            ruta = input("Introduce la ruta de la carpeta a escanear: ").strip()
            if not validate_path(ruta):
                sys.exit(1)
            find_duplicates(ruta)
        else:
            print("Opción no válida.")
        return

    args = parser.parse_args()

    if args.cmd == "list":
        list_partitions()
    elif args.cmd == "topdirs":
        if validate_path(args.path):
            top_directories(args.path, args.n)
    elif args.cmd == "duplicates":
        if validate_path(args.path):
            find_duplicates(args.path)

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")

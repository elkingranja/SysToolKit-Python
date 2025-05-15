#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

# Configurar consola Windows para UTF-8
if sys.platform == "win32":
    try:
        subprocess.run(["chcp", "65001"], shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DESCRIPTION = """
SysToolKit – scheduler
Permite crear, listar y eliminar tareas programadas:
  * Linux (cron)
  * Windows (schtasks)
"""

def add_task_linux(cmd, interval, name):
    # interval en minutos
    cron_line = f"*/{interval} * * * * {cmd} # {name}"
    try:
        # obtener crontab actual
        proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = proc.stdout if proc.returncode == 0 else ""
        new_cron = existing + cron_line + "\n"
        p = subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
        print(f"[OK] Tarea '{name}' añadida cada {interval} minutos.")
    except Exception as e:
        print(f"[ERROR] add_task_linux: {e}")

def list_tasks_linux():
    try:
        proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        print("Tareas cron actuales:\n" + proc.stdout)
    except subprocess.CalledProcessError:
        print("No hay tareas cron definidas.")

def remove_task_linux(name):
    try:
        proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        lines = [l for l in proc.stdout.splitlines() if f"# {name}" not in l]
        new_cron = "\n".join(lines) + "\n"
        subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
        print(f"[OK] Tarea '{name}' eliminada.")
    except Exception as e:
        print(f"[ERROR] remove_task_linux: {e}")

def add_task_windows(cmd, interval, name):
    # interval en minutos
    try:
        subprocess.run([
            "schtasks", "/Create",
            "/SC", "MINUTE",
            "/MO", str(interval),
            "/TN", name,
            "/TR", cmd
        ], check=True, capture_output=True)
        print(f"[OK] Tarea '{name}' creada cada {interval} minutos.")
    except Exception as e:
        print(f"[ERROR] add_task_windows: {e}")

def list_tasks_windows():
    try:
        proc = subprocess.run(["schtasks"], capture_output=True, text=True, check=True)
        print("Tareas programadas:\n" + proc.stdout)
    except Exception as e:
        print(f"[ERROR] list_tasks_windows: {e}")

def remove_task_windows(name):
    try:
        subprocess.run(["schtasks", "/Delete", "/TN", name, "/F"],
                       check=True, capture_output=True)
        print(f"[OK] Tarea '{name}' eliminada.")
    except Exception as e:
        print(f"[ERROR] remove_task_windows: {e}")

def main():
    parser = argparse.ArgumentParser(
        prog="scheduler",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="action", required=True, metavar="accion")

    # Agregar
    p = sub.add_parser("add", help="Agregar tarea programada")
    p.add_argument("--cmd", required=True, help="Comando o script a ejecutar")
    p.add_argument("--interval", type=int, required=True,
                   help="Intervalo en minutos")
    p.add_argument("--name", required=True, help="Nombre identificador de la tarea")

    # Listar
    sub.add_parser("list", help="Listar tareas programadas")

    # Eliminar
    p = sub.add_parser("remove", help="Eliminar tarea por nombre")
    p.add_argument("--name", required=True, help="Nombre identificador de la tarea")

    args = parser.parse_args()
    sistema = sys.platform  # Corregir indentación

    if sistema.startswith("linux"):
        if args.action == "add":
            if args.interval <= 0:  # Validación adicional
                print("[ERROR] El intervalo debe ser un número positivo.")
                sys.exit(1)
            add_task_linux(args.cmd, args.interval, args.name)
        elif args.action == "list":
            list_tasks_linux()
        elif args.action == "remove":
            remove_task_linux(args.name)

    elif sistema in ("win32", "cygwin"):
        if args.action == "add":
            if args.interval <= 0:  # Validación adicional
                print("[ERROR] El intervalo debe ser un número positivo.")
                sys.exit(1)
            add_task_windows(args.cmd, args.interval, args.name)
        elif args.action == "list":
            list_tasks_windows()
        elif args.action == "remove":
            remove_task_windows(args.name)

    else:
        print("ERROR: Sistema operativo no compatible. Este script solo soporta Linux y Windows.")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")

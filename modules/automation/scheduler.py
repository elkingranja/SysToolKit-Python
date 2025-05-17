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

Ejemplos de uso:
  python scheduler.py add --cmd "python mi_script.py" --interval 10 --name MiTarea
  python scheduler.py list
  python scheduler.py remove --name MiTarea
"""

def add_task_linux(cmd, interval, name):
    cron_line = f"*/{interval} * * * * {cmd} # {name}"
    try:
        proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = proc.stdout if proc.returncode == 0 else ""
        new_cron = existing + cron_line + "\n"
        subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
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
        if len(lines) == len(proc.stdout.splitlines()):
            print(f"[INFO] No se encontró una tarea con el nombre '{name}'.")
            return
        confirm = input(f"¿Seguro que deseas eliminar la tarea '{name}'? (s/n): ").strip().lower()
        if confirm != "s":
            print("Operación cancelada.")
            return
        new_cron = "\n".join(lines) + "\n"
        subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
        print(f"[OK] Tarea '{name}' eliminada.")
    except Exception as e:
        print(f"[ERROR] remove_task_linux: {e}")

def add_task_windows(cmd, interval, name):
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
        confirm = input(f"¿Seguro que deseas eliminar la tarea '{name}'? (s/n): ").strip().lower()
        if confirm != "s":
            print("Operación cancelada.")
            return
        resultado = subprocess.run(
            ["schtasks", "/Delete", "/TN", name, "/F"],
            capture_output=True, text=True
        )
        if resultado.returncode != 0:
            if "ERROR:" in resultado.stderr and "No se encuentra" in resultado.stderr:
                print(f"[INFO] No se encontró una tarea con el nombre '{name}'.")
            else:
                print(f"[ERROR] remove_task_windows: {resultado.stderr.strip()}")
        else:
            print(f"[OK] Tarea '{name}' eliminada.")
    except Exception as e:
        print(f"[ERROR] remove_task_windows: {e}")

def main():
    parser = argparse.ArgumentParser(
        prog="scheduler",
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # Desactiva la ayuda automática en inglés
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Muestra este mensaje de ayuda y sale."
    )
    sub = parser.add_subparsers(dest="action", metavar="acción")

    # Agregar
    p = sub.add_parser("add", help="Agregar tarea programada")
    p.add_argument("--cmd", help="Comando o script a ejecutar")
    p.add_argument("--interval", type=int, help="Intervalo en minutos")
    p.add_argument("--name", help="Nombre identificador de la tarea (elige el que desees)")

    # Listar
    sub.add_parser("list", help="Listar tareas programadas")

    # Eliminar
    p = sub.add_parser("remove", help="Eliminar tarea por nombre")
    p.add_argument("--name", help="Nombre identificador de la tarea a eliminar")

    # Mostrar ayuda si no hay argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        while True:
            respuesta = input("\n¿Deseas usar el menú interactivo? (s/n/help): ").strip().lower()
            if respuesta in ("s", "si"):
                break
            elif respuesta in ("n", "no", "salir", "exit"):
                print("Saliendo del programa.")
                sys.exit(0)
            elif respuesta in ("help", "ayuda", "-h"):
                parser.print_help()
            else:
                print("Por favor, responde con 's', 'n', 'help' o 'salir'.")

    args = parser.parse_args()

    # Si no hay acción, mostrar menú interactivo
    while not getattr(args, "action", None):
        print("\n¿Qué deseas hacer?")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Eliminar tarea")
        print("4. Salir")
        opcion = input("Selecciona opción: ").strip()
        if opcion == "1":
            args.action = "add"
        elif opcion == "2":
            args.action = "list"
        elif opcion == "3":
            args.action = "remove"
        elif opcion == "4":
            print("¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción no válida.")

    # Si faltan argumentos, pedirlos por input
    if args.action == "add":
        # Usar hasattr para evitar AttributeError si no existen
        while not getattr(args, "cmd", None):
            args.cmd = input("Comando o script a ejecutar: ").strip()
        while not getattr(args, "interval", None):
            try:
                args.interval = int(input("Intervalo en minutos: ").strip())
                if args.interval <= 0:
                    print("[ERROR] El intervalo debe ser un número positivo.")
                    args.interval = None
            except ValueError:
                print("[ERROR] Ingresa un número válido.")
        while not getattr(args, "name", None):
            args.name = input("Nombre identificador de la tarea: ").strip()
    elif args.action == "remove" and not getattr(args, "name", None):
        args.name = input("Nombre identificador de la tarea a eliminar: ").strip()

    sistema = sys.platform

    if sistema.startswith("linux"):
        if args.action == "add":
            add_task_linux(args.cmd, args.interval, args.name)
        elif args.action == "list":
            list_tasks_linux()
        elif args.action == "remove":
            remove_task_linux(args.name)

    elif sistema in ("win32", "cygwin"):
        if args.action == "add":
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

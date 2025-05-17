#!/usr/bin/env python3
import psutil
import time
import os
from datetime import datetime
import platform
from colorama import init
init(autoreset=True)

LOG_DIR = os.path.expanduser("~/SysToolKit_logs")
LOG_FILE = os.path.join(LOG_DIR, "custom_alert.log")
os.makedirs(LOG_DIR, exist_ok=True)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def input_int(prompt, min_val, max_val):
    while True:
        val = input(prompt)
        if val.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del programa.")
            exit(0)
        try:
            val = int(val)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Por favor, ingresa un valor entre {min_val} y {max_val}.")
        except ValueError:
            print("Entrada inválida. Intenta de nuevo.")

def choose_metrics():
    choices = {}
    print("=== SELECCIÓN DE MÉTRICAS A MONITORIZAR ===")
    print("Escribe 'q' en cualquier momento para salir.\n")
    if input("¿Monitorear CPU? (s/n): ").lower() == 's':
        threshold = input_int("  Umbral CPU (%): ", 1, 100)
        choices['cpu'] = threshold
    if input("¿Monitorear RAM? (s/n): ").lower() == 's':
        threshold = input_int("  Umbral RAM (%): ", 1, 100)
        choices['ram'] = threshold
    if input("¿Monitorear disco? (s/n): ").lower() == 's':
        threshold = input_int("  Umbral Disco (%): ", 1, 100)
        disks = get_disks()
        if disks:
            print("Discos disponibles:")
            for idx, d in enumerate(disks):
                print(f"  {idx+1}. {d}")
            while True:
                selected = input(f"Selecciona el/los disco(s) (1-{len(disks)}, separados por coma): ")
                if selected.lower() in ['q', 'salir', 'exit']:
                    print("Saliendo del programa.")
                    exit(0)
                indices = [int(i)-1 for i in selected.split(",") if i.strip().isdigit() and 0 < int(i) <= len(disks)]
                if indices:
                    choices['disk'] = {'threshold': threshold, 'disks': [disks[i] for i in indices]}
                    break
                else:
                    print("Selección inválida. Intenta de nuevo.")
        else:
            print("No se encontraron discos para monitorear.")

    if not choices:
        print("No se seleccionó ninguna métrica. Saliendo.")
        exit(0)
    return choices

def get_disks():
    partitions = psutil.disk_partitions(all=False)
    disks = []
    for part in partitions:
        if 'cdrom' in part.opts or part.fstype == '':
            continue
        disks.append(part.mountpoint)
    return disks

def resumen_config(choices):
    print("\n=== RESUMEN DE CONFIGURACIÓN ===")
    if 'cpu' in choices:
        print(f"CPU: Umbral {choices['cpu']}%")
    if 'ram' in choices:
        print(f"RAM: Umbral {choices['ram']}%")
    if 'disk' in choices:
        print(f"Disco(s): {', '.join(choices['disk']['disks'])} Umbral {choices['disk']['threshold']}%")
    print("===============================\n")

def monitor(choices, interval):
    disks = choices['disk']['disks'] if 'disk' in choices else []
    print(f"\nMonitoreando cada {interval}s. Presiona Ctrl+C para detener.\n")
    try:
        while True:
            start_time = time.time()
            now = datetime.now().strftime("%H:%M:%S")
            if 'cpu' in choices:
                cpu = psutil.cpu_percent(interval=0)
                msg = f"CPU: {cpu}% (umbral {choices['cpu']}%)"
                if cpu > choices['cpu']:
                    print(f"{RED}{now} {msg}{RESET}")
                    log_event(f"ALERTA CPU - {msg}")
                else:
                    print(f"{GREEN}{now} {msg}{RESET}")

            if 'ram' in choices:
                ram = psutil.virtual_memory().percent
                msg = f"RAM: {ram}% (umbral {choices['ram']}%)"
                if ram > choices['ram']:
                    print(f"{RED}{now} {msg}{RESET}")
                    log_event(f"ALERTA RAM - {msg}")
                else:
                    print(f"{GREEN}{now} {msg}{RESET}")

            if 'disk' in choices:
                for d in disks:
                    try:
                        usage = psutil.disk_usage(d).percent
                        msg = f"DISCO[{d}]: {usage}% (umbral {choices['disk']['threshold']}%)"
                        if usage > choices['disk']['threshold']:
                            print(f"{YELLOW}{now} {msg}{RESET}")
                            log_event(f"ALERTA DISCO[{d}] - {msg}")
                        else:
                            print(f"{GREEN}{now} {msg}{RESET}")
                    except FileNotFoundError:
                        print(f"{RED}No se pudo acceder al disco {d}.{RESET}")
                        log_event(f"ERROR - No se pudo acceder al disco {d}.")

            elapsed_time = time.time() - start_time
            time.sleep(max(0, interval - elapsed_time))
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")
    except psutil.Error as e:
        log_event(f"ERROR PSUTIL - {str(e)}")
        print(f"{RED}Error de psutil: {str(e)}{RESET}")
    except Exception as e:
        log_event(f"ERROR - {str(e)}")
        print(f"{RED}Error inesperado: {str(e)}{RESET}")

def mostrar_ayuda():
    print("""
=== AYUDA RÁPIDA ===
Este script permite monitorear CPU, RAM y discos.
- Puedes salir en cualquier momento escribiendo 'q'.
- Los logs se guardan en: {}
- Usa colores para alertas y estados normales.
- Si tienes dudas, revisa el archivo de log para más detalles.
====================
""".format(LOG_FILE))

def main():
    print("=== ALERTAS PERSONALIZADAS MEJORADAS ===\n")
    if any(arg in ['-h', '--help', 'help'] for arg in os.sys.argv):
        mostrar_ayuda()
        return
    choices = choose_metrics()
    resumen_config(choices)
    try:
        interval = input("\nIntervalo de verificación (1-3600s, Enter=10): ")
        if interval.strip() == "":
            interval = 10
        else:
            interval = int(interval)
            if not (1 <= interval <= 3600):
                raise ValueError
    except ValueError:
        print("Intervalo inválido. Usando 10s por defecto.")
        interval = 10

    print("El script se está ejecutando correctamente.")
    monitor(choices, interval)

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una herramienta para monitorear métricas del sistema y enviar alertas personalizadas. 
# Utiliza las bibliotecas psutil y datetime para obtener información sobre el sistema.
# La función log_event() registra eventos en un archivo de log.
# La función choose_metrics() permite al usuario seleccionar qué métricas desea monitorear y establecer umbrales.
# La función get_disks() obtiene las unidades de disco disponibles en el sistema.
# La función monitor() supervisa las métricas seleccionadas y envía alertas si los umbrales se superan.
# La función main() orquesta la ejecución del script, solicitando al usuario la selección de métricas y el intervalo de verificación.
# El módulo incluye una verificación para ejecutar la función si se ejecuta como un script independiente.

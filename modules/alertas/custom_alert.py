#!/usr/bin/env python3
import psutil
import time
import os
from datetime import datetime
import platform
from colorama import init  # Para compatibilidad de colores ANSI en Windows
init(autoreset=True)

LOG_DIR = os.path.expanduser("~/SysToolKit_logs")
LOG_FILE = os.path.join(LOG_DIR, "custom_alert.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Colores ANSI (funciona en la mayoría de terminales)
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def choose_metrics():
    choices = {}
    print("=== SELECCIÓN DE MÉTRICAS A MONITORIZAR ===\n")
    try:
        if input("¿Monitorear CPU? (s/n): ").lower() == 's':
            threshold = int(input("  Umbral CPU (%): "))
            if not 0 < threshold <= 100:
                raise ValueError("El umbral debe estar entre 1 y 100.")
            choices['cpu'] = threshold
        if input("\n¿Monitorear RAM? (s/n): ").lower() == 's':
            threshold = int(input("  Umbral RAM (%): "))
            if not 0 < threshold <= 100:
                raise ValueError("El umbral debe estar entre 1 y 100.")
            choices['ram'] = threshold
        if input("\n¿Monitorear disco? (s/n): ").lower() == 's':
            threshold = int(input("  Umbral Disco (%): "))
            if not 0 < threshold <= 100:
                raise ValueError("El umbral debe estar entre 1 y 100.")
            choices['disk'] = threshold
    except ValueError as e:
        print(f"Entrada inválida: {e}")
        exit(1)

    if not choices:
        print("No se seleccionó ninguna métrica. Saliendo.")
        exit(0)
    return choices

def get_disks():
    system = platform.system().lower()
    partitions = psutil.disk_partitions(all=False)
    disks = []
    for part in partitions:
        # filtrar CD-ROMs y unidades ocultas
        if 'cdrom' in part.opts or part.fstype == '':
            continue
        disks.append(part.mountpoint)
    return disks

def monitor(choices, interval):
    disks = get_disks() if 'disk' in choices else []
    if 'disk' in choices and not disks:
        print("No se encontraron discos disponibles para monitorear.")
        choices.pop('disk')

    print(f"\nMonitoreando cada {interval}s. Presiona Ctrl+C para detener.\n")
    try:
        while True:
            start_time = time.time()
            now = datetime.now().strftime("%H:%M:%S")
            if 'cpu' in choices:
                cpu = psutil.cpu_percent(interval=0)  # Evitar retraso adicional
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
                        msg = f"DISCO[{d}]: {usage}% (umbral {choices['disk']}%)"
                        if usage > choices['disk']:
                            print(f"{YELLOW}{now} {msg}{RESET}")
                            log_event(f"ALERTA DISCO[{d}] - {msg}")
                        else:
                            print(f"{GREEN}{now} {msg}{RESET}")
                    except FileNotFoundError:
                        print(f"{RED}No se pudo acceder al disco {d}.{RESET}")
                        log_event(f"ERROR - No se pudo acceder al disco {d}.")

            elapsed_time = time.time() - start_time
            time.sleep(max(0, interval - elapsed_time))  # Ajustar el intervalo
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")
    except psutil.Error as e:
        log_event(f"ERROR PSUTIL - {str(e)}")
        print(f"{RED}Error de psutil: {str(e)}{RESET}")
    except Exception as e:
        log_event(f"ERROR - {str(e)}")
        print(f"{RED}Error inesperado: {str(e)}{RESET}")

def main():
    print("=== ALERTAS PERSONALIZADAS MEJORADAS ===\n")
    choices = choose_metrics()
    try:
        interval = int(input("\nIntervalo de verificación (1-3600s): "))
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

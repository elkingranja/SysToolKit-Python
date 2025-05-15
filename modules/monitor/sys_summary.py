# -*- coding: utf-8 -*-
import platform
import psutil
import socket
import shutil
import datetime
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def obtener_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "No disponible"

def obtener_uptime():
    segundos = psutil.boot_time()
    ahora = datetime.datetime.now()
    encendido = datetime.datetime.fromtimestamp(segundos)
    return str(ahora - encendido).split('.')[0]  # sin microsegundos

def sys_summary():
    print("=== RESUMEN COMPLETO DEL SISTEMA ===\n")
    print(f"Sistema: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Uptime: {obtener_uptime()}")
    print(f"Usuario actual: {os.getlogin()}")
    print(f"Dirección IP: {obtener_ip()}")

    print("\nCPU:")
    print(f" - Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f" - Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    print(f" - Uso actual: {psutil.cpu_percent(interval=1)}%")

    print("\nRAM:")
    ram = psutil.virtual_memory()
    print(f" - Total: {ram.total // (1024**2)} MB")
    print(f" - En uso: {ram.percent}%")

    print("\nDisco:")
    disco = shutil.disk_usage("/")
    print(f" - Total: {disco.total // (1024**3)} GB")
    print(f" - En uso: {disco.used // (1024**3)} GB ({(disco.used/disco.total)*100:.1f}%)")

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    sys_summary()  # Llamada a la función principal
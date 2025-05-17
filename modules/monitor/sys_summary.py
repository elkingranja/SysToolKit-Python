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

def obtener_ips():
    ips = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ips.append(f"{iface}: {addr.address}")
    return ips if ips else ["No disponible"]

def sys_summary():
    resumen = []
    resumen.append("=== RESUMEN COMPLETO DEL SISTEMA ===\n")
    resumen.append(f"Sistema: {platform.system()} {platform.release()} ({platform.machine()})")
    resumen.append(f"Uptime: {obtener_uptime()}")
    try:
        usuario = os.getlogin()
    except Exception:
        usuario = "No disponible"
    resumen.append(f"Usuario actual: {usuario}")
    resumen.append(f"Dirección IP principal: {obtener_ip()}")

    resumen.append("\n--- CPU ---")
    resumen.append(f" - Núcleos físicos: {psutil.cpu_count(logical=False)}")
    resumen.append(f" - Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    resumen.append(f" - Uso actual: {psutil.cpu_percent(interval=1)}%")

    resumen.append("\n--- RAM ---")
    ram = psutil.virtual_memory()
    resumen.append(f" - Total: {ram.total // (1024**2)} MB")
    resumen.append(f" - En uso: {ram.percent}%")

    resumen.append("\n--- Direcciones IP ---")
    for ip in obtener_ips():
        resumen.append(f" - {ip}")

    resumen.append(f"\nProcesos activos: {len(psutil.pids())}")

    resumen.append("\n--- Disco ---")
    if os.name == "nt":
        disco = shutil.disk_usage(os.environ["SystemDrive"] + "\\")
    else:
        disco = shutil.disk_usage("/")
    resumen.append(f" - Total: {disco.total // (1024**3)} GB")
    resumen.append(f" - En uso: {disco.used // (1024**3)} GB ({(disco.used/disco.total)*100:.1f}%)")

    print("\n".join(resumen))

    opcion = input("\n¿Desea guardar este resumen en un archivo? (s/n): ").strip().lower()
    if opcion == "s":
        with open("resumen_sistema.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(resumen))
        print("Resumen guardado en resumen_sistema.txt")

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    sys_summary()  # Llamada a la función principal
# -*- coding: utf-8 -*-
import sys
import time
import platform
import psutil
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ''
        RED = ''
        YELLOW = ''
        CYAN = ''
    class Style:
        RESET_ALL = ''

def obtener_unidades():
    sistema = platform.system()
    unidades = {}
    try:
        for p in psutil.disk_partitions():
            if sistema == "Windows":
                if 'removable' in p.opts:
                    unidades[p.device] = p.mountpoint
            else:
                if "/media" in p.mountpoint or "/run/media" in p.mountpoint:
                    unidades[p.device] = p.mountpoint
    except Exception as e:
        print(f"{Fore.YELLOW}Advertencia: Error al obtener las unidades: {e}{Style.RESET_ALL}")
    return unidades

def mostrar_ayuda():
    print(f"""{Fore.CYAN}
=== AYUDA USB ALERT ===
- Este módulo monitorea la conexión y desconexión de dispositivos USB.
- Puedes definir el intervalo de verificación.
- Presiona Ctrl+C para salir en cualquier momento.
- Se notificará tanto la conexión como la desconexión de unidades.
========================={Style.RESET_ALL}
""")

def usb_alert_config():
    print(f"{Fore.CYAN}=== ALERTA POR CONEXIÓN/DESCONEXIÓN DE USB ==={Style.RESET_ALL}\n")
    if any(arg in ['-h', '--help', 'help'] for arg in sys.argv):
        mostrar_ayuda()
        return
    try:
        intervalo = int(input("Intervalo de verificación en segundos (default 5): ").strip() or 5)
        if intervalo <= 0:
            print(f"{Fore.YELLOW}Advertencia: El intervalo debe ser un número positivo. Usando 5 segundos.{Style.RESET_ALL}")
            intervalo = 5
    except ValueError:
        print(f"{Fore.YELLOW}Advertencia: Entrada no válida. Usando 5 segundos.{Style.RESET_ALL}")
        intervalo = 5

    anteriores = obtener_unidades()
    print(f"{Fore.GREEN}Unidades conectadas al iniciar:{Style.RESET_ALL}")
    if anteriores:
        for dev, punto in anteriores.items():
            print(f" - {dev} en {punto}")
    else:
        print(" (Ninguna unidad USB detectada)")
    print(f"\n{Fore.YELLOW}Monitoreando... (Ctrl+C para salir){Style.RESET_ALL}\n")
    try:
        while True:
            actuales = obtener_unidades()
            nuevas = {dev: mp for dev, mp in actuales.items() if dev not in anteriores}
            removidas = {dev: mp for dev, mp in anteriores.items() if dev not in actuales}
            for dev, punto in nuevas.items():
                ruta_limpia = punto.strip("/\\")
                etiqueta = os.path.basename(ruta_limpia) or "Desconocida"
                print(f"{Fore.GREEN}Alerta: Unidad {dev} ({etiqueta}) conectada en {punto}{Style.RESET_ALL}")
            for dev, punto in removidas.items():
                ruta_limpia = punto.strip("/\\")
                etiqueta = os.path.basename(ruta_limpia) or "Desconocida"
                print(f"{Fore.RED}Alerta: Unidad {dev} ({etiqueta}) desconectada de {punto}{Style.RESET_ALL}")
            anteriores = actuales
            time.sleep(max(intervalo, 1))
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}Monitoreo detenido por el usuario.{Style.RESET_ALL}")

if __name__ == "__main__":
    usb_alert_config()
    input("\nPresiona Enter para volver al menú...")

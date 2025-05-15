# -*- coding: utf-8 -*-
import sys
import io
import time
import platform
import psutil
import os

# Configurar salida estándar para UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
        print(f"Advertencia: Error al obtener las unidades: {e}")
    return unidades

def usb_alert_config():
    print("=== ALERTA POR CONEXIÓN DE USB ===\n")
    try:
        intervalo = int(input("Intervalo de verificación en segundos (default 5): ").strip() or 5)
        if intervalo <= 0:
            print("Advertencia: El intervalo debe ser un número positivo. Usando el valor por defecto de 5 segundos.")
            intervalo = 5
    except ValueError:
        print("Advertencia: Entrada no válida. Usando el valor por defecto de 5 segundos.")
        intervalo = 5

    anteriores = obtener_unidades()
    print("Monitoreando... (Ctrl+C para salir)\n")
    try:
        while True:
            actuales = obtener_unidades()
            nuevas = {dev: mp for dev, mp in actuales.items() if dev not in anteriores}
            if nuevas:
                for dev, punto in nuevas.items():
                    ruta_limpia = punto.strip("/\\")
                    etiqueta = os.path.basename(ruta_limpia) or "Desconocida"
                    print(f"Alerta: Unidad {dev} ({etiqueta}) conectada en {punto}")
            anteriores = actuales
            time.sleep(max(intervalo, 1))  # Asegura un intervalo mínimo de 1 segundo
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")

if __name__ == "__main__":
    usb_alert_config()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para monitorear la conexión de dispositivos USB en el sistema.
    # Utiliza la biblioteca psutil para obtener información sobre las unidades conectadas.
    # La función usb_alert_config() permite al usuario definir un intervalo de verificación y muestra alertas cuando se conecta un nuevo dispositivo USB.

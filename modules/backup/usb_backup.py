import os
import time
import psutil
import shutil
from datetime import datetime

def obtener_unidades_usb():
    unidades = []
    for part in psutil.disk_partitions():
        if "removable" in part.opts.lower() or "media" in part.mountpoint.lower():
            unidades.append(part.mountpoint)
    return unidades

def generar_nombre_unico(base_path, nombre_base):
    contador = 1
    nombre = nombre_base
    while os.path.exists(f"{os.path.join(base_path, nombre)}.zip"):
        nombre = f"{nombre_base}_{contador}"
        contador += 1
    return nombre

def usb_backup():
    print("=== COPIA AL DETECTAR USB ===\n")
    origen = input("Carpeta a respaldar automáticamente: ").strip()
    if not os.path.isdir(origen):
        print("Carpeta de origen inválida.")
        return

    print("Esperando conexión de USB... (Ctrl + C para detener)")
    detectadas = set(obtener_unidades_usb())

    try:
        while True:
            actuales = set(obtener_unidades_usb())
            nuevas = actuales - detectadas
            if nuevas:
                for unidad in nuevas:
                    print(f"Unidad USB detectada: {unidad}")
                    nombre_base = f"usb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    nombre_unico = generar_nombre_unico(unidad, nombre_base)
                    ruta_zip = os.path.join(unidad, nombre_unico)

                    try:
                        shutil.make_archive(ruta_zip, 'zip', origen)
                        print(f"Copia enviada a: {ruta_zip}.zip")
                    except Exception as e:
                        print(f"Error al crear la copia de seguridad: {e}")
                break
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    usb_backup()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para realizar copias de seguridad automáticas al detectar la conexión de un dispositivo USB.
    # Utiliza la biblioteca psutil para obtener información sobre las unidades conectadas y shutil para crear archivos zip.
    # La función usb_backup() permite al usuario especificar una carpeta de origen y realiza la copia de seguridad automáticamente al detectar un dispositivo USB.
    # Se asegura de que el nombre del archivo zip sea único en la unidad USB.

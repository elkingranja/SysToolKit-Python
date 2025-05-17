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

def mostrar_contenido_usb(unidad):
    print("\nContenido del USB:")
    for archivo in os.listdir(unidad):
        print("  -", archivo)

def usb_backup():
    while True:
        print("=== COPIA AL DETECTAR USB ===\n")
        while True:
            origen = input("Carpeta a respaldar automáticamente (ej: C:\\MisDocumentos, o 'salir' para cancelar): ").strip()
            if origen.lower() == "salir":
                print("Operación cancelada.")
                return
            if os.path.isdir(origen):
                break
            print("Carpeta de origen inválida. Intenta de nuevo.")

        print("Esperando conexión de USB... (Ctrl + C para detener)")
        detectadas = set(obtener_unidades_usb())

        try:
            while True:
                actuales = set(obtener_unidades_usb())
                nuevas = actuales - detectadas
                if nuevas:
                    unidades = list(nuevas)
                    if len(unidades) > 1:
                        print("Se detectaron varias unidades USB:")
                        for idx, unidad in enumerate(unidades, 1):
                            print(f"{idx}. {unidad}")
                        while True:
                            seleccion = input("Selecciona el número de la unidad USB destino (o escribe 'c' para cancelar): ").strip()
                            if seleccion.lower() == 'c':
                                print("Operación cancelada por el usuario.")
                                return
                            if seleccion.isdigit() and 1 <= int(seleccion) <= len(unidades):
                                unidad = unidades[int(seleccion) - 1]
                                break
                            print("Selección inválida. Intenta de nuevo o escribe 'c' para cancelar.")
                    else:
                        unidad = unidades[0]
                    print(f"Unidad USB detectada: {unidad}")
                    nombre_base = f"usb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    nombre_unico = generar_nombre_unico(unidad, nombre_base)
                    ruta_zip = os.path.join(unidad, nombre_unico)

                    try:
                        shutil.make_archive(ruta_zip, 'zip', origen)
                        print(f"\n¡Copia enviada a: {ruta_zip}.zip!")
                        mostrar_contenido_usb(unidad)
                    except Exception as e:
                        print(f"Error al crear la copia de seguridad: {e}")
                    break
                time.sleep(3)
        except KeyboardInterrupt:
            print("\nDetenido por el usuario.")
        except Exception as e:
            print(f"Error inesperado: {e}")

        repetir = input("\n¿Deseas hacer otra copia? (s/n): ").strip().lower()
        if repetir != 's':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    usb_backup()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para realizar copias de seguridad automáticas al detectar la conexión de un dispositivo USB.
    # Utiliza la biblioteca psutil para obtener información sobre las unidades conectadas y shutil para crear archivos zip.
    # La función usb_backup() permite al usuario especificar una carpeta de origen y realiza la copia de seguridad automáticamente al detectar un dispositivo USB.
    # Se asegura de que el nombre del archivo zip sea único en la unidad USB.

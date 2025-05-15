import os
import shutil
import platform
from datetime import datetime
import sys

# Configurar la consola para usar UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

def crear_backup(origen, destino):
    try:
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = f"autobackup_{marca}"
        ruta_zip = os.path.join(destino, nombre)
        shutil.make_archive(ruta_zip, 'zip', origen)
        print(f"Copia creada: {ruta_zip}.zip")
    except Exception as e:
        print(f"Error al crear la copia de seguridad: {e}")

def programar_tarea(origen, destino, intervalo):
    sistema = platform.system()
    script_path = os.path.abspath(__file__)
    
    try:
        if sistema == "Linux":
            crontab_line = f"*/{intervalo} * * * * python3 '{script_path}'\n"
            os.system(f"(crontab -l 2>/dev/null; echo \"{crontab_line}\") | crontab -")
            print("Tarea programada en crontab.")
        elif sistema == "Windows":
            bat_path = os.path.expanduser("~/Desktop/auto_backup.bat")
            with open(bat_path, "w") as f:
                f.write(f"@echo off\npython \"{script_path}\"\n")
            print(f"Archivo BAT creado en el escritorio: {bat_path}")
            print("Ábrelo con el Programador de tareas para configurarlo manualmente.")
        else:
            print("Sistema operativo no compatible para automatización.")
    except Exception as e:
        print(f"Error al programar la tarea: {e}")

def validar_ruta(ruta, tipo="origen"):
    if not os.path.isdir(ruta):
        print(f"La carpeta de {tipo} no es válida o no existe: {ruta}")
        return False
    return True

def solicitar_intervalo():
    try:
        intervalo = int(input("Intervalo en minutos entre cada copia: ").strip())
        if intervalo <= 0:
            print("El intervalo debe ser un número positivo.")
            return None
        return intervalo
    except ValueError:
        print("Intervalo inválido. Debes ingresar un número.")
        return None

def auto_backup():
    print("=== COPIA DE SEGURIDAD AUTOMÁTICA ===\n")
    origen = input("Carpeta a respaldar: ").strip()
    if not validar_ruta(origen, "origen"):
        return

    destino = input("Carpeta destino de copias: ").strip()
    if not validar_ruta(destino, "destino"):
        return

    intervalo = solicitar_intervalo()
    if intervalo is None:
        return

    print("\n¿Deseas programar esta tarea automáticamente?")
    opcion = input("1 = Sí, 2 = No (solo ejecutar una vez): ").strip()

    if opcion == "1":
        programar_tarea(origen, destino, intervalo)
    elif opcion == "2":
        crear_backup(origen, destino)
    else:
        print("Opción no válida.")

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una herramienta para crear copias de seguridad automáticas de carpetas.
# Utiliza las bibliotecas os, shutil y platform para manejar archivos y directorios.
# La función auto_backup() solicita al usuario la ruta de la carpeta a respaldar y la carpeta de destino.
# Verifica si las rutas son válidas y solicita el intervalo en minutos entre cada copia.
# Ofrece la opción de programar la tarea automáticamente en Linux o crear un archivo BAT en Windows.
# Si la carpeta de origen no es válida, muestra un mensaje de error.
# Si la carpeta de destino no es válida, también muestra un mensaje de error.
# Si el intervalo no es válido, muestra un mensaje de error.
# Si la tarea se programa con éxito, muestra un mensaje confirmando la programación.
# Si ocurre un error durante la creación de la copia o la programación de la tarea, muestra un mensaje de error.


import os
import shutil
import platform
from datetime import datetime
import sys
import time

# Configurar la consola para usar UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def crear_backup(origen, destino):
    try:
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = f"autobackup_{marca}"
        ruta_zip = os.path.join(destino, nombre)
        zip_final = f"{ruta_zip}.zip"
        if os.path.exists(zip_final):
            sobrescribir = input(f"Ya existe {zip_final}. ¿Deseas sobrescribirlo? (s/n): ").strip().lower()
            if sobrescribir != 's':
                print("Operación cancelada.")
                return False, None, 0
        inicio = time.time()
        shutil.make_archive(ruta_zip, 'zip', origen)
        fin = time.time()
        print(f"\n¡Copia creada con éxito en: {zip_final}!")
        # Registrar en log
        with open("backup_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: Backup de {origen} a {zip_final}\n")
        return True, zip_final, fin - inicio
    except Exception as e:
        print(f"Error al crear la copia de seguridad: {e}")
        return False, None, 0

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
    # Validar permisos de escritura para destino
    if tipo == "destino":
        try:
            testfile = os.path.join(ruta, "test_perm.txt")
            with open(testfile, "w") as f:
                f.write("test")
            os.remove(testfile)
        except Exception:
            print(f"No tienes permisos de escritura en la carpeta destino: {ruta}")
            return False
    return True

def solicitar_intervalo():
    while True:
        try:
            intervalo = int(input("Intervalo en minutos entre cada copia: ").strip())
            if intervalo <= 0:
                print("El intervalo debe ser un número positivo.")
                continue
            return intervalo
        except ValueError:
            print("Intervalo inválido. Debes ingresar un número.")

def mostrar_contenido_carpeta(carpeta):
    print("\nContenido de la carpeta destino:")
    for archivo in os.listdir(carpeta):
        print("  -", archivo)

def mostrar_log():
    print("\n=== LOG DE COPIAS REALIZADAS ===")
    if os.path.exists("backup_log.txt"):
        with open("backup_log.txt", encoding="utf-8") as f:
            print(f.read())
    else:
        print("No hay registros aún.")

def auto_backup():
    while True:
        print("\n=== COPIA DE SEGURIDAD AUTOMÁTICA ===\n")
        print("Escribe 'salir' en cualquier momento para cancelar.")
        origen = input("Carpeta a respaldar (ej: C:\\MisDocumentos): ").strip()
        if origen.lower() == "salir":
            print("Operación cancelada.")
            break
        if not validar_ruta(origen, "origen"):
            continue

        destino = input("Carpeta destino de copias (ej: D:\\Backups): ").strip()
        if destino.lower() == "salir":
            print("Operación cancelada.")
            break
        if not validar_ruta(destino, "destino"):
            continue

        intervalo = solicitar_intervalo()
        if intervalo is None:
            continue

        print("\n¿Deseas programar esta tarea automáticamente?")
        print("1 = Sí, 2 = No (solo ejecutar una vez), 3 = Ver log, 'salir' para cancelar")
        opcion = input("Opción: ").strip()
        if opcion.lower() == "salir":
            print("Operación cancelada.")
            break

        if opcion == "1":
            programar_tarea(origen, destino, intervalo)
        elif opcion == "2":
            exito, zip_path, duracion = crear_backup(origen, destino)
            if exito:
                print(f"Tiempo transcurrido: {duracion:.2f} segundos")
                ver = input("¿Deseas ver el contenido de la carpeta destino? (s/n): ").strip().lower()
                if ver == 's':
                    mostrar_contenido_carpeta(destino)
            else:
                print("No se pudo crear la copia.")
        elif opcion == "3":
            mostrar_log()
        else:
            print("Opción no válida.")

        repetir = input("\n¿Deseas realizar otra operación? (s/n): ").strip().lower()
        if repetir != 's':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    auto_backup()


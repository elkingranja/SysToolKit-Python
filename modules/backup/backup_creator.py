import os
import shutil
import time
import re

def es_nombre_valido(nombre):
    """Verifica si el nombre del archivo es válido."""
    return bool(re.match(r'^[\w\-.]+$', nombre))

def tiene_permisos_escritura(carpeta):
    """Verifica si se tienen permisos de escritura en la carpeta."""
    try:
        prueba = os.path.join(carpeta, ".prueba_permiso")
        with open(prueba, "w") as f:
            f.write("test")
        os.remove(prueba)
        return True
    except OSError:
        return False

def crear_copia(origen, destino, nombre):
    """Crea una copia de seguridad en formato ZIP."""
    zip_path = os.path.join(destino, nombre)
    if os.path.exists(f"{zip_path}.zip"):
        print(f"Advertencia: Ya existe un archivo llamado {nombre}.zip en la carpeta de destino.")
        sobrescribir = input("¿Deseas sobrescribirlo? (s/n): ").strip().lower()
        if sobrescribir != 's':
            print("Operación cancelada.")
            return
    try:
        shutil.make_archive(zip_path, 'zip', origen)
        print(f"Copia creada en: {zip_path}.zip")
    except (OSError, shutil.Error) as e:
        print(f"Error al crear la copia: {e}")

def backup_creator():
    print("=== CREADOR DE COPIAS DE SEGURIDAD ===\n")
    origen = input("Ruta de la carpeta a respaldar: ").strip()
    destino = input("Carpeta donde guardar la copia: ").strip()

    if not os.path.isdir(origen):
        print("Carpeta de origen no válida o no existe.")
        return
    if not os.path.isdir(destino):
        print("Carpeta de destino no válida o no existe.")
        return
    if not tiene_permisos_escritura(destino):
        print("No tienes permisos de escritura en la carpeta de destino.")
        return

    nombre = input("Nombre para la copia (sin espacios): ").strip() or f"backup_{int(time.time())}"
    if not es_nombre_valido(nombre):
        print("El nombre contiene caracteres no válidos. Usa solo letras, números, guiones o puntos.")
        return

    crear_copia(origen, destino, nombre)
    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una herramienta para crear copias de seguridad de carpetas.
# Utiliza las bibliotecas os y shutil para manejar archivos y directorios.
# La función backup_creator() solicita al usuario la ruta de la carpeta a respaldar y la carpeta de destino.
# Verifica si las rutas son válidas y crea un archivo zip de la carpeta de origen en la carpeta de destino.
# Si la carpeta de origen no es válida, muestra un mensaje de error.
# Si la carpeta de destino no es válida, también muestra un mensaje de error.
# Si la copia se crea con éxito, muestra la ruta del archivo zip creado.
# Si ocurre un error durante la creación de la copia, muestra un mensaje de error
# El módulo incluye una verificación para ejecutar la función si se ejecuta como un script independiente.

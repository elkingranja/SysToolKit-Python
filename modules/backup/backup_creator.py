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
            return False, None, 0
    try:
        inicio = time.time()
        shutil.make_archive(zip_path, 'zip', origen)
        fin = time.time()
        print(f"\n¡Copia creada con éxito en: {zip_path}.zip!")
        return True, f"{zip_path}.zip", fin - inicio
    except (OSError, shutil.Error) as e:
        print(f"Error al crear la copia: {e}")
        return False, None, 0

def mostrar_contenido_carpeta(carpeta):
    print("\nContenido de la carpeta destino:")
    for archivo in os.listdir(carpeta):
        print("  -", archivo)

def pedir_ruta(mensaje, debe_existir=True):
    while True:
        ruta = input(mensaje).strip()
        if not ruta:
            print("La ruta no puede estar vacía.")
            continue
        if debe_existir and not os.path.isdir(ruta):
            print("La carpeta no existe. Intenta de nuevo.")
            continue
        return ruta

def pedir_nombre():
    while True:
        nombre = input("Nombre para la copia (sin espacios): ").strip()
        if not nombre:
            nombre = f"backup_{int(time.time())}"
            print(f"Usando nombre por defecto: {nombre}")
        if es_nombre_valido(nombre):
            return nombre
        print("El nombre contiene caracteres no válidos. Usa solo letras, números, guiones o puntos.")

def backup_creator():
    while True:
        print("\n=== CREADOR DE COPIAS DE SEGURIDAD ===\n")
        origen = pedir_ruta("Ruta de la carpeta a respaldar (ej: C:\\MisDocumentos): ")
        destino = pedir_ruta("Carpeta donde guardar la copia (ej: D:\\Backups): ")
        if not tiene_permisos_escritura(destino):
            print("No tienes permisos de escritura en la carpeta de destino.")
            continue
        nombre = pedir_nombre()
        print("\nCreando copia de seguridad...")
        exito, zip_path, duracion = crear_copia(origen, destino, nombre)
        if exito:
            print(f"Tiempo transcurrido: {duracion:.2f} segundos")
            ver = input("¿Deseas ver el contenido de la carpeta destino? (s/n): ").strip().lower()
            if ver == 's':
                mostrar_contenido_carpeta(destino)
        repetir = input("\n¿Deseas hacer otra copia? (s/n): ").strip().lower()
        if repetir != 's':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    backup_creator()
# Este módulo proporciona una herramienta para crear copias de seguridad de carpetas.
# Utiliza las bibliotecas os y shutil para manejar archivos y directorios.
# La función backup_creator() solicita al usuario la ruta de la carpeta a respaldar y la carpeta de destino.
# Verifica si las rutas son válidas y crea un archivo zip de la carpeta de origen en la carpeta de destino.
# Si la carpeta de origen no es válida, muestra un mensaje de error.
# Si la carpeta de destino no es válida, también muestra un mensaje de error.
# Si la copia se crea con éxito, muestra la ruta del archivo zip creado.
# Si ocurre un error durante la creación de la copia, muestra un mensaje de error
# El módulo incluye una verificación para ejecutar la función si se ejecuta como un script independiente.

import os
import shutil

def restore_backup():
    print("=== RESTAURAR COPIA DE SEGURIDAD ===\n")
    archivo = input("Ruta del archivo .zip de copia: ").strip()
    destino = input("Carpeta donde restaurar: ").strip()

    if not os.path.isfile(archivo):
        print(f"Error: El archivo '{archivo}' no existe o no es válido.")
        return
    if not archivo.endswith(".zip"):
        print(f"Error: El archivo '{archivo}' no tiene la extensión .zip.")
        return
    if not os.path.isdir(destino):
        print(f"Error: La carpeta de destino '{destino}' no es válida.")
        return

    try:
        shutil.unpack_archive(archivo, destino)
        print(f"Copia restaurada correctamente en: {destino}")
    except shutil.ReadError:
        print(f"Error: El archivo '{archivo}' no es un archivo zip válido o está corrupto.")
    except Exception as e:
        print(f"Error inesperado al restaurar: {e}")

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    input("\nPresiona Enter para volver al menú...")
# # Este módulo proporciona una herramienta para restaurar copias de seguridad de archivos zip.
# # Utiliza las bibliotecas os y shutil para manejar archivos y directorios
# # La función restore_backup() solicita al usuario la ruta del archivo zip de la copia de seguridad y la carpeta de destino.
# # Verifica si el archivo es un zip válido y si la carpeta de destino es válida.
# # Si el archivo no es válido o no es un zip, muestra un mensaje de error.


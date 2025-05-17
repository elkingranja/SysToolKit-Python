import os
import shutil

def mostrar_contenido_carpeta(carpeta):
    print("\nContenido restaurado:")
    for archivo in os.listdir(carpeta):
        print("  -", archivo)

def restore_backup():
    while True:
        print("\n=== RESTAURAR COPIA DE SEGURIDAD ===")
        print("Escribe 'salir' en cualquier momento para cancelar.\n")
        archivo = input("Ruta del archivo .zip de copia (ej: D:\\Backups\\backup_20240517.zip): ").strip()
        if archivo.lower() == "salir":
            print("Operación cancelada.")
            break
        destino = input("Carpeta donde restaurar (ej: C:\\MisDocumentosRestaurados): ").strip()
        if destino.lower() == "salir":
            print("Operación cancelada.")
            break

        if not os.path.isfile(archivo):
            print(f"Error: El archivo '{archivo}' no existe o no es válido.")
            continue
        if not archivo.endswith(".zip"):
            print(f"Error: El archivo '{archivo}' no tiene la extensión .zip.")
            continue
        if not os.path.isdir(destino):
            print(f"Error: La carpeta de destino '{destino}' no es válida.")
            continue

        # Confirmar sobrescritura si la carpeta destino no está vacía
        if os.listdir(destino):
            sobre = input("La carpeta destino no está vacía. ¿Sobrescribir archivos existentes? (s/n): ").strip().lower()
            if sobre != 's':
                print("Operación cancelada.")
                continue

        try:
            shutil.unpack_archive(archivo, destino)
            print(f"\n¡Copia restaurada correctamente en: {destino}!")
            mostrar_contenido_carpeta(destino)
        except shutil.ReadError:
            print(f"Error: El archivo '{archivo}' no es un archivo zip válido o está corrupto.")
        except Exception as e:
            print(f"Error inesperado al restaurar: {e}")

        repetir = input("\n¿Deseas restaurar otra copia? (s/n): ").strip().lower()
        if repetir != 's':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    restore_backup()


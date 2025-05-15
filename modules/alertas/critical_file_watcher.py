import os
import time
import hashlib
import sys
from datetime import datetime

# Configurar salida estándar para UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

def calcular_hash(ruta):
    """Devuelve el hash SHA256 de un archivo o None si falla"""
    try:
        with open(ruta, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {ruta}")
    except PermissionError:
        print(f"[ERROR] Permiso denegado para leer el archivo: {ruta}")
    except Exception as e:
        print(f"[ERROR] Error inesperado al calcular hash de {ruta}: {e}")
    return None

def critical_file_watcher():
    print("=== VIGILANTE DE ARCHIVOS CRÍTICOS ===\n")

    entrada = input("Ingrese rutas completas de archivos separados por coma: ").strip()
    if not entrada:
        print("[ERROR] No se ingresaron rutas de archivos.")
        return

    posibles = [a.strip() for a in entrada.split(",")]
    archivos = []

    # Validar rutas
    for archivo in posibles:
        if os.path.isfile(archivo):
            if archivo not in archivos:
                archivos.append(archivo)
        else:
            print(f"[ERROR] No se encontró el archivo o no es válido: {archivo}")

    if not archivos:
        print("[ERROR] No hay archivos válidos para vigilar.")
        return

    # Inicializar hash por archivo
    estado_inicial = {a: calcular_hash(a) for a in archivos}

    # Solicitar intervalo de monitoreo
    try:
        intervalo = int(input("Ingrese intervalo de monitoreo en segundos [por defecto 5]: ").strip() or 5)
        if intervalo <= 0:
            print("[ERROR] El intervalo debe ser mayor a 0. Se usará el valor por defecto (5 segundos).")
            intervalo = 5
    except ValueError:
        print("[ERROR] Intervalo inválido. Se usará el valor por defecto (5 segundos).")
        intervalo = 5

    print("\n[INFO] Monitoreando archivos... (presione Ctrl+C para detener)\n")
    try:
        while True:
            for archivo in estado_inicial.keys():
                if not os.path.exists(archivo):
                    print(f"[ALERTA] {archivo} ha sido ELIMINADO. ({datetime.now()})")
                    estado_inicial[archivo] = None  # Mantener la entrada para detectar si reaparece
                else:
                    nuevo_hash = calcular_hash(archivo)
                    if nuevo_hash and nuevo_hash != estado_inicial[archivo]:
                        print(f"[ALERTA] {archivo} ha sido MODIFICADO. ({datetime.now()})")
                        estado_inicial[archivo] = nuevo_hash
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoreo detenido por el usuario.")
    except Exception as e:
        print(f"[ERROR] Se produjo un error inesperado: {e}")

if __name__ == "__main__":
    critical_file_watcher()
    input("\nPresiona Enter para volver al menú...")
# # Este módulo proporciona una herramienta para vigilar archivos críticos en el sistema.
# # Utiliza las bibliotecas os, time y hashlib para manejar archivos y calcular hashes.
# # La función calcular_hash() calcula el hash SHA256 de un archivo dado.
# # La función critical_file_watcher() solicita al usuario rutas de archivos y valida su existencia.
# # Si los archivos son válidos, inicia un bucle que monitorea cambios en los archivos.
# # Si un archivo es eliminado, se muestra un mensaje de alerta.
# # Si un archivo es modificado, se muestra un mensaje de alerta.
# # El módulo incluye una verificación para ejecutar la función si se ejecuta como un script independiente.
# # La función critical_file_watcher() se ejecuta en un bucle infinito hasta que se interrumpe manualmente
# # o se detecta un cambio en los archivos vigilados.
# # La función también maneja excepciones para errores comunes como archivo no encontrado o permisos denegados.
# # Se proporciona una salida estándar para errores y mensajes de información.
# # El módulo está diseñado para ser fácil de usar y ofrece una solución simple para la vigilancia de archivos críticos.





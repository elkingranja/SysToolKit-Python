import os
import sys
import platform
import subprocess
from datetime import datetime, timedelta

def configurar_utf8_windows():
    """Configura la consola Windows para usar UTF-8."""
    if sys.platform == "win32":
        subprocess.run(["chcp", "65001"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass  # Python <3.7 en Windows puede no soportar reconfigure

def ejecutar_comando(cmd):
    """Ejecuta un comando y devuelve (exit_code, stdout, stderr)."""
    result = subprocess.run(cmd, shell=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout, result.stderr

def leer_ultimas_lineas(ruta, num_lineas=30):
    """Lee las últimas líneas de un archivo."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines()[-num_lineas:])
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def ver_logs():
    sistema = platform.system()
    if sistema == "Linux":
        logs_disponibles = {
            "1": "/var/log/syslog",
            "2": "/var/log/auth.log",
            "3": "/var/log/dmesg"
        }
    elif sistema == "Windows":
        logs_disponibles = {
            "1": "C:\\Windows\\System32\\winevt\\Logs\\Application.evtx",
            "2": "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx",
            "3": "C:\\Windows\\System32\\winevt\\Logs\\System.evtx"
        }
    else:
        print("Sistema no soportado.")
        return

    print("Archivos de log disponibles:")
    for k, v in logs_disponibles.items():
        print(f"{k}. {v}")

    opcion = input("\nOpción: ").strip()
    if opcion not in logs_disponibles:
        print("Error: opción inválida.")
        return

    ruta = logs_disponibles[opcion]
    if not os.path.exists(ruta):
        print(f"Error: el archivo {ruta} no existe.")
        return

    if sistema == "Linux":
        cmd = ["tail", "-n", "30", ruta]
        code, out, err = ejecutar_comando(cmd)
        if code == 0:
            print(f"\nÚltimas 30 líneas de {ruta}:\n")
            print(out)
        else:
            print(f"Error al ejecutar '{' '.join(cmd)}': Código {code}\n{err}")
    elif sistema == "Windows":
        print(f"\nÚltimas 30 líneas de {ruta}:\n")
        print(leer_ultimas_lineas(ruta))

def limpiar_logs():
    try:
        dias = int(input("Eliminar logs con más de cuántos días: ").strip())
        if dias <= 0:
            print("Error: el número debe ser mayor que 0.")
            return
    except ValueError:
        print("Error: valor inválido.")
        return

    cmd = f"find /var/log -type f -mtime +{dias} -exec rm -f {{}} \\;"
    print(f"\nEjecutando limpieza: {cmd}\n")
    code, out, err = ejecutar_comando(cmd)
    if code == 0:
        print("Limpieza completada.")
    else:
        print(f"Error al limpiar logs:\n{err}")
        print(f"Error al ejecutar el comando '{cmd}': Código de salida {code}")
        print(f"Detalles del error:\n{err}")

def log_manager():
    configurar_utf8_windows()
    print("GESTOR DE LOGS\n")
    sistema = platform.system()

    if sistema != "Linux" and sistema != "Windows":
        print("Este módulo solo está disponible en sistemas Linux y Windows.")
        input("Presiona Enter para salir...")
        return

    print("1. Ver logs del sistema")
    print("2. Limpiar logs antiguos (solo Linux)")
    print("0. Salir")

    opcion = input("\nSeleccione una opción: ").strip()
    if opcion == "1":
        ver_logs()
    elif opcion == "2" and sistema == "Linux":
        limpiar_logs()
    elif opcion == "0":
        return
    else:
        print("Opción inválida.")

    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    input("\nPresiona Enter para volver al menú...")

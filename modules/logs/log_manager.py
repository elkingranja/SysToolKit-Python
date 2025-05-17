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

def ver_logs():
    sistema = platform.system()
    if sistema == "Linux":
        logs_disponibles = {
            "1": ("/var/log/syslog", "Eventos del sistema"),
            "2": ("/var/log/auth.log", "Eventos de autenticación"),
            "3": ("/var/log/dmesg", "Mensajes del kernel")
        }
    elif sistema == "Windows":
        logs_disponibles = {
            "1": ("C:\\Windows\\System32\\winevt\\Logs\\Application.evtx", "Eventos de aplicación"),
            "2": ("C:\\Windows\\System32\\winevt\\Logs\\Security.evtx", "Eventos de seguridad"),
            "3": ("C:\\Windows\\System32\\winevt\\Logs\\System.evtx", "Eventos del sistema")
        }
    else:
        print("Sistema no soportado.")
        input("Presiona Enter para volver al menú...")
        return

    print("\nArchivos de log disponibles:")
    for k, (ruta, desc) in logs_disponibles.items():
        print(f"{k}. {desc} ({ruta})")

    opcion = input("\nOpción: ").strip()
    if opcion not in logs_disponibles:
        print("Error: opción inválida.")
        input("Presiona Enter para volver al menú...")
        return

    ruta, desc = logs_disponibles[opcion]
    if not os.path.exists(ruta):
        print(f"Error: el archivo {ruta} no existe.")
        input("Presiona Enter para volver al menú...")
        return

    print(f"\nMostrando: {desc}\n{'-'*40}")
    if sistema == "Linux":
        cmd = f"tail -n 30 {ruta}"
        code, out, err = ejecutar_comando(cmd)
        if code == 0:
            print(f"\nÚltimas 30 líneas de {ruta}:\n")
            print(out)
        else:
            print(f"Error al ejecutar '{cmd}': Código {code}\n{err}")
    elif sistema == "Windows":
        log_name = os.path.splitext(os.path.basename(ruta))[0]
        cmd = f'wevtutil qe {log_name} /c:30 /f:text'
        code, out, err = ejecutar_comando(cmd)
        if code == 0:
            print(f"\nÚltimos 30 eventos de {desc}:\n")
            print(out)
        else:
            print(f"Error al ejecutar '{cmd}': Código {code}\n{err}")

    guardar = input("¿Desea guardar este resultado en un archivo? (s/n): ").strip().lower()
    if guardar == "s":
        nombre_archivo = f"log_exportado_{desc.replace(' ', '_').lower()}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Log guardado en {nombre_archivo}")

    input("\nPresiona Enter para volver al menú...")

def limpiar_logs():
    sistema = platform.system()
    if sistema != "Linux":
        print("La limpieza de logs solo está disponible en Linux.")
        input("Presiona Enter para volver al menú...")
        return
    try:
        dias = int(input("Eliminar logs con más de cuántos días: ").strip())
        if dias <= 0:
            print("Error: el número debe ser mayor que 0.")
            input("Presiona Enter para volver al menú...")
            return
    except ValueError:
        print("Error: valor inválido.")
        input("Presiona Enter para volver al menú...")
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

    input("\nPresiona Enter para volver al menú...")

def log_manager():
    configurar_utf8_windows()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("GESTOR DE LOGS\n")
        sistema = platform.system()

        if sistema not in ("Linux", "Windows"):
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
            print("Saliendo del gestor de logs.")
            break
        else:
            print("Opción inválida.")
            input("Presiona Enter para volver al menú...")

if __name__ == "__main__":
    log_manager()

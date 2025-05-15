import sys
import os
import platform
import subprocess
import shutil
import logging
from datetime import datetime

# Configurar UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def run_cmd(cmd, shell=False):
    """
    Ejecuta un comando y retorna (stdout, stderr, returncode).
    """
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def resumen_linux():
    print("\nDetectando sistema operativo...")
    print("Sistema operativo detectado: Linux")

    # Usuarios conectados
    if shutil.which("who"):
        out, err, code = run_cmd(["who"])
        print("\nUsuarios conectados:")
        print(out or "(ninguno)")
    else:
        print("\nEl comando 'who' no está disponible.")

    # Intentos fallidos
    log_path = "/var/log/auth.log"
    if os.path.exists(log_path):
        if shutil.which("grep"):
            out, err, code = run_cmd(f"grep 'Failed password' {log_path} | tail -n 5", shell=True)
            print("\nÚltimos intentos de acceso fallidos:")
            print(out or "(no hay registros recientes)")
        else:
            print("\nEl comando 'grep' no está disponible.")
    else:
        print(f"\nNo se encontró el archivo de registro: {log_path}")

    # Actualizaciones pendientes
    if shutil.which("apt"):
        out, err, code = run_cmd(["apt", "list", "--upgradable"])
        lines = [l for l in out.splitlines() if "Listing..." not in l]
        print("\nActualizaciones pendientes (APT):")
        print("\n".join(lines) or "(ninguna)")
    elif shutil.which("dnf"):
        out, err, code = run_cmd(["dnf", "check-update"])
        print("\nActualizaciones pendientes (DNF):")
        print(out or "(ninguna)")
    else:
        print("\nNo se encontró un gestor de paquetes compatible.")

def resumen_windows():
    print("\nDetectando sistema operativo...")
    print("Sistema operativo detectado: Windows")

    try:
        if shutil.which("query"):
            out, err, code = run_cmd("query user", shell=True)
            print("\nUsuarios conectados:")
            print(out or "(ninguno)")
        else:
            print("\nEl comando 'query user' no está disponible en este sistema.")
            print("\nPara ver intentos de acceso fallidos:")
            print("1. Presione 'Win + S' y busque 'Visor de eventos'.")
            print("2. Abra el Visor de eventos.")
            print("3. Navegue a 'Registros de Windows' > 'Seguridad'.")
            print("4. Busque eventos relacionados con intentos de inicio de sesión fallidos.")
    except Exception as e:
        print(f"\nError inesperado en resumen_windows: {e}")

def security_summary(sistema_operativo):
    print("\nRESUMEN DE SEGURIDAD")
    print(f"\nSistema operativo: {platform.system()} {platform.release()}")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if sistema_operativo == "linux":
        resumen_linux()
    elif sistema_operativo == "windows":
        resumen_windows()
    else:
        print(f"\nEl sistema operativo '{sistema_operativo}' no es compatible con este módulo.")

if __name__ == "__main__":
    sistema_operativo = platform.system().lower()
    security_summary(sistema_operativo)

    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona un resumen de la seguridad del sistema operativo, incluyendo usuarios conectados y actualizaciones pendientes.
    # Se ejecuta automáticamente al iniciar el programa principal.

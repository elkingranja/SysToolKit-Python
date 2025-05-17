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
    resumen = []
    resumen.append("\n" + "="*40)
    resumen.append("RESUMEN DE SEGURIDAD PARA WINDOWS")
    resumen.append("="*40)
    resumen.append("\n[Usuarios en el sistema]")
    resumen.append("Esta sección muestra las cuentas locales configuradas en tu equipo.\n")
    try:
        if shutil.which("query"):
            out, err, code = run_cmd("query user", shell=True)
            resumen.append("Usuarios conectados actualmente:")
            resumen.append(out or "(ninguno)")
        else:
            if shutil.which("net"):
                out, err, code = run_cmd("net user", shell=True)
                resumen.append("Cuentas de usuario locales:")
                resumen.append(out or "(ninguna)")
                # Advertencia si 'Invitado' está habilitado
                if "Invitado" in out and "Cuenta deshabilitada" not in out:
                    resumen.append("\n[!] Advertencia: La cuenta 'Invitado' está presente. Se recomienda deshabilitarla si no se usa.")
            else:
                resumen.append("No se pudo obtener la lista de usuarios.")
        resumen.append("\n[Intentos de acceso fallidos]")
        resumen.append("Para ver los intentos de acceso fallidos, sigue estos pasos:")
        resumen.append("1. Presiona 'Win + S' y busca 'Visor de eventos'.")
        resumen.append("2. Abre el Visor de eventos.")
        resumen.append("3. Navega a 'Registros de Windows' > 'Seguridad'.")
        resumen.append("4. Busca eventos relacionados con intentos de inicio de sesión fallidos.")
    except Exception as e:
        resumen.append(f"\nError inesperado en resumen_windows: {e}")
    resumen.append("\n" + "="*40)
    resumen.append("Fin del resumen de seguridad.")
    resumen.append("="*40)
    return "\n".join(resumen)

def security_summary(sistema_operativo):
    print("\nRESUMEN DE SEGURIDAD")
    print(f"\nSistema operativo: {platform.system()} {platform.release()}")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    resumen = ""
    if sistema_operativo == "linux":
        resumen_linux()
    elif sistema_operativo == "windows":
        resumen = resumen_windows()
        print(resumen)
    else:
        print(f"\nEl sistema operativo '{sistema_operativo}' no es compatible con este módulo.")
        return

    # Opción para guardar el resumen
    if resumen:
        guardar = input("\n¿Desea guardar este resumen en un archivo? (s/n): ").strip().lower()
        if guardar == "s":
            nombre = input("Nombre del archivo (ej: resumen_seguridad.txt): ").strip() or "resumen_seguridad.txt"
            try:
                with open(nombre, "w", encoding="utf-8") as f:
                    f.write(resumen)
                print(f"Resumen guardado en '{nombre}'.")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    sistema_operativo = platform.system().lower()
    security_summary(sistema_operativo)
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona un resumen de la seguridad del sistema operativo, incluyendo usuarios conectados y actualizaciones pendientes.
    # Se ejecuta automáticamente al iniciar el programa principal.

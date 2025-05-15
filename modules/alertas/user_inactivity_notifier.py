# -*- coding: utf-8 -*-

import platform
import subprocess
import shutil

def user_inactivity_notifier():
    if platform.system() != "Linux":
        print("Este módulo solo está disponible en sistemas Linux.")
        input("Presione Enter para salir...")
        return

    if not shutil.which("lastlog"):
        print("El comando 'lastlog' no está disponible en este sistema.")
        input("Presione Enter para salir...")
        return

    print("=== USUARIOS INACTIVOS ===\n")
    while True:
        try:
            dias = int(input("Ingrese la cantidad de días de inactividad a verificar: "))
            if dias < 0:
                print("Por favor, ingrese un número positivo.")
                continue
            break
        except ValueError:
            print("Error: entrada inválida. Por favor, ingrese un número entero.")

    print(f"\nUsuarios que no han iniciado sesión en los últimos {dias} días:\n")
    comando = ["lastlog", "-b", str(dias)]
    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    user_inactivity_notifier()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para verificar la inactividad de los usuarios en sistemas Linux.
    # Utiliza la biblioteca subprocess para ejecutar comandos del sistema.
    # La función user_inactivity_notifier() utiliza el comando 'lastlog' para verificar la inactividad de los usuarios en el sistema.
    # El usuario puede especificar la cantidad de días de inactividad a verificar.

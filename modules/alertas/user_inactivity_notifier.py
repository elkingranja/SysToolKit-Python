# -*- coding: utf-8 -*-

import platform
import subprocess
import shutil
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        CYAN = ''
    class Style:
        RESET_ALL = ''

def mostrar_ayuda():
    print(f"""{Fore.CYAN}
=== AYUDA USUARIOS INACTIVOS ===
- Este módulo muestra usuarios que no han iniciado sesión en X días.
- Solo funciona en Linux y requiere el comando 'lastlog'.
- Puedes salir en cualquier momento escribiendo 'q'.
========================={Style.RESET_ALL}
""")

def user_inactivity_notifier():
    if platform.system() != "Linux":
        print(f"{Fore.YELLOW}Este módulo solo está disponible en sistemas Linux.{Style.RESET_ALL}")
        input("Presione Enter para salir...")
        return

    if not shutil.which("lastlog"):
        print(f"{Fore.YELLOW}El comando 'lastlog' no está disponible en este sistema.{Style.RESET_ALL}")
        input("Presione Enter para salir...")
        return

    print(f"{Fore.CYAN}=== USUARIOS INACTIVOS ==={Style.RESET_ALL}\n")
    print("Puedes escribir 'q' para salir o 'help' para ayuda.\n")
    while True:
        dias = input("Ingrese la cantidad de días de inactividad a verificar: ").strip()
        if dias.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del módulo.")
            return
        if dias.lower() in ['help', '-h', '--help']:
            mostrar_ayuda()
            continue
        try:
            dias_int = int(dias)
            if dias_int < 0:
                print(f"{Fore.YELLOW}Por favor, ingrese un número positivo.{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Error: entrada inválida. Por favor, ingrese un número entero.{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Usuarios que no han iniciado sesión en los últimos {dias} días:{Style.RESET_ALL}\n")
    comando = ["lastlog", "-b", str(dias)]
    try:
        resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
        if resultado.stdout:
            print(f"{Fore.GREEN}{resultado.stdout}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No se encontraron usuarios inactivos en ese rango de días.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al ejecutar el comando: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Se produjo un error inesperado: {e}{Style.RESET_ALL}")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    user_inactivity_notifier()
    input("\nPresiona Enter para volver al menú...")
    # Este módulo proporciona una herramienta para verificar la inactividad de los usuarios en sistemas Linux.
    # Utiliza la biblioteca subprocess para ejecutar comandos del sistema.
    # La función user_inactivity_notifier() utiliza el comando 'lastlog' para verificar la inactividad de los usuarios en el sistema.
    # El usuario puede especificar la cantidad de días de inactividad a verificar.

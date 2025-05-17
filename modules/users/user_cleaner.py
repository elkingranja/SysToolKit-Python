import platform
import subprocess
import sys
import os

def configurar_utf8():
    """Configura la codificación UTF-8 en Windows."""
    if sys.platform == "win32":
        os.system("chcp 65001 > nul")
        sys.stdout.reconfigure(encoding='utf-8')

def user_cleaner():
    """Busca usuarios inactivos en sistemas Linux."""
    configurar_utf8()

    if platform.system() != "Linux":
        print("Este módulo solo funciona en sistemas Linux.")
        input("Presione Enter para volver...")
        return

    print("=== USUARIOS INACTIVOS (solo Linux) ===\n")

    try:
        dias = int(input("Ingrese el número de días de inactividad a verificar: "))
        if dias < 0:
            print("El número de días no puede ser negativo.")
            return
    except ValueError:
        print("Entrada inválida. Debe ingresar un número entero.")
        return

    print(f"\nBuscando usuarios que no han iniciado sesión en los últimos {dias} días...\n")
    comando = ["lastlog", "-b", str(dias)]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        if resultado.stdout.strip():
            print(resultado.stdout)
        else:
            print("No se encontraron usuarios inactivos.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except FileNotFoundError:
        print("El comando 'lastlog' no está disponible en este sistema.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    user_cleaner()
    input("\nPresiona Enter para volver al menú...")
    # El código se ejecuta directamente si se llama a este script
    # desde la línea de comandos. Si se importa como un módulo, no se ejecutará.
    # Esto es útil para pruebas unitarias o para evitar la ejecución accidental.

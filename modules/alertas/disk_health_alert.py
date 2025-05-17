# -*- coding: utf-8 -*-
import platform
import os
import subprocess
import shutil
import glob

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
    class Style:
        RESET_ALL = ''

def verificar_sistema():
    if platform.system() != "Linux":
        print(f"{Fore.YELLOW}Este módulo solo funciona en sistemas Linux.{Style.RESET_ALL}")
        return False
    if not shutil.which("smartctl"):
        print(f"{Fore.YELLOW}El comando 'smartctl' no está disponible. Instálelo antes de continuar (sudo apt install smartmontools).{Style.RESET_ALL}")
        return False
    return True

def listar_discos():
    # Busca discos típicos en Linux
    discos = glob.glob("/dev/sd?") + glob.glob("/dev/nvme?n1")
    return discos

def verificar_disco(disco):
    if not os.path.exists(disco):
        print(f"{Fore.RED}El disco especificado no existe.{Style.RESET_ALL}")
        return False
    return True

def ejecutar_comando(comando):
    try:
        resultado = subprocess.run(comando, text=True, capture_output=True, check=True)
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al ejecutar el comando: {e.stderr}{Style.RESET_ALL}")
        if "Permission denied" in e.stderr:
            print(f"{Fore.YELLOW}¿Ejecutaste el script con permisos de superusuario?{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")
        return None

def interpretar_smart(salida):
    if "PASSED" in salida:
        print(f"\n{Fore.GREEN}Estado SMART: El disco está en buen estado ✅{Style.RESET_ALL}")
    elif "FAILED" in salida:
        print(f"\n{Fore.RED}Estado SMART: ¡El disco tiene problemas! ❌{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}No se pudo interpretar el estado SMART.{Style.RESET_ALL}")

def mostrar_ayuda():
    print(f"""
{Fore.CYAN}=== AYUDA ===
Este módulo verifica el estado de salud de discos usando SMART.
- Solo funciona en Linux y requiere smartctl instalado.
- Se recomienda ejecutar como root o con sudo.
- Elija el disco de la lista sugerida.
- Si ve errores de permisos, ejecute el script con sudo.
================{Style.RESET_ALL}
""")

def disk_health_alert():
    print(f"{Fore.CYAN}=== ESTADO DE SALUD DEL DISCO (SMART) ==={Style.RESET_ALL}\n")
    if not verificar_sistema():
        return

    discos = listar_discos()
    if not discos:
        print(f"{Fore.RED}No se encontraron discos disponibles.{Style.RESET_ALL}")
        return

    print("Discos detectados:")
    for idx, d in enumerate(discos):
        print(f"  {idx+1}. {d}")
    while True:
        seleccion = input(f"Seleccione el disco a analizar (1-{len(discos)}), o escriba 'q' para salir: ").strip()
        if seleccion.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del módulo.")
            return
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(discos):
            disco = discos[int(seleccion)-1]
            break
        else:
            print(f"{Fore.YELLOW}Selección inválida. Intente de nuevo.{Style.RESET_ALL}")

    print(f"\nRevisando estado SMART de {Fore.CYAN}{disco}{Style.RESET_ALL}...\n")
    salida = ejecutar_comando(["sudo", "smartctl", "-H", disco])
    if salida:
        print(salida)
        interpretar_smart(salida)
    else:
        print(f"{Fore.RED}No se pudo obtener el estado SMART.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}Información completa del disco:{Style.RESET_ALL}\n")
    salida = ejecutar_comando(["sudo", "smartctl", "-A", disco])
    if salida:
        print(salida)
    else:
        print(f"{Fore.RED}No se pudo obtener la información completa del disco.{Style.RESET_ALL}")

    input(f"\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        mostrar_ayuda()
    else:
        disk_health_alert()

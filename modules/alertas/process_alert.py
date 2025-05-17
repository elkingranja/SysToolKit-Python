import psutil
import time

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

DEFAULT_INTERVAL = 10  # Intervalo por defecto en segundos

def buscar_proceso(nombre):
    """
    Busca si un proceso con el nombre dado está activo.
    :param nombre: Nombre del proceso a buscar.
    :return: True si el proceso está activo, False en caso contrario.
    """
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if nombre.lower() in proc.info['name'].lower():
            return True
    return False

def mostrar_procesos(filtro=None):
    procesos = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if not filtro or filtro.lower() in proc.info['name'].lower():
            procesos.append(proc.info)
    if not procesos:
        print(f"{Fore.YELLOW}No se encontraron procesos con ese filtro.{Style.RESET_ALL}")
    else:
        for p in procesos:
            print(f" - {p['name']} ({p['pid']})")
    return procesos

def mostrar_ayuda():
    print(f"""
{Fore.CYAN}=== AYUDA ===
Este módulo permite monitorear si un proceso está activo o inactivo.
- Puedes filtrar procesos por nombre.
- Puedes salir en cualquier momento escribiendo 'q'.
- Elige si quieres alerta cuando el proceso esté activo o inactivo.
- Elige el intervalo de revisión.
========================={Style.RESET_ALL}
""")

def process_alert():
    """
    Función principal para monitorear el estado de un proceso y mostrar alertas.
    """
    print(f"{Fore.CYAN}=== MONITOREO DE PROCESO ==={Style.RESET_ALL}\n")
    if any(arg in ['-h', '--help', 'help'] for arg in getattr(__import__('sys'), 'argv', [])):
        mostrar_ayuda()
        return

    while True:
        filtro = input("Filtra procesos por nombre (Enter para mostrar todos, 'q' para salir, 'help' para ayuda): ").strip()
        if filtro.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del módulo.")
            return
        if filtro.lower() in ['help', '-h', '--help']:
            mostrar_ayuda()
            continue
        procesos = mostrar_procesos(filtro)
        if procesos:
            break

    while True:
        proceso = input("Ingrese el nombre del proceso a monitorear (o 'q' para salir): ").strip()
        if proceso.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del módulo.")
            return
        if buscar_proceso(proceso):
            break
        else:
            print(f"{Fore.YELLOW}No se encontró ningún proceso con ese nombre. Intenta de nuevo o revisa la lista.{Style.RESET_ALL}")

    print("\nOpciones de alerta:")
    print("1. Mostrar alerta si el proceso está activo")
    print("2. Mostrar alerta si el proceso NO está activo")
    while True:
        alerta = input("Seleccione una opción [1 o 2]: ").strip()
        if alerta in ("1", "2"):
            break
        if alerta.lower() in ['q', 'salir', 'exit']:
            print("Saliendo del módulo.")
            return
        print("Opción inválida. Intenta de nuevo.")

    intervalo = input(f"Intervalo entre revisiones en segundos (por defecto {DEFAULT_INTERVAL}): ").strip()
    try:
        intervalo = int(intervalo)
        if intervalo <= 0:
            raise ValueError("El intervalo debe ser un número positivo.")
    except ValueError as e:
        print(f"Entrada inválida: {e}. Usando intervalo por defecto ({DEFAULT_INTERVAL} segundos).")
        intervalo = DEFAULT_INTERVAL

    print(f"\nResumen de configuración:\nProceso: {proceso}\nAlerta: {'activo' if alerta=='1' else 'inactivo'}\nIntervalo: {intervalo}s\n")
    input("Presiona Enter para iniciar el monitoreo...")

    print(f"\n{Fore.YELLOW}Iniciando monitoreo... Presione Ctrl+C para detener.{Style.RESET_ALL}\n")
    estado_anterior = None  # Para evitar mensajes repetidos

    try:
        while True:
            activo = buscar_proceso(proceso)
            if alerta == "1" and activo and estado_anterior != activo:
                print(f"{Fore.GREEN}[ALERTA] El proceso '{proceso}' está ACTIVO.{Style.RESET_ALL}")
            elif alerta == "2" and not activo and estado_anterior != activo:
                print(f"{Fore.RED}[ALERTA] El proceso '{proceso}' NO está en ejecución.{Style.RESET_ALL}")
            estado_anterior = activo
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\nMonitoreo finalizado por el usuario.")

if __name__ == "__main__":
    process_alert()
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una herramienta para monitorear el estado de un proceso en el sistema.
# Utiliza la biblioteca psutil para obtener información sobre los procesos activos.
# La función process_alert() muestra una lista de procesos activos y permite al usuario seleccionar uno para monitorear.
# Dependiendo de la elección del usuario, se mostrará una alerta si el proceso está activo o inactivo.
# El monitoreo se realiza en un intervalo especificado por el usuario, con un valor predeterminado de 10 segundos.

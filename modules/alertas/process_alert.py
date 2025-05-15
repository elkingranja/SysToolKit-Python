import psutil
import time

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

def process_alert():
    """
    Función principal para monitorear el estado de un proceso y mostrar alertas.
    """
    print("=== MONITOREO DE PROCESO ===\n")

    # Mostrar lista de procesos activos
    print("Lista de procesos activos (nombre - PID):")
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        print(f" - {proc.info['name']} ({proc.info['pid']})")
    print("\n")

    proceso = input("Ingrese el nombre del proceso a monitorear: ").strip()

    print("\nOpciones de alerta:")
    print("1. Mostrar alerta si el proceso está activo")
    print("2. Mostrar alerta si el proceso NO está activo")
    alerta = input("Seleccione una opción [1 o 2]: ").strip()

    if alerta not in ("1", "2"):
        print("Opción inválida. Terminando.")
        return

    intervalo = input(f"Intervalo entre revisiones en segundos (por defecto {DEFAULT_INTERVAL}): ").strip()
    try:
        intervalo = int(intervalo)
        if intervalo <= 0:
            raise ValueError("El intervalo debe ser un número positivo.")
    except ValueError as e:
        print(f"Entrada inválida: {e}. Usando intervalo por defecto ({DEFAULT_INTERVAL} segundos).")
        intervalo = DEFAULT_INTERVAL

    print("\nIniciando monitoreo... Presione Ctrl+C para detener.\n")
    estado_anterior = None  # Para evitar mensajes repetidos

    try:
        while True:
            activo = buscar_proceso(proceso)
            if alerta == "1" and activo and estado_anterior != activo:
                print(f"[ALERTA] El proceso '{proceso}' está ACTIVO.")
            elif alerta == "2" and not activo and estado_anterior != activo:
                print(f"[ALERTA] El proceso '{proceso}' NO está en ejecución.")
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

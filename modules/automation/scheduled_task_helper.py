import os
import platform
import subprocess
import sys
import shutil  # Para verificar si python está en el PATH

# Configurar salida en UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime

def programar_tarea_linux():
    print("\nAsistente para programar tareas en Linux usando crontab")

    # Validar si Python está en el PATH
    if shutil.which("python3") is None:
        print("Advertencia: 'python3' no está en el PATH. Asegúrate de que esté disponible para que la tarea funcione.")
        return

    ruta = input("Ruta absoluta del módulo a ejecutar: ").strip()
    if not os.path.isfile(ruta):
        print("Error: el archivo no existe.")
        return

    try:
        minutos = int(input("Cada cuántos minutos ejecutar el módulo: "))
        if minutos < 1:
            raise ValueError
    except ValueError:
        print("Error: ingrese un número entero válido mayor a 0.")
        return

    nombre_tarea = input("Nombre identificador de la tarea: ").strip()
    if not nombre_tarea:
        print("Error: el nombre de la tarea no puede estar vacío.")
        return

    # Usar la ruta absoluta al ejecutable de Python
    python_path = sys.executable
    cron_linea = f"*/{minutos} * * * * {python_path} {ruta} # {nombre_tarea}"

    try:
        resultado = subprocess.run(
            ['bash', '-c', f'(crontab -l 2>/dev/null; echo "{cron_linea}") | crontab -'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Tarea '{nombre_tarea}' programada correctamente cada {minutos} minutos.")
    except FileNotFoundError:
        print("Error: no se encontró el comando 'bash'. Asegúrate de que esté instalado.")
    except PermissionError:
        print("Error: no tienes permisos suficientes para modificar el crontab.")
    except subprocess.CalledProcessError as e:
        print("Error al agregar la tarea al crontab:")
        print(e.stderr.strip())

def programar_tarea_windows():
    print("\nAsistente para programar tareas en Windows usando schtasks")

    # Validar si Python está en el PATH
    if shutil.which("python") is None:
        print("Advertencia: 'python' no está en el PATH. Asegúrate de que esté disponible para que la tarea funcione.")
        return

    ruta = input("Ruta absoluta del módulo a ejecutar: ").strip()
    if not os.path.isfile(ruta):
        print("Error: el archivo no existe.")
        return

    nombre_tarea = input("Nombre identificador de la tarea: ").strip()
    if not nombre_tarea:
        print("Error: el nombre de la tarea no puede estar vacío.")
        return

    intervalo = input("Cada cuánto tiempo ejecutar la tarea (ejemplo: 5 minutos, 1 hora): ").strip()
    if not intervalo:
        print("Error: el intervalo no puede estar vacío.")
        return

    try:
        # Convertir el intervalo a un formato válido para schtasks
        if "minuto" in intervalo.lower():
            frecuencia = "MINUTE"
            valor = int(intervalo.split()[0])
        elif "hora" in intervalo.lower():
            frecuencia = "HOURLY"
            valor = int(intervalo.split()[0])
        else:
            print("Error: intervalo no válido. Usa 'X minutos' o 'X horas'.")
            return

        # Usar la ruta absoluta al ejecutable de Python
        python_path = sys.executable

        # Crear el comando schtasks
        comando = [
            "schtasks",
            "/Create",
            "/SC", frecuencia,
            "/MO", str(valor),
            "/TN", nombre_tarea,
            "/TR", f'"{python_path}" "{ruta}"',
            "/F"
        ]

        # Ejecutar el comando
        resultado = subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Tarea '{nombre_tarea}' programada correctamente para ejecutarse cada {intervalo}.")
    except ValueError:
        print("Error: el intervalo debe ser un número válido.")
    except subprocess.CalledProcessError as e:
        print("Error al programar la tarea:")
        print(e.stderr.strip())

def instrucciones_windows():
    print("\nInstrucciones para programar tareas en Windows:")
    print("1. Abre el menú Inicio y busca 'Programador de tareas'.")
    print("2. Crea una nueva tarea básica.")
    print("3. Configura que se ejecute: python")
    print("4. En argumentos, coloca la ruta completa del archivo .py que quieres ejecutar.")
    print("5. Ajusta la frecuencia de ejecución (diario, cada hora, etc.).")
    print("Ejemplo de comando:")
    print('python "C:\\ruta\\a\\tu_script.py"')

def scheduled_task_helper():
    print("=== Asistente de tareas programadas ===\n")
    sistema = platform.system()

    if sistema == "Linux":
        programar_tarea_linux()
    elif sistema == "Windows":
        print("¿Deseas programar la tarea automáticamente o seguir las instrucciones manuales?")
        print("1. Programar automáticamente")
        print("2. Mostrar instrucciones manuales")
        opcion = input("Selecciona una opción (1/2): ").strip()

        if opcion == "1":
            programar_tarea_windows()
        elif opcion == "2":
            instrucciones_windows()
        else:
            print("Opción no válida.")
    else:
        print("Sistema operativo no compatible.")

    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    input("\nPresiona Enter para volver al menú...")

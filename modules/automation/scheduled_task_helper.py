import os
import platform
import subprocess
import sys
import shutil
from datetime import datetime

if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

def programar_tarea_linux():
    print("\nAsistente para programar tareas en Linux usando crontab")

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

def listar_tareas_linux():
    print("\nTareas programadas en crontab:")
    try:
        resultado = subprocess.check_output(['crontab', '-l'], text=True)
        print(resultado)
    except subprocess.CalledProcessError:
        print("No hay tareas programadas o no se pudo leer el crontab.")

def eliminar_tarea_linux():
    nombre = input("Nombre identificador de la tarea a eliminar: ").strip()
    try:
        lines = subprocess.check_output(['crontab', '-l'], text=True).splitlines()
        nuevas = [l for l in lines if f"# {nombre}" not in l]
        if len(nuevas) == len(lines):
            print("No se encontró una tarea con ese nombre.")
            return
        contenido = "\n".join(nuevas)
        subprocess.run(['bash', '-c', f'echo "{contenido}" | crontab -'], check=True)
        print(f"Tarea '{nombre}' eliminada correctamente.")
    except Exception as e:
        print("Error al eliminar la tarea:", e)

def programar_tarea_windows():
    print("\nAsistente para programar tareas en Windows usando schtasks")

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
        if "minuto" in intervalo.lower():
            frecuencia = "MINUTE"
            valor = int(intervalo.split()[0])
        elif "hora" in intervalo.lower():
            frecuencia = "HOURLY"
            valor = int(intervalo.split()[0])
        else:
            print("Error: intervalo no válido. Usa 'X minutos' o 'X horas'.")
            return

        python_path = sys.executable

        comando = [
            "schtasks",
            "/Create",
            "/SC", frecuencia,
            "/MO", str(valor),
            "/TN", nombre_tarea,
            "/TR", f'"{python_path}" "{ruta}"',
            "/F"
        ]

        resultado = subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Tarea '{nombre_tarea}' programada correctamente para ejecutarse cada {intervalo}.")
    except ValueError:
        print("Error: el intervalo debe ser un número válido.")
    except subprocess.CalledProcessError as e:
        print("Error al programar la tarea:")
        print(e.stderr.strip())

def listar_tareas_windows():
    print("\nTareas programadas en Windows:")
    try:
        resultado = subprocess.check_output(["schtasks"], text=True, stderr=subprocess.DEVNULL)
        print(resultado)
    except Exception as e:
        print("No se pudieron listar las tareas:", e)

def eliminar_tarea_windows():
    nombre = input("Nombre identificador de la tarea a eliminar: ").strip()
    try:
        subprocess.run(["schtasks", "/Delete", "/TN", nombre, "/F"], check=True)
        print(f"Tarea '{nombre}' eliminada correctamente.")
    except subprocess.CalledProcessError:
        print("No se pudo eliminar la tarea. ¿El nombre es correcto?")

def instrucciones_windows():
    print("\nInstrucciones para programar tareas en Windows:")
    print("1. Abre el menú Inicio y busca 'Programador de tareas'.")
    print("2. Crea una nueva tarea básica.")
    print("3. Configura que se ejecute: python")
    print("4. En argumentos, coloca la ruta completa del archivo .py que quieres ejecutar.")
    print("5. Ajusta la frecuencia de ejecución (diario, cada hora, etc.).")
    print("Ejemplo de comando:")
    print('python "C:\\ruta\\a\\tu_script.py"')

def mostrar_menu():
    print("\n=== Asistente de tareas programadas ===")
    print("1. Programar tarea automáticamente")
    print("2. Mostrar instrucciones manuales")
    print("3. Listar tareas programadas")
    print("4. Eliminar una tarea programada")
    print("5. Salir")

def scheduled_task_helper():
    sistema = platform.system()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1/2/3/4/5): ").strip()
        if sistema == "Linux":
            if opcion == "1":
                programar_tarea_linux()
            elif opcion == "2":
                print("\nConsulta la documentación de tu entorno gráfico para programar tareas manualmente.")
            elif opcion == "3":
                listar_tareas_linux()
            elif opcion == "4":
                eliminar_tarea_linux()
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida.")
        elif sistema == "Windows":
            if opcion == "1":
                programar_tarea_windows()
            elif opcion == "2":
                instrucciones_windows()
            elif opcion == "3":
                listar_tareas_windows()
            elif opcion == "4":
                eliminar_tarea_windows()
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida.")
        else:
            print("Sistema operativo no compatible.")
            break
        input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    scheduled_task_helper()

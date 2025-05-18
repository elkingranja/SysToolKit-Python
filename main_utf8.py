#!/usr/bin/env python3
import os
import sys
import platform

# Asegurar soporte UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        print("Advertencia: No se pudo reconfigurar la salida a UTF-8.")

# Verifica que la carpeta modules y subcarpetas existan
def verificar_estructura():
    carpetas = [
        "modules/monitor", "modules/backup", "modules/alertas",
        "modules/seguridad", "modules/users", "modules/automation",
        "modules/logs", "modules/tools"
    ]
    for carpeta in carpetas:
        if not os.path.isdir(carpeta):
            print(f"Advertencia: Falta la carpeta '{carpeta}'.")

# Establecer permisos de ejecución en Linux
def set_permissions():
    if platform.system() != "Linux":
        print("Advertencia: La función 'set_permissions' solo es aplicable en Linux.")
        return
    for root, _, files in os.walk("modules"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    os.chmod(path, 0o755)
                except Exception as e:
                    print(f"Error al cambiar permisos de {path}: {e}")

# Ejecutar un módulo y mostrar errores si ocurren
def ejecutar_modulo(path):
    if not os.path.isfile(path):
        print(f"ERROR: Módulo no encontrado: {path}")
        return
    try:
        retorno = os.system(f'python "{path}"')
        if retorno != 0:
            print(f"ERROR al ejecutar {path}, código de salida: {retorno}")
    except Exception as e:
        print(f"Excepción al ejecutar el módulo: {e}")

# Diccionario con rutas por categoría
CATEGORIAS = {
    "1": [
        "modules/monitor/system_monitor.py",
        "modules/monitor/network_toolkit.py",
        "modules/monitor/sys_summary.py"
    ],
    "2": [
        "modules/backup/backup_creator.py",
        "modules/backup/restore_backup.py",
        "modules/backup/auto_backup.py",
        "modules/backup/usb_backup.py"
    ],
    "3": [
        "modules/alertas/custom_alert.py",
        "modules/alertas/usb_alert_config.py",
        "modules/alertas/critical_file_watcher.py",
        "modules/alertas/disk_health_alert.py",
        "modules/alertas/user_inactivity_notifier.py",
        "modules/alertas/process_alert.py"
    ],
    "4": [
        "modules/seguridad/rootkit_permission_scan.py",
        "modules/seguridad/user_monitor.py",
        "modules/seguridad/auth_fail_monitor.py",
        "modules/seguridad/security_summary.py",
        "modules/seguridad/permission_checker.py"
    ],
    "5": [
        "modules/users/user_creator.py",
        "modules/users/user_lister.py",
        "modules/users/user_cleaner.py",
        "modules/users/user_groups.py"
    ],
    "6": [
        "modules/automation/startup_manager.py",
        "modules/automation/auto_update_checker.py",
        "modules/automation/scheduled_task_helper.py"
    ],
    "7": [
        "modules/logs/log_manager.py"
    ],
    "8": [
        "modules/tools/file_tools.py"
    ]
}

# Diccionario de descripciones de módulos
DESCRIPCIONES = {
    "modules/monitor/system_monitor.py": "Monitorea el uso de CPU, RAM y disco en tiempo real.",
    "modules/monitor/network_toolkit.py": "Herramientas para analizar y diagnosticar la red.",
    "modules/monitor/sys_summary.py": "Resumen general del sistema y sus recursos.",
    "modules/backup/backup_creator.py": "Crea copias de seguridad de archivos y carpetas.",
    "modules/backup/restore_backup.py": "Restaura archivos desde una copia de seguridad.",
    "modules/backup/auto_backup.py": "Automatiza la creación de copias de seguridad.",
    "modules/backup/usb_backup.py": "Realiza copias de seguridad automáticas en USB.",
    "modules/alertas/custom_alert.py": "Configura alertas personalizadas del sistema.",
    "modules/alertas/usb_alert_config.py": "Alerta cuando se conecta un dispositivo USB.",
    "modules/alertas/critical_file_watcher.py": "Vigila cambios en archivos críticos.",
    "modules/alertas/disk_health_alert.py": "Alerta sobre el estado de salud del disco.",
    "modules/alertas/user_inactivity_notifier.py": "Notifica inactividad de usuarios.",
    "modules/alertas/process_alert.py": "Alerta sobre procesos sospechosos.",
    "modules/seguridad/rootkit_permission_scan.py": "Escanea rootkits y permisos peligrosos.",
    "modules/seguridad/user_monitor.py": "Monitorea actividad de usuarios.",
    "modules/seguridad/auth_fail_monitor.py": "Detecta intentos fallidos de autenticación.",
    "modules/seguridad/security_summary.py": "Resumen de seguridad del sistema.",
    "modules/seguridad/permission_checker.py": "Verifica permisos de archivos y carpetas.",
    "modules/users/user_creator.py": "Crea nuevos usuarios en el sistema.",
    "modules/users/user_lister.py": "Lista todos los usuarios registrados.",
    "modules/users/user_cleaner.py": "Elimina usuarios inactivos o innecesarios.",
    "modules/users/user_groups.py": "Gestiona grupos de usuarios.",
    "modules/automation/startup_manager.py": "Gestiona programas que inician con el sistema.",
    "modules/automation/auto_update_checker.py": "Verifica y aplica actualizaciones automáticas.",
    "modules/automation/scheduled_task_helper.py": "Ayuda a programar tareas automáticas.",
    "modules/logs/log_manager.py": "Gestiona y visualiza logs del sistema.",
    "modules/tools/file_tools.py": "Herramientas varias para archivos y documentos."
}

# Filtra los módulos existentes para mostrar solo los que están presentes
def obtener_modulos_existentes(rutas):
    existentes = []
    for ruta in rutas:
        if os.path.isfile(ruta):
            existentes.append(ruta)
        else:
            print(f"Advertencia: El módulo '{ruta}' no existe y no será mostrado.")
    return existentes

# Mostrar menú principal
def mostrar_menu():
    print("\n=== SysToolKit - Menú Principal ===")
    print("Seleccione una categoría:")
    print("1. Monitoreo del sistema")
    print("2. Copias de seguridad y restauración")
    print("3. Alertas y notificaciones")
    print("4. Seguridad y permisos")
    print("5. Gestión de usuarios")
    print("6. Automatización del sistema")
    print("7. Logs")
    print("8. Herramientas de productividad")
    print("0. Salir")
    print("Escriba 'volver' en cualquier momento para regresar al menú principal.")

# Ejecución del menú principal
def main():
    verificar_estructura()
    set_permissions()
    while True:
        mostrar_menu()
        opcion = input("\nIngrese el número de categoría: ").strip().lower()
        if opcion == "0" or opcion == "volver":
            print("Saliendo del programa.")
            break

        rutas = CATEGORIAS.get(opcion)
        if not rutas:
            print("Opción no válida.")
            continue

        modulos_disponibles = obtener_modulos_existentes(rutas)
        if not modulos_disponibles:
            print("No hay módulos disponibles en esta categoría.")
            continue

        # Submenú de módulos para la categoría seleccionada
        while True:
            print(f"\nMódulos en categoría {opcion}:")
            for i, ruta in enumerate(modulos_disponibles, 1):
                descripcion = DESCRIPCIONES.get(ruta, "Sin descripción disponible.")
                print(f"  {i}. {os.path.basename(ruta)} - {descripcion}")
            print("  0. Volver al menú principal")
            print("  Escriba 'volver' para regresar al menú principal")

            sel = input("Seleccione módulo: ").strip().lower()
            if sel == "0" or sel == "volver":
                break
            if not sel.isdigit() or not (1 <= int(sel) <= len(modulos_disponibles)):
                print("Selección inválida.")
                continue

            # Ejecutar el módulo elegido
            ruta_elegida = modulos_disponibles[int(sel) - 1]
            ejecutar_modulo(ruta_elegida)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

# Asegurar soporte UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        print("Advertencia: No se pudo reconfigurar la salida a UTF-8.")

# Función para establecer permisos de ejecución en Linux
def set_permissions():
    if platform.system() != "Linux":
        print("Advertencia: La función 'set_permissions' solo es aplicable en Linux.")
        return
    for root, _, files in os.walk("modules"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                os.chmod(path, 0o755)

# Ejecutar un módulo mediante subprocess para manejar errores
def ejecutar_modulo(path):
    if not os.path.isfile(path):
        print(f"ERROR: Módulo no encontrado: {path}")
        return
    # Llamada con os.system para que el módulo reciba stdin normalmente
    retorno = os.system(f'python "{path}"')
    if retorno != 0:
        print(f"ERROR al ejecutar {path}, código de salida: {retorno}")

# Validar rutas de módulos
def validar_rutas():
    for categoria, rutas in CATEGORIAS.items():
        for ruta in rutas:
            if not os.path.isfile(ruta):
                print(f"Advertencia: La ruta {ruta} no existe.")

# Mostrar menú principal con categorías y descripciones
def mostrar_menu():
    print("\n=== SysToolKit - Menú Principal ===")
    print("Seleccione una categoría:")
    print("1. Monitoreo del sistema")
    print("   - system_monitor.py: Monitorea CPU, RAM y disco")
    print("   - network_toolkit.py: Herramientas de red y escaneo de puertos")
    print("   - sys_summary.py: Resumen completo del sistema")
    print("2. Copias de seguridad y restauración")
    print("   - backup_creator.py: Crear copias de seguridad")
    print("   - restore_backup.py: Restaurar copias")
    print("   - auto_backup.py: Respaldos automáticos programados")
    print("   - usb_backup.py: Copia automática al conectar USB")
    print("3. Alertas y notificaciones")
    print("   - custom_alert.py: Alertas por CPU, RAM o disco")
    print("   - usb_alert_config.py: Alertas por conexión USB")
    print("   - critical_file_watcher.py: Monitoreo de archivos críticos")
    print("   - disk_health_alert.py: Estado SMART del disco (Linux)")
    print("   - user_inactivity_notifier.py: Usuarios inactivos (Linux)")
    print("   - process_alert.py: Monitoreo de procesos")
    print("4. Seguridad y permisos")
    print("   - rootkit_permission_scan.py: Detección de rootkits y permisos inseguros")
    print("   - user_monitor.py: Usuarios conectados en tiempo real")
    print("   - auth_fail_monitor.py: Fallos de autenticación (Linux)")
    print("   - security_summary.py: Informe de seguridad del sistema")
    print("   - permission_checker.py: Permisos peligrosos en archivos")
    print("5. Gestión de usuarios")
    print("   - user_creator.py: Crear usuarios (Linux)")
    print("   - user_lister.py: Listar usuarios existentes")
    print("   - user_cleaner.py: Limpiar usuarios inactivos (Linux)")
    print("   - user_groups.py: Consultar grupos de usuario")
    print("6. Automatización del sistema")
    print("   - startup_manager.py: Programas al inicio del sistema")
    print("   - auto_update_checker.py: Verificar/instalar actualizaciones")
    print("   - scheduled_task_helper.py: Asistente para tareas programadas")
    print("7. Logs")
    print("   - log_manager.py: Visualización y limpieza de logs del sistema")
    print("8. Herramientas de productividad")
    print("   - file_tools.py: Conversión y manipulación de archivos")
    print("0. Salir")

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

# Ejecución del menú
def main():
    set_permissions()
    validar_rutas()
    while True:
        mostrar_menu()
        opcion = input("\nIngrese el número de categoría: ").strip()
        if opcion == "0":
            print("Saliendo del programa.")
            break

        rutas = CATEGORIAS.get(opcion)
        if not rutas:
            print("Opción no válida.")
            continue

        # Submenú de módulos para la categoría seleccionada
        while True:
            print(f"\nMódulos en categoría {opcion}:")
            for i, ruta in enumerate(rutas, 1):
                print(f"  {i}. {os.path.basename(ruta)}")
            print("  0. Volver al menú principal")

            sel = input("Seleccione módulo: ").strip()
            if sel == "0":
                break
            if not sel.isdigit() or not (1 <= int(sel) <= len(rutas)):
                print("Selección inválida.")
                continue

            # Ejecutar el módulo elegido
            try:
                ruta_elegida = rutas[int(sel) - 1]
                ejecutar_modulo(ruta_elegida)
            except IndexError:
                print("Error: índice fuera de rango. Intente nuevamente.")

if __name__ == "__main__":
    main()

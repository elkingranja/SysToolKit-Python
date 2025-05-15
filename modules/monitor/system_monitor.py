import platform
import psutil
import shutil
import os
import sys

# Configurar la consola para usar UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

def system_monitor():
    print("=== MONITOR DEL SISTEMA ===\n")
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"CPU: {psutil.cpu_percent(interval=1)}%")
    print(f"RAM: {psutil.virtual_memory().percent}%")
    disco = shutil.disk_usage("/")
    print(f"Disco usado: {(disco.used/disco.total)*100:.1f}%")
    input("\nPresiona Enter para volver al menú...")  # Corregido "menú"

if __name__ == "__main__":
    system_monitor()
    input("\nPresiona Enter para volver al menú...")
# Este módulo proporciona una función para monitorear el sistema.
# Utiliza las bibliotecas psutil y shutil para obtener información sobre el uso de CPU, RAM y disco.
# La función system_monitor() imprime la información del sistema y espera a que el usuario presione Enter para volver al menú.
# El módulo también incluye una verificación para ejecutar la función si se ejecuta como un script independiente.
# Esta estructura permite importar el módulo en otros scripts sin ejecutar la función automáticamente.
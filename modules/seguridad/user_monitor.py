# -*- coding: utf-8 -*-
import platform
import subprocess
import shutil
import os
import sys

# Configurar la consola para usar UTF-8
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

# Constantes para mensajes
SEPARADOR = "=" * 30
MSG_NO_COMPATIBLE = "Sistema operativo no compatible."
MSG_PRESIONA_ENTER = "\nPresiona Enter para volver al menú..."

def comando_disponible(comando):
    """Verifica si un comando está disponible en el sistema."""
    return shutil.which(comando) is not None

def mostrar_usuarios_linux():
    """Muestra los usuarios conectados en sistemas Linux."""
    if not comando_disponible("who"):
        print("El comando 'who' no está disponible en este sistema.")
        return

    try:
        resultado = subprocess.check_output(["who"], text=True)
        print(resultado)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar 'who':", e.output.strip())
    except Exception as e:
        print(f"Error inesperado al ejecutar 'who': {e}")

def mostrar_usuarios_windows():
    """Muestra los usuarios conectados o locales en sistemas Windows."""
    advertencia = ""
    resultado = ""
    resumen_riesgo = ""
    usuarios_conectados = False

    if comando_disponible("query"):
        print("Mostrando usuarios conectados actualmente:\n")
        try:
            resultado = subprocess.check_output("query user", shell=True, text=True, stderr=subprocess.STDOUT)
            if resultado.strip():
                print(resultado)
                usuarios_conectados = True
            else:
                print("No hay usuarios conectados actualmente.")
        except subprocess.CalledProcessError as e:
            print("Este comando requiere Windows Pro o superior o privilegios de administrador.")
            print("Detalles:", e.output.strip())
        except Exception as e:
            print(f"Error inesperado al ejecutar 'query user': {e}")

    if not usuarios_conectados and comando_disponible("net"):
        print("\nMostrando todas las cuentas locales con 'net user':\n")
        try:
            resultado = subprocess.check_output("net user", shell=True, text=True, stderr=subprocess.STDOUT)
            print(resultado)
            if "Invitado" in resultado and "Cuenta deshabilitada" not in resultado:
                advertencia = "\n[!] Advertencia: La cuenta 'Invitado' está presente. Se recomienda deshabilitarla si no se usa."
                print(advertencia)
                resumen_riesgo = "¡Atención! Hay cuentas inseguras activas."
            else:
                resumen_riesgo = "No se detectaron cuentas inseguras."
        except Exception as e:
            print(f"Error inesperado al ejecutar 'net user': {e}")
    elif not usuarios_conectados:
        print("No se pudo obtener la lista de usuarios con 'query user' ni con 'net user'.")
        resumen_riesgo = "No se pudo analizar el riesgo de cuentas inseguras."

    # Resumen de riesgos
    if resumen_riesgo:
        print("\nResumen de seguridad:")
        print(resumen_riesgo)

    # Opción para guardar el resultado
    if resultado:
        guardar = input("\n¿Desea guardar este resultado en un archivo? (s/n): ").strip().lower()
        if guardar == "s":
            nombre = input("Nombre del archivo (ej: usuarios.txt): ").strip() or "usuarios.txt"
            try:
                with open(nombre, "w", encoding="utf-8") as f:
                    f.write(resultado)
                    if advertencia:
                        f.write(advertencia)
                    if resumen_riesgo:
                        f.write("\nResumen de seguridad:\n" + resumen_riesgo)
                print(f"Resultado guardado en '{nombre}'.")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

def user_monitor():
    """Función principal para mostrar usuarios conectados según el sistema operativo."""
    print(SEPARADOR)
    print("USUARIOS CONECTADOS")
    print(SEPARADOR)

    sistema = platform.system()

    if sistema == "Linux":
        mostrar_usuarios_linux()
    elif sistema == "Windows":
        mostrar_usuarios_windows()
    else:
        print(MSG_NO_COMPATIBLE)

    input(MSG_PRESIONA_ENTER)

if __name__ == "__main__":
    user_monitor()
    input("\nPresiona Enter para volver al menú...")

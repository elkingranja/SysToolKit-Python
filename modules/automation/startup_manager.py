# -*- coding: utf-8 -*-
import os
import sys
import platform
import subprocess

def configurar_utf8_windows():
    """Configura la consola de Windows para usar UTF-8."""
    try:
        subprocess.run(["chcp", "65001"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception as e:
        print(f"[Error] No se pudo configurar la consola en UTF-8: {e}")

def ruta_inicio_windows():
    appdata = os.getenv('APPDATA')
    if not appdata:
        print("[Error] No se pudo determinar la ruta APPDATA.")
        return None
    return os.path.join(appdata, 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

def ruta_inicio_linux():
    ruta = os.path.expanduser("~/.config/autostart")
    os.makedirs(ruta, exist_ok=True)
    return ruta

def agregar_al_inicio(nombre, comando):
    sistema = platform.system()

    if sistema == "Windows":
        ruta = ruta_inicio_windows()
        if not ruta:
            return
        ruta_destino = os.path.join(ruta, f"{nombre}.bat")
        contenido = f'start "" "{comando}"\n'

    elif sistema == "Linux":
        ruta = ruta_inicio_linux()
        ruta_destino = os.path.join(ruta, f"{nombre}.desktop")
        contenido = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            f"Exec={comando}\n"
            "Hidden=false\n"
            "NoDisplay=false\n"
            "X-GNOME-Autostart-enabled=true\n"
            f"Name={nombre}\n"
        )

    else:
        print("[Error] Sistema operativo no compatible.")
        return

    try:
        with open(ruta_destino, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"[OK] Entrada de inicio creada en: {ruta_destino}")
    except Exception as e:
        print(f"[Error] No se pudo crear la entrada: {e}")

def quitar_del_inicio(nombre):
    sistema = platform.system()

    if sistema == "Windows":
        ruta = ruta_inicio_windows()
        if not ruta:
            return
        archivo = os.path.join(ruta, f"{nombre}.bat")
    elif sistema == "Linux":
        archivo = os.path.join(ruta_inicio_linux(), f"{nombre}.desktop")
    else:
        print("[Error] Sistema operativo no compatible.")
        return

    if os.path.exists(archivo):
        try:
            os.remove(archivo)
            print(f"[OK] Entrada eliminada: {archivo}")
        except Exception as e:
            print(f"[Error] No se pudo eliminar: {e}")
    else:
        print("[Info] No se encontró ninguna entrada con ese nombre.")

def mostrar_menu():
    print("\n=== Gestor de inicio automático ===")
    print("1. Agregar programa/script al inicio")
    print("2. Eliminar entrada del inicio")
    print("0. Salir")
    return input("Seleccione una opción: ").strip()

def startup_manager():
    if sys.platform == "win32":
        configurar_utf8_windows()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            nombre = input("Nombre para la entrada: ").strip()
            comando = input("Comando o ruta del script/programa: ").strip()
            if not nombre or not comando:
                print("[Error] El nombre y el comando no pueden estar vacíos.")
                continue
            agregar_al_inicio(nombre, comando)

        elif opcion == "2":
            nombre = input("Nombre de la entrada a eliminar: ").strip()
            if not nombre:
                print("[Error] El nombre no puede estar vacío.")
                continue
            quitar_del_inicio(nombre)

        elif opcion == "0":
            break

        else:
            print("[Error] Opción no válida.")

if __name__ == "__main__":
    startup_manager()
    input("\nPresiona Enter para volver al menú...")

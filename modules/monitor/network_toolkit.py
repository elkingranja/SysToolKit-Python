#!/usr/bin/env python3
import os
import sys
import socket
import psutil
import re

# Asegurar soporte UTF-8 en Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

def mostrar_red():
    print("=== MONITOR DE RED ===\n")
    try:
        nombre_host = socket.gethostname()
        ip_local = socket.gethostbyname(nombre_host)
        print(f"Host: {nombre_host}")
        print(f"IP local: {ip_local}")
    except Exception as e:
        print("No se pudo obtener IP:", e)

    if_addrs = psutil.net_if_addrs()
    print("\nInterfaces de red:")
    for interface, addrs in if_addrs.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f" - {interface}: {addr.address}")

    print("\nEstadísticas de red:")
    stats = psutil.net_io_counters()
    print(f"Bytes recibidos: {stats.bytes_recv}")
    print(f"Bytes enviados: {stats.bytes_sent}")

def es_ip_valida(ip):
    patron = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(patron, ip):
        return all(0 <= int(num) <= 255 for num in ip.split('.'))
    return False

def escanear_puertos():
    print("\n=== ESCÁNER DE PUERTOS ===")
    while True:
        print("\nOpciones de escaneo:")
        print("1. Escanear un puerto específico")
        print("2. Escanear un rango de puertos (por defecto 20-1024)")
        print("3. Escanear puertos comunes en una IP/hostname")
        print("0. Volver al menú")
        opcion = input("Seleccione una opción: ").strip()
        if opcion.lower() in ("0", "volver", "salir"):
            return

        if opcion == "1":
            destino = input("Ingrese la IP o hostname a escanear (Enter para localhost, o escriba 'volver'/'salir' para regresar): ").strip()
            if destino.lower() in ("volver", "salir"):
                continue
            if destino == "":
                destino = "127.0.0.1"
            else:
                try:
                    socket.gethostbyname(destino)
                except Exception:
                    print("IP o hostname inválido.")
                    continue
            puerto = input("Ingrese el número de puerto a escanear (ejemplo 80, o 'salir' para cancelar): ").strip()
            if puerto.lower() in ("volver", "salir"):
                continue
            if not puerto.isdigit() or not (1 <= int(puerto) <= 65535):
                print("Puerto inválido.")
                continue
            puerto = int(puerto)
            print(f"Escaneando {destino}:{puerto}...")
            abierto = False
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)
                    if sock.connect_ex((destino, puerto)) == 0:
                        abierto = True
                servicio = obtener_servicio(puerto)
                resultado = f"El puerto {puerto} ({servicio}) en {destino} está {'ABIERTO' if abierto else 'cerrado'}."
                print(resultado)
                guardar = input("¿Desea guardar el resultado en un archivo? (s/n): ").strip().lower()
                if guardar == "s":
                    with open("resultado_escaner.txt", "a", encoding="utf-8") as f:
                        f.write(resultado + "\n")
                        print("Resultado guardado en resultado_escaner.txt")
            except Exception as e:
                print(f"No se pudo escanear {destino}:{puerto} -> {e}")
            input("\nPresiona Enter para continuar...")
            continue

        if opcion == "2":
            rango = input("Ingrese el rango de puertos (ejemplo 20-1024, Enter para usar el predeterminado): ").strip()
            if rango == "":
                inicio, fin = 20, 1024
            else:
                try:
                    partes = rango.split("-")
                    inicio = int(partes[0])
                    fin = int(partes[1])
                    if inicio < 1 or fin > 65535 or inicio > fin:
                        raise ValueError
                except Exception:
                    print("Rango inválido.")
                    continue
            puertos_abiertos = []
            for puerto in range(inicio, fin + 1):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)
                    if sock.connect_ex(("127.0.0.1", puerto)) == 0:
                        puertos_abiertos.append(puerto)
                if (puerto - inicio) % 100 == 0:
                    print(f"Escaneando puerto {puerto}...")
            if puertos_abiertos:
                print("Puertos abiertos:")
                for p in puertos_abiertos:
                    print(f" - Puerto {p}")
            else:
                print(f"No se detectaron puertos abiertos en el rango {inicio}-{fin}.")
            input("\nPresiona Enter para continuar...")
            continue

        if opcion == "3":
            destino = input("Ingrese la IP o hostname a escanear (Enter para localhost, o escriba 'volver'/'salir' para regresar): ").strip()
            if destino.lower() in ("volver", "salir"):
                continue
            if destino == "":
                destino = "127.0.0.1"
            else:
                try:
                    socket.gethostbyname(destino)
                except Exception:
                    print("IP o hostname inválido.")
                    continue
            puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]
            print(f"Escaneando puertos comunes en {destino}...")
            abiertos = []
            for puerto in puertos_comunes:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(0.5)
                        if sock.connect_ex((destino, puerto)) == 0:
                            abiertos.append(puerto)
                except Exception:
                    pass
            if abiertos:
                print("Puertos abiertos:")
                for p in abiertos:
                    servicio = obtener_servicio(p)
                    print(f" - Puerto {p} ({servicio})")
            else:
                print("No se detectaron puertos comunes abiertos.")
            input("\nPresiona Enter para continuar...")
            continue

        print("Opción inválida. Inténtelo de nuevo.")

def network_toolkit():
    while True:
        mostrar_red()
        escanear_puertos()
        opcion = input("\nPresiona Enter para regresar al menú o escribe 'salir' para salir: ").strip()
        if opcion.lower() == "salir":
            break

def obtener_servicio(puerto):
    try:
        return socket.getservbyport(puerto)
    except Exception:
        return "desconocido"

def main():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ejecutar herramientas de red")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            network_toolkit()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys
import socket
import psutil

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

def escanear_puertos():
    print("\n=== ESCÁNER DE PUERTOS (localhost) ===")
    try:
        puertos_abiertos = []
        for puerto in range(20, 1025):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex(("127.0.0.1", puerto)) == 0:
                    puertos_abiertos.append(puerto)

        if puertos_abiertos:
            print("Puertos abiertos:")
            for p in puertos_abiertos:
                print(f" - Puerto {p}")
        else:
            print("No se detectaron puertos abiertos en el rango 20-1024.")
    except Exception as e:
        print("Error en el escaneo:", e)

def network_toolkit():
    while True:
        mostrar_red()
        escanear_puertos()
        opcion = input("\nPresiona Enter para regresar al menú o escribe 'salir' para salir: ").strip()
        if opcion.lower() == "salir":
            break

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

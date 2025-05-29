# SysToolKit-Python
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
> Suite modular de administración, automatización y monitoreo de sistemas en Python para Windows y Linux.

## Contenido
- [Características principales](#caracter%C3%ADsticas-principales)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalaci%C3%B3n)
- [Uso](#uso)
- [Configuración](#configuraci%C3%B3n)
- [Empaquetado](#empaquetado)
- [Contribución](#contribuci%C3%B3n)
- [Licencia](#licencia)
- [Referencias](#referencias)

## Características principales
- Monitoreo de CPU, RAM, disco y red
- Escaneo de puertos y detección de rootkits
- Automatización de respaldos con cron desde el menú
- Generación de reportes PDF/HTML
- Gestión de usuarios y limpieza de logs
- Multiplataforma: Windows (Git Bash/WSL) y Linux

## Estructura del proyecto
```
SysToolKit-Python/
├─ build_exe.bat
├─ build_exe.sh
├─ config_example.ini
├─ LICENSE
├─ main_utf8.py
├─ README.md
├─ requirements.txt
└─ modules/
   ├─ monitor/
   ├─ backup/
   ├─ alertas/
   ├─ seguridad/
   ├─ users/
   ├─ automation/
   └─ logs/
```

## Requisitos
- Python ≥ 3.7
- pip
- Git

## Instalación
```bash
git clone https://github.com/elkingranja/SysToolKit-Python.git
cd SysToolKit-Python
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

Ejecuta el menú principal desde la raíz del proyecto:

```bash
python main_utf8.py
```

Selecciona una categoría del menú (1 al 8).  
Luego, elige el módulo correspondiente.  
Tras la ejecución, pulsa Enter para volver o 0 para salir.

## Configuración
1. Copia el ejemplo de configuración:
   ```bash
   cp config_example.ini config.ini
   ```
2. Edita `config.ini` y ajusta rutas, umbrales y e-mail.

## Empaquetado
- Instalar localmente:
  ```bash
  pip install .
  ```
- Crear ejecutable (Windows/Linux):
  ```bash
  pyinstaller --onefile main_utf8.py --name SysToolKit
  ```

## Contribución
1. Haz un fork
2. Crea una rama (`feature/nombre`)
3. Commit y push
4. Abre un Pull Request

## Licencia
Este proyecto está bajo la licencia MIT — ver [LICENSE](LICENSE) para más detalles.

## Referencias

- Glances: https://nicolargo.github.io/glances/
- psutil (monitor de recursos): https://github.com/giampaolo/psutil
- PyInstaller (generación de ejecutables): https://pyinstaller.org
- PDF libraries: https://pypi.org/project/fpdf/, https://pypi.org/project/pdf2docx/

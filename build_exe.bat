@echo off
REM ==============================================
REM  Script: build_exe.bat
REM  Descripción: Genera SysToolKit.exe usando PyInstaller
REM  Mejoras: Manejo de errores, verificación de archivos, logs, mensajes claros
REM ==============================================

set LOGFILE=build_exe.log
echo Iniciando proceso de compilación... > %LOGFILE%

echo =============================================
echo  Generando ejecutable SysToolKit (UTF-8)
echo =============================================

REM 1. Verificar archivos necesarios
if not exist "main_utf8.py" (
    echo [ERROR] No se encontró main_utf8.py. >> %LOGFILE%
    echo ERROR: No se encontró main_utf8.py. Asegúrate de que el archivo existe en el directorio actual.
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo [ADVERTENCIA] No se encontró requirements.txt. >> %LOGFILE%
    echo ADVERTENCIA: No se encontró requirements.txt. Se omitirá la instalación de dependencias.
)

REM 2. Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat >> %LOGFILE% 2>&1
    echo Entorno virtual activado. >> %LOGFILE%
) else (
    echo [ADVERTENCIA] No se encontró entorno virtual. Se usará Python global. >> %LOGFILE%
)

REM 3. Instalar dependencias si existe requirements.txt
if exist "requirements.txt" (
    echo Instalando dependencias...
    pip install -r requirements.txt >> %LOGFILE% 2>&1
    if errorlevel 1 (
        echo [ERROR] Falló la instalación de dependencias. >> %LOGFILE%
        echo ERROR: Falló la instalación de dependencias. Revisa el archivo build_exe.log para más detalles.
        pause
        exit /b 1
    )
)

REM 4. Limpiar compilaciones anteriores
echo Limpiando carpetas build/ dist/ y spec...
rmdir /s /q build >> %LOGFILE% 2>&1
rmdir /s /q dist >> %LOGFILE% 2>&1
del /q main_utf8.spec 2>>%LOGFILE%

REM 5. Ejecutar PyInstaller para crear un único exe
echo Ejecutando PyInstaller...
pyinstaller --onefile main_utf8.py --name SysToolKit >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo [ERROR] Falló la creación del ejecutable. >> %LOGFILE%
    echo ERROR: Falló la creación del ejecutable. Revisa el archivo build_exe.log para más detalles.
    pause
    exit /b 1
)

REM 6. Finalización
if exist "dist\SysToolKit.exe" (
    echo.
    echo =============================================
    echo  ¡Listo! Ejecutable generado en: dist\SysToolKit.exe
    echo  Puedes ejecutar el programa haciendo doble clic en ese archivo.
    echo =============================================
    echo [OK] Compilación exitosa. >> %LOGFILE%
) else (
    echo [ERROR] No se encontró el ejecutable generado. >> %LOGFILE%
    echo ERROR: No se encontró el ejecutable generado. Revisa el archivo build_exe.log para más detalles.
)

pause
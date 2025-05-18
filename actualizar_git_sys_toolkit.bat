@echo off
echo ==============================
echo   Actualizando repositorio Git
echo ==============================
cd /d %~dp0

REM Añadir todos los archivos
git add .
IF %ERRORLEVEL% NEQ 0 (
    echo Error al ejecutar 'git add'.
    pause
    exit /b 1
)

REM Mostrar archivos a commitear
echo Archivos listos para commit:
git status
echo.

REM Confirmar antes de continuar
set /p CONTINUAR="¿Deseas continuar con el commit y push? (s/n): "
if /I not "%CONTINUAR%"=="s" (
    echo Operación cancelada por el usuario.
    pause
    exit /b 0
)

REM Crear commit solo si hay cambios
git diff --cached --quiet
IF %ERRORLEVEL% EQU 0 (
    echo No hay cambios para commitear.
    pause
    exit /b 0
)

for /f %%i in ('powershell -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set FECHA=%%i
git commit -m "Actualización automática %FECHA%"
IF %ERRORLEVEL% NEQ 0 (
    echo Error al ejecutar 'git commit'.
    pause
    exit /b 1
)

REM Enviar al repositorio remoto
git push origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Error al ejecutar 'git push'.
    pause
    exit /b 1
)

echo.
echo ¡Actualización completada con éxito!
pause

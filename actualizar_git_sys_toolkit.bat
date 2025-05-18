@echo off
echo ==============================
echo   Actualizando repositorio Git
echo ==============================
cd /d %~dp0

REM Añadir todos los archivos
git add .

REM Crear commit con marca de tiempo automática
for /f %%i in ('powershell -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set FECHA=%%i
git commit -m "Actualización automática %FECHA%"

REM Enviar al repositorio remoto
git push origin main

pause

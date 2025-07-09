@echo off
setlocal

REM Paso 1: Verificar si Python 3.12 está instalado
where python >nul 2>nul
if errorlevel 1 (
echo Python no está instalado. Por favor instalá Python 3.12 manualmente desde:
echo https://www.python.org/downloads/release/python-3120/
pause
exit /b
)

for /f "tokens=2 delims=[]" %%a in ('python -V 2^>^&1') do set "PY_VERSION=%%a"
echo Detectado Python %PY_VERSION%

REM Paso 2: Verificar si existe el entorno virtual
echo.
if exist .venv\Scripts\activate (
echo Entorno virtual ya existe. Se usará el existente.
) else (
echo Creando entorno virtual...
python -m venv .venv
if errorlevel 1 (
echo Error al crear el entorno virtual.
pause
exit /b
)
)

REM Paso 3: Activar el entorno virtual
echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

REM Paso 4: Verificar si dependencias están instaladas
echo.
if exist .venv\installed.flag (
echo Requisitos ya instalados previamente.
) else (
echo Instalando dependencias desde requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
echo Fallo la instalación de dependencias.
pause
exit /b
)
echo Instalación completada. > .venv\installed.flag
)

REM Paso 5: Ejecutar el script
echo.
echo Ejecutando main.py...
python main.py

endlocal
pause
@echo off
setlocal

REM Paso 1: Verificar si Python 3.12 está disponible
py -3.12 -V >nul 2>nul
if errorlevel 1 (
echo Python 3.12 no está instalado o no se encuentra en el PATH.
echo Por favor instalá Python 3.12 desde: https://www.python.org/downloads/release/python-3120/
pause
exit /b
)

echo Detectado Python 3.12

REM Paso 2: Crear entorno virtual si no existe
if not exist ".venv" (
echo.
echo Creando entorno virtual...
py -3.12 -m venv .venv
if errorlevel 1 (
echo Error al crear el entorno virtual.
pause
exit /b
)
) else (
echo.
echo Entorno virtual ya existe. Usando entorno existente.
)

REM Paso 3: Activar entorno virtual
call .venv\Scripts\activate

REM Paso 4: Instalar dependencias si no están instaladas
if not exist ".venv\Lib\site-packages\pygame" (
echo.
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
) else (
echo.
echo Dependencias ya instaladas.
)

REM Paso 5: Ejecutar main.py
echo.
echo Ejecutando main.py...
python main.py

endlocal
pause
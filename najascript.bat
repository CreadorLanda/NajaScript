@echo off
REM NajaScript v1.2.0 - Launcher
setlocal enabledelayedexpansion

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.6+ de https://python.org
    pause
    exit /b 1
)

REM Definir diretório do NajaScript
set "NAJA_DIR=%~dp0"

REM Adicionar ao PYTHONPATH
set "PYTHONPATH=%NAJA_DIR%;%PYTHONPATH%"

REM Executar NajaScript
if "%1"=="" (
    python "%NAJA_DIR%\najascript.py" --help
) else (
    python "%NAJA_DIR%\najascript.py" %*
)

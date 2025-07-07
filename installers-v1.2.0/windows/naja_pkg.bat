@echo off
REM NajaScript Package Manager v1.2.0
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

REM Executar Package Manager
python "%NAJA_DIR%\naja_github_package_manager.py" %*

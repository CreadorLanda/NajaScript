@echo off
setlocal

:: Obtém o diretório do script
set "SCRIPT_DIR=%~dp0"

:: Verifica se o ambiente virtual existe
if not exist "%SCRIPT_DIR%venv" (
    echo Criando ambiente virtual...
    python -m venv "%SCRIPT_DIR%venv"
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
    python "%SCRIPT_DIR%post_install.py"
) else (
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
)

:: Executa o REPL
python "%SCRIPT_DIR%naja_repl.py"

endlocal 
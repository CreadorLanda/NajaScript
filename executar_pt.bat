@echo off
REM Executa um script NajaScript com suporte a português

IF "%1"=="" (
    ECHO Uso: executar_pt.bat [arquivo.naja]
    EXIT /B 1
)

python najascript.py --pt %1

IF %ERRORLEVEL% NEQ 0 (
    ECHO Erro ao executar o script.
    EXIT /B %ERRORLEVEL%
)

EXIT /B 0 
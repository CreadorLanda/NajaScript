#!/bin/bash
# Executa um script NajaScript com suporte a português

if [ "$#" -ne 1 ]; then
    echo "Uso: ./executar_pt.sh arquivo.naja"
    exit 1
fi

python najascript.py --pt "$1"

if [ $? -ne 0 ]; then
    echo "Erro ao executar o script."
    exit $?
fi

exit 0 
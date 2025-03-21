#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper para o interpretador NajaScript.
Este script permite executar arquivos NajaScript diretamente do terminal.
"""

import sys
import os
import importlib.util
import subprocess
from pathlib import Path

def find_interpreter():
    """
    Procura pelo interpretador najascript.py em várias localizações possíveis.
    """
    # Lista de possíveis localizações para o interpretador
    possible_locations = [
        # No mesmo diretório deste script
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "najascript.py"),
        # No diretório do PyInstaller (_MEIPASS)
        getattr(sys, '_MEIPASS', None) and os.path.join(sys._MEIPASS, "najascript.py"),
        # Em subdiretórios
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "najascript.py"),
        # Em diretórios pai
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "najascript.py"),
    ]
    
    # Remover valores None
    possible_locations = [loc for loc in possible_locations if loc]
    
    # Verificar cada localização
    for location in possible_locations:
        if os.path.exists(location):
            return location
    
    return None

def run_interpreter_as_module(args):
    """
    Executa o interpretador como um módulo Python.
    """
    interpreter_path = find_interpreter()
    if not interpreter_path:
        print("Erro: Não foi possível encontrar o interpretador NajaScript!")
        return 1
    
    try:
        # Tentar importar como módulo
        spec = importlib.util.spec_from_file_location("najascript", interpreter_path)
        if spec is None:
            raise ImportError("Não foi possível carregar o interpretador como módulo")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["najascript"] = module
        spec.loader.exec_module(module)
        
        # Configurar sys.argv para o módulo
        orig_argv = sys.argv
        sys.argv = [interpreter_path] + args
        
        # Executar a função principal do interpretador
        if hasattr(module, "main"):
            result = module.main()
        else:
            print("Aviso: O interpretador não possui uma função main(). Tentando método alternativo.")
            result = run_interpreter_as_process(args)
        
        # Restaurar sys.argv
        sys.argv = orig_argv
        return result
    except Exception as e:
        print(f"Erro ao executar o interpretador como módulo: {e}")
        return run_interpreter_as_process(args)

def run_interpreter_as_process(args):
    """
    Executa o interpretador como um processo separado.
    """
    interpreter_path = find_interpreter()
    if not interpreter_path:
        print("Erro: Não foi possível encontrar o interpretador NajaScript!")
        return 1
    
    try:
        # Executar como um processo Python
        cmd = [sys.executable, interpreter_path] + args
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        print(f"Erro ao executar o interpretador como processo: {e}")
        return 1

def show_help():
    """
    Exibe a mensagem de ajuda.
    """
    print("NajaScript - Interpretador para a linguagem NajaScript")
    print("\nUso:")
    print("  najascript <arquivo.naja> [opções]")
    print("\nOpções:")
    print("  --help, -h     : Exibe esta mensagem de ajuda")
    print("  --version, -v  : Exibe a versão do interpretador")
    print("\nExemplos:")
    print("  najascript exemplo.naja")
    print("  najascript caminho/para/script.naja")

def main():
    """
    Função principal que processa os argumentos e executa o interpretador.
    """
    # Verificar se temos argumentos suficientes
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        show_help()
        return 0
    
    # Verificar a versão
    if sys.argv[1] in ["--version", "-v"]:
        print("NajaScript Versão 1.0")
        return 0
    
    # Passar todos os argumentos para o interpretador
    return run_interpreter_as_module(sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from lexer import Lexer
from parser_naja import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Uso: python najascript.py <arquivo.naja>")
        return

    # Lê o arquivo fonte
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        source = file.read()

    try:
        # Inicializa o lexer, parser e interpretador
        lexer = Lexer(source)
        parser = Parser(lexer)
        interpreter = Interpreter()
        
        # Analisa o código fonte e cria a AST
        ast = parser.parse()
        
        # Interpreta a AST
        result = interpreter.interpret(ast)
        
        if result:
            print(f"Programa executado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        # Adiciona traceback para depuração
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
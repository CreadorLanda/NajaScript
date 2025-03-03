#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from lexer import Lexer
from parser_naja import Parser
from interpreter import Interpreter
from jit_compiler import JITCompiler
from aot_compiler import AOTCompiler

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='NajaScript - Interpretador/Compilador')
    parser.add_argument('arquivo', help='Arquivo fonte NajaScript (.naja)')
    parser.add_argument('--jit', action='store_true', help='Ativa o compilador JIT')
    parser.add_argument('--compile', action='store_true', help='Compila para um executável nativo')
    parser.add_argument('--output', '-o', help='Nome do arquivo de saída')
    parser.add_argument('--optimize', '-O', action='store_true', help='Ativa otimizações')
    parser.add_argument('--target', help='Target triple para compilação (ex: x86_64-pc-linux-gnu)')

    args = parser.parse_args()

    # Verifica se o arquivo existe
    if not os.path.exists(args.arquivo):
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado.")
        return 1

    # Tenta ler o arquivo com diferentes codificações
    source = None
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(args.arquivo, 'r', encoding=encoding) as file:
                source = file.read()
                print(f"Arquivo lido com sucesso usando codificação: {encoding}")
                break
        except UnicodeDecodeError:
            continue
    
    if source is None:
        print(f"Erro: Não foi possível ler o arquivo '{args.arquivo}' com nenhuma das codificações tentadas.")
        return 1

    try:
        # Inicializa o lexer e parser
        lexer = Lexer(source)
        parser = Parser(lexer)
        
        # Analisa o código fonte e cria a AST
        ast = parser.parse()
        
        # Determina o modo de execução
        if args.compile:
            # Modo de compilação AOT
            output_file = args.output or os.path.splitext(args.arquivo)[0]
            
            # Inicializa o compilador AOT
            compiler = AOTCompiler(target_triple=args.target)
            
            # Compila o programa
            print(f"Compilando '{args.arquivo}' para executável nativo...")
            result = compiler.compile(ast, output_file=output_file, optimize=args.optimize)
            
            print(f"Compilação concluída! Executável gerado: {result}")
            
        else:
            # Modo de interpretação (com ou sem JIT)
            interpreter = Interpreter()
            
            if args.jit:
                # Ativa o JIT compiler
                jit_compiler = JITCompiler()
                interpreter.set_jit_compiler(jit_compiler)
                print("Interpretador JIT ativado")
            
            # Interpreta a AST
            result = interpreter.interpret(ast)
            
            if result:
                print("Programa executado com sucesso!")
    
    except Exception as e:
        print(f"Erro: {e}")
        # Adiciona traceback para depuração
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
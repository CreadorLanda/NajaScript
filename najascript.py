#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
import traceback

try:
    from lexer import Lexer
    from parser_naja import Parser
    from interpreter import Interpreter
    from naja_bytecode import NajaBytecodeCompiler, BytecodeInterpreter
    from naja_llvm import NajaLLVMGenerator
    from ast_nodes import ImportStatement
    from llvmlite import binding as llvm
except Exception as e:
    print(f"Erro ao importar módulos: {e}")
    traceback.print_exc()
    sys.exit(1)

def initialize_llvm():
    """Inicializa o LLVM"""
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    
    # Cria o engine de execução
    target = llvm.get_native_target()
    target_machine = target.create_target_machine()
    
    return target_machine

def main():
    parser = argparse.ArgumentParser(description='NajaScript Interpreter')
    parser.add_argument('file', nargs='?', help='Script para executar')
    parser.add_argument('--module-path', action='append', help='Caminhos adicionais para buscar módulos')
    parser.add_argument('--pt', action='store_true', help='Habilitar suporte a português')
    parser.add_argument('--debug', action='store_true', help='Mostrar informações de depuração')
    args = parser.parse_args()

    # Criar o interpretador
    interpreter = Interpreter()
    interpreter.debug = args.debug
    
    # Modo de depuração
    debug = args.debug
    
    # Definir caminhos de módulos
    module_paths = ['.', './modules']
    if args.module_path:
        module_paths.extend(args.module_path)
    
    # Se o arquivo for fornecido, adiciona o diretório do arquivo como caminho de módulo
    if args.file:
        file_dir = os.path.dirname(os.path.abspath(args.file))
        if file_dir not in module_paths:
            module_paths.append(file_dir)
    
    # Configurar caminhos de módulos no interpretador
    interpreter.module_paths = module_paths
    
    # Carregar o módulo NajaPt se a flag --pt estiver presente
    if args.pt:
        # Cria uma instrução de importação e executa
        import_stmt = ImportStatement('"NajaPt"')
        interpreter.execute_ImportStatement(import_stmt)
    
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Aplicar pré-processamento ao código fonte
            if hasattr(interpreter, 'preprocess_source'):
                source = interpreter.preprocess_source(source)
                if debug:
                    print("\n--- Código após pré-processamento ---")
                    print(source)
                    print("--------------------------------------\n")
                
            # Analisar e executar o código
            lexer = Lexer(source)
            parser = Parser(lexer)
            try:
                ast = parser.parse()
                
                if debug:
                    print("\n--- AST gerada ---")
                    print(f"Tipo: {type(ast)}")
                    print(f"Statements: {len(ast.statements) if hasattr(ast, 'statements') else 'N/A'}")
                    if hasattr(ast, 'statements'):
                        for i, stmt in enumerate(ast.statements):
                            print(f"Statement {i}: {type(stmt).__name__}")
                    print("------------------\n")
                
                try:
                    # Execução do código
                    result = interpreter.interpret(ast)
                    
                    # Valor de retorno de script
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"Erro durante a interpretação: {e}")
                    if debug:
                        print("\n--- Traceback detalhado ---")
                        traceback.print_exc()
                        print("---------------------------\n")
            except Exception as e:
                print(f"Erro durante a análise do código: {e}")
                if debug:
                    traceback.print_exc()
                
        except FileNotFoundError:
            print(f"Erro: Arquivo '{args.file}' não encontrado.")
        except Exception as e:
            print(f"Erro: {e}")
    else:
        # Modo interativo
        print("NajaScript v0.1 - Modo Interativo (Digite 'sair()' para encerrar)")
        while True:
            try:
                line = input(">> ")
                if line.strip() == 'sair()':
                    break
                
                # Aplicar pré-processamento ao código fonte
                if hasattr(interpreter, 'preprocess_source'):
                    processed_line = interpreter.preprocess_source(line)
                    if debug and processed_line != line:
                        print(f"Processado: {processed_line}")
                    line = processed_line
                
                lexer = Lexer(line)
                parser = Parser(lexer)
                ast = parser.parse()
                result = interpreter.interpret(ast)
                
                if result is not None:
                    print(result)
            except KeyboardInterrupt:
                print("\nOperação interrompida")
                break
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == "__main__":
    main()
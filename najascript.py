#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os
import traceback
import time

try:
    from lexer import Lexer
    from parser_naja import Parser
    from interpreter import Interpreter, Environment
    from naja_bytecode import NajaBytecodeCompiler, BytecodeInterpreter
    from naja_llvm import NajaLLVMGenerator
    from ast_nodes import ImportStatement
    from llvmlite import binding as llvm
except Exception as e:
    print(f"Erro ao importar módulos: {e}")
    traceback.print_exc()
    sys.exit(1)

# Configure logging
import logging
logging.basicConfig(filename='najascript.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger('naja')

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
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description='NajaScript Interpreter')
    parser.add_argument('file', nargs='?', help='Script para executar')
    parser.add_argument('--module-path', action='append', help='Caminhos adicionais para buscar módulos')
    parser.add_argument('--pt', action='store_true', help='Habilitar suporte a português')
    parser.add_argument('--debug', action='store_true', help='Mostrar informações de depuração')
    args = parser.parse_args()

    # Criar o interpretador
    interpreter = Interpreter()
    interpreter.debug = args.debug  # Usar o argumento de linha de comando
    interpreter.logger = logger
    
    # Log de início
    logger.info("Iniciando interpretador NajaScript")
    
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
    
    # Executar o arquivo principal
    if args.file:
        try:
            # Carregar o código fonte
            with open(args.file, 'r', encoding='utf-8') as file:
                source = file.read()
            
            # Pré-processamento do código (suporte a português)
            source = interpreter.preprocess_source(source)

            # Iniciar o lexer e parser
            lexer = Lexer(source)
            parser = Parser(lexer)
            ast = parser.parse()
            
            # Executar o código
            interpreter.current_file = os.path.abspath(args.file)
            resultado = interpreter.interpret(ast)
            
            if resultado is not None:
                print(resultado)
            
        except Exception as e:
            print(f"Erro durante a interpretação: {str(e)}")
            if args.debug:
                import traceback
                traceback.print_exc()
    else:
        print("Nenhum arquivo fornecido para execução")
    
    # Exibir tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nTempo de execução: {execution_time:.5f} segundos")

if __name__ == "__main__":
    main()
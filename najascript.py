#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from lexer import Lexer
from parser_naja import Parser
from interpreter import Interpreter
from naja_bytecode import NajaBytecodeCompiler, BytecodeInterpreter
from naja_llvm import NajaLLVMGenerator
from llvmlite import binding as llvm

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
    parser = argparse.ArgumentParser(description='Interpretador NajaScript')
    parser.add_argument('arquivo', help='Arquivo fonte NajaScript')
    parser.add_argument('--interpret', action='store_true', help='Usar interpretador')
    parser.add_argument('--bytecode', action='store_true', help='Usar bytecode')
    parser.add_argument('--llvm', action='store_true', help='Usar LLVM')
    args = parser.parse_args()
    
    # Lê o arquivo fonte
    try:
        with open(args.arquivo, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        sys.exit(1)
        
    # Análise léxica e sintática
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    if args.interpret:
        # Modo interpretador
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    elif args.bytecode:
        # Modo bytecode
        compiler = NajaBytecodeCompiler()
        bytecode = compiler.compile(ast)
        interpreter = BytecodeInterpreter()
        # Configura o interpretador
        compiler.set_interpreter(interpreter)
        interpreter.execute(bytecode)
        
    elif args.llvm:
        # Modo LLVM
        # Primeiro compila para bytecode
        compiler = NajaBytecodeCompiler()
        bytecode = compiler.compile(ast)
        
        # Depois gera LLVM IR
        llvm_gen = NajaLLVMGenerator()
        module = llvm_gen.generate(bytecode)
        
        # Inicializa LLVM
        target_machine = initialize_llvm()
        
        # Compila e executa
        llvm_ir = str(module)
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()
        
        # Aplica otimizações
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 2
        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)
        pm.run(mod)
        
        # Executa o código
        engine = llvm.create_mcjit_compiler(mod, target_machine)
        engine.finalize_object()
        
        # Obtém e executa a função main
        func_ptr = engine.get_function_address("main")
        
        # Cria um wrapper Python para a função
        from ctypes import CFUNCTYPE, c_int
        cfunc = CFUNCTYPE(c_int)(func_ptr)
        
        # Executa
        result = cfunc()
        print(f"Resultado: {result}")
        
    else:
        # Modo padrão (interpretador)
        interpreter = Interpreter()
        interpreter.interpret(ast)

if __name__ == '__main__':
    main() 
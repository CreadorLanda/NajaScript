#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import traceback
from lexer import Lexer
from parser_naja import Parser
from interpreter import Interpreter

class NajaREPL:
    def __init__(self):
        self.interpreter = Interpreter()
        self.history = []
        self.current_line = 0
        self.buffer = ""
        self.in_multiline = False
        
    def print_welcome(self):
        print("NajaScript REPL v0.1")
        print("Digite 'sair()' para encerrar")
        print("Digite 'ajuda()' para ver os comandos disponíveis")
        print("Use '...' para continuar uma linha")
        print("Use '\\' para continuar uma linha")
        print()
        
    def print_help(self):
        print("\nComandos disponíveis:")
        print("  sair()      - Encerra o REPL")
        print("  ajuda()     - Mostra esta mensagem de ajuda")
        print("  limpar()    - Limpa a tela")
        print("  historico() - Mostra o histórico de comandos")
        print("  reset()     - Reseta o ambiente de execução")
        print()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_welcome()
        
    def show_history(self):
        if not self.history:
            print("Nenhum comando no histórico")
            return
            
        print("\nHistórico de comandos:")
        for i, cmd in enumerate(self.history, 1):
            print(f"{i}. {cmd}")
        print()
        
    def reset_environment(self):
        self.interpreter = Interpreter()
        print("Ambiente de execução resetado")
        
    def process_command(self, command):
        if command == 'sair()':
            return False
        elif command == 'ajuda()':
            self.print_help()
            return True
        elif command == 'limpar()':
            self.clear_screen()
            return True
        elif command == 'historico()':
            self.show_history()
            return True
        elif command == 'reset()':
            self.reset_environment()
            return True
            
        try:
            # Adiciona ao histórico se não for um comando especial
            if not command.startswith(('ajuda()', 'limpar()', 'historico()', 'reset()')):
                self.history.append(command)
                
            # Processa o comando
            lexer = Lexer(command)
            parser = Parser(lexer)
            ast = parser.parse()
            result = self.interpreter.interpret(ast)
            
            if result is not None:
                print(result)
                
        except Exception as e:
            print(f"Erro: {e}")
            if hasattr(self.interpreter, 'debug') and self.interpreter.debug:
                traceback.print_exc()
                
        return True
        
    def run(self):
        self.print_welcome()
        
        while True:
            try:
                # Lê a entrada do usuário
                if self.in_multiline:
                    prompt = "... "
                else:
                    prompt = ">> "
                    
                line = input(prompt)
                
                # Verifica se é uma continuação de linha
                if line.endswith('...') or line.endswith('\\'):
                    self.buffer += line[:-3] if line.endswith('...') else line[:-1]
                    self.in_multiline = True
                    continue
                    
                # Adiciona a linha atual ao buffer
                if self.in_multiline:
                    self.buffer += line
                else:
                    self.buffer = line
                    
                # Processa o comando
                if not self.process_command(self.buffer):
                    break
                    
                # Limpa o buffer e reseta o estado
                self.buffer = ""
                self.in_multiline = False
                
            except KeyboardInterrupt:
                print("\nOperação interrompida")
                self.buffer = ""
                self.in_multiline = False
                continue
            except EOFError:
                print("\nAté logo!")
                break
            except Exception as e:
                print(f"Erro: {e}")
                self.buffer = ""
                self.in_multiline = False

if __name__ == "__main__":
    repl = NajaREPL()
    repl.run() 
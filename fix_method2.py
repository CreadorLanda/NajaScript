#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Este script corrige o método execute_WhileStatement no arquivo interpreter.py

with open('interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define o método corrigido
method_fixed = '''    def execute_WhileStatement(self, stmt):
        """Executa uma declaração while"""
        result = None
        
        try:
            while self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    result = self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    continue
                except BreakException:
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise e
            
        return result'''

# Vamos localizar o método com um padrão mais específico
import re
pattern = r'def execute_WhileStatement\(self, stmt\):.*?return result'
flags = re.DOTALL  # Para fazer o ponto corresponder também a quebras de linha

# Substitui apenas o método problemático
if re.search(pattern, content, flags):
    new_content = re.sub(pattern, method_fixed, content, flags=flags)
    
    # Salva o arquivo modificado
    with open('interpreter.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Método execute_WhileStatement corrigido com sucesso!")
else:
    print("Método execute_WhileStatement não encontrado com o padrão esperado.") 
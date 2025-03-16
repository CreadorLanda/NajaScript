#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Método correto
correct_method = '''    def execute_WhileStatement(self, stmt):
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
            
        return result
'''

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra o início do método
start_line = -1
for i, line in enumerate(lines):
    if 'def execute_WhileStatement' in line:
        start_line = i
        break

if start_line == -1:
    print("Método não encontrado!")
    exit(1)

# Encontra o final do método
end_line = -1
for i in range(start_line + 1, len(lines)):
    if lines[i].startswith('    def '):
        end_line = i - 1
        break

# Se não encontrou o final, assume que é o último método do arquivo
if end_line == -1:
    end_line = len(lines) - 1
    print("Método é o último do arquivo, usando até o final.")

# Substitui o método
new_lines = lines[:start_line] + correct_method.splitlines(True) + lines[end_line+1:]

# Escreve o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Método corrigido! Linhas {start_line+1} até {end_line+1} foram substituídas.") 
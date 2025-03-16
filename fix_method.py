#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Este script corrige o método execute_WhileStatement no arquivo interpreter.py

with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Localiza o método execute_WhileStatement
start_line = 0
end_line = 0
for i, line in enumerate(lines):
    if 'def execute_WhileStatement' in line:
        start_line = i
        # Encontra o final do método (próxima definição de método ou fim do arquivo)
        for j in range(i+1, len(lines)):
            if 'def ' in lines[j] and not lines[j].startswith(' '):
                end_line = j - 1
                break
        if end_line == 0:  # Se não encontrou outro método, assume até o final do arquivo
            end_line = len(lines) - 1
        break

if start_line > 0:
    # Substitui o método com a versão corrigida
    method_fixed = [
        '    def execute_WhileStatement(self, stmt):\n',
        '        """Executa uma declaração while"""\n',
        '        result = None\n',
        '        \n',
        '        try:\n',
        '            while self.is_truthy(self.evaluate(stmt.condition)):\n',
        '                try:\n',
        '                    result = self.execute_block(stmt.body, Environment(self.environment))\n',
        '                except ContinueException:\n',
        '                    continue\n',
        '                except BreakException:\n',
        '                    break\n',
        '        except Exception as e:\n',
        '            if not isinstance(e, (BreakException, ContinueException, ReturnException)):\n',
        '                raise e\n',
        '            \n',
        '        return result\n',
        '    \n'
    ]
    
    # Substitui o método antigo pelo novo
    new_lines = lines[:start_line] + method_fixed + lines[end_line+1:]
    
    # Salva o arquivo modificado
    with open('interpreter.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Método corrigido! Linhas {start_line+1} até {end_line+1} foram substituídas.")
else:
    print("Método execute_WhileStatement não encontrado no arquivo.") 
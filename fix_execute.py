#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pelo método execute
for i in range(len(lines)):
    if 'def execute(self, statement):' in lines[i]:
        # Encontra o final do método
        start_line = i
        end_line = i
        for j in range(i+1, len(lines)):
            if lines[j].startswith('    def '):
                end_line = j
                break
        
        # Substitui o método execute
        execute_method = [
            '    def execute(self, statement):\n',
            '        """Executa uma declaração"""\n',
            '        try:\n',
            '            statement_type = statement.__class__.__name__\n',
            '            method_name = f"execute_{statement_type}"\n',
            '            \n',
            '            if hasattr(self, method_name):\n',
            '                return getattr(self, method_name)(statement)\n',
            '            else:\n',
            '                return self.execute_default(statement)\n',
            '        except (ReturnException, BreakException, ContinueException):\n',
            '            # Propaga exceções de controle de fluxo\n',
            '            raise\n',
            '        except Exception as e:\n',
            '            print(f"Erro durante a interpretação: {e}")\n',
            '    \n'
        ]
        
        # Substitui o método execute
        lines = lines[:start_line] + execute_method + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Método execute corrigido!") 
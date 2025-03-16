#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pelo método interpret
for i in range(len(lines)):
    if 'def interpret(self, ast):' in lines[i]:
        # Encontra o final do método
        end_line = i
        for j in range(i+1, len(lines)):
            if lines[j].startswith('    def '):
                end_line = j
                break
        
        # Adiciona o método evaluate após o método interpret
        evaluate_method = [
            '    def evaluate(self, expr):\n',
            '        """Avalia uma expressão e retorna seu valor"""\n',
            '        if expr is None:\n',
            '            return None\n',
            '        \n',
            '        expr_type = expr.__class__.__name__\n',
            '        method_name = f"evaluate_{expr_type}"\n',
            '        \n',
            '        if hasattr(self, method_name):\n',
            '            return getattr(self, method_name)(expr)\n',
            '        else:\n',
            '            raise Exception(f"Tipo de expressão não implementado: {expr_type}")\n',
            '    \n'
        ]
        
        # Insere o método evaluate
        lines = lines[:end_line] + evaluate_method + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Método evaluate adicionado!") 
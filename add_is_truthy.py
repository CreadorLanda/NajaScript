#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pelo método evaluate
for i in range(len(lines)):
    if 'def evaluate(self, expr):' in lines[i]:
        # Encontra o final do método
        end_line = i
        for j in range(i+1, len(lines)):
            if lines[j].startswith('    def '):
                end_line = j
                break
        
        # Adiciona o método is_truthy após o método evaluate
        is_truthy_method = [
            '    def is_truthy(self, value):\n',
            '        """Verifica se um valor é considerado verdadeiro"""\n',
            '        if value is None:\n',
            '            return False\n',
            '        if isinstance(value, bool):\n',
            '            return value\n',
            '        if isinstance(value, (int, float)):\n',
            '            return value != 0\n',
            '        if isinstance(value, str):\n',
            '            return len(value) > 0\n',
            '        if hasattr(value, "length") and callable(value.length):\n',
            '            return value.length() > 0\n',
            '        if hasattr(value, "isEmpty") and callable(value.isEmpty):\n',
            '            return not value.isEmpty()\n',
            '        # Por padrão, qualquer objeto é considerado verdadeiro\n',
            '        return True\n',
            '    \n'
        ]
        
        # Insere o método is_truthy
        lines = lines[:end_line] + is_truthy_method + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Método is_truthy adicionado!") 
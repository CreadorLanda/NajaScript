#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pelo método is_truthy
for i in range(len(lines)):
    if 'def is_truthy(self, value):' in lines[i]:
        # Encontra o final do método
        end_line = i
        for j in range(i+1, len(lines)):
            if lines[j].startswith('    def '):
                end_line = j
                break
        
        # Adiciona o método execute_block após o método is_truthy
        execute_block_method = [
            '    def execute_block(self, statements, environment):\n',
            '        """Executa um bloco de código em um ambiente específico"""\n',
            '        previous_env = self.environment\n',
            '        self.environment = environment\n',
            '        \n',
            '        try:\n',
            '            for statement in statements:\n',
            '                self.execute(statement)\n',
            '        finally:\n',
            '            self.environment = previous_env\n',
            '        \n',
            '        return None\n',
            '    \n'
        ]
        
        # Insere o método execute_block
        lines = lines[:end_line] + execute_block_method + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Método execute_block adicionado!") 
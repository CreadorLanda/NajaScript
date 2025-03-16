#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pela chamada ao método _register_native_functions
for i in range(len(lines)):
    if '_register_native_functions()' in lines[i]:
        # Comenta a linha
        lines[i] = lines[i].replace('self._register_native_functions()', '# self._register_native_functions()')
        break

# Escreve o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Chamada para _register_native_functions removida!") 
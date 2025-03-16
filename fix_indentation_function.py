#!/usr/bin/env python3

# Script para corrigir a indentação da função evaluate_FunctionCall no arquivo interpreter.py

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procura pela definição da função
start_line = -1
for i, line in enumerate(lines):
    if 'def evaluate_FunctionCall' in line:
        start_line = i
        break

if start_line != -1:
    # Verifica a indentação da linha de definição
    current_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
    
    # Corrige a indentação da linha de definição
    if current_indent != 4:
        print(f"Corrigindo indentação na linha {start_line+1} (indentação atual: {current_indent})")
        lines[start_line] = "    def evaluate_FunctionCall(self, expr):\n"
    
    # Corrige a indentação das linhas seguintes
    for i in range(start_line + 1, len(lines)):
        # Se encontrar a próxima definição de função/método, pare
        if 'def ' in lines[i] and not lines[i].startswith(' '):
            break
            
        # Verifica se a linha não está em branco
        if lines[i].strip():
            indent = len(lines[i]) - len(lines[i].lstrip())
            if indent < 8:  # deveria ter pelo menos 8 espaços (4 + 4)
                print(f"Corrigindo indentação na linha {i+1} (indentação atual: {indent})")
                lines[i] = "        " + lines[i].lstrip()
        
# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("A indentação da função evaluate_FunctionCall foi corrigida com sucesso!") 
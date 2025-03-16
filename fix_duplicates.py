#!/usr/bin/env python3

# Script para corrigir problemas de sintaxe no arquivo interpreter.py

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Verifica por else duplicados
previous_line_was_else = False
to_remove = []

for i, line in enumerate(lines):
    line_stripped = line.strip()
    
    # Verifica se é um else
    if line_stripped == "else:":
        if previous_line_was_else:
            # Este é um else duplicado
            print(f"Encontrado else duplicado na linha {i+1}")
            to_remove.append(i)
        else:
            previous_line_was_else = True
    else:
        previous_line_was_else = False

# Remove as linhas marcadas para remoção (de trás para frente para não afetar os índices)
for i in sorted(to_remove, reverse=True):
    print(f"Removendo linha {i+1}: {lines[i].strip()}")
    del lines[i]

# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.writelines(lines)

print(f"Arquivo atualizado com sucesso. Removidas {len(to_remove)} linhas.")

# Agora verifica por definições de função duplicadas
with open('interpreter.py', 'r', encoding='utf-8') as file:
    content = file.read()

import re
func_defs = re.findall(r'def (\w+)\(', content)
duplicates = set([func for func in func_defs if func_defs.count(func) > 1])

if duplicates:
    print(f"\nFunções duplicadas encontradas: {duplicates}")
    
    # Para cada função duplicada, procura a primeira e última ocorrência
    for func in duplicates:
        pattern = rf'def {func}\('
        matches = list(re.finditer(pattern, content))
        if len(matches) >= 2:
            first_match = matches[0]
            last_match = matches[-1]
            
            first_line = content[:first_match.start()].count('\n') + 1
            last_line = content[:last_match.start()].count('\n') + 1
            
            print(f"Função '{func}' encontrada nas linhas {first_line} e {last_line}")
else:
    print("\nNenhuma função duplicada encontrada.") 
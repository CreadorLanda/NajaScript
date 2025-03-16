#!/usr/bin/env python3

# Script para corrigir erros de sintaxe no arquivo interpreter.py

with open('interpreter.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procura por erros específicos
for i in range(len(lines)):
    # Corrige o problema do raise ... e
    if "raise RuntimeError" in lines[i] and lines[i].strip().endswith("e"):
        print(f"Corrigindo erro na linha {i+1}: {lines[i].strip()}")
        lines[i] = lines[i].replace(" e\n", "\n")
    
    # Procura por else duplicados
    if i > 0 and lines[i].strip() == "else:" and lines[i-1].strip() == "else:":
        print(f"Removendo else duplicado na linha {i+1}")
        lines[i] = ""

    # Procura por raise duplicados
    if i > 0 and i < len(lines) - 1:
        if ("raise RuntimeError" in lines[i] and 
            "raise RuntimeError" in lines[i+1] and
            "Não é possível chamar" in lines[i] and
            "Não é possível chamar" in lines[i+1]):
            print(f"Removendo raise duplicado nas linhas {i+1}-{i+2}")
            lines[i] = ""

# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("Arquivo interpreter.py atualizado com sucesso!") 
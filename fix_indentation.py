#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script para mostrar e analisar o conteúdo do método execute_DoWhileStatement no arquivo interpreter.py

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Corrige a indentação do método execute_WhileStatement
for i in range(len(lines)):
    if 'def execute_WhileStatement' in lines[i]:
        # Verifica se a indentação está incorreta
        if not lines[i].startswith('    def'):
            # Corrige a indentação
            lines[i] = '    ' + lines[i].lstrip()
            # Corrige também as próximas linhas se necessário
            for j in range(i+1, min(i+20, len(lines))):
                if lines[j].startswith('        '):
                    # Já está indentado corretamente
                    break
                elif lines[j].strip() and not lines[j].startswith('    def'):
                    # Adiciona a indentação correta
                    lines[j] = '        ' + lines[j].lstrip()
        break

# Escreve o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Indentação do método execute_WhileStatement corrigida!")

# Procurar pela definição do método execute_DoWhileStatement
start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if 'def execute_DoWhileStatement' in line:
        start_line = i
        break

if start_line != -1:
    # Encontrou o início do método, agora procura o final
    indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
    
    # Procura pela próxima linha com a mesma indentação que indica o próximo método
    for i in range(start_line + 1, len(lines)):
        if lines[i].strip() and len(lines[i]) - len(lines[i].lstrip()) <= indent_level:
            if 'def ' in lines[i]:
                end_line = i - 1
                break
    
    # Se não encontrou o próximo método, considera até o final do arquivo
    if end_line == -1:
        end_line = len(lines) - 1
    
    # Exibe o conteúdo do método
    print(f"Método execute_DoWhileStatement (linhas {start_line+1} a {end_line+1}):")
    for i in range(start_line, end_line + 1):
        print(f"{i+1:4d}: {lines[i].rstrip()}")
        
    # Analisando a estrutura try/except
    print("\nProcurando por problemas de indentação no try/except...")
    in_try_block = False
    in_while_block = False
    in_nested_try = False
    
    for i in range(start_line, end_line + 1):
        line = lines[i].rstrip()
        indent = len(lines[i]) - len(lines[i].lstrip())
        
        if "try:" in line:
            if in_try_block:
                in_nested_try = True
                print(f"{i+1:4d}: Início de try aninhado (indent={indent})")
            else:
                in_try_block = True
                print(f"{i+1:4d}: Início de try principal (indent={indent})")
                
        elif "while " in line and in_try_block:
            in_while_block = True
            print(f"{i+1:4d}: Início de while dentro do try (indent={indent})")
            
        elif "except " in line:
            if in_nested_try:
                if indent == 16:  # Deve ser 20 para estar dentro do while
                    print(f"{i+1:4d}: *** ERRO DE INDENTAÇÃO *** except no nível errado (indent={indent}, deveria ser 20)")
                    # Corrige a indentação
                    lines[i] = "                    " + lines[i].lstrip()
                    print(f"      Corrigido para: {lines[i].rstrip()}")
                else:
                    print(f"{i+1:4d}: except dentro do try aninhado (indent={indent})")
            else:
                print(f"{i+1:4d}: except no try principal (indent={indent})")
                
    # Se encontrou e corrigiu algum problema, salva o arquivo
    print("\nSalvando alterações...")
    with open('interpreter.py', 'w', encoding='utf-8') as file:
        file.writelines(lines)
    print("Arquivo interpreter.py atualizado.")
    
else:
    print("Método execute_DoWhileStatement não encontrado no arquivo.") 
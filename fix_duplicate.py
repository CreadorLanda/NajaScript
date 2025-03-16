#!/usr/bin/env python3

# Script para remover blocos finally duplicados no arquivo interpreter.py

with open('interpreter.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procura por padrões de finally duplicados
i = 0
while i < len(lines) - 10:  # evita indexação fora dos limites
    current_line = lines[i].strip()
    if current_line == "finally:":
        # Verifica se há um segundo finally após um return e antes do próximo def
        for j in range(i+1, len(lines)):
            if "return result" in lines[j]:
                # Encontrou um return, procura por finally duplicado após ele
                for k in range(j+1, len(lines)):
                    if lines[k].strip() == "finally:":
                        # Duplicata encontrada, remove o segundo bloco finally e tudo até o próximo return
                        start_remove = k
                        end_remove = k
                        for m in range(k+1, len(lines)):
                            if "return result" in lines[m]:
                                end_remove = m
                                break
                        
                        print(f"Removendo bloco finally duplicado (linhas {start_remove+1}-{end_remove+1})")
                        lines = lines[:start_remove] + lines[end_remove+1:]
                        break
                break
    i += 1

# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.writelines(lines)

print("Arquivo interpreter.py atualizado com sucesso!") 
#!/usr/bin/env python3

# Script para escrever corretamente a função evaluate_FunctionCall em interpreter.py

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procura pelo início e fim da função
start_line = -1
end_line = -1
for i, line in enumerate(lines):
    if 'def evaluate_FunctionCall' in line:
        start_line = i
        break

if start_line != -1:
    # Procura pelo próximo 'def' que indica a próxima função
    for i in range(start_line + 1, len(lines)):
        if line.strip().startswith('def '):
            end_line = i - 1
            break
    
    # Se não encontrou o próximo def, considera até o final do arquivo
    if end_line == -1:
        end_line = len(lines) - 1
    
    # Define a nova implementação da função
    new_function = [
        "    def evaluate_FunctionCall(self, expr):\n",
        "        \"\"\"Avalia uma chamada de função\"\"\"\n",
        "        # Obtém a função\n",
        "        callee = self.environment.get(expr.name)\n",
        "        \n",
        "        # Avalia os argumentos\n",
        "        arguments = []\n",
        "        for arg in expr.arguments:\n",
        "            arguments.append(self.evaluate(arg))\n",
        "        \n",
        "        # Verifica se é uma função nativa (Python) ou uma função NajaScript\n",
        "        if callable(callee):\n",
        "            try:\n",
        "                # Tenta chamar a função com os argumentos\n",
        "                return callee(*arguments)\n",
        "            except TypeError as e:\n",
        "                # Se houver erro de tipo, pode ser uma função que espera um interpretador\n",
        "                if isinstance(callee, Function):\n",
        "                    return callee(self, arguments)\n",
        "                else:\n",
        "                    raise e\n",
        "        else:\n",
        "            raise RuntimeError(f\"Não é possível chamar '{expr.name}' como função\")\n",
        "    \n"
    ]
    
    # Substitui a função antiga pela nova
    lines[start_line:end_line+1] = new_function
    
    # Salva o arquivo atualizado
    with open('interpreter.py', 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    print(f"Função evaluate_FunctionCall reescrita com sucesso (linhas {start_line+1}-{start_line+len(new_function)})")
else:
    print("Função evaluate_FunctionCall não encontrada no arquivo.") 
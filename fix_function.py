#!/usr/bin/env python3

# Definição correta da função evaluate_FunctionCall
correct_function = """    def evaluate_FunctionCall(self, expr):
        \"\"\"Avalia uma chamada de função\"\"\"
        # Obtém a função
        callee = self.environment.get(expr.name)
        
        # Avalia os argumentos
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        
        # Verifica se é uma função nativa (Python) ou uma função NajaScript
        if callable(callee):
            try:
                # Tenta chamar a função com os argumentos
                return callee(*arguments)
            except TypeError as e:
                # Se houver erro de tipo, pode ser uma função que espera um interpretador
                if isinstance(callee, Function):
                    return callee(self, arguments)
                else:
                    raise e
        else:
            raise RuntimeError(f"Não é possível chamar '{expr.name}' como função")"""

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as file:
    content = file.read()

# Tenta encontrar a função atual e substituí-la pela correta
import re
pattern = r'def evaluate_FunctionCall.*?como função"\)'
new_content = re.sub(pattern, correct_function, content, flags=re.DOTALL)

# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.write(new_content)

print("A função evaluate_FunctionCall foi substituída com sucesso!") 
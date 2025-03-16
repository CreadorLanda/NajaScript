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
        
        # Adiciona métodos para avaliar expressões básicas
        evaluate_methods = [
            '    def evaluate_Variable(self, expr):\n',
            '        """Avalia uma variável"""\n',
            '        return self.environment.get(expr.name)\n',
            '    \n',
            '    def evaluate_StringLiteral(self, expr):\n',
            '        """Avalia um literal de string"""\n',
            '        return expr.value\n',
            '    \n',
            '    def evaluate_IntegerLiteral(self, expr):\n',
            '        """Avalia um literal inteiro"""\n',
            '        return expr.value\n',
            '    \n',
            '    def evaluate_FloatLiteral(self, expr):\n',
            '        """Avalia um literal de ponto flutuante"""\n',
            '        return expr.value\n',
            '    \n',
            '    def evaluate_BooleanLiteral(self, expr):\n',
            '        """Avalia um literal booleano"""\n',
            '        return expr.value\n',
            '    \n',
            '    def evaluate_NullLiteral(self, expr):\n',
            '        """Avalia um literal nulo"""\n',
            '        return None\n',
            '    \n',
            '    def evaluate_BinaryOperation(self, expr):\n',
            '        """Avalia uma operação binária"""\n',
            '        left = self.evaluate(expr.left)\n',
            '        right = self.evaluate(expr.right)\n',
            '        \n',
            '        if expr.operator == "+":\n',
            '            # Concatenação de strings\n',
            '            if isinstance(left, str) or isinstance(right, str):\n',
            '                return str(left) + str(right)\n',
            '            # Soma numérica\n',
            '            return left + right\n',
            '        elif expr.operator == "-":\n',
            '            return left - right\n',
            '        elif expr.operator == "*":\n',
            '            return left * right\n',
            '        elif expr.operator == "/":\n',
            '            return left / right\n',
            '        elif expr.operator == "%":\n',
            '            return left % right\n',
            '        elif expr.operator == "**":\n',
            '            return left ** right\n',
            '        elif expr.operator == "==":\n',
            '            return left == right\n',
            '        elif expr.operator == "!=":\n',
            '            return left != right\n',
            '        elif expr.operator == "<":\n',
            '            return left < right\n',
            '        elif expr.operator == ">":\n',
            '            return left > right\n',
            '        elif expr.operator == "<=":\n',
            '            return left <= right\n',
            '        elif expr.operator == ">=":\n',
            '            return left >= right\n',
            '        elif expr.operator == "&&" or expr.operator == "and":\n',
            '            return self.is_truthy(left) and self.is_truthy(right)\n',
            '        elif expr.operator == "||" or expr.operator == "or":\n',
            '            return self.is_truthy(left) or self.is_truthy(right)\n',
            '        else:\n',
            '            raise Exception(f"Operador não implementado: {expr.operator}")\n',
            '    \n',
            '    def evaluate_UnaryOperation(self, expr):\n',
            '        """Avalia uma operação unária"""\n',
            '        operand = self.evaluate(expr.operand)\n',
            '        \n',
            '        if expr.operator == "-":\n',
            '            return -operand\n',
            '        elif expr.operator == "!" or expr.operator == "not":\n',
            '            return not self.is_truthy(operand)\n',
            '        else:\n',
            '            raise Exception(f"Operador unário não implementado: {expr.operator}")\n',
            '    \n',
            '    def evaluate_FunctionCall(self, expr):\n',
            '        """Avalia uma chamada de função"""\n',
            '        # Avalia a função (pode ser um nome ou uma expressão)\n',
            '        callee = None\n',
            '        if isinstance(expr.name, str):\n',
            '            # Função referenciada por nome\n',
            '            callee = self.environment.get(expr.name)\n',
            '        else:\n',
            '            # Função referenciada por expressão\n',
            '            callee = self.evaluate(expr.name)\n',
            '        \n',
            '        # Avalia os argumentos\n',
            '        arguments = []\n',
            '        for arg in expr.arguments:\n',
            '            arguments.append(self.evaluate(arg))\n',
            '        \n',
            '        # Verifica se é uma função chamável\n',
            '        if callable(callee):\n',
            '            # Função nativa do Python\n',
            '            return callee(*arguments)\n',
            '        elif hasattr(callee, "__call__"):\n',
            '            # Função definida em NajaScript\n',
            '            return callee(self, arguments)\n',
            '        else:\n',
            '            raise Exception(f"{expr.name} não é uma função")\n',
            '    \n'
        ]
        
        # Insere os métodos para avaliar expressões
        lines = lines[:end_line] + evaluate_methods + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Métodos para avaliar expressões adicionados!") 
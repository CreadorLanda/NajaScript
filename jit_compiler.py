#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast as py_ast
import inspect
from numba import jit, njit
import numpy as np
from ast_nodes import *

class JITCompiler:
    """
    Compilador JIT para NajaScript usando Numba
    """
    def __init__(self):
        self.compiled_functions = {}
        self.cached_code = {}
        
    def compile_function(self, ast_function, environment):
        """
        Compila uma função AST para código Python otimizado com JIT
        """
        # Obtém o nome da função
        function_name = ast_function.name
        
        print(f"JIT: Tentando compilar função: {function_name}")
        
        # Verifica se já está no cache
        if function_name in self.compiled_functions:
            print(f"JIT: Função {function_name} já está compilada, usando versão em cache")
            return self.compiled_functions[function_name]
        
        # Converte a AST do NajaScript para código Python
        py_code = self._convert_to_python(ast_function)
        
        try:
            # Compila o código Python
            print(f"JIT: Compilando função {function_name} com Numba")
            compiled_func = self._compile_with_numba(py_code, function_name)
            
            # Armazena no cache
            self.compiled_functions[function_name] = compiled_func
            print(f"JIT: Função {function_name} compilada com sucesso")
            
            return compiled_func
        except Exception as e:
            print(f"JIT: Erro ao compilar função {function_name}: {str(e)}")
            return None
    
    def _convert_to_python(self, ast_function):
        """
        Converte uma função AST NajaScript para código Python
        """
        # Extrai parâmetros
        params = []
        
        for param in ast_function.parameters:
            if isinstance(param, tuple) and len(param) == 2:
                # Formato (tipo, nome)
                param_name = param[1]
                params.append(param_name)
            elif hasattr(param, 'name'):
                # Objeto com atributo name
                param_name = param.name
                params.append(param_name)
            else:
                raise ValueError(f"Formato de parâmetro não suportado: {param}")
        
        # Inicializa o gerador de código Python
        code_generator = PythonCodeGenerator()
        
        # Gera o código da função
        if isinstance(ast_function.body, list):
            # Se o corpo da função for uma lista de declarações, use _generate_block
            function_body = code_generator._generate_block(ast_function.body)
        else:
            # Caso contrário, use o método generate padrão
            function_body = code_generator.generate(ast_function.body)
        
        # Se o corpo da função estiver vazio, adicione um pass
        if not function_body.strip():
            function_body = "    pass"
        
        # Certifique-se de que o corpo da função está indentado corretamente
        # Divida o corpo em linhas e adicione a indentação adequada
        indented_body = []
        for line in function_body.split('\n'):
            if line.strip():  # Se a linha não está vazia
                # Certifique-se de que a linha começa com pelo menos 4 espaços
                if not line.startswith('    '):
                    line = '    ' + line
                indented_body.append(line)
            else:
                indented_body.append(line)  # Mantém linhas vazias
        
        # Juntar as linhas novamente
        processed_body = '\n'.join(indented_body)
        
        # Cria o código da função Python com indentação correta
        py_code = f"""def {ast_function.name}({', '.join(params)}):
{processed_body}
"""
        
        # Armazena o código fonte para uso posterior
        self.cached_code[ast_function.name] = py_code
        # Gera o código Python
        py_code = self._generate_python_code(ast_function, environment)
        
        # Compila o código Python
        try:
            # Comentado para remover debug
            # print(f"Código Python gerado:\n{py_code}")  # Debugging
            
            # Compila o código Python para uma função
            compiled_code = compile(py_code, f"<{ast_function.name}>", "exec")
            
            # Cria o namespace para a função
            namespace = {}
            
            # Executa o código compilado no namespace criado
            exec(compiled_code, namespace)
            
            # Retorna a função compilada
            return namespace[ast_function.name]
        except Exception as e:
            print(f"Erro ao compilar função {ast_function.name}: {e}")
            raise
    
    def _compile_with_numba(self, py_code, function_name):
        """
        Compila o código Python usando Numba JIT
        """
        # Compila o código
        global_vars = globals()
        local_vars = {}
        
        # Primeiro, execute o código para definir a função no escopo
        exec(py_code, global_vars, local_vars)
        
        # Adicione a função ao escopo global para permitir recursão
        global_vars[function_name] = local_vars[function_name]
        
        # Reexecute para garantir que a função recursiva possa se encontrar
        exec(py_code, global_vars, local_vars)
        
        # Obtém a função compilada
        func = local_vars[function_name]
        
        # Aplica o decorador JIT da Numba para otimização
        jitted_func = njit(func)
        
        return jitted_func
    
    def is_optimizable(self, ast_node):
        """
        Verifica se um nó AST pode ser otimizado pelo JIT
        """
        # Por enquanto, apenas funções com operações numéricas são otimizáveis
        if isinstance(ast_node, FunctionDeclaration):
            # Verifica se só tem operações numéricas
            return self._contains_only_numeric_ops(ast_node.body)
        
        return False
    
    def _contains_only_numeric_ops(self, statements):
        """
        Verifica se um bloco de código contém apenas operações numéricas
        """
        # Implementação simplificada - deve ser expandida
        for stmt in statements:
            if not self._is_numeric_operation(stmt):
                return False
                
        return True
    
    def _is_numeric_operation(self, statement):
        """
        Verifica se uma declaração envolve apenas operações numéricas
        """
        # Implementação simplificada - deve ser expandida
        if isinstance(statement, ExpressionStatement):
            expr = statement.expression
            return self._is_numeric_expression(expr)
        elif isinstance(statement, ReturnStatement):
            return self._is_numeric_expression(statement.value)
        
        # Por padrão, assume não numérico
        return False
    
    def _is_numeric_expression(self, expression):
        """
        Verifica se uma expressão é numérica
        """
        if isinstance(expression, BinaryOperation):
            return self._is_numeric_expression(expression.left) and self._is_numeric_expression(expression.right)
        elif isinstance(expression, UnaryOperation):
            return self._is_numeric_expression(expression.operand)
        elif isinstance(expression, IntegerLiteral) or isinstance(expression, FloatLiteral):
            return True
        
        # Por padrão, assume não numérico
        return False


class PythonCodeGenerator:
    """
    Gerador de código Python a partir de AST NajaScript
    """
    def __init__(self):
        self.indent_level = 0
        
    def generate(self, ast_node):
        """
        Gera código Python a partir de nós AST
        """
        method_name = f"_generate_{ast_node.__class__.__name__.lower()}"
        generator = getattr(self, method_name, self._generate_default)
        return generator(ast_node)
    
    def _generate_default(self, node):
        """
        Gerador padrão para nós não implementados
        """
        return f"# Não implementado: {node.__class__.__name__}"
    
    def _generate_block(self, statements):
        """
        Gera código para um bloco de declarações
        """
        self.indent_level += 1
        code = []
        
        for stmt in statements:
            stmt_code = self.generate(stmt)
            code.append(self._indent(stmt_code))
        
        self.indent_level -= 1
        
        if not code:
            return self._indent("pass")
            
        return "\n".join(code)
    
    def _indent(self, code):
        """
        Aplica indentação ao código
        """
        return "    " * self.indent_level + code
    
    # Implementações específicas para cada tipo de nó
    
    def _generate_expressionstatement(self, stmt):
        return self.generate(stmt.expression)
    
    def _generate_returnstatement(self, stmt):
        if stmt.value:
            return f"return {self.generate(stmt.value)}"
        else:
            return "return None"
    
    def _generate_binaryoperation(self, expr):
        left = self.generate(expr.left)
        right = self.generate(expr.right)
        
        # Mapeamento de operadores NajaScript para Python
        op_map = {
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "%": "%",
            "**": "**",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "&&": "and",
            "||": "or"
        }
        
        op = op_map.get(expr.operator, expr.operator)
        
        return f"({left} {op} {right})"
    
    def _generate_unaryoperation(self, expr):
        operand = self.generate(expr.operand)
        
        # Mapeamento de operadores unários
        op_map = {
            "-": "-",
            "!": "not "
        }
        
        op = op_map.get(expr.operator, expr.operator)
        
        return f"{op}({operand})"
    
    def _generate_integerliteral(self, expr):
        return str(expr.value)
    
    def _generate_floatliteral(self, expr):
        return str(expr.value)
    
    def _generate_variable(self, expr):
        return expr.name
    
    def _generate_ifstatement(self, stmt):
        condition = self.generate(stmt.condition)
        then_branch = self._generate_block(stmt.then_branch)
        
        code = f"if {condition}:\n{then_branch}"
        
        if stmt.else_branch:
            else_branch = self._generate_block(stmt.else_branch)
            code += f"\nelse:\n{else_branch}"
        
        return code
    
    def _generate_functioncall(self, expr):
        func_name = expr.name if isinstance(expr.name, str) else self.generate(expr.name)
        args = []
        
        if expr.arguments:
            for arg in expr.arguments:
                args.append(self.generate(arg))
        
        return f"{func_name}({', '.join(args)})" 
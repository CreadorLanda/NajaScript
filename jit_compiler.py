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
        
        # Verifica se já está no cache
        if function_name in self.compiled_functions:
            return self.compiled_functions[function_name]
        
        # Converte a AST do NajaScript para código Python
        py_code = self._convert_to_python(ast_function)
        
        # Compila o código Python
        compiled_func = self._compile_with_numba(py_code, function_name)
        
        # Armazena no cache
        self.compiled_functions[function_name] = compiled_func
        
        return compiled_func
    
    def _convert_to_python(self, ast_function):
        """
        Converte uma função AST NajaScript para código Python
        """
        # Extrai parâmetros
        params = [param.name for param in ast_function.parameters]
        
        # Inicializa o gerador de código Python
        code_generator = PythonCodeGenerator()
        
        # Gera o código da função
        function_body = code_generator.generate(ast_function.body)
        
        # Cria o código da função Python
        py_code = f"""
def {ast_function.name}({', '.join(params)}):
    {function_body}
        """
        
        # Armazena o código fonte para uso posterior
        self.cached_code[ast_function.name] = py_code
        
        return py_code
    
    def _compile_with_numba(self, py_code, function_name):
        """
        Compila o código Python usando Numba JIT
        """
        # Compila o código
        local_vars = {}
        exec(py_code, globals(), local_vars)
        
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
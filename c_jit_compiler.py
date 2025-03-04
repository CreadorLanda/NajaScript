#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess
import ctypes
from ast_nodes import *

class CCodeGenerator:
    """
    Gerador de código C a partir de AST NajaScript
    """
    def __init__(self):
        self.indent_level = 0
        self.include_stdio = False
        
    def indent(self):
        """Incrementa o nível de indentação"""
        self.indent_level += 1
        
    def dedent(self):
        """Decrementa o nível de indentação"""
        if self.indent_level > 0:
            self.indent_level -= 1
            
    def get_indent(self):
        """Retorna a indentação atual"""
        return "    " * self.indent_level
        
    def generate(self, node):
        """
        Gera código C a partir de um nó AST, chamando o gerador apropriado com base no tipo do nó
        """
        method_name = f"_generate_{node.__class__.__name__.lower()}"
        generator = getattr(self, method_name, None)
        
        if generator:
            return generator(node)
        else:
            return f"/* Não implementado: {node.__class__.__name__} */"
            
    def _generate_functiondeclaration(self, node):
        """Gera código C para declaração de função"""
        self.include_stdio = True  # Adicionamos stdio.h para funções com print
        
        return_type = "int"  # Tipo padrão, poderia ser inferido da análise
        
        params = []
        for param in node.parameters:
            # Verifica se o parâmetro é uma tupla (tipo, nome)
            if isinstance(param, tuple) and len(param) == 2:
                param_type, param_name = param
                # Mapeia tipos NajaScript para tipos C
                type_map = {
                    "int": "int",
                    "float": "double",
                    "string": "char*",
                    "bool": "int"
                }
                c_type = type_map.get(param_type, "int")
                params.append(f"{c_type} {param_name}")
            else:
                # Se não for tupla, assume que é um nome e usa int como padrão
                params.append(f"int {param}")
            
        params_str = ", ".join(params) if params else "void"
        
        func_header = f"{return_type} {node.name}({params_str}) {{\n"
        
        self.indent()
        body = []
        for stmt in node.body:
            body.append(f"{self.get_indent()}{self.generate(stmt)}")
        self.dedent()
        
        func_body = "\n".join(body)
        func_footer = "\n}"
        
        return func_header + func_body + func_footer
        
    def _generate_returnstatement(self, node):
        """Gera código C para instrução return"""
        if node.value:
            return f"return {self.generate(node.value)};"
        else:
            return "return 0;"
            
    def _generate_binaryoperation(self, node):
        """Gera código C para operações binárias"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        
        # Mapear operadores para C
        op_map = {
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "%": "%",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "&&": "&&",
            "||": "||"
        }
        
        op = op_map.get(node.operator, node.operator)
        
        return f"({left} {op} {right})"
        
    def _generate_unaryoperation(self, node):
        """Gera código C para operações unárias"""
        operand = self.generate(node.operand)
        
        # Mapear operadores unários
        op_map = {
            "-": "-",
            "!": "!",
            "+": "+"
        }
        
        op = op_map.get(node.operator, node.operator)
        
        return f"{op}({operand})"
        
    def _generate_integerliteral(self, node):
        """Gera código C para literais inteiros"""
        return str(node.value)
        
    def _generate_floatliteral(self, node):
        """Gera código C para literais float"""
        return str(node.value)
        
    def _generate_stringliteral(self, node):
        """Gera código C para literais string"""
        # Escapa as aspas
        escaped_value = node.value.replace('"', '\\"')
        return f'"{escaped_value}"'
        
    def _generate_identifier(self, node):
        """Gera código C para identificadores"""
        return node.name
        
    def _generate_blockstatement(self, node):
        """Gera código C para blocos de código"""
        self.indent()
        lines = []
        for stmt in node.statements:
            lines.append(f"{self.get_indent()}{self.generate(stmt)}")
        self.dedent()
        
        return "{\n" + "\n".join(lines) + f"\n{self.get_indent()}}}"
        
    def _generate_expressionstatement(self, node):
        """Gera código C para expressões como statements"""
        return f"{self.generate(node.expression)};"
        
    def _generate_ifstatement(self, node):
        """Gera código C para estrutura if-else"""
        condition = self.generate(node.condition)
        
        if_part = f"if ({condition}) {{\n"
        self.indent()
        
        # Processando o then_branch
        if isinstance(node.then_branch, list):
            then_code = []
            for stmt in node.then_branch:
                then_code.append(f"{self.get_indent()}{self.generate(stmt)}")
            if_body = "\n".join(then_code)
        else:
            if_body = f"{self.get_indent()}{self.generate(node.then_branch)}"
        
        self.dedent()
        if_part += if_body + f"\n{self.get_indent()}}}"
        
        # Processando a alternativa (parte else), se houver
        if node.else_branch:
            else_part = f" else {{\n"
            self.indent()
            
            if isinstance(node.else_branch, list):
                else_code = []
                for stmt in node.else_branch:
                    else_code.append(f"{self.get_indent()}{self.generate(stmt)}")
                else_body = "\n".join(else_code)
            else:
                else_body = f"{self.get_indent()}{self.generate(node.else_branch)}"
                
            self.dedent()
            else_part += else_body + f"\n{self.get_indent()}}}"
            
            return if_part + else_part
        
        return if_part
        
    def _generate_whilestatement(self, node):
        """Gera código C para estrutura while"""
        condition = self.generate(node.condition)
        
        while_header = f"while ({condition}) {{\n"
        self.indent()
        
        if isinstance(node.body, list):
            body_code = []
            for stmt in node.body:
                body_code.append(f"{self.get_indent()}{self.generate(stmt)}")
            body = "\n".join(body_code)
        else:
            body = f"{self.get_indent()}{self.generate(node.body)}"
            
        self.dedent()
        while_footer = f"\n{self.get_indent()}}}"
        
        return while_header + body + while_footer
        
    def _generate_functioncall(self, node):
        """Gera código C para chamadas de função"""
        args = []
        for arg in node.arguments:
            args.append(self.generate(arg))
        
        args_str = ", ".join(args)
        
        return f"{node.name}({args_str})"
        
    def generate_complete_c_file(self, ast_function):
        """Gera um arquivo C completo a partir de uma função AST"""
        includes = '#include <stdio.h>\n#include <stdlib.h>\n\n' if self.include_stdio else ''
        
        function_code = self.generate(ast_function)
        
        # Adiciona função main para testes, se necessário
        # main_code = 'int main() {\n    printf("%d\\n", fibonacci(10));\n    return 0;\n}\n'
        
        return includes + function_code # + main_code

class CJITCompiler:
    """
    Compilador JIT para NajaScript que gera e compila código C
    """
    def __init__(self):
        self.compiled_functions = {}  # Cache de funções compiladas
        self.temp_dir = tempfile.mkdtemp(prefix="najascript_c_jit_")
        print(f"CJITCompiler: Diretório temporário criado em {self.temp_dir}")
    
    def is_optimizable(self, ast_node):
        """
        Verifica se um nó AST pode ser otimizado pelo JIT
        """
        # Para a versão C, podemos suportar mais tipos de operações
        if isinstance(ast_node, FunctionDeclaration):
            # Consideramos praticamente todas as funções otimizáveis
            return True
        
        return False
    
    def _contains_only_numeric_ops(self, statements):
        """
        Verifica se um bloco de código contém apenas operações numéricas
        Usado apenas para compatibilidade com a interface
        """
        return True
    
    def _is_numeric_operation(self, statement):
        """
        Verifica se uma declaração envolve apenas operações numéricas
        Usado apenas para compatibilidade com a interface
        """
        return True
    
    def _is_numeric_expression(self, expression):
        """
        Verifica se uma expressão é numérica
        Usado apenas para compatibilidade com a interface
        """
        return True
    
    def compile_function(self, ast_function, environment):
        """
        Compila uma função AST para código nativo usando C como intermediário
        
        :param ast_function: Nó AST da função a ser compilada
        :param environment: Ambiente de execução (para contexto)
        :return: Uma função Python que chama o código C compilado
        """
        function_name = ast_function.name
        
        # Verifica se a função já está em cache
        if function_name in self.compiled_functions:
            print(f"CJITCompiler: Usando função '{function_name}' do cache")
            return self.compiled_functions[function_name]
            
        print(f"CJITCompiler: Compilando função '{function_name}'")
        
        try:
            # Gera o código C
            generator = CCodeGenerator()
            c_code = generator.generate_complete_c_file(ast_function)
            
            # Cria arquivos temporários
            c_file_path = os.path.join(self.temp_dir, f"{function_name}.c")
            so_file_path = os.path.join(self.temp_dir, f"{function_name}.so")
            
            # Escreve o código C em um arquivo
            with open(c_file_path, 'w') as f:
                f.write(c_code)
                
            print(f"CJITCompiler: Código C gerado em {c_file_path}")
            
            # Compila o código C para uma biblioteca compartilhada
            compile_cmd = [
                "gcc", "-shared", "-fPIC", "-O3",
                "-o", so_file_path, c_file_path
            ]
            
            process = subprocess.run(
                compile_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            if process.returncode != 0:
                raise Exception(f"Erro ao compilar C: {process.stderr}")
                
            print(f"CJITCompiler: Biblioteca compilada em {so_file_path}")
            
            # Carrega a biblioteca compartilhada
            lib = ctypes.CDLL(so_file_path)
            
            # Obtém a função da biblioteca
            c_func = getattr(lib, function_name)
            
            # Define tipos de parâmetros e retorno
            # Por padrão, assume int para todos
            c_func.argtypes = [ctypes.c_int] * len(ast_function.parameters)
            c_func.restype = ctypes.c_int
            
            # Cria a função Python que chama a função C
            def wrapper_function(*args):
                # Converte argumentos Python para tipos C
                c_args = []
                for i, arg in enumerate(args):
                    c_args.append(ctypes.c_int(arg))
                
                # Chama a função C
                result = c_func(*c_args)
                return result
                
            # Armazena a função em cache
            self.compiled_functions[function_name] = wrapper_function
            
            return wrapper_function
            
        except Exception as e:
            print(f"CJITCompiler: Erro ao compilar função '{function_name}': {e}")
            raise 
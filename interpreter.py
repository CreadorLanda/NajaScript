#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast_nodes import *
import os
import re
from lexer import Lexer
from parser_naja import Parser
from environment import Environment
import sys

# Primeiro, adiciono uma classe para representar o valor flux
class FluxValue:
    """Representa um valor flux que é reavaliado dinamicamente"""
    def __init__(self, expression, interpreter, environment):
        self.expression = expression  # A expressão AST
        self.interpreter = interpreter  # Referência ao interpretador
        self.environment = environment  # Ambiente de avaliação
        self.on_change_callbacks = []  # Callbacks para eventos onChange
        
    def evaluate(self):
        """Avalia a expressão no ambiente atual e retorna o resultado"""
        prev_env = self.interpreter.environment
        self.interpreter.environment = self.environment
        try:
            result = self.interpreter.evaluate(self.expression)
            return result
        finally:
            self.interpreter.environment = prev_env
            
    def add_on_change_listener(self, callback):
        """Adiciona um callback que será chamado quando o valor mudar"""
        self.on_change_callbacks.append(callback)
        
    def notify_change(self, old_value, new_value):
        """Notifica os ouvintes sobre a mudança de valor"""
        for callback in self.on_change_callbacks:
            callback(old_value, new_value)
            
    def __str__(self):
        return str(self.evaluate())
        
    def __repr__(self):
        return self.__str__()

class BreakException(Exception):
    """Exceção lançada quando um comando break é encontrado"""
    pass

class ContinueException(Exception):
    """Exceção lançada quando um comando continue é encontrado"""
    pass

class ReturnException(Exception):
    """Exceção lançada quando um comando return é encontrado"""
    def __init__(self, value=None):
        self.value = value

class NajaVector:
    """Implementação de um vetor imutável em NajaScript"""
    def __init__(self, elements=None):
        self._elements = tuple(elements) if elements else tuple()
    
    def get(self, index):
        if 0 <= index < len(self._elements):
            return self._elements[index]
        raise Exception(f"Índice {index} fora dos limites do vetor")
    
    def length(self):
        return len(self._elements)
    
    def __str__(self):
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"vecto({elements_str})"
    
    def __repr__(self):
        return self.__str__()

class NajaList:
    """Implementação de uma lista em NajaScript"""
    def __init__(self, elements=None):
        self._elements = list(elements) if elements else []
    
    def add(self, value):
        self._elements.append(value)
        return value
    
    def remove(self, index_or_value):
        if isinstance(index_or_value, int):
            if 0 <= index_or_value < len(self._elements):
                return self._elements.pop(index_or_value)
            raise Exception(f"Índice {index_or_value} fora dos limites da lista")
        else:
            if index_or_value in self._elements:
                self._elements.remove(index_or_value)
                return index_or_value
            raise Exception(f"Valor {index_or_value} não encontrado na lista")
    
    def removeLast(self):
        if not self._elements:
            raise Exception("Não é possível remover de uma lista vazia")
        return self._elements.pop()
    
    def replace(self, index, value):
        if 0 <= index < len(self._elements):
            old_value = self._elements[index]
            self._elements[index] = value
            return old_value
        raise Exception(f"Índice {index} fora dos limites da lista")
    
    def get(self, index):
        if 0 <= index < len(self._elements):
            return self._elements[index]
        raise Exception(f"Índice {index} fora dos limites da lista")
    
    def length(self):
        return len(self._elements)
    
    def sort(self):
        sorted_list = NajaList(sorted(self._elements))
        return sorted_list
    
    def isEmpty(self):
        return len(self._elements) == 0
    
    def count(self, item):
        return self._elements.count(item)
    
    def __str__(self):
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"[{elements_str}]"
    
    def __repr__(self):
        return self.__str__()

class NajaDict:
    """Implementação de um dicionário em NajaScript"""
    def __init__(self, items=None):
        self._dict = {}
        if items:
            for i, item in enumerate(items):
                self._dict[i] = item
    
    def add(self, key, value=None):
        if value is None:
            # Se apenas um argumento, adiciona como valor com chave automática
            key_to_use = len(self._dict)
            self._dict[key_to_use] = key
            return key
        else:
            self._dict[key] = value
            return value
    
    def remove(self, key):
        if key in self._dict:
            value = self._dict[key]
            del self._dict[key]
            return value
        raise Exception(f"Chave {key} não encontrada no dicionário")
    
    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        raise Exception(f"Chave {key} não encontrada no dicionário")
    
    def length(self):
        return len(self._dict)
    
    def isEmpty(self):
        return len(self._dict) == 0
    
    def __str__(self):
        items = []
        for k, v in self._dict.items():
            items.append(f"{k}: {str(v)}")
        return f"{{{', '.join(items)}}}"
    
    def __repr__(self):
        return self.__str__()

class Function:
    """Representação de uma função em NajaScript"""
    def __init__(self, declaration, environment):
        self.declaration = declaration
        self.environment = environment
        self.compiled_version = None  # Versão compilada JIT
    
    def __call__(self, interpreter, arguments):
        """Chama a função com os argumentos fornecidos"""
        # Verifica se podemos usar a versão compilada JIT
        if self.compiled_version:
            try:
                # Executa a versão compilada diretamente
                return self.compiled_version(*arguments)
            except Exception as e:
                # Se falhar, volta para a versão interpretada
                print(f"JIT: Erro ao executar versão compilada, usando interpretador: {e}")
        
        # Versão interpretada original
        # Cria um novo ambiente com o ambiente de definição como pai
        environment = Environment(self.environment)
        
        # Define os parâmetros no novo ambiente
        for i, param in enumerate(self.declaration.parameters):
            if i < len(arguments):
                # param pode ser uma tupla (tipo, nome)
                param_name = param.name if hasattr(param, 'name') else param[1]
                environment.define(param_name, arguments[i])
            else:
                # Parâmetro não fornecido, define como null
                param_name = param.name if hasattr(param, 'name') else param[1]
                environment.define(param_name, None)
        
        # Executa o corpo da função no novo ambiente
        previous_env = interpreter.environment
        interpreter.environment = environment
        
        try:
            # Executa o corpo da função
            interpreter.execute_block(self.declaration.body, environment)
            return None
        except ReturnException as return_value:
            return return_value.value
        finally:
            # Restaura o ambiente original
            interpreter.environment = previous_env
            
    # Adicionando suporte para callbacks onChange
    def as_callback(self):
        """Converte esta função em um callback para onChange"""
        def callback_wrapper(var_name, old_value, new_value):
            return self(self.environment.interpreter, [var_name, old_value, new_value])
        return callback_wrapper

class Interpreter:
    """Interpretador para NajaScript"""
    def __init__(self):
        self.environment = Environment()
        self.globals = self.environment
        self.locals = self.environment
        self.error = None
        # Inicializar caminhos de módulos e módulos importados
        self.imported_modules = {}
        self.module_paths = ['.', './modules']
        
        # Registro de funções nativas
        self._register_native_functions()
        # Configurar builtins
        self._setup_builtins()
    
    def set_jit_compiler(self, jit_compiler):
        """Define o compilador JIT a ser utilizado"""
        self.jit_compiler = jit_compiler
    
    def _setup_builtins(self):
        """Configura as funções nativas da linguagem"""
        # print
        def print_func(*args):
            print(*args, end="")
            return None
        self.environment.define("print", print_func)
        
        # println
        def println_func(*args):
            print(*args)
            return None
        self.environment.define("println", println_func)
        
        # input
        def input_func(prompt=""):
            return input(prompt)
        self.environment.define("input", input_func)
        
        # type
        def type_func(value):
            if isinstance(value, int):
                return "int"
            elif isinstance(value, float):
                return "float"
            elif isinstance(value, str):
                return "string"
            elif isinstance(value, bool):
                return "bool"
            elif isinstance(value, NajaDict):
                return "dict"
            elif isinstance(value, NajaList):
                return "list"
            elif isinstance(value, NajaVector):
                return "vecto"
            elif isinstance(value, FluxValue):
                return "flux"
            elif value is None:
                return "null"
            # Qualquer outro tipo é considerado "any"
            return "any"
        self.environment.define("type", type_func)
        
        # min, max
        self.environment.define("min", min)
        self.environment.define("max", max)
        
        # vecto e list construtores
        def vecto_func(*args):
            return NajaVector(args)
        self.environment.define("vecto", vecto_func)
        
        def list_func(*args):
            return NajaList(args)
        self.environment.define("list", list_func)
        
        # dict construtor
        def dict_func(*args):
            return NajaDict(args)
        self.environment.define("dict", dict_func)
        
        # Função para adicionar um listener onChange
        def on_change_func(var_name, callback):
            if not isinstance(var_name, str):
                raise Exception("O primeiro argumento de onChange deve ser o nome da variável como string")
            
            # Se o callback for uma função NajaScript
            if isinstance(callback, Function):
                callback = callback.as_callback()
            elif not callable(callback):
                raise Exception("O segundo argumento de onChange deve ser uma função callback")
            
            self.environment.add_change_listener(var_name, callback)
            return None
        self.environment.define("onChange", on_change_func)
        
        # Função para imprimir variáveis que mudaram
        def print_change_func(var_name, old_value, new_value):
            print(f"Variável '{var_name}' mudou: {old_value} -> {new_value}")
            return None
        self.environment.define("printChange", print_change_func)
    
    def interpret(self, ast):
        """Interpreta a árvore sintática abstrata"""
        if ast is None:
            return None
        
        result = None
        try:
            # Se for um objeto Program, obtém as statements
            if isinstance(ast, Program):
                statements = ast.statements
            else:
                statements = ast
            
            # Executa todas as statements
            for statement in statements:
                result = self.evaluate(statement)
            
        except Exception as e:
            self.error = str(e)
            print(f"Erro durante a interpretação: {e}")
        
        return result
    
    def execute(self, statement):
        """Executa uma declaração"""
        try:
            statement_type = statement.__class__.__name__
            method_name = f"execute_{statement_type}"
            
            if hasattr(self, method_name):
                return getattr(self, method_name)(statement)
            else:
                return self.execute_default(statement)
        except Exception as e:
            print(f"Erro durante a interpretação: {e}")
    
    def execute_default(self, statement):
        """Método padrão para executar instruções não tratadas especificamente"""
        raise Exception(f"Tipo de instrução não implementado: {type(statement).__name__}")
    
    def execute_VarDeclaration(self, stmt):
        """Executa uma declaração de variável"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        
        self.environment.define(stmt.name, value, stmt.is_const)
        return None
    
    def execute_ExpressionStatement(self, stmt):
        """Executa uma expressão como uma instrução"""
        return self.evaluate(stmt.expression)
    
    def execute_IfStatement(self, stmt):
        """Executa uma declaração if"""
        condition = self.evaluate(stmt.condition)
        
        if self.is_truthy(condition):
            return self.execute_block(stmt.then_branch, Environment(self.environment))
        elif stmt.elif_branches:
            for elif_branch in stmt.elif_branches:
                elif_condition, elif_body = elif_branch
                if self.is_truthy(self.evaluate(elif_condition)):
                    return self.execute_block(elif_body, Environment(self.environment))
            
            if stmt.else_branch:
                return self.execute_block(stmt.else_branch, Environment(self.environment))
        elif stmt.else_branch:
            return self.execute_block(stmt.else_branch, Environment(self.environment))
            
        return None
    
    def execute_WhileStatement(self, stmt):
        """Executa uma declaração while"""
        result = None
        
        try:
            while self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    result = self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    continue
                except BreakException:
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise
        
        return result
    
    def execute_DoWhileStatement(self, stmt):
        """Executa uma declaração do-while"""
        result = None
        
        try:
            # Executa o bloco pelo menos uma vez
            result = self.execute_block(stmt.body, Environment(self.environment))
            
            # Continua executando enquanto a condição for verdadeira
            while self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    result = self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    continue
                except BreakException:
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise
        
        return result
    
    def execute_ForStatement(self, stmt):
        """Executa uma declaração for"""
        result = None
        
        # Cria um novo ambiente para o escopo do loop for
        env = Environment(self.environment)
        old_env = self.environment
        self.environment = env
        
        try:
            # Inicialização
            if stmt.init:
                self.execute(stmt.init)
            
            # Loop principal
            while not stmt.condition or self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    # Corpo do loop
                    result = self.execute_block(stmt.body, Environment(env))
                except ContinueException:
                    # Continue: pula para a atualização
                    pass
                except BreakException:
                    # Break: sai do loop
                    break
                
                # Atualização
                if stmt.update:
                    self.evaluate(stmt.update)
            
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise
        finally:
            # Restaura o ambiente anterior
            self.environment = old_env
        
        return result
    
    def execute_ForInStatement(self, stmt):
        """Executa uma declaração 'forin'"""
        result = None
        
        # Avalia o iterável
        iterable = self.evaluate(stmt.iterable)
        
        # Verifica se o objeto é iterável (lista, dicionário, etc.)
        if isinstance(iterable, NajaList) or isinstance(iterable, NajaDict) or isinstance(iterable, NajaVector) or isinstance(iterable, list) or isinstance(iterable, dict):
            # Cria um novo ambiente para o escopo do loop
            env = Environment(self.environment)
            old_env = self.environment
            self.environment = env
            
            try:
                # Para listas e vetores
                if isinstance(iterable, NajaList) or isinstance(iterable, NajaVector) or isinstance(iterable, list):
                    if isinstance(iterable, list):
                        items = iterable
                    else:
                        items = iterable.elements if hasattr(iterable, 'elements') else []
                    
                    for item in items:
                        # Define a variável do item no ambiente
                        env.define(stmt.item, item)
                        
                        try:
                            # Executa o corpo do loop
                            result = self.execute_block(stmt.body, Environment(env))
                        except ContinueException:
                            continue
                        except BreakException:
                            break
                
                # Para dicionários
                elif isinstance(iterable, NajaDict) or isinstance(iterable, dict):
                    if isinstance(iterable, dict):
                        keys = iterable.keys()
                    else:
                        keys = [item[0] for item in iterable.items] if hasattr(iterable, 'items') else []
                    
                    for key in keys:
                        # Define a variável do item (chave) no ambiente
                        env.define(stmt.item, key)
                        
                        try:
                            # Executa o corpo do loop
                            result = self.execute_block(stmt.body, Environment(env))
                        except ContinueException:
                            continue
                        except BreakException:
                            break
            
            except Exception as e:
                if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                    raise
            finally:
                # Restaura o ambiente anterior
                self.environment = old_env
        
        return result
    
    def execute_FunctionDeclaration(self, stmt):
        """Executa uma declaração de função"""
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name, function)
        return None
    
    def execute_ReturnStatement(self, stmt):
        """Executa uma declaração return"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        
        # Lança uma exceção para sinalizar o retorno, que será capturada no escopo apropriado
        raise ReturnException(value)
    
    def execute_BreakStatement(self, stmt):
        """Executa uma declaração break"""
        raise BreakException()
    
    def execute_ContinueStatement(self, stmt):
        """Executa uma declaração continue"""
        raise ContinueException()
    
    def execute_SwitchStatement(self, stmt):
        """Executa uma declaração switch"""
        value = self.evaluate(stmt.value)
        
        # Flag para indicar se algum caso já foi correspondido
        matched = False
        
        # Itera sobre todos os casos
        for case_value, case_body in stmt.cases:
            if matched or self.is_equal(value, self.evaluate(case_value)):
                matched = True
                try:
                    self.execute_block(case_body, Environment(self.environment))
                except BreakException:
                    break
        
        # Se nenhum caso corresponder e houver um caso padrão
        if not matched and stmt.default:
            self.execute_block(stmt.default, Environment(self.environment))
        
        return None
    
    def execute_block(self, statements, environment):
        """Executa um bloco de instruções em um novo ambiente"""
        previous = self.environment
        try:
            self.environment = environment
            
            # Executamos cada instrução no bloco
            # NOTA: É importante que ReturnException, BreakException e ContinueException
            # sejam propagadas para o chamador, para permitir que funções recursivas
            # retornem corretamente.
            for statement in statements:
                self.execute(statement)
            
            return None
        finally:
            self.environment = previous
    
    def evaluate(self, node):
        """Avalia um nó da AST e retorna seu valor"""
        # Despacha para o método apropriado com base no tipo do nó
        method_name = f"evaluate_{node.__class__.__name__}"
        method = getattr(self, method_name, None)
        
        if method is None:
            # Tenta usar execute para statements
            method_name = f"execute_{node.__class__.__name__}"
            method = getattr(self, method_name, None)
            
            if method is None:
                raise RuntimeError(f"Método não implementado para {node.__class__.__name__}")
        
        return method(node)
    
    def evaluate_BinaryOperation(self, expr):
        """Avalia uma operação binária"""
        # Para operadores lógicos curto-circuito (&&, ||), não avaliamos os dois lados imediatamente
        if expr.operator == '&&':
            left = self.evaluate(expr.left)
            if not self.is_truthy(left):
                return False  # Curto-circuito para AND quando o lado esquerdo é falso
            return self.is_truthy(self.evaluate(expr.right))
        
        elif expr.operator == '||':
            left = self.evaluate(expr.left)
            if self.is_truthy(left):
                return True  # Curto-circuito para OR quando o lado esquerdo é verdadeiro
            return self.is_truthy(self.evaluate(expr.right))
        
        # Para outros operadores, avalia ambos os lados
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        # Operações aritméticas
        if expr.operator == '+':
            # Se um dos operandos for string, faz concatenação
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif expr.operator == '-':
            return left - right
        elif expr.operator == '*':
            return left * right
        elif expr.operator == '/':
            return left / right
        elif expr.operator == '%':
            return left % right
        elif expr.operator == '**':
            return left ** right
        
        # Operações de comparação
        elif expr.operator == '==':
            return self.is_equal(left, right)
        elif expr.operator == '!=':
            return not self.is_equal(left, right)
        elif expr.operator == '<':
            return left < right
        elif expr.operator == '>':
            return left > right
        elif expr.operator == '<=':
            return left <= right
        elif expr.operator == '>=':
            return left >= right
        
        raise Exception(f"Operador binário não suportado: {expr.operator}")
    
    def evaluate_UnaryOperation(self, expr):
        """Avalia uma operação unária"""
        right = self.evaluate(expr.operand)
        
        if expr.operator == '-':
            return -right
        elif expr.operator == '!':
            return not self.is_truthy(right)
        
        raise Exception(f"Operador unário não suportado: {expr.operator}")
    
    def evaluate_TernaryOperator(self, expr):
        """Avalia um operador ternário"""
        condition = self.evaluate(expr.condition)
        
        if self.is_truthy(condition):
            return self.evaluate(expr.then_expr)
        else:
            return self.evaluate(expr.else_expr)
    
    def evaluate_Variable(self, expr):
        """Avalia uma variável"""
        return self.environment.get(expr.name)
    
    def evaluate_Assignment(self, expr):
        """Avalia uma atribuição"""
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def evaluate_FunctionCall(self, expr):
        """Avalia uma chamada de função"""
        # Obtém a função
        callee = self.environment.get(expr.name)
        
        # Avalia os argumentos
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        
        # Verifica se é uma função nativa (Python) ou uma função NajaScript
        if callable(callee) and not isinstance(callee, Function):
            # Função nativa
            return callee(*arguments)
        elif isinstance(callee, Function):
            # Função NajaScript
            return callee(self, arguments)
        else:
            raise RuntimeError(f"Não é possível chamar '{expr.name}' como função")
    
    def evaluate_MethodCall(self, expr):
        """Avalia uma chamada de método"""
        obj = self.evaluate(expr.object)
        method_name = expr.method
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        
        # Verifica se o objeto tem o método
        if isinstance(obj, NajaList):
            if method_name == "add":
                return obj.add(*arguments)
            elif method_name == "remove":
                return obj.remove(*arguments)
            elif method_name == "removeLast":
                return obj.removeLast()
            elif method_name == "replace":
                return obj.replace(*arguments)
            elif method_name == "get":
                return obj.get(*arguments)
            elif method_name == "length":
                return obj.length()
            elif method_name == "sort":
                return obj.sort()
            elif method_name == "isEmpty":
                return obj.isEmpty()
            elif method_name == "count":
                return obj.count(*arguments)
            else:
                raise Exception(f"Método desconhecido '{method_name}' para objeto do tipo list")
        
        elif isinstance(obj, NajaVector):
            if method_name == "get":
                return obj.get(*arguments)
            elif method_name == "length":
                return obj.length()
            else:
                raise Exception(f"Método desconhecido '{method_name}' para objeto do tipo vecto")
        
        elif isinstance(obj, NajaDict):
            if method_name == "add":
                return obj.add(*arguments)
            elif method_name == "remove":
                return obj.remove(*arguments)
            elif method_name == "get":
                return obj.get(*arguments)
            elif method_name == "length":
                return obj.length()
            elif method_name == "isEmpty":
                return obj.isEmpty()
            else:
                raise Exception(f"Método desconhecido '{method_name}' para objeto do tipo dict")
        
        else:
            raise Exception(f"Tipo de objeto '{type(obj)}' não suporta métodos")
    
    def evaluate_IntegerLiteral(self, expr):
        """Avalia um literal inteiro"""
        return expr.value
    
    def evaluate_FloatLiteral(self, expr):
        """Avalia um literal float"""
        return expr.value
    
    def evaluate_StringLiteral(self, expr):
        """Avalia uma expressão de literal de string"""
        return expr.value
    
    def evaluate_BooleanLiteral(self, expr):
        """Avalia um literal booleano"""
        return expr.value
    
    def evaluate_NullLiteral(self, expr):
        """Avalia um literal null"""
        return None
    
    def evaluate_ListLiteral(self, expr):
        """Avalia um literal lista"""
        elements = [self.evaluate(element) for element in expr.elements]
        return NajaList(elements)
    
    def evaluate_DictLiteral(self, expr):
        """Avalia um literal dicionário"""
        items = []
        for item in expr.items:
            items.append(self.evaluate(item))
        return NajaDict(items)
    
    def is_truthy(self, value):
        """Determina se um valor é considerado verdadeiro"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, (NajaList, NajaVector, NajaDict)):
            return value.length() > 0
        return True
    
    def is_equal(self, a, b):
        """Verifica se dois valores são iguais"""
        if a is None and b is None:
            return True
        if a is None:
            return False
        
        return a == b
    
    def execute_FluxDeclaration(self, stmt):
        # Cria um FluxValue
        env = self.environment
        flux_value = FluxValue(stmt.expression, self, env)
        
        # Registra o valor no ambiente
        env.define(stmt.name, flux_value)
        
        # Avalia inicialmente a expressão e notifica os listeners
        value = flux_value.evaluate()
        return value

    def _import_najaPt(self):
        """Implementa a importação do módulo NajaPt"""
        
        # Mapeamento de palavras em português para NajaScript
        pt_to_naja = {
            # Palavras-chave
            'se': 'if',
            'senao': 'else',
            'para': 'for',
            'enquanto': 'while',
            'funcao': 'fun',
            'retornar': 'return',
            'verdadeiro': 'true',
            'falso': 'false',
            'em': 'in',
            'paracada': 'forin',
            'nulo': 'null',
            'continuar': 'continue',
            'parar': 'break',
            'fazer': 'do',
            
            # Operadores lógicos - estes serão tratados de maneira especial
            # para garantir que não conflitem com outras palavras
            'e': '&&',
            'ou': '||',
            'nao': '!',
            
            # Tipos
            'inteiro': 'int',
            'decimal': 'float',
            'texto': 'string',
            'booleano': 'bool',
            'lista': 'list',
            'dicionario': 'dict',
            'qualquer': 'any',
            
            # Funções
            'escrever': 'print',
            'escreverln': 'println',
            'comprimento': 'length',
            'converter_para_texto': 'toString',
            'converter_para_inteiro': 'toInt',
            'converter_para_decimal': 'toFloat',
            
            # Métodos
            'adicionar': 'add',
            'remover': 'remove',
            'obter': 'get',
            'adicionarUltimo': 'add',
            'removerUltimo': 'removeLast',
            'substituir': 'replace',
            'estaVazia': 'isEmpty'
        }
        
        # Função para traduzir código de português para NajaScript
        def traduzir_pt_para_naja(codigo):
            # Vamos preservar os comentários de linha
            linhas = codigo.split('\n')
            resultado = []
            
            for linha in linhas:
                # Verifica se a linha contém um comentário
                comentario_pos = linha.find('//')
                if comentario_pos == -1:
                    comentario_pos = linha.find('#')
                    
                # Se tem comentário, preserva ele
                if comentario_pos != -1:
                    parte_codigo = linha[:comentario_pos]
                    parte_comentario = linha[comentario_pos:]
                    
                    # Traduz apenas a parte do código
                    parte_codigo = traduzir_linha(parte_codigo, pt_to_naja)
                    
                    # Reconstrói a linha com o comentário preservado
                    resultado.append(parte_codigo + parte_comentario)
                else:
                    # Sem comentário: traduz toda a linha
                    resultado.append(traduzir_linha(linha, pt_to_naja))
            
            # Preservar comentários de bloco (/* ... */)
            codigo_resultante = '\n'.join(resultado)
            return codigo_resultante
        
        def traduzir_linha(linha, pt_to_naja):
            # Primeiro, tratamos os operadores lógicos - precisamos de cuidados especiais
            
            # 'nao' precisa de um tratamento especial pois é um operador unário
            linha = re.sub(r'\bnao\s+', '!', linha)
            
            # Outros operadores lógicos
            linha = re.sub(r'\be\b', '&&', linha)
            linha = re.sub(r'\bou\b', '||', linha)
            
            # Agora traduzimos as outras palavras-chave
            for pt, naja in pt_to_naja.items():
                # Pulamos os operadores lógicos que já foram tratados
                if pt in ['e', 'ou', 'nao']:
                    continue
                # Para palavras-chave: garantir que são palavras completas
                linha = re.sub(r'\b' + pt + r'\b', naja, linha)
            
            return linha
        
        # Registrar no ambiente a função de tradução
        self.environment.define('__traduzir_pt_para_naja', traduzir_pt_para_naja, True)
        
        # Definir funções e variáveis do módulo NajaPt
        for pt, naja in pt_to_naja.items():
            # Ignora operadores lógicos que são tratados de maneira especial
            if pt in ['e', 'ou', 'nao']:
                continue
            
            # Se for um tipo ou palavra-chave, não definimos como variável
            if pt not in ['inteiro', 'decimal', 'texto', 'booleano', 'lista', 'dicionario', 
                           'se', 'senao', 'para', 'enquanto', 'funcao', 'retornar',
                           'verdadeiro', 'falso', 'nulo', 'continuar', 'parar', 'em', 'paracada', 'fazer']:
                # Para funções, definimos aliases
                if pt in ['escrever', 'escreverln', 'comprimento', 'lista', 'dicionario', 'vecto']:
                    # Obtém a função original do ambiente
                    func = self.environment.get(naja)
                    # Define o alias em português
                    self.environment.define(pt, func, True)
        
        # Funções específicas para lista, dicionário e vecto (tratadas separadamente)
        try:
            self.environment.define('lista', self.environment.get('list'), True)
        except RuntimeError:
            print("Aviso: Função 'list' não encontrada para criar alias 'lista'")
            
        try:
            self.environment.define('dicionario', self.environment.get('dict'), True)
        except RuntimeError:
            print("Aviso: Função 'dict' não encontrada para criar alias 'dicionario'")
        
        # Registrar biblioteca no cache de importações
        self.imported_modules['NajaPt'] = True
        
        # Registra função para pré-processar o código fonte
        def najaPt_preprocessor(source_code):
            # Esta função será chamada antes da análise léxica
            return traduzir_pt_para_naja(source_code)
        
        # Registra o pré-processador na instância atual
        self.register_preprocessor(najaPt_preprocessor)
        
        return True
    
    def register_preprocessor(self, preprocessor_func):
        """Registra uma função de pré-processamento do código fonte"""
        if not hasattr(self, 'preprocessors'):
            self.preprocessors = []
        self.preprocessors.append(preprocessor_func)
    
    def preprocess_source(self, source_code):
        """Aplica todos os pré-processadores registrados ao código fonte"""
        if hasattr(self, 'preprocessors'):
            for preprocessor in self.preprocessors:
                source_code = preprocessor(source_code)
        return source_code

    def import_module(self, module_name):
        """Importa um módulo pelo nome"""
        
        # Verifica se o módulo já foi importado
        if module_name in self.imported_modules:
            return self.imported_modules[module_name]
        
        # Módulos especiais tratados internamente
        if module_name == "NajaPt":
            self._import_najaPt()
            return True
        
        # Tenta encontrar o arquivo do módulo nos caminhos definidos
        for path in self.module_paths:
            file_path = os.path.join(path, module_name)
            # Tentamos com e sem extensão .naja
            for try_path in [file_path, file_path + ".naja"]:
                if os.path.exists(try_path):
                    try:
                        with open(try_path, 'r', encoding='utf-8') as f:
                            source = f.read()
                        
                        # Pré-processa o código fonte
                        source = self.preprocess_source(source)
                        
                        # Análise léxica e sintática do módulo
                        lexer = Lexer(source)
                        parser = Parser(lexer)
                        ast = parser.parse()
                        
                        # Cria um novo interpretador para o módulo
                        module_interpreter = Interpreter()
                        # Configura o ambiente do módulo
                        module_interpreter.module_paths = self.module_paths
                        # Copia pré-processadores para o novo interpretador
                        if hasattr(self, 'preprocessors'):
                            for preprocessor in self.preprocessors:
                                module_interpreter.register_preprocessor(preprocessor)
                        # Interpreta o módulo
                        module_interpreter.interpret(ast)
                        
                        # Armazena o módulo carregado
                        self.imported_modules[module_name] = module_interpreter
                        
                        # Exporta variáveis e funções do módulo para o ambiente atual
                        for name, value in module_interpreter.environment.values.items():
                            if not name.startswith('_'):  # Não importa variáveis privadas
                                self.environment.define(name, value[0], value[1], value[2])
                        
                        return True
                    except Exception as e:
                        print(f"Erro ao importar módulo {module_name}: {e}")
                        return False
        
        print(f"Módulo não encontrado: {module_name}")
        return False

    def execute_ImportStatement(self, stmt):
        """Executa uma declaração de importação"""
        # Usa a função import_module para importar o módulo
        module_name = stmt.module_name
        
        # Remove as aspas se presentes
        if module_name.startswith('"') and module_name.endswith('"'):
            module_name = module_name[1:-1]
        elif module_name.startswith("'") and module_name.endswith("'"):
            module_name = module_name[1:-1]
        
        self.import_module(module_name)
        return None

    def _register_native_functions(self):
        """Registra todas as funções nativas na linguagem"""
        
        # Função de impressão
        def print_function(*args):
            result = " ".join(str(arg) for arg in args)
            print(result, end="")
            sys.stdout.flush()
            return None
        
        # Função de impressão com quebra de linha
        def println_function(*args):
            result = " ".join(str(arg) for arg in args)
            print(result)
            sys.stdout.flush()
            return None
        
        # Função para obter o comprimento de strings ou listas
        def length_function(obj):
            if isinstance(obj, str) or isinstance(obj, list) or isinstance(obj, dict):
                return len(obj)
            elif isinstance(obj, NajaList) or isinstance(obj, NajaDict) or isinstance(obj, NajaVector):
                return obj.length()
            raise RuntimeError(f"Objeto do tipo {type(obj)} não tem comprimento")
        
        # Função para converter para string
        def to_string_function(obj):
            return str(obj)
        
        # Função para converter para inteiro
        def to_int_function(obj):
            try:
                return int(obj)
            except ValueError:
                raise RuntimeError(f"Não foi possível converter '{obj}' para inteiro")
        
        # Função para converter para float
        def to_float_function(obj):
            try:
                return float(obj)
            except ValueError:
                raise RuntimeError(f"Não foi possível converter '{obj}' para decimal")
        
        # Registrar funções no ambiente
        self.environment.define("print", print_function, True)
        self.environment.define("println", println_function, True)
        self.environment.define("length", length_function, True)
        self.environment.define("toString", to_string_function, True)
        self.environment.define("toInt", to_int_function, True)
        self.environment.define("toFloat", to_float_function, True)

    def execute_ImportStatement(self, stmt):
        """
        Executa uma declaração de importação.
        Formatos suportados:
        - import "module";  # Importa todo o módulo
        """
        module_name = stmt.module_name.value if hasattr(stmt.module_name, 'value') else stmt.module_name
        return self.import_module(module_name)

    def execute_FunctionDeclaration(self, stmt):
        """Executa uma declaração de função"""
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name, function)
        return None

    def evaluate_BooleanLiteral(self, expr):
        """Avalia um literal booleano"""
        return expr.value

    def evaluate_StringLiteral(self, expr):
        """Avalia um literal string"""
        return expr.value 
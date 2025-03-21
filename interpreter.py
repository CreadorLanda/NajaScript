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
        
        # Garantir que arguments seja uma lista
        if not isinstance(arguments, list):
            arguments = [arguments]
        
        # Define os parâmetros no novo ambiente
        for i, param in enumerate(self.declaration.parameters):
            if i < len(arguments):
                # param pode ser uma tupla (tipo, nome) ou um objeto Parameter
                if hasattr(param, 'name'):
                    param_name = param.name
                elif isinstance(param, tuple) and len(param) > 1:
                    param_name = param[1]
                else:
                    param_name = str(param)
                environment.define(param_name, arguments[i])
            else:
                # Parâmetro não fornecido, define como null
                if hasattr(param, 'name'):
                    param_name = param.name
                elif isinstance(param, tuple) and len(param) > 1:
                    param_name = param[1]
                else:
                    param_name = str(param)
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

class NajaModule:
    """Representa um módulo NajaScript importado"""
    def __init__(self, name, environment):
        self.name = name
        self.environment = environment
        self.methods = {}
        
        # Mapeia as funções do ambiente para métodos do módulo
        for name, func in environment.functions.items():
            if not name.startswith("_"):  # Não exporta variáveis privadas
                self.methods[name] = func
        
        # Mapeia também os valores do ambiente
        for name, (value, _, _) in environment.values.items():
            if not name.startswith("_") and name not in self.methods:  # Não exporta variáveis privadas
                self.methods[name] = value
    
    def get_method(self, name):
        """Recupera um método ou valor do módulo pelo nome"""
        if name in self.methods:
            return self.methods[name]
        
        # Fallback para verificar diretamente no ambiente
        try:
            return self.environment.get(name)
        except RuntimeError:
            raise Exception(f"Método ou atributo '{name}' não encontrado no módulo '{self.name}'")
    
    def __str__(self):
        """Representação em string do módulo"""
        return f"<módulo '{self.name}'>"

class Interpreter:
    """Interpretador para NajaScript"""
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = self.environment
        self.error = None
        self.module_paths = ['.', './modules']
        self.jit_compiler = None
        self.debug = False
        self.source_map = {}
        self.imported_modules = {}
        
        # Inicializa as funções nativas
        self._setup_builtins()
        self._register_native_functions()
    
    def preprocess_source(self, source):
        """Pré-processa o código fonte, traduzindo comandos em português para NajaScript"""
        # Dicionário de tradução português -> NajaScript
        traducoes = {
            # Palavras-chave
            r'\bfuncao\b': 'fun',
            r'\bse\b': 'if',
            r'\bsenao se\b': 'elif',
            r'\bsenao\b': 'else',
            r'\benquanto\b': 'while',
            r'\bpara\b': 'for',
            r'\bparacada\b': 'forin',
            r'\bretornar\b': 'return',
            r'\bverdadeiro\b': 'true',
            r'\bfalso\b': 'false',
            r'\bem\b': 'in',
            r'\bnulo\b': 'null',
            r'\bcontinuar\b': 'continue',
            r'\bparar\b': 'break',
            r'\bimportar\b': 'import',
            
            # Tipos
            r'\binteiro\b': 'int',
            r'\bdecimal\b': 'float',
            r'\btexto\b': 'string',
            r'\bbooleano\b': 'bool',
            r'\blista\b': 'list',
            r'\bdicionario\b': 'dict',
            r'\bqualquer\b': 'any',
            
            # Funções
            r'\bescrever\b': 'print',
            r'\bescreverln\b': 'println',
            r'\bcomprimento\b': 'length',
            r'\bconverter_para_texto\b': 'toString',
            r'\bconverter_para_inteiro\b': 'toInt',
            r'\bconverter_para_decimal\b': 'toFloat',
            
            # Métodos
            r'\badicionar\b': 'add',
            r'\bremover\b': 'remove',
            r'\bobter\b': 'get',
            r'\badicionarUltimo\b': 'add',
            r'\bremoverUltimo\b': 'removeLast',
            r'\bsubstituir\b': 'replace'
        }
        
        # Aplica as traduções
        import re
        resultado = source
        
        # Primeiro, aplicar substituições específicas que podem conflitar
        # Por exemplo, "senao se" deve ser substituído antes de "senao"
        expressoes_especificas = [
            (r'\bsenao se\b', 'elif'),
            (r'\badicionarUltimo\b', 'add'),
            (r'\bremoverUltimo\b', 'removeLast'),
            (r'\bconverter_para_texto\b', 'toString'),
            (r'\bconverter_para_inteiro\b', 'toInt'),
            (r'\bconverter_para_decimal\b', 'toFloat')
        ]
        
        for padrao, substituto in expressoes_especificas:
            resultado = re.sub(padrao, substituto, resultado)
            # Remover esses padrões do dicionário principal
            if padrao in traducoes:
                del traducoes[padrao]
        
        # Depois, aplicar o restante das substituições
        for padrao, substituto in traducoes.items():
            resultado = re.sub(padrao, substituto, resultado)
        
        return resultado
        
    def set_jit_compiler(self, jit_compiler):
        """Define o compilador JIT para uso"""
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
    
        def int_func(value):
            """Converte um valor para inteiro"""
            if isinstance(value, str):
                try:
                    return int(value)
                except ValueError:
                    return 0
            elif isinstance(value, (int, float)):
                return int(value)
            return 0
        
        self.environment.define("int", int_func)  # Adicionando função int()
    
    def _register_native_functions(self):
        """Registra funções nativas no ambiente"""
        # Funções de E/S
        self.environment.define("print", print)
        self.environment.define("input", input)
        
        # Funções de conversão
        self.environment.define("int", int)
        self.environment.define("float", float)
        self.environment.define("str", str)
        self.environment.define("toString", str)  # Alias para str
        
        # Funções matemáticas
        self.environment.define("abs", abs)
        self.environment.define("round", round)
        self.environment.define("min", min)
        self.environment.define("max", max)
    
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
            for i, statement in enumerate(statements):
                try:
                    statement_type = statement.__class__.__name__
                    if self.debug:
                        print(f"\nDEBUG: Executando statement {i}: {statement_type}")
                        if hasattr(statement, '__dict__'):
                            for key, value in statement.__dict__.items():
                                if key == 'body' and hasattr(value, '__len__'):
                                    print(f"DEBUG: {key}: [bloco com {len(value)} statements]")
                                else:
                                    print(f"DEBUG: {key}: {value}")
                
                    # Executa a statement
                    result = self.execute(statement)
                    
                    if self.debug:
                        print(f"DEBUG: Statement {i} ({statement_type}) executada com sucesso")
                        if statement_type == "FunctionDeclaration":
                            # Verifica se a função está disponível após definição
                            function_name = statement.name
                            try:
                                func = self.environment.get(function_name)
                                print(f"DEBUG: Verificação - função '{function_name}' disponível: {type(func)}")
                                print(f"DEBUG: Ambiente atual: functions={list(self.environment.functions.keys())}")
                            except Exception as e:
                                print(f"DEBUG: Erro ao verificar função '{function_name}': {e}")
                except Exception as e:
                    if self.debug:
                        print(f"DEBUG: Erro na statement {i} ({statement_type}): {e}")
                        import traceback
                        traceback.print_exc()
                    raise
        
        except Exception as e:
            self.error = str(e)
            if self.debug:
                print(f"DEBUG: Erro durante a interpretação: {e}")
                import traceback
                traceback.print_exc()
            else:
                print(f"Erro durante a interpretação: {e}")
        
        return result
    
    def execute(self, stmt):
        """Executa uma instrução e retorna seu valor"""
        if stmt is None:
            return None
        
        stmt_type = stmt.__class__.__name__
        method_name = f"execute_{stmt_type}"
        
        if hasattr(self, method_name):
            return getattr(self, method_name)(stmt)
        else:
            raise Exception(f"Tipo de instrução não implementado: {stmt_type}")
    
    def evaluate(self, expr):
        """Avalia uma expressão e retorna seu valor"""
        if expr is None:
            return None
        
        # Adiciona verificação direta para strings
        if isinstance(expr, str):
            print(f"DEBUG: Recebido objeto string literal diretamente: '{expr}'")
            return expr
            
        expr_type = expr.__class__.__name__
        method_name = f"evaluate_{expr_type}"
        
        if hasattr(self, method_name):
            return getattr(self, method_name)(expr)
        else:
            # Adicionando mensagem de erro mais clara para depuração
            if self.debug:
                print(f"Erro de depuração: Tipo de expressão '{expr_type}' não implementado.")
                print(f"Expressão: {expr}")
                print(f"Tipo Python: {type(expr)}")
                print(f"Atributos: {dir(expr) if hasattr(expr, '__dict__') else 'N/A'}")
                if isinstance(expr, str):
                    print(f"Conteúdo da string: {expr}")
            
            # Mensagem de erro padrão
            raise Exception(f"Tipo de expressão não implementado: {expr_type}")
    
    def evaluate_Variable(self, expr):
        """Avalia uma variável"""
        return self.environment.get(expr.name)
    
    def evaluate_GetAttr(self, expr):
        """Avalia uma expressão de acesso a atributo (obj.attr)"""
        obj = self.evaluate(expr.object)
        
        # Verifica se é um módulo
        if isinstance(obj, NajaModule):
            return obj.get_method(expr.name)
        
        # Pode adicionar outros tipos de objetos que suportam acesso a atributos aqui
        
        raise Exception(f"Objeto do tipo {type(obj).__name__} não suporta acesso a atributos")
    
    def evaluate_ModuleMethodCall(self, expr):
        """Avalia uma chamada de método de módulo (ModuleName.method())"""
        module = self.evaluate(expr.module)
        
        # Verifica se é um módulo
        if isinstance(module, NajaModule):
            method = module.get_method(expr.method)
            
            # Avalia os argumentos
            arguments = [self.evaluate(arg) for arg in expr.arguments]
            
            # Verifica se o método é chamável
            if isinstance(method, Function):
                return method(self, arguments)
            elif callable(method) and not isinstance(method, (int, float, str, bool)):
                return method(*arguments)
            else:
                raise Exception(f"'{expr.method}' no módulo '{module.name}' não é uma função chamável")
        else:
            raise Exception(f"Objeto do tipo {type(module).__name__} não é um módulo")
    
    def evaluate_StringLiteral(self, expr):
        """Avalia um literal de string"""
        return expr.value
    
    def evaluate_IntegerLiteral(self, expr):
        """Avalia um literal inteiro"""
        return expr.value
    
    def evaluate_FloatLiteral(self, expr):
        """Avalia um literal de ponto flutuante"""
        return expr.value
    
    def evaluate_BooleanLiteral(self, expr):
        """Avalia um literal booleano"""
        return expr.value
    
    def evaluate_NullLiteral(self, expr):
        """Avalia um literal nulo"""
        return None
    
    def evaluate_BinaryOperation(self, expr):
        """Avalia uma operação binária"""
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator == "+":
            # Concatenação de strings
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            # Soma numérica
            return left + right
        elif expr.operator == "-":
            return left - right
        elif expr.operator == "*":
            return left * right
        elif expr.operator == "/":
            return left / right
        elif expr.operator == "%":
            return left % right
        elif expr.operator == "**":
            return left ** right
        elif expr.operator == "==":
            return left == right
        elif expr.operator == "!=":
            return left != right
        elif expr.operator == "<":
            return left < right
        elif expr.operator == ">":
            return left > right
        elif expr.operator == "<=":
            return left <= right
        elif expr.operator == ">=":
            return left >= right
        elif expr.operator == "&&" or expr.operator == "and":
            return self.is_truthy(left) and self.is_truthy(right)
        elif expr.operator == "||" or expr.operator == "or":
            return self.is_truthy(left) or self.is_truthy(right)
        else:
            raise Exception(f"Operador não implementado: {expr.operator}")
    
    def evaluate_UnaryOperation(self, expr):
        """Avalia uma operação unária"""
        right = self.evaluate(expr.operand)
        
        if expr.operator == "-":
            if isinstance(right, (int, float)):
                return -right
            raise TypeError(f"Operador '-' não suportado para {type(right)}")
        elif expr.operator == "!":
            return not self.is_truthy(right)
        
        # Operador não suportado
        raise ValueError(f"Operador unário não suportado: {expr.operator}")
    
    def evaluate_FunctionCall(self, expr):
        """Avalia uma chamada de função"""
        # Avalia a função (pode ser um nome ou uma expressão)
        callee = None
        
        function_name = None
        if isinstance(expr.name, Variable):
            # Função referenciada por nome via objeto Variable
            function_name = expr.name.name
        elif isinstance(expr.name, str):
            # Função referenciada diretamente por string (como 'println')
            function_name = expr.name
        
        # Se temos um nome de função, buscamos no ambiente
        if function_name:
            try:
                callee = self.environment.get(function_name)
            except Exception as e:
                raise
        else:
            # Função referenciada por expressão mais complexa
            callee = self.evaluate(expr.name)
        
        # Avalia os argumentos
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        
        # Verificações de tipo mais seguras
        if hasattr(callee, '__class__') and callee.__class__.__name__ == "NajaGameFunction":
            return callee(self, arguments)
        # Se for um objeto Function, usa o método __call__ dele
        elif isinstance(callee, Function):
            return callee(self, arguments)
        # Se for uma função nativa do Python (mas não um int ou outro tipo primitivo)
        elif callable(callee) and not (isinstance(callee, (int, float, str, bool))):
            return callee(*arguments)
        # Se for um objeto com método __call__, chama-o com argumentos
        elif hasattr(callee, "__call__") and callable(getattr(callee, "__call__")):
            # Tenta chamar o método __call__ diretamente
            try:
                return callee.__call__(self, arguments)
            except TypeError:
                # Se falhar, tenta chamar de outra forma
                try:
                    return callee(self, arguments)
                except TypeError:
                    try:
                        return callee(*arguments)
                    except Exception as e:
                        raise Exception(f"Erro ao chamar função: {e}")
        else:
            name = function_name if function_name else (expr.name.name if isinstance(expr.name, Variable) else str(expr.name))
            raise Exception(f"'{name}' não é uma função ou não é chamável")
    
    def evaluate_MethodCall(self, expr):
        """Avalia uma chamada de método em um objeto"""
        # Avalia o objeto
        obj = self.evaluate(expr.object)
        
        # Extrai o nome do método
        method_name = expr.method
        
        # Avalia os argumentos
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        
        # Verifica se o objeto é um módulo
        if isinstance(obj, NajaModule):
            method = obj.get_method(method_name)
            if method is None:
                raise Exception(f"Método '{method_name}' não encontrado no módulo '{obj.name}'")
            
            # Verifica se o método é chamável
            if isinstance(method, Function):
                return method(self, arguments)
            elif callable(method) and not isinstance(method, (int, float, str, bool)):
                return method(*arguments)
            else:
                raise Exception(f"'{method_name}' no módulo '{obj.name}' não é uma função chamável")
        
        # Verifica se o objeto tem o método solicitado
        elif isinstance(obj, NajaList):
            if method_name == "length":
                return obj.length()
            elif method_name == "get":
                if len(arguments) != 1:
                    raise Exception(f"Método get() espera 1 argumento, recebeu {len(arguments)}")
                return obj.get(arguments[0])
            elif method_name == "add":
                if len(arguments) != 1:
                    raise Exception(f"Método add() espera 1 argumento, recebeu {len(arguments)}")
                return obj.add(arguments[0])
            elif method_name == "remove":
                if len(arguments) != 1:
                    raise Exception(f"Método remove() espera 1 argumento, recebeu {len(arguments)}")
                return obj.remove(arguments[0])
            elif method_name == "removeLast":
                if len(arguments) != 0:
                    raise Exception(f"Método removeLast() não espera argumentos, recebeu {len(arguments)}")
                return obj.removeLast()
            else:
                raise Exception(f"Listas não possuem o método '{method_name}'")
        elif isinstance(obj, NajaDict):
            if method_name == "length":
                return obj.length()
            elif method_name == "get":
                if len(arguments) != 1:
                    raise Exception(f"Método get() espera 1 argumento, recebeu {len(arguments)}")
                return obj.get(arguments[0])
            elif method_name == "add":
                if len(arguments) not in [1, 2]:
                    raise Exception(f"Método add() espera 1 ou 2 argumentos, recebeu {len(arguments)}")
                if len(arguments) == 1:
                    return obj.add(arguments[0])
                else:
                    return obj.add(arguments[0], arguments[1])
            elif method_name == "remove":
                if len(arguments) != 1:
                    raise Exception(f"Método remove() espera 1 argumento, recebeu {len(arguments)}")
                return obj.remove(arguments[0])
            else:
                raise Exception(f"Dicionários não possuem o método '{method_name}'")
        elif isinstance(obj, str):
            if method_name == "length":
                return len(obj)
            elif method_name == "substring":
                if len(arguments) not in [1, 2]:
                    raise Exception(f"Método substring() espera 1 ou 2 argumentos, recebeu {len(arguments)}")
                start = arguments[0]
                if not isinstance(start, int):
                    raise Exception(f"O índice inicial deve ser um número inteiro")
                if len(arguments) == 1:
                    return obj[start:]
                end = arguments[1]
                if not isinstance(end, int):
                    raise Exception(f"O índice final deve ser um número inteiro")
                return obj[start:end]
            else:
                raise Exception(f"Strings não possuem o método '{method_name}'")
        else:
            raise Exception(f"O objeto do tipo {type(obj).__name__} não suporta chamadas de método")

    def is_truthy(self, value):
        """Verifica se um valor é considerado verdadeiro"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if hasattr(value, "length") and callable(value.length):
            return value.length() > 0
        if hasattr(value, "isEmpty") and callable(value.isEmpty):
            return not value.isEmpty()
        # Por padrão, qualquer objeto é considerado verdadeiro
        return True
    
    def execute_block(self, statements, environment):
        """Executa um bloco de código em um ambiente específico"""
        previous_env = self.environment
        self.environment = environment
        
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_env
        
        return None
    
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
    
    def execute_ImportStatement(self, stmt):
        """Executa uma instrução de importação"""
        module_name = stmt.module_name
        
        # Remove aspas se presentes
        if module_name.startswith('"'): module_name = module_name[1:]
        if module_name.endswith('"'): module_name = module_name[:-1]
        if module_name.startswith("'"): module_name = module_name[1:]
        if module_name.endswith("'"): module_name = module_name[:-1]
        
        # Verifica se o módulo já foi importado
        if module_name in self.imported_modules:
            return self.imported_modules[module_name]
        
        # Tratamento especial para o módulo NajaGame
        if module_name == "NajaGame":
            try:
                # Importa o módulo pygame_bridge
                import importlib.util
                spec = importlib.util.spec_from_file_location("pygame_bridge", "modules/pygame_bridge.py")
                pygame_bridge = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(pygame_bridge)
                
                # Registra as funções exportadas no ambiente global
                for name, func in pygame_bridge.naja_exports.items():
                    self.environment.define(name, func)
                
                self.imported_modules[module_name] = True
                return True
            except Exception as e:
                raise Exception(f"Erro ao importar módulo NajaGame: {str(e)}")
        
        # Procura o módulo nos caminhos definidos
        module_found = False
        module_path = None
        
        for path in self.module_paths:
            # Tenta encontrar o módulo como arquivo .naja
            potential_path = os.path.join(path, module_name + ".naja")
            if os.path.exists(potential_path):
                module_path = potential_path
                module_found = True
                break
            
            # Tenta encontrar o módulo como arquivo .py
            potential_path = os.path.join(path, module_name + ".py")
            if os.path.exists(potential_path):
                module_path = potential_path
                module_found = True
                break
            
            # Tenta encontrar o módulo como diretório com __init__.naja
            potential_path = os.path.join(path, module_name, "__init__.naja")
            if os.path.exists(potential_path):
                module_path = potential_path
                module_found = True
                break
        
        if not module_found:
            raise Exception(f"Módulo não encontrado: {module_name}")
        
        # Carrega e executa o módulo
        try:
            with open(module_path, "r", encoding="utf-8") as f:
                module_source = f.read()
            
            # Cria um novo ambiente para o módulo
            module_env = Environment(self.globals)
            
            # Analisa e executa o código do módulo
            lexer = Lexer(module_source)
            parser = Parser(lexer)
            ast = parser.parse()
            
            # Salva o ambiente atual
            previous_env = self.environment
            self.environment = module_env
            
            try:
                # Executa o módulo
                self.interpret(ast)
                
                # Registra o módulo como importado
                self.imported_modules[module_name] = module_env
                
                # Cria um objeto de módulo para acessos qualificados
                module_obj = NajaModule(module_name, module_env)
                
                # Define o objeto de módulo no ambiente global
                self.globals.define(module_name, module_obj)
                
                # Exporta as definições do módulo para o ambiente global para compatibilidade
                for name, func in module_env.functions.items():
                    if not name.startswith("_"):  # Não exporta variáveis privadas
                        self.globals.define(name, func)
                
                # Também exporta os valores do ambiente
                for name, (value, is_const, is_flux) in module_env.values.items():
                    if not name.startswith("_"):  # Não exporta variáveis privadas
                        if name not in self.globals.functions:  # Evita duplicatas
                            self.globals.define(name, value, is_const, is_flux)
                
                return module_env
            finally:
                # Restaura o ambiente original
                self.environment = previous_env
        except Exception as e:
            raise Exception(f"Erro ao carregar módulo {module_name}: {str(e)}")
    
    def execute_WhileStatement(self, stmt):
        """Executa uma instrução while"""
        while self.is_truthy(self.evaluate(stmt.condition)):
            try:
                # Executa o corpo do loop em um novo ambiente
                self.execute_block(stmt.body, self.environment)
            except BreakException:
                break
            except ContinueException:
                continue
        return None
    
    def execute_Assignment(self, stmt):
        """Executa uma atribuição"""
        value = self.evaluate(stmt.value)
        self.environment.assign(stmt.name, value)
        return value
    
    def evaluate_ListLiteral(self, expr):
        """Avalia um literal de lista"""
        elements = []
        for element in expr.elements:
            elements.append(self.evaluate(element))
        return NajaList(elements)
    
    def evaluate_DictLiteral(self, expr):
        """Avalia um literal de dicionário"""
        items = []
        for item in expr.items:
            items.append(self.evaluate(item))
        return NajaDict(items)
    
    # Adicionando método para avaliar atribuições diretamente como expressões
    def evaluate_Assignment(self, expr):
        """Avalia uma expressão de atribuição diretamente"""
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def execute_ForStatement(self, stmt):
        """Executa uma instrução for"""
        # Cria um novo ambiente para o loop
        loop_env = Environment(self.environment)
        
        # Execute a inicialização (primeira parte do for)
        prev_env = self.environment
        self.environment = loop_env
        
        try:
            # Execute a inicialização (primeira parte do for)
            if isinstance(stmt.init, VarDeclaration):
                # Se a inicialização for uma declaração de variável
                self.execute_VarDeclaration(stmt.init)
            else:
                # Se a inicialização for uma expressão
                self.evaluate(stmt.init)
                
            # Loop principal
            while True:
                # Verifica a condição
                if not self.is_truthy(self.evaluate(stmt.condition)):
                    break
                
                try:
                    # Executa o corpo do loop
                    self.execute_block(stmt.body, loop_env)
                    
                    # Executa a expressão de atualização (terceira parte do for)
                    self.evaluate(stmt.update)
                    
                except BreakException:
                    break
                except ContinueException:
                    # Continua com a próxima iteração, ainda executando a atualização
                    self.evaluate(stmt.update)
                    continue
        finally:
            # Restaura o ambiente original
            self.environment = prev_env

    def execute_FunctionDeclaration(self, stmt):
        """Executa uma declaração de função"""
        # Cria uma nova função e a armazena no ambiente atual
        function = Function(stmt, self.environment)
        
        # Armazena a função no ambiente
        self.environment.define(stmt.name, function)
        
        return None

    def execute_ReturnStatement(self, stmt):
        """Executa uma declaração de retorno"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast_nodes import *
import os
import re
from lexer import Lexer, TokenType
from parser_naja import Parser
import sys
import importlib.util
import inspect
import types
import asyncio
import traceback
import math

class ExportedValue:
    """Wrapper para valores primitivos exportados"""
    def __init__(self, value):
        self.value = value
        self.exported = True
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return repr(self.value)
    
    def __eq__(self, other):
        if isinstance(other, ExportedValue):
            return self.value == other.value
        return self.value == other
    
    # Reenviar operações para o valor interno
    def __add__(self, other):
        if isinstance(other, ExportedValue):
            return self.value + other.value
        return self.value + other
    
    def __sub__(self, other):
        if isinstance(other, ExportedValue):
            return self.value - other.value
        return self.value - other
    
    def __mul__(self, other):
        if isinstance(other, ExportedValue):
            return self.value * other.value
        return self.value * other
    
    def __truediv__(self, other):
        if isinstance(other, ExportedValue):
            return self.value / other.value
        return self.value / other
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __bool__(self):
        return bool(self.value)

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

# Now import Environment after FluxValue is defined
from environment import Environment

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

class NajaSet:
    """Implementação de um conjunto em NajaScript"""
    def __init__(self, elements=None):
        self._elements = set(elements) if elements else set()
    
    def add(self, value):
        """Adiciona um valor ao conjunto"""
        self._elements.add(value)
        return value
    
    def remove(self, value):
        """Remove um valor do conjunto"""
        if value in self._elements:
            self._elements.remove(value)
            return value
        raise Exception(f"Valor {value} não encontrado no conjunto")
    
    def has(self, value):
        """Verifica se um valor está no conjunto"""
        return value in self._elements
    
    def clear(self):
        """Remove todos os elementos do conjunto"""
        self._elements.clear()
        return None
    
    def size(self):
        """Retorna o número de elementos no conjunto"""
        return len(self._elements)
    
    def union(self, other_set):
        """Retorna a união deste conjunto com outro"""
        if not isinstance(other_set, (NajaSet, set)):
            raise Exception("União só pode ser feita com outro conjunto")
        
        elements = other_set._elements if isinstance(other_set, NajaSet) else other_set
        return NajaSet(self._elements.union(elements))
    
    def intersection(self, other_set):
        """Retorna a interseção deste conjunto com outro"""
        if not isinstance(other_set, (NajaSet, set)):
            raise Exception("Interseção só pode ser feita com outro conjunto")
        
        elements = other_set._elements if isinstance(other_set, NajaSet) else other_set
        return NajaSet(self._elements.intersection(elements))
    
    def difference(self, other_set):
        """Retorna a diferença deste conjunto com outro"""
        if not isinstance(other_set, (NajaSet, set)):
            raise Exception("Diferença só pode ser feita com outro conjunto")
        
        elements = other_set._elements if isinstance(other_set, NajaSet) else other_set
        return NajaSet(self._elements.difference(elements))
    
    def __str__(self):
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"set({elements_str})"
    
    def __repr__(self):
        return self.__str__()

class NajaMap:
    """Implementação de um mapa em NajaScript"""
    def __init__(self, items=None):
        self._map = {}
        if items:
            for k, v in items:
                self._map[k] = v
    
    def set(self, key, value):
        """Define um valor para uma chave"""
        self._map[key] = value
        return value
    
    def get(self, key):
        """Obtém o valor associado a uma chave"""
        if key in self._map:
            return self._map[key]
        raise Exception(f"Chave {key} não encontrada no mapa")
    
    def has(self, key):
        """Verifica se uma chave está no mapa"""
        return key in self._map
    
    def delete(self, key):
        """Remove uma entrada do mapa"""
        if key in self._map:
            value = self._map[key]
            del self._map[key]
            return value
        raise Exception(f"Chave {key} não encontrada no mapa")
    
    def clear(self):
        """Remove todas as entradas do mapa"""
        self._map.clear()
        return None
    
    def size(self):
        """Retorna o número de entradas no mapa"""
        return len(self._map)
    
    def keys(self):
        """Retorna uma lista com as chaves do mapa"""
        return NajaList(self._map.keys())
    
    def values(self):
        """Retorna uma lista com os valores do mapa"""
        return NajaList(self._map.values())
    
    def entries(self):
        """Retorna uma lista de pares chave-valor"""
        return NajaList([NajaTuple([k, v]) for k, v in self._map.items()])
    
    def __str__(self):
        items = []
        for k, v in self._map.items():
            items.append(f"{k} => {v}")
        return f"map({', '.join(items)})"
    
    def __repr__(self):
        return self.__str__()

class NajaTuple:
    """Implementação de uma tupla imutável em NajaScript"""
    def __init__(self, elements=None):
        self._elements = tuple(elements) if elements else tuple()
    
    def get(self, index):
        """Obtém o elemento no índice especificado"""
        if 0 <= index < len(self._elements):
            return self._elements[index]
        raise Exception(f"Índice {index} fora dos limites da tupla")
    
    def length(self):
        """Retorna o número de elementos na tupla"""
        return len(self._elements)
    
    def __str__(self):
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"tuple({elements_str})"
    
    def __repr__(self):
        return self.__str__()

class NajaObject:
    """Representa um objeto de uma classe definida pelo usuário"""
    def __init__(self, class_name):
        self._class_name = class_name
        self._properties = {}         # {name: value}
        self._property_access = {}    # {name: access_modifier}
        self._methods = {}            # {name: Function}
        self._method_access = {}      # {name: access_modifier}
    
    def _define_property(self, name, value, access_modifier="public"):
        """Define uma propriedade no objeto com um modificador de acesso"""
        self._properties[name] = value
        self._property_access[name] = access_modifier
    
    def _define_method(self, name, method, access_modifier="public"):
        """Define um método no objeto com um modificador de acesso"""
        self._methods[name] = method
        self._method_access[name] = access_modifier
    
    def _get_property(self, name, accessing_class=None):
        """Obtém uma propriedade do objeto respeitando o controle de acesso"""
        if name in self._properties:
            # Verifica se o acesso é permitido
            if accessing_class is None or self._is_access_allowed(name, self._property_access.get(name, "public"), accessing_class):
                return self._properties[name]
            else:
                raise Exception(f"Acesso negado: Propriedade '{name}' é {self._property_access.get(name)} em '{self._class_name}'")
        raise Exception(f"Propriedade '{name}' não encontrada no objeto '{self._class_name}'")
    
    def _set_property(self, name, value, accessing_class=None):
        """Define o valor de uma propriedade respeitando o controle de acesso"""
        if name in self._properties:
            # Verifica se o acesso é permitido
            if accessing_class is None or self._is_access_allowed(name, self._property_access.get(name, "public"), accessing_class):
                self._properties[name] = value
                return value
            else:
                raise Exception(f"Acesso negado: Propriedade '{name}' é {self._property_access.get(name)} em '{self._class_name}'")
        
        # Se a propriedade não existe, a criamos (desde que estejamos dentro de um método da classe)
        if accessing_class == self._class_name:
            self._define_property(name, value, "public")
            return value
            
        raise Exception(f"Propriedade '{name}' não encontrada no objeto '{self._class_name}'")
    
    def _call_method(self, name, interpreter, arguments, accessing_class=None):
        """Chama um método do objeto respeitando o controle de acesso"""
        if name in self._methods:
            # Verifica se o acesso é permitido
            if accessing_class is None or self._is_access_allowed(name, self._method_access.get(name, "public"), accessing_class):
                method = self._methods[name]
                
                # Configura o ambiente do método com 'this'
                method_env = Environment(method.environment)
                method_env.define("this", self)
                method.environment = method_env
                
                return method(interpreter, arguments)
            else:
                raise Exception(f"Acesso negado: Método '{name}' é {self._method_access.get(name)} em '{self._class_name}'")
        
        raise Exception(f"Método '{name}' não encontrado no objeto '{self._class_name}'")
    
    def _is_access_allowed(self, member_name, access_modifier, accessing_class):
        """Verifica se o acesso a um membro é permitido com base no modificador de acesso"""
        if access_modifier == "public":
            return True
        elif access_modifier == "protected":
            # Protected pode ser acessado pela própria classe ou subclasses
            if accessing_class == self._class_name:
                return True
                
            # TODO: Verificar se accessing_class é subclasse de this._class_name
            # Esta lógica depende de como as definições de classe estão armazenadas
            
            return False
        elif access_modifier == "private":
            # Private só pode ser acessado pela própria classe
            return accessing_class == self._class_name
        
        # Por padrão, considerar como public
        return True
    
    def __str__(self):
        """Representação de string do objeto"""
        properties = []
        for name, value in self._properties.items():
            if self._property_access.get(name) == "public":
                properties.append(f"{name}: {value}")
        
        return f"{self._class_name}{{{', '.join(properties)}}}"

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
    def __init__(self, name, environment, debug=False):
        self.name = name
        self.environment = environment
        self.methods = {}
        self.exports = {}  # Dicionário para armazenar apenas os símbolos exportados
        self.export_count = 0  # Para depuração
        self.debug = debug
        
        # Mapeia as funções do ambiente para métodos do módulo
        # e identifica quais são exportadas
        for name, value in environment.values.items():
            # Verifica para funções
            if hasattr(value, 'declaration') and hasattr(value.declaration, 'exported'):
                self.methods[name] = value
                if value.declaration.exported:
                    self.exports[name] = value
                    self.export_count += 1
                    if self.debug:
                        print(f"DEBUG: Função exportada: {name}")
                        
            # Verifica para valores simples exportados
            elif hasattr(value, 'exported') and value.exported:
                self.exports[name] = value
                self.export_count += 1
                if self.debug:
                    print(f"DEBUG: Valor exportado: {name}")
        
        # Debug para informar quais símbolos foram exportados
        print(f"DEBUG: Módulo {name} exportando: {list(self.exports.keys())} ({self.export_count} itens)")
    
    def get_method(self, name):
        """Recupera um método ou valor do módulo pelo nome"""
        # Primeiro verifica nos exports se estiver usando a importação com namespace
        if name in self.exports:
            value = self.exports[name]
            # Se for um valor exportado encapsulado, retorna o valor interno
            if isinstance(value, ExportedValue):
                return value.value
            return value
            
        # Fallback para o comportamento anterior para compatibilidade
        if name in self.methods:
            return self.methods[name]
        
        # Fallback para verificar diretamente no ambiente
        try:
            value = self.environment.get(name)
            # Se for um valor exportado encapsulado, retorna o valor interno
            if isinstance(value, ExportedValue):
                return value.value
            return value
        except RuntimeError:
            raise Exception(f"Método ou atributo '{name}' não encontrado no módulo '{self.name}'")
    
    def debug_exports(self):
        """Método para depuração dos exports do módulo"""
        print(f"\nDEBUG: Detalhes do módulo '{self.name}':")
        print(f"- Total de exports: {len(self.exports)}")
        print(f"- Total de métodos: {len(self.methods)}")
        print(f"- Exports disponíveis:")
        for name, value in self.exports.items():
            value_type = type(value).__name__
            if isinstance(value, ExportedValue):
                print(f"  - {name}: ExportedValue({value.value})")
            elif hasattr(value, 'declaration') and hasattr(value.declaration, 'exported'):
                print(f"  - {name}: Function (exported={value.declaration.exported})")
            else:
                print(f"  - {name}: {value_type}")
        
        # Verificar o ambiente do módulo
        print("\nDEBUG: Ambiente do Módulo:")
        for name, value in self.environment.values.items():
            is_exported = "✓" if name in self.exports else "✗"
            print(f"  - {name}: {type(value).__name__} [exported: {is_exported}]")
            
            # Verifica se o valor tem a flag exported
            if hasattr(value, 'exported'):
                print(f"    - Tem atributo exported: {value.exported}")
            elif hasattr(value, 'declaration') and hasattr(value.declaration, 'exported'):
                print(f"    - Declaração tem exported: {value.declaration.exported}")
    
    def __str__(self):
        """Representação em string do módulo"""
        return f"<módulo '{self.name}'>"

class Interpreter:
    """Interpretador para NajaScript"""
    def __init__(self, debug=False):
        """Inicializa o interpretador"""
        self.debug = debug
        self.globals = Environment(None)
        self.environment = self.globals
        self.modules = {}  # Dicionário para módulos nativos
        self.imported_modules = {}  # Dicionário para módulos importados
        self.current_class = None
        self.current_module = None
        self.current_file = None
        self.for_loops = []
        self.loop_depth = 0
        self.jit_compiler = None
        self._setup_builtins()
        self._register_native_functions()
        self.type_registry = {}  # Registro de classes para o sistema de tipos
        self.async_event_loop = None  # Loop de eventos para async/await
        self.logger = None
    
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
        
        # Enhanced input function
        def input_func(prompt=""):
            # Get the raw input as string
            user_input = input(prompt)
            
            # Get the caller's stack frame to check for type annotations
            import inspect, re
            frame = inspect.currentframe()
            if frame:
                try:
                    caller_frame = frame.f_back
                    if caller_frame:
                        # Get the code context where input() is being called
                        context = inspect.getframeinfo(caller_frame).code_context
                        if context:
                            # Extract the line with the input call
                            call_line = context[0].strip()
                            
                            # Check for int input() pattern
                            if re.search(r'int\s+input\s*\(', call_line) or re.search(r':\s*int\s*=\s*input\s*\(', call_line):
                                try:
                                    return int(user_input)
                                except ValueError:
                                    print("Warning: Invalid integer input. Returning 0.")
                                    return 0
                            
                            # Check for float input() pattern
                            if re.search(r'float\s+input\s*\(', call_line) or re.search(r':\s*float\s*=\s*input\s*\(', call_line):
                                try:
                                    return float(user_input)
                                except ValueError:
                                    print("Warning: Invalid float input. Returning 0.0.")
                                    return 0.0
                                    
                            # Check for bool input() pattern
                            if re.search(r'bool\s+input\s*\(', call_line) or re.search(r':\s*bool\s*=\s*input\s*\(', call_line):
                                lower_input = user_input.lower().strip()
                                if lower_input in ('true', 'yes', 'y', '1'):
                                    return True
                                elif lower_input in ('false', 'no', 'n', '0'):
                                    return False
                                else:
                                    print("Warning: Invalid boolean input. Returning False.")
                                    return False
                            
                            # Check variable names for type hints
                            var_match = re.search(r'(\w+)\s*=\s*input\s*\(', call_line)
                            if var_match:
                                var_name = var_match.group(1).lower()
                                
                                # Check for numeric variable names
                                if re.match(r'(num|count|age|year|id|index|amount|total|sum|value).*', var_name):
                                    try:
                                        # First try to convert to int
                                        return int(user_input)
                                    except ValueError:
                                        try:
                                            # Try float if int fails
                                            return float(user_input)
                                        except ValueError:
                                            print(f"Warning: Expecting numeric input for '{var_name}'. Returning 0.")
                                            return 0
                                            
                                # Check for float-like variable names
                                if re.match(r'(price|cost|rate|percent|average|avg|decimal|float|weight|height).*', var_name):
                                    try:
                                        return float(user_input)
                                    except ValueError:
                                        print(f"Warning: Expecting float input for '{var_name}'. Returning 0.0.")
                                        return 0.0
                                        
                                # Check for boolean variable names
                                if re.match(r'(is|has|can|should|will|enable|allow|accept|confirm|valid|flag|toggle|status|ready|active).*', var_name):
                                    lower_input = user_input.lower().strip()
                                    if lower_input in ('true', 'yes', 'y', '1'):
                                        return True
                                    elif lower_input in ('false', 'no', 'n', '0'):
                                        return False
                                    else:
                                        print(f"Warning: Expecting boolean input for '{var_name}'. Returning False.")
                                        return False
                finally:
                    # Clean up reference to avoid memory leaks
                    del frame
            
            # Default behavior: return as string
            return user_input
            
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
        
        # Função para sleep assíncrono
        def async_sleep(ms):
            """Implementação simplificada para simular sleep assíncrono"""
            import time
            time.sleep(ms / 1000)  # Convertendo ms para segundos
            return None
        self.environment.define("asyncSleep", async_sleep)
    
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
    
        # Float function similar to int_func
        def float_func(value):
            """Converte um valor para float"""
            if isinstance(value, str):
                try:
                    return float(value)
                except ValueError:
                    return 0.0
            elif isinstance(value, (int, float)):
                return float(value)
            return 0.0
        
        self.environment.define("float", float_func)  # Adicionando função float()
    
        def bool_func(value):
            """Converte um valor para booleano"""
            if isinstance(value, str):
                lower_val = value.lower().strip()
                if lower_val in ('true', 'yes', 'y', '1'):
                    return True
                elif lower_val in ('false', 'no', 'n', '0', ''):
                    return False
                return bool(value)
            return bool(value)
        
        self.environment.define("bool", bool_func)  # Adicionando função bool()
    
    def _register_native_functions(self):
        """Registra funções nativas no ambiente"""
        # Funções de E/S
        self.environment.define("print", print)
        self.environment.define("input", input)
        
        # Funções de conversão
        self.environment.define("int", int)
        self.environment.define("float", float)
        
        # Custom bool function that handles string inputs better
        def bool_converter(value):
            if isinstance(value, str):
                lower_val = value.lower().strip()
                if lower_val in ('true', 'yes', 'y', '1'):
                    return True
                elif lower_val in ('false', 'no', 'n', '0', ''):
                    return False
            return bool(value)
        self.environment.define("bool", bool_converter)
        
        self.environment.define("str", str)
        self.environment.define("toString", str)  # Alias para str
        
        # Funções matemáticas
        self.environment.define("abs", abs)
        self.environment.define("round", round)
        self.environment.define("min", min)
        self.environment.define("max", max)
        
        # Import math functions
        self.environment.define("sqrt", math.sqrt)
        self.environment.define("pow", pow)
        self.environment.define("sin", math.sin)
        self.environment.define("cos", math.cos)
        self.environment.define("tan", math.tan)
        self.environment.define("floor", math.floor)
        self.environment.define("ceil", math.ceil)
        self.environment.define("PI", math.pi)
        self.environment.define("E", math.e)
    
    def interpret(self, ast):
        """Interpreta a árvore sintática abstrata"""
        if ast is None:
            return None
        
        self.source = ast
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
                        if self.logger:
                            self.logger.debug(f"\nDEBUG: Executando statement {i}: {statement_type}")
                        else:
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
                        if self.logger:
                            self.logger.debug(f"DEBUG: Statement {i} ({statement_type}) executada com sucesso")
                        else:
                            print(f"DEBUG: Statement {i} ({statement_type}) executada com sucesso")
                        if statement_type == "FunctionDeclaration":
                            # Verifica se a função está disponível após definição
                            function_name = statement.name
                            try:
                                func = self.environment.get(function_name)
                                if self.logger:
                                    self.logger.debug(f"DEBUG: Verificação - função '{function_name}' disponível: {type(func)}")
                                else:
                                    print(f"DEBUG: Verificação - função '{function_name}' disponível: {type(func)}")
                                print(f"DEBUG: Ambiente atual: functions={list(self.environment.functions.keys())}")
                            except Exception as e:
                                if self.logger:
                                    self.logger.error(f"DEBUG: Erro ao verificar função '{function_name}': {e}")
                                else:
                                    print(f"DEBUG: Erro ao verificar função '{function_name}': {e}")
                except Exception as e:
                    if self.debug:
                        if self.logger:
                            self.logger.error(f"DEBUG: Erro na statement {i} ({statement_type}): {e}")
                        else:
                            print(f"DEBUG: Erro na statement {i} ({statement_type}): {e}")
                        import traceback
                        traceback.print_exc()
                    raise
        
        except Exception as e:
            self.error = str(e)
            if self.debug:
                if self.logger:
                    self.logger.error(f"DEBUG: Erro durante a interpretação: {e}")
                else:
                    print(f"DEBUG: Erro durante a interpretação: {e}")
                import traceback
                traceback.print_exc()
            else:
                print(f"Erro durante a interpretação: {e}")
        
        return result
    
    def execute(self, stmt):
        """Execute uma instrução"""
        method_name = f"execute_{type(stmt).__name__}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(stmt)
        else:
            raise Exception(f"Método não implementado: {method_name}")
    
    def execute_BlockStatement(self, stmt):
        """Executa um bloco de declarações"""
        result = None
        for statement in stmt.statements:
            result = self.execute(statement)
        return result
    
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
                if self.logger:
                    self.logger.error(f"Erro de depuração: Tipo de expressão '{expr_type}' não implementado.")
                    self.logger.error(f"Expressão: {expr}")
                    self.logger.error(f"Tipo Python: {type(expr)}")
                    self.logger.error(f"Atributos: {dir(expr) if hasattr(expr, '__dict__') else 'N/A'}")
                    if isinstance(expr, str):
                        self.logger.error(f"Conteúdo da string: {expr}")
            
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
        
        # Se for uma instância de NajaObject (objetos de classe)
        elif isinstance(obj, NajaObject):
            return obj._get_property(expr.name)
        
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
        
        # Log de depuração
        if self.debug:
            if self.logger:
                self.logger.debug(f"MethodCall: objeto={obj}, método={method_name}, argumentos={arguments}")
                self.logger.debug(f"Tipo do objeto: {type(obj).__name__}")
            else:
                print(f"DEBUG: MethodCall: objeto={obj}, método={method_name}, argumentos={arguments}")
                print(f"DEBUG: Tipo do objeto: {type(obj).__name__}")
        
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
        
        # Verifica se é um objeto de uma classe definida pelo usuário
        elif isinstance(obj, NajaObject):
            try:
                # Chama o método no objeto
                return obj._call_method(method_name, self, arguments)
            except Exception as e:
                raise Exception(f"Erro ao chamar método '{method_name}' no objeto {obj._class_name}: {e}")
        
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
            
        if value is None and stmt.var_type != "any" and stmt.var_type != "void":
            # Para tipos específicos, garantir valores padrão
            if stmt.var_type == "int":
                value = 0
            elif stmt.var_type == "float":
                value = 0.0
            elif stmt.var_type == "string":
                value = ""
            elif stmt.var_type == "bool":
                value = False
            elif stmt.var_type == "list":
                value = NajaList()
            elif stmt.var_type == "dict":
                value = NajaDict()
            elif stmt.var_type == "set":
                value = NajaSet()
            elif stmt.var_type == "map":
                value = NajaMap()
            elif stmt.var_type == "tuple":
                value = NajaTuple()
        
        # Para valores primitivos como int, float, boolean, etc. não podemos
        # adicionar o atributo exported diretamente. Vamos envolver em um 
        # wrapper se for necessário exportar.
        if stmt.exported:
            if self.debug:
                print(f"DEBUG: Variável '{stmt.name}' marcada como exportada")
                print(f"DEBUG: Tipo de valor: {type(value)}")
                
            # Para objetos complexos, podemos definir o atributo diretamente
            if isinstance(value, (NajaList, NajaDict, NajaSet, NajaMap, NajaTuple, Function)):
                value.exported = True
        if self.debug:
            print(f"DEBUG: Adicionando atributo 'exported' diretamente ao valor de '{stmt.name}'")
        else:
            # Para tipos primitivos, precisamos armazenar em uma classe wrapper
            value = ExportedValue(value)
            if self.debug:
                print(f"DEBUG: Encapsulando valor '{stmt.name}' em ExportedValue")
        
        if stmt.is_const:
            self.environment.define_const(stmt.name, value)
        else:
            self.environment.define(stmt.name, value)
        
        # Verificar se a variável foi corretamente armazenada com a flag exported
        if self.debug and stmt.exported:
            stored_value = self.environment.get(stmt.name)
            if isinstance(stored_value, ExportedValue):
                print(f"DEBUG: Verificação de exportação na variável '{stmt.name}': OK (ExportedValue)")
            elif hasattr(stored_value, 'exported'):
                print(f"DEBUG: Verificação de exportação na variável '{stmt.name}': {stored_value.exported}")
            else:
                print(f"DEBUG: ERRO! Variável '{stmt.name}' não tem flag exported")
        
        return value
    
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
        """Executa uma declaração de importação de módulo"""
        module_name = stmt.module_name.strip('"').strip("'")
        
        if self.debug:
            print(f"DEBUG: Importando módulo: {module_name}")
        
        # Se o módulo já foi carregado, reutiliza
        if module_name in self.imported_modules:
            module = self.imported_modules[module_name]
            # Define o módulo no ambiente atual
            self.environment.define(module_name, module)
            
            # Para depuração
            if self.debug:
                print(f"DEBUG: Módulo {module_name} carregado do cache")
                print(f"DEBUG: Tipo do módulo: {type(module)}")
                module.debug_exports()
            
            # Quando um módulo é importado, define apenas seus símbolos exportados
            # no ambiente atual para acesso direto
            if self.debug:
                print(f"DEBUG: Exportando símbolos do módulo {module_name}:")
            
            for name, value in module.exports.items():
                if self.debug:
                    print(f"DEBUG:   - {name}: {type(value)}")
                    
                # Se for um valor encapsulado, extrai o valor interno
                if isinstance(value, ExportedValue):
                    value_to_define = value.value
                    if self.debug:
                        print(f"DEBUG:     (Desencapsulado para {type(value_to_define)})")
                else:
                    value_to_define = value
                
                # Adiciona ao ambiente atual
                self.environment.define(name, value_to_define)
                if self.debug:
                    print(f"DEBUG:     Adicionado ao ambiente: {name}")
            
            # Verificar se os valores foram realmente adicionados ao ambiente
            if self.debug:
                print("\nDEBUG: Verificando valores exportados no ambiente:")
                for name in module.exports.keys():
                    try:
                        value = self.environment.get(name)
                        print(f"DEBUG:   - {name}: {type(value)}")
                    except Exception as e:
                        print(f"DEBUG:   - {name}: ERRO! {str(e)}")
        
            return module
        
        # Tenta encontrar o módulo nos caminhos registrados
        module_path = None
        
        # Primeiro verifica se é um módulo nativo
        if module_name in self.modules:
            # Para módulos nativos, cria um módulo a partir das funções exportadas
            native_module = self.modules[module_name]
            
            # Cria um novo ambiente para o módulo
            module_env = Environment(self.globals)
            
            # Adiciona todas as funções exportadas ao ambiente do módulo
            for name, func in native_module.items():
                module_env.define(name, func)
                # Marca a função como exportada para garantir a consistência
                if hasattr(func, 'declaration'):
                    func.declaration.exported = True
            
            # Cria o objeto módulo
            module = NajaModule(module_name, module_env, self.debug)
            
            # Debug do módulo criado
            if self.debug:
                print(f"\nDEBUG: Módulo nativo {module_name} criado")
                module.debug_exports()
            
            # Armazena para reutilização
            self.imported_modules[module_name] = module
            
            # Define o módulo no ambiente atual para acesso com notação de ponto
            self.environment.define(module_name, module)
            
            # Define todos os símbolos exportados no ambiente atual para acesso direto
            for name, value in module.exports.items():
                if self.debug:
                    print(f"DEBUG:   - {name}: {type(value)}")
                    
                # Se for um valor encapsulado, extrai o valor interno
                if isinstance(value, ExportedValue):
                    value_to_define = value.value
                    if self.debug:
                        print(f"DEBUG:     (Desencapsulado para {type(value_to_define)})")
                else:
                    value_to_define = value
                
                # Adiciona ao ambiente atual
                self.environment.define(name, value_to_define)
                if self.debug:
                    print(f"DEBUG:     Adicionado ao ambiente: {name}")
            
            # Verificar se os valores foram realmente adicionados ao ambiente
            if self.debug:
                print("\nDEBUG: Verificando valores exportados no ambiente:")
                for name in module.exports.keys():
                    try:
                        value = self.environment.get(name)
                        print(f"DEBUG:   - {name}: {type(value)}")
                    except Exception as e:
                        print(f"DEBUG:   - {name}: ERRO! {str(e)}")
            
            return module
        
        # Caso contrário, procura nos caminhos de módulos
        for path in self.module_paths:
            # Tenta como módulo interno no diretório modules/
            potential_path = os.path.join(path, module_name + ".naja")
            if os.path.exists(potential_path):
                module_path = potential_path
                break
            
            # Tenta como módulo interno no diretório naja_modules/
            potential_path = os.path.join(path, "naja_modules", module_name, "index.naja")
            if os.path.exists(potential_path):
                module_path = potential_path
                break
            
            # Tenta como caminho relativo ao caminho atual
            potential_path = os.path.join(path, module_name)
            if os.path.exists(potential_path) and os.path.isdir(potential_path):
                index_path = os.path.join(potential_path, "index.naja")
                if os.path.exists(index_path):
                    module_path = index_path
                break
        
        # Verifica se encontrou o módulo
        if not module_path:
            raise Exception(f"Módulo '{module_name}' não encontrado")
        
        # Carrega o módulo
        try:
            with open(module_path, 'r', encoding='utf-8') as file:
                module_source = file.read()
                
            # Salva o arquivo atual e módulo atual
            previous_file = self.current_file
            previous_module = self.current_module
            
            # Define o arquivo atual e módulo atual
            self.current_file = module_path
            self.current_module = module_name
            
            # Cria um novo ambiente para o módulo
            module_env = Environment(self.globals)
            
            # Salva o ambiente atual e define o ambiente do módulo
            previous_env = self.environment
            self.environment = module_env
            
            try:
                # Pré-processa o código fonte (se tiver suporte a português)
                module_source = self.preprocess_source(module_source)
                
                # Cria o lexer e parser
                lexer = Lexer(module_source)
                parser = Parser(lexer)
                
                # Analisa o módulo
                ast = parser.parse()
                
                # Executa o módulo
                self.interpret(ast)
                
                # Cria o objeto módulo
                module = NajaModule(module_name, module_env, self.debug)
                
                # Debug do módulo criado
                if self.debug:
                    print(f"\nDEBUG: Módulo de arquivo {module_name} criado")
                    module.debug_exports()
                
                # Armazena para reutilização
                self.imported_modules[module_name] = module
                
                # Define o módulo no ambiente atual para acesso com notação de ponto
                previous_env.define(module_name, module)
                
                # Define apenas os símbolos exportados no ambiente atual para acesso direto
                for name, value in module.exports.items():
                    if self.debug:
                        print(f"DEBUG:   - {name}: {type(value)}")
                        
                    # Se for um valor encapsulado, extrai o valor interno
                    if isinstance(value, ExportedValue):
                        value_to_define = value.value
                        if self.debug:
                            print(f"DEBUG:     (Desencapsulado para {type(value_to_define)})")
                    else:
                        value_to_define = value
                    
                    # Adiciona ao ambiente anterior
                    previous_env.define(name, value_to_define)
                    if self.debug:
                        print(f"DEBUG:     Adicionado ao ambiente: {name}")
                
                # Verificar se os valores foram realmente adicionados ao ambiente
                if self.debug:
                    print("\nDEBUG: Verificando valores exportados no ambiente anterior:")
                    for name in module.exports.keys():
                        try:
                            value = previous_env.get(name)
                            print(f"DEBUG:   - {name}: {type(value)}")
                        except Exception as e:
                            print(f"DEBUG:   - {name}: ERRO! {str(e)}")
                
                return module
                
            finally:
                # Restaura o ambiente, arquivo e módulo anteriores
                self.environment = previous_env
                self.current_file = previous_file
                self.current_module = previous_module
                
        except Exception as e:
            raise Exception(f"Erro ao carregar módulo '{module_name}': {str(e)}")
    
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
        
        # Verifica se estamos atribuindo a uma propriedade de objeto (GetAttr)
        if isinstance(stmt.name, GetAttr):
            # Avalia o objeto
            obj = self.evaluate(stmt.name.object)
            
            # Se for um objeto NajaObject, define a propriedade
            if isinstance(obj, NajaObject):
                obj._set_property(stmt.name.name, value)
            else:
                raise Exception(f"Não é possível atribuir à propriedade '{stmt.name.name}' em um não-objeto")
        else:
            # Atribuição normal a uma variável
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
        
        # Verifica se estamos atribuindo a uma propriedade de objeto (GetAttr)
        if isinstance(expr.name, GetAttr):
            # Avalia o objeto
            obj = self.evaluate(expr.name.object)
            
            # Se for um objeto NajaObject, define a propriedade
            if isinstance(obj, NajaObject):
                obj._set_property(expr.name.name, value)
            else:
                raise Exception(f"Não é possível atribuir à propriedade '{expr.name.name}' em um não-objeto")
        else:
            # Atribuição normal a uma variável
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
        function = Function(stmt, self.environment)
        
        # Armazenar a informação de exportação
        if hasattr(stmt, 'exported') and stmt.exported:
            function.declaration.exported = True
        if self.debug:
                print(f"DEBUG: Função '{stmt.name}' marcada como exportada")
        
        self.environment.define(stmt.name, function)
        
        # Verificar se a função foi corretamente armazenada e com a flag exported
        if self.debug and hasattr(stmt, 'exported') and stmt.exported:
            stored_function = self.environment.get(stmt.name)
            if hasattr(stored_function, 'declaration') and hasattr(stored_function.declaration, 'exported'):
                print(f"DEBUG: Verificação de exportação na função '{stmt.name}': {stored_function.declaration.exported}")
                else:
                print(f"DEBUG: ERRO! Função '{stmt.name}' não tem declaração ou flag exported")
        
        return function

    def execute_ReturnStatement(self, stmt):
        """Executa uma declaração de retorno"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

    def execute_FluxDeclaration(self, stmt):
        """Executa uma declaração flux"""
        if self.debug:
            if self.logger:
                self.logger.debug(f"DEBUG: Executando flux {stmt.name}")
            else:
                print(f"DEBUG: Executando flux {stmt.name}")
        
        # Cria um valor flux
        flux_value = FluxValue(stmt.expression, self, self.environment)
        
        # Define a variável no ambiente atual
        self.environment.define(stmt.name, flux_value, False, True)
        
        return None

    def evaluate_AwaitExpression(self, expr):
        """Avalia uma expressão de await"""
        # Esta é uma implementação simplificada, sem real assincronicidade
        # Em uma implementação completa, seria necessário usar async/await do Python
        
        # Avalia a expressão sendo aguardada
        result = self.evaluate(expr.expression)
        
        if self.debug:
            if self.logger:
                self.logger.debug(f"DEBUG: Avaliando expressão await: {result}")
            else:
                print(f"DEBUG: Avaliando expressão await: {result}")
        
        # Simplesmente retorna o resultado, simulando que a espera foi concluída
        return result
        
    def evaluate_TypeCast(self, expr):
        """Avalia uma expressão de cast de tipo (tipo)expressão"""
        # Avalia a expressão que está sendo convertida
        value = self.evaluate(expr.expression)
        
        if self.debug:
            if self.logger:
                self.logger.debug(f"DEBUG: Convertendo {value} para {expr.target_type}")
            else:
                print(f"DEBUG: Convertendo {value} para {expr.target_type}")
        
        target_type = expr.target_type
        
        # Realiza a conversão com base no tipo alvo
        if target_type == "int":
            try:
                if isinstance(value, str):
                    return int(value)
                elif isinstance(value, (int, float)):
                    return int(value)
                else:
                    raise Exception(f"Não é possível converter {type(value).__name__} para int")
            except ValueError:
                return 0  # Valor padrão se a conversão falhar
        
        elif target_type == "float":
            try:
                if isinstance(value, str):
                    return float(value)
                elif isinstance(value, (int, float)):
                    return float(value)
                else:
                    raise Exception(f"Não é possível converter {type(value).__name__} para float")
            except ValueError:
                return 0.0  # Valor padrão se a conversão falhar
        
        elif target_type == "string":
            return str(value)
        
        elif target_type == "bool":
            return self.is_truthy(value)
        
        # Para outros tipos, por enquanto apenas retorna o valor original
        return value

    def evaluate_SuperExpression(self, expr):
        """Avalia uma expressão super"""
        # Buscar a classe base do objeto atual
        if not hasattr(self.environment, "get") or not self.environment.get("this"):
            raise Exception("'super' só pode ser usado dentro de métodos de classe")
        
        current_obj = self.environment.get("this")
        if not isinstance(current_obj, NajaObject) or not hasattr(current_obj, "_class_name"):
            raise Exception("'super' só pode ser usado dentro de métodos de classe")
        
        # Obter a classe base
        class_name = current_obj._class_name
        class_def = self.environment.get_class_definition(class_name)
        
        if not class_def or not class_def.extends:
            raise Exception(f"A classe '{class_name}' não tem uma classe base")
        
        base_class_name = class_def.extends
        base_class = self.environment.get_class_definition(base_class_name)
        
        if not base_class:
            raise Exception(f"Classe base '{base_class_name}' não encontrada")
        
        # Se estamos chamando um método específico
        if expr.method:
            # Encontrar o método na classe base
            method = None
            for m in base_class.methods:
                if m.name == expr.method:
                    method = m
                    break
            
            if not method:
                raise Exception(f"Método '{expr.method}' não encontrado na classe base '{base_class_name}'")
            
            # Criar um Function com o método da classe base
            function = Function(method, self.environment)
            
            # Avaliar os argumentos
            arguments = [self.evaluate(arg) for arg in expr.arguments]
            
            # Chamar o método com 'this' apontando para o objeto atual
            prev_env = self.environment
            method_env = Environment(self.environment)
            method_env.define("this", current_obj)
            
            try:
                self.environment = method_env
                return function(self, arguments)
            finally:
                self.environment = prev_env
        
        # Se estamos apenas referenciando super sem chamar um método específico
        return base_class_name

    def evaluate_NewExpression(self, expr):
        """Avalia uma expressão de instanciação de classe (new ClassName())"""
        # Obtém a definição da classe
        class_name = expr.class_name
        class_def = self.environment.get_class_definition(class_name)
        
        if not class_def:
            raise Exception(f"Classe '{class_name}' não encontrada")
        
        # Cria um novo objeto da classe
        obj = NajaObject(class_name)
        
        # Se a classe estender outra classe, herda propriedades e métodos
        if class_def.extends:
            base_class_name = class_def.extends
            base_class_def = self.environment.get_class_definition(base_class_name)
            
            if base_class_def:
                # Define as propriedades da classe base
                for prop in base_class_def.properties:
                    obj._define_property(prop.name, None if prop.value is None else self.evaluate(prop.value), prop.access_modifier)
                
                # Herda os métodos da classe base que não foram sobreescritos
                for method in base_class_def.methods:
                    if method.name != "constructor" and not any(m.name == method.name for m in class_def.methods):
                        method_func = Function(method, self.environment)
                        obj._define_method(method.name, method_func, method.access_modifier)
        
        # Define propriedades do objeto com valores padrão
        for prop in class_def.properties:
            obj._define_property(prop.name, None if prop.value is None else self.evaluate(prop.value), prop.access_modifier)
        
        # Define métodos do objeto
        for method in class_def.methods:
            if method.name != "constructor":  # Construtores são tratados separadamente
                method_func = Function(method, self.environment)
                obj._define_method(method.name, method_func, method.access_modifier)
        
        # Procura e executa o construtor
        constructor = None
        for method in class_def.methods:
            if method.name == "constructor":
                constructor = method
                break
        
        # Se a classe tiver um construtor, chama-o com os argumentos fornecidos
        if constructor:
            # Avalia os argumentos
            arguments = [self.evaluate(arg) for arg in expr.arguments]
            
            # Cria e configura a função construtora
            constructor_func = Function(constructor, self.environment)
            
            # Configura o ambiente com 'this'
            prev_env = self.environment
            constructor_env = Environment(self.environment)
            
            # Importante: Definimos 'this' no ambiente do construtor
            constructor_env.define("this", obj)
            
            # Também passamos os parâmetros do construtor para o ambiente
            for i, param in enumerate(constructor.parameters):
                if i < len(arguments):
                    # param pode ser uma tupla (tipo, nome) ou um objeto Parameter
                    if hasattr(param, 'name'):
                        param_name = param.name
                    elif isinstance(param, tuple) and len(param) > 1:
                        param_name = param[1]
                    else:
                        param_name = str(param)
                    constructor_env.define(param_name, arguments[i])
            
            try:
                # Define o ambiente temporário
                self.environment = constructor_env
                
                # Chama o construtor executando seu corpo
                self.execute_block(constructor.body, constructor_env)
            finally:
                # Restaura o ambiente
                self.environment = prev_env
            
        return obj

    def execute_ClassDeclaration(self, stmt):
        """Executa uma declaração de classe"""
        # Define a classe no ambiente
        self.environment.define_class(stmt.name, stmt)
        
        # Também define um construtor de classe (função que cria novas instâncias)
        class_constructor = lambda *args: self.create_instance(stmt.name, args)
        self.environment.define(stmt.name, class_constructor)
        
        return None
        
    def create_instance(self, class_name, args):
        """Cria uma nova instância de classe programaticamente"""
        # Criamos uma expressão NewExpression
        expr = NewExpression(class_name, args)
        
        # E avaliamos usando o método existente
        return self.evaluate_NewExpression(expr)

    def execute_CompoundAssignment(self, stmt):
        """Executa uma atribuição composta (+=, -=, etc.)"""
        # Obtém o valor atual da variável
        current_value = self.environment.get(stmt.name)
        
        # Obtém o valor a ser combinado
        new_value = self.evaluate(stmt.value)
        
        result = None
        
        # Aplica a operação composta adequada
        if stmt.operator == TokenType.PLUS_ASSIGN:
            result = current_value + new_value
        elif stmt.operator == TokenType.MINUS_ASSIGN:
            result = current_value - new_value
        elif stmt.operator == TokenType.MULTIPLY_ASSIGN:
            result = current_value * new_value
        elif stmt.operator == TokenType.DIVIDE_ASSIGN:
            result = current_value / new_value
        elif stmt.operator == TokenType.MODULO_ASSIGN:
            result = current_value % new_value
        elif stmt.operator == TokenType.POWER_ASSIGN:
            result = current_value ** new_value
        else:
            raise Exception(f"Operador de atribuição composta não suportado: {stmt.operator}")
        
        # Atribui o novo valor
        self.environment.assign(stmt.name, result)
        
        return result

    def evaluate_CompoundAssignment(self, expr):
        """Avalia uma atribuição composta como expressão"""
        # Obtém o valor atual da variável
        current_value = self.environment.get(expr.name)
        
        # Obtém o valor a ser combinado
        new_value = self.evaluate(expr.value)
        
        result = None
        
        # Aplica a operação composta adequada
        if expr.operator == TokenType.PLUS_ASSIGN:
            result = current_value + new_value
        elif expr.operator == TokenType.MINUS_ASSIGN:
            result = current_value - new_value
        elif expr.operator == TokenType.MULTIPLY_ASSIGN:
            result = current_value * new_value
        elif expr.operator == TokenType.DIVIDE_ASSIGN:
            result = current_value / new_value
        elif expr.operator == TokenType.MODULO_ASSIGN:
            result = current_value % new_value
        elif expr.operator == TokenType.POWER_ASSIGN:
            result = current_value ** new_value
        else:
            raise Exception(f"Operador de atribuição composta não suportado: {expr.operator}")
        
        # Atribui o novo valor
        self.environment.assign(expr.name, result)
        
        return result

    def evaluate_ThisExpression(self, expr):
        """Avalia a palavra-chave 'this'"""
        # Tenta obter 'this' do ambiente
        this_obj = self.environment.get("this")
        
        if this_obj is None:
            raise Exception("A palavra-chave 'this' só pode ser usada dentro de métodos de classe")
        
        return this_obj

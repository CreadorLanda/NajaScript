#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast_nodes import *

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
        # Adiciona informações de depuração
        print(f"DEBUG: Chamando função: {self.declaration.name}")
        print(f"DEBUG: Parâmetros da declaração: {self.declaration.parameters}")
        print(f"DEBUG: Argumentos fornecidos: {arguments}")
        
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
                # Aqui está o problema - param pode ser uma tupla (tipo, nome)
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
            for statement in self.declaration.body:
                interpreter.execute(statement)
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

class Environment:
    """Ambiente de execução para armazenar variáveis"""
    def __init__(self, enclosing=None):
        self.values = {}
        self.constants = set()
        self.flux_variables = set()  # Conjunto para rastrear variáveis flux
        self.enclosing = enclosing
        self.dependencies = {}  # Para rastrear quais variáveis afetam quais fluxes
        self.change_listeners = {}  # Para armazenar callbacks onChange
    
    def define(self, name, value, is_const=False, is_flux=False):
        self.values[name] = value
        if is_const:
            self.constants.add(name)
        if is_flux:
            self.flux_variables.add(name)
            # Se for um flux, precisamos analisar suas dependências
            if isinstance(value, FluxValue):
                self._register_dependencies(name, value.expression)
    
    def get(self, name):
        if name in self.values:
            value = self.values[name]
            # Se for um flux, avaliamos dinamicamente
            if name in self.flux_variables and isinstance(value, FluxValue):
                return value.evaluate()
            return value
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise Exception(f"Variável '{name}' não definida")
    
    def assign(self, name, value):
        old_value = None
        if name in self.values:
            if name in self.constants:
                raise Exception(f"Não é possível alterar uma constante: '{name}'")
            
            old_value = self.values[name]
            if name in self.flux_variables and isinstance(old_value, FluxValue):
                # Se for um flux, precisamos atualizar sua expressão
                old_value.expression = value
                # Também precisamos atualizar as dependências
                self._register_dependencies(name, value)
            else:
                self.values[name] = value
            
            # Notificar sobre a mudança
            if old_value != value:
                # Notificar onChange listeners desta variável
                self._notify_change_listeners(name, old_value, value)
                # Notificar fluxes que dependem desta variável
                self._notify_dependent_fluxes(name, old_value, value)
            
            return
        
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise Exception(f"Variável '{name}' não definida")
    
    def add_change_listener(self, var_name, callback):
        """Adiciona um listener para mudanças em uma variável"""
        if var_name not in self.change_listeners:
            self.change_listeners[var_name] = []
        self.change_listeners[var_name].append(callback)
    
    def _notify_change_listeners(self, var_name, old_value, new_value):
        """Notifica os listeners sobre mudanças em uma variável"""
        if var_name in self.change_listeners:
            for callback in self.change_listeners[var_name]:
                callback(var_name, old_value, new_value)
    
    def _notify_dependent_fluxes(self, var_name, old_value, new_value):
        """Notifica os fluxes que dependem da variável alterada"""
        if var_name in self.dependencies:
            for dependent_flux in self.dependencies[var_name]:
                if dependent_flux in self.flux_variables and dependent_flux in self.values:
                    flux_value = self.values[dependent_flux]
                    if isinstance(flux_value, FluxValue):
                        # Avalia o novo valor do flux
                        new_flux_value = flux_value.evaluate()
                        # Notifica os listeners do flux
                        flux_value.notify_change(old_value, new_flux_value)
                        # Também notifica os listeners da variável flux
                        self._notify_change_listeners(dependent_flux, old_value, new_flux_value)
    
    def _register_dependencies(self, flux_name, expression):
        """Registra as dependências de um flux baseado em sua expressão"""
        # Extrai variáveis usadas na expressão
        variables = self._extract_variables(expression)
        
        # Registra cada variável como uma dependência para este flux
        for var_name in variables:
            if var_name not in self.dependencies:
                self.dependencies[var_name] = set()
            self.dependencies[var_name].add(flux_name)
    
    def _extract_variables(self, expression):
        """Extrai os nomes de variáveis usados em uma expressão"""
        variables = set()
        
        # Função recursiva para extrair variáveis de uma expressão
        def extract_from_expr(expr):
            if isinstance(expr, Variable):
                variables.add(expr.name)
            elif isinstance(expr, BinaryOperation):
                extract_from_expr(expr.left)
                extract_from_expr(expr.right)
            elif isinstance(expr, UnaryOperation):
                extract_from_expr(expr.operand)
            elif isinstance(expr, TernaryOperator):
                extract_from_expr(expr.condition)
                extract_from_expr(expr.then_expr)
                extract_from_expr(expr.else_expr)
            elif isinstance(expr, FunctionCall):
                for arg in expr.arguments:
                    extract_from_expr(arg)
            elif isinstance(expr, MethodCall):
                extract_from_expr(expr.object)
                for arg in expr.arguments:
                    extract_from_expr(arg)
        
        # Inicia o processo de extração
        extract_from_expr(expression)
        return variables

class Interpreter:
    """Interpretador para NajaScript"""
    def __init__(self):
        self.environment = Environment()
        self.jit_compiler = None
        self._function_stats = {}  # Estatísticas de chamadas de funções
        self._jit_threshold = 10   # Limiar para compilação JIT
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
    
    def interpret(self, program):
        """Interpreta um programa NajaScript"""
        try:
            for statement in program.statements:
                self.execute(statement)
            return True
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            return False
    
    def execute(self, statement):
        """Executa uma instrução"""
        statement_type = type(statement).__name__
        method_name = f"execute_{statement_type.lower()}"
        method = getattr(self, method_name, self.execute_default)
        return method(statement)
    
    def execute_default(self, statement):
        """Método padrão para executar instruções não tratadas especificamente"""
        raise Exception(f"Tipo de instrução não implementado: {type(statement).__name__}")
    
    def execute_vardeclaration(self, stmt):
        """Executa uma declaração de variável"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        
        self.environment.define(stmt.name, value, stmt.is_const)
        return None
    
    def execute_expressionstatement(self, stmt):
        """Executa uma instrução de expressão"""
        return self.evaluate(stmt.expression)
    
    def execute_ifstatement(self, stmt):
        """Executa uma instrução if"""
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute_block(stmt.then_branch, Environment(self.environment))
        else:
            # Verifica os blocos elif
            for elif_condition, elif_body in stmt.elif_branches:
                if self.is_truthy(self.evaluate(elif_condition)):
                    self.execute_block(elif_body, Environment(self.environment))
                    return None
            
            # Se não entrou em nenhum bloco if ou elif, tenta o else
            if stmt.else_branch:
                self.execute_block(stmt.else_branch, Environment(self.environment))
        
        return None
    
    def execute_whilestatement(self, stmt):
        """Executa uma instrução while"""
        while self.is_truthy(self.evaluate(stmt.condition)):
            try:
                self.execute_block(stmt.body, Environment(self.environment))
            except BreakException:
                break
            except ContinueException:
                continue
        
        return None
    
    def execute_dowhilestatement(self, stmt):
        """Executa uma instrução do-while"""
        while True:
            try:
                self.execute_block(stmt.body, Environment(self.environment))
            except BreakException:
                break
            except ContinueException:
                pass
            
            if not self.is_truthy(self.evaluate(stmt.condition)):
                break
        
        return None
    
    def execute_forstatement(self, stmt):
        """Executa uma instrução for"""
        env = Environment(self.environment)
        
        # Inicialização
        if stmt.init:
            self.execute(stmt.init)
        
        while self.is_truthy(self.evaluate(stmt.condition)):
            try:
                # Corpo do loop
                self.execute_block(stmt.body, Environment(env))
            except BreakException:
                break
            except ContinueException:
                pass
            
            # Atualização
            self.evaluate(stmt.update)
        
        return None
    
    def execute_forinstatement(self, stmt):
        """Executa uma instrução for-in"""
        iterable = self.evaluate(stmt.iterable)
        
        # Verifica se o objeto é iterável
        if isinstance(iterable, (NajaList, NajaVector)):
            length = iterable.length()
            for i in range(length):
                env = Environment(self.environment)
                env.define(stmt.item, iterable.get(i))
                
                try:
                    self.execute_block(stmt.body, env)
                except BreakException:
                    break
                except ContinueException:
                    continue
        else:
            raise Exception(f"Objeto não é iterável: {iterable}")
        
        return None
    
    def execute_functiondeclaration(self, stmt):
        """Executa uma declaração de função"""
        print(f"DEBUG: Declaração de função: {stmt.name}")
        print(f"DEBUG: Parâmetros: {stmt.parameters}")
        
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name, function)
        
        # Inicializa estatísticas para esta função
        self._function_stats[stmt.name] = {
            'call_count': 0,
            'compiled': False
        }
        
        # Verifica se podemos pré-compilar com JIT
        if self.jit_compiler and self.jit_compiler.is_optimizable(stmt):
            # Pré-compilar funções otimizáveis
            try:
                compiled_func = self.jit_compiler.compile_function(stmt, self.environment)
                function.compiled_version = compiled_func
                self._function_stats[stmt.name]['compiled'] = True
                print(f"JIT: Função '{stmt.name}' pré-compilada para execução otimizada")
            except Exception as e:
                print(f"JIT: Erro ao pré-compilar função '{stmt.name}': {e}")
    
    def execute_returnstatement(self, stmt):
        """Executa uma instrução return"""
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)
        
        raise ReturnException(value)
    
    def execute_breakstatement(self, stmt):
        """Executa uma instrução break"""
        raise BreakException()
    
    def execute_continuestatement(self, stmt):
        """Executa uma instrução continue"""
        raise ContinueException()
    
    def execute_switchstatement(self, stmt):
        """Executa uma instrução switch"""
        value = self.evaluate(stmt.value)
        
        matched = False
        for case_value, case_body in stmt.cases:
            if self.is_equal(value, self.evaluate(case_value)):
                matched = True
                try:
                    self.execute_block(case_body, Environment(self.environment))
                except BreakException:
                    break
        
        if not matched and stmt.default:
            try:
                self.execute_block(stmt.default, Environment(self.environment))
            except BreakException:
                pass
        
        return None
    
    def execute_block(self, statements, environment):
        """Executa um bloco de instruções em um novo ambiente"""
        previous = self.environment
        try:
            self.environment = environment
            
            for statement in statements:
                self.execute(statement)
            
            return None
        finally:
            self.environment = previous
    
    def evaluate(self, expr):
        """Avalia uma expressão e retorna seu valor"""
        # Primeiro, verifica se é a própria expressão ou um tipo específico
        if expr is None:
            return None
        
        try:
            method_name = f"evaluate_{expr.__class__.__name__.lower()}"
            method = getattr(self, method_name, self.evaluate_default)
            return method(expr)
        except Exception as e:
            # Adicionar informações detalhadas de depuração
            print(f"DEBUG: Erro ao avaliar expressão do tipo {expr.__class__.__name__}")
            print(f"DEBUG: Método procurado: {method_name}")
            print(f"DEBUG: Expressão: {expr}")
            raise e
    
    def evaluate_default(self, expr):
        """Método padrão para avaliar expressões não tratadas especificamente"""
        raise Exception(f"Tipo de expressão não implementado: {type(expr).__name__}")
    
    def evaluate_binaryoperation(self, expr):
        """Avalia uma operação binária"""
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator == '+':
            # Converte automaticamente para string se um dos operandos for string
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif expr.operator == '-':
            return left - right
        elif expr.operator == '*':
            return left * right
        elif expr.operator == '/':
            if right == 0:
                raise Exception("Divisão por zero")
            return left / right
        elif expr.operator == '%':
            return left % right
        elif expr.operator == '**':
            return left ** right
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
        
        raise Exception(f"Operador não implementado: {expr.operator}")
    
    def evaluate_unaryoperation(self, expr):
        """Avalia uma operação unária"""
        right = self.evaluate(expr.operand)
        
        if expr.operator == '-':
            return -right
        elif expr.operator == '!':
            return not self.is_truthy(right)
        
        raise Exception(f"Operador unário não implementado: {expr.operator}")
    
    def evaluate_ternaryoperator(self, expr):
        """Avalia um operador ternário"""
        condition = self.evaluate(expr.condition)
        
        if self.is_truthy(condition):
            return self.evaluate(expr.then_expr)
        else:
            return self.evaluate(expr.else_expr)
    
    def evaluate_variable(self, expr):
        """Avalia uma variável"""
        return self.environment.get(expr.name)
    
    def evaluate_assignment(self, expr):
        """Avalia uma atribuição"""
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def evaluate_functioncall(self, expr):
        """Avalia uma chamada de função"""
        # Adiciona informações de depuração
        print(f"DEBUG: FunctionCall: {expr}")
        print(f"DEBUG: expr.name type: {type(expr.name)}")
        print(f"DEBUG: expr.name: {expr.name}")
        print(f"DEBUG: expr.arguments: {expr.arguments}")
        
        # Verifica se o nome da função é uma string ou uma expressão
        if isinstance(expr.name, str):
            # Se for uma string, tenta obter a função diretamente do ambiente
            try:
                callee = self.environment.get(expr.name)
            except Exception:
                raise RuntimeError(f"Função não definida: {expr.name}")
        else:
            # Se for uma expressão, avalia a expressão
            callee = self.evaluate(expr.name)
        
        # Verifica se é uma função válida
        if not isinstance(callee, Function) and not callable(callee):
            raise RuntimeError(f"Não é possível chamar {expr.name}, pois não é uma função.")
        
        # Compila a função com JIT se for chamada muitas vezes
        func_name = expr.name if isinstance(expr.name, str) else (
            expr.name.name if hasattr(expr.name, 'name') else "anônima"
        )
        
        if isinstance(func_name, str) and func_name in self._function_stats:
            self._function_stats[func_name]['call_count'] += 1
            
            # Verifica se deve usar JIT
            should_jit = (
                self.jit_compiler and 
                not self._function_stats[func_name]['compiled'] and
                self._function_stats[func_name]['call_count'] >= self._jit_threshold
            )
            
            if should_jit and isinstance(callee, Function):
                try:
                    # Compila a função usando JIT
                    compiled_func = self.jit_compiler.compile_function(
                        callee.declaration, 
                        callee.environment
                    )
                    callee.compiled_version = compiled_func
                    self._function_stats[func_name]['compiled'] = True
                    print(f"JIT: Função '{func_name}' compilada após {self._function_stats[func_name]['call_count']} chamadas")
                except Exception as e:
                    print(f"JIT: Erro ao compilar função '{func_name}': {e}")
        
        # Avalia os argumentos
        arguments = []
        if expr.arguments:
            for arg in expr.arguments:
                arguments.append(self.evaluate(arg))
        
        # Chama a função
        if isinstance(callee, Function):
            return callee(self, arguments)
        else:
            # Função nativa do Python
            return callee(*arguments)
    
    def evaluate_methodcall(self, expr):
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
    
    def evaluate_integerliteral(self, expr):
        """Avalia um literal inteiro"""
        return expr.value
    
    def evaluate_floatliteral(self, expr):
        """Avalia um literal float"""
        return expr.value
    
    def evaluate_stringliteral(self, expr):
        """Avalia uma expressão de literal de string"""
        return expr.value
    
    def evaluate_booleanliteral(self, expr):
        """Avalia um literal booleano"""
        return expr.value
    
    def evaluate_nullliteral(self, expr):
        """Avalia um literal null"""
        return None
    
    def evaluate_listliteral(self, expr):
        """Avalia um literal lista"""
        elements = [self.evaluate(element) for element in expr.elements]
        return NajaList(elements)
    
    def evaluate_dictliteral(self, expr):
        """Avalia um literal dicionário"""
        items = [self.evaluate(item) for item in expr.items]
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
    
    def execute_fluxdeclaration(self, stmt):
        """Executa uma declaração flux"""
        # Criamos um valor flux que será reavaliado dinamicamente
        flux_value = FluxValue(stmt.expression, self, self.environment)
        
        # Registramos a variável como flux no ambiente
        self.environment.define(stmt.name, flux_value, is_flux=True)
        
        return None 
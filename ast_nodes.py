#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Definição das classes para representar os nós da AST

class Node:
    """Classe base para todos os nós da AST"""
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Statement(Node):
    """Classe base para todos os tipos de declarações"""
    pass

class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class VarDeclaration(Statement):
    def __init__(self, var_type, name, value=None, is_const=False, exported=False):
        self.var_type = var_type
        self.name = name
        self.value = value
        self.is_const = is_const
        self.exported = exported

class FluxDeclaration(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression  # Expressão a ser reavaliada

class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class CompoundAssignment(Statement):
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator  # +=, -=, *=, etc.
        self.value = value

class IfStatement(Statement):
    def __init__(self, condition, then_branch, elif_branches=None, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches if elif_branches else []
        self.else_branch = else_branch

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class DoWhileStatement(Statement):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class ForStatement(Statement):
    def __init__(self, init, condition, update, body):
        self.init = init           # Inicialização (int i = 0)
        self.condition = condition  # Condição (i < 5)
        self.update = update        # Atualização (i = i + 1)
        self.body = body            # Corpo do loop

class ForInStatement(Statement):
    def __init__(self, item, iterable, body):
        self.item = item
        self.iterable = iterable
        self.body = body

class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, body, return_type=None, is_async=False, generic_params=None, exported=False):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type
        self.is_async = is_async
        self.generic_params = generic_params if generic_params else []
        self.decorators = []  # Lista de decoradores
        self.exported = exported

class ClassDeclaration(Statement):
    def __init__(self, name, methods=None, properties=None, extends=None, implements=None, generic_params=None):
        self.name = name
        self.methods = methods if methods else []
        self.properties = properties if properties else []
        self.extends = extends  # Classe base
        self.implements = implements if implements else []  # Interfaces implementadas
        self.generic_params = generic_params if generic_params else []
        self.decorators = []  # Lista de decoradores

class InterfaceDeclaration(Statement):
    def __init__(self, name, methods=None, extends=None, generic_params=None):
        self.name = name
        self.methods = methods if methods else []
        self.extends = extends if extends else []  # Interfaces estendidas
        self.generic_params = generic_params if generic_params else []

class PropertyDeclaration(Node):
    def __init__(self, name, prop_type, access_modifier="public", value=None, is_static=False):
        self.name = name
        self.prop_type = prop_type
        self.access_modifier = access_modifier  # public, private, protected
        self.value = value
        self.is_static = is_static

class MethodDeclaration(FunctionDeclaration):
    def __init__(self, name, parameters, body, return_type=None, access_modifier="public", is_static=False, is_async=False, generic_params=None):
        super().__init__(name, parameters, body, return_type, is_async, generic_params)
        self.access_modifier = access_modifier  # public, private, protected
        self.is_static = is_static

class ConstructorDeclaration(MethodDeclaration):
    def __init__(self, parameters, body, access_modifier="public"):
        super().__init__("constructor", parameters, body, None, access_modifier)

class ReturnStatement(Statement):
    def __init__(self, value=None):
        self.value = value

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class ThrowStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class TryStatement(Statement):
    def __init__(self, try_block, catch_clauses=None, finally_block=None):
        self.try_block = try_block
        self.catch_clauses = catch_clauses if catch_clauses else []
        self.finally_block = finally_block

class CatchClause(Node):
    def __init__(self, exception_type, variable_name, body):
        self.exception_type = exception_type
        self.variable_name = variable_name
        self.body = body

class SwitchStatement(Statement):
    def __init__(self, value, cases, default=None):
        self.value = value
        self.cases = cases
        self.default = default

class ImportStatement(Statement):
    def __init__(self, module_name):
        self.module_name = module_name

class MatchStatement(Statement):
    def __init__(self, expression, cases):
        self.expression = expression
        self.cases = cases  # Lista de padrões e expressões correspondentes

class MatchCase(Node):
    def __init__(self, pattern, body, condition=None):
        self.pattern = pattern  # O padrão a ser comparado
        self.body = body        # O corpo a ser executado se o padrão corresponder
        self.condition = condition  # Condição adicional opcional (when)

# Expressões
class Expression(Node):
    """Classe base para todas as expressões"""
    pass

class BinaryOperation(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOperation(Expression):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class TernaryOperator(Expression):
    def __init__(self, condition, then_expr, else_expr):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

class Variable(Expression):
    def __init__(self, name):
        self.name = name

class FunctionCall(Expression):
    def __init__(self, name, arguments=None, type_arguments=None):
        self.name = name
        self.arguments = arguments if arguments else []
        self.type_arguments = type_arguments if type_arguments else []
        self.is_await = False  # Se for uma chamada await

class MethodCall(Expression):
    def __init__(self, object, method, arguments=None, type_arguments=None):
        self.object = object  # Objeto no qual o método é chamado
        self.method = method  # Nome do método
        self.arguments = arguments if arguments else []
        self.type_arguments = type_arguments if type_arguments else []
        self.is_await = False  # Se for uma chamada await

class GetAttr(Expression):
    def __init__(self, object, name):
        self.object = object  # Objeto do qual queremos acessar um atributo
        self.name = name      # Nome do atributo

class ModuleMethodCall(Expression):
    def __init__(self, module, method, arguments=None, type_arguments=None):
        self.module = module    # Módulo no qual o método é chamado
        self.method = method    # Nome do método
        self.arguments = arguments if arguments else []
        self.type_arguments = type_arguments if type_arguments else []
        self.is_await = False  # Se for uma chamada await

class AwaitExpression(Expression):
    def __init__(self, expression):
        self.expression = expression  # Expressão a ser aguardada

class NewExpression(Expression):
    def __init__(self, class_name, arguments=None, type_arguments=None):
        self.class_name = class_name
        self.arguments = arguments if arguments else []
        self.type_arguments = type_arguments if type_arguments else []

class ThisExpression(Expression):
    pass

class SuperExpression(Expression):
    def __init__(self, method=None, arguments=None):
        self.method = method  # Método a ser chamado em super, se for uma chamada
        self.arguments = arguments if arguments else []

class SpreadExpression(Expression):
    def __init__(self, expression):
        self.expression = expression  # Expressão a ser expandida

class TypeCast(Expression):
    def __init__(self, target_type, expression):
        self.target_type = target_type  # Tipo alvo para o cast
        self.expression = expression    # Expressão a ser convertida

class Decorator(Node):
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments if arguments else []

# Literais
class Literal(Expression):
    """Classe base para todos os valores literais"""
    pass

class IntegerLiteral(Literal):
    def __init__(self, value):
        self.value = value

class FloatLiteral(Literal):
    def __init__(self, value):
        self.value = value

class StringLiteral(Literal):
    def __init__(self, value):
        self.value = value

class BooleanLiteral(Literal):
    def __init__(self, value):
        self.value = value

class NullLiteral(Literal):
    pass

class ListLiteral(Literal):
    def __init__(self, elements=None):
        self.elements = elements if elements else []

class DictLiteral(Literal):
    def __init__(self, items=None):
        self.items = items if items else []

class SetLiteral(Literal):
    def __init__(self, elements=None):
        self.elements = elements if elements else []

class MapLiteral(Literal):
    def __init__(self, items=None):
        self.items = items if items else []

class TupleLiteral(Literal):
    def __init__(self, elements=None):
        self.elements = elements if elements else []

class ExportStatement(Statement):
    def __init__(self, declaration):
        self.declaration = declaration
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

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class VarDeclaration(Statement):
    def __init__(self, var_type, name, value=None, is_const=False):
        self.var_type = var_type
        self.name = name
        self.value = value
        self.is_const = is_const

class FluxDeclaration(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression  # Expressão a ser reavaliada

class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name
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
    def __init__(self, name, parameters, body, return_type=None):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.return_type = return_type

class ReturnStatement(Statement):
    def __init__(self, value=None):
        self.value = value

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class SwitchStatement(Statement):
    def __init__(self, value, cases, default=None):
        self.value = value
        self.cases = cases
        self.default = default

class ImportStatement(Statement):
    def __init__(self, module_name):
        self.module_name = module_name

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
    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments if arguments else []

class MethodCall(Expression):
    def __init__(self, object, method, arguments=None):
        self.object = object  # Objeto no qual o método é chamado
        self.method = method  # Nome do método
        self.arguments = arguments if arguments else []

class GetAttr(Expression):
    def __init__(self, object, name):
        self.object = object  # Objeto do qual queremos acessar um atributo
        self.name = name      # Nome do atributo

class ModuleMethodCall(Expression):
    def __init__(self, module, method, arguments=None):
        self.module = module    # Módulo no qual o método é chamado
        self.method = method    # Nome do método
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
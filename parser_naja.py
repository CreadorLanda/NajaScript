#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lexer import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, message):
        raise Exception(f"Erro sintático na linha {self.current_token.line}, coluna {self.current_token.column}: {message}")
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.current_token = self.lexer.get_next_token()
            return token
        else:
            self.error(f"Esperado token do tipo {token_type}, mas encontrado {self.current_token.type}")
    
    def parse(self):
        """Ponto de entrada para o parser"""
        program = self.program()
        self.eat(TokenType.EOF)
        return program
    
    def program(self):
        """
        program : statement_list
        """
        statements = self.statement_list()
        return Program(statements)
    
    def statement_list(self):
        """
        statement_list : statement
                      | statement statement_list
        """
        statements = []
        
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        
        return statements
    
    def statement(self):
        """
        statement : var_declaration
                  | if_statement
                  | while_statement
                  | do_while_statement
                  | for_statement
                  | forin_statement
                  | function_declaration
                  | match_statement
                  | try_statement
                  | expression_statement
                  | return_statement
                  | break_statement
                  | continue_statement
                  | class_declaration
                  | interface_declaration
                  | switch_statement
                  | throw_statement
                  | import_statement
                  | flux_declaration
                  | export_statement
        """
        
        # Verificar se é uma declaração de exportação
        if self.current_token.type == TokenType.EXPORT:
            return self.export_statement()
        elif self.current_token.type == TokenType.INT or \
           self.current_token.type == TokenType.FLOAT or \
           self.current_token.type == TokenType.STRING or \
           self.current_token.type == TokenType.BOOL or \
           self.current_token.type == TokenType.VOID or \
           self.current_token.type == TokenType.ANY or \
           self.current_token.type == TokenType.DICT or \
           self.current_token.type == TokenType.LIST or \
           self.current_token.type == TokenType.VECTO or \
           self.current_token.type == TokenType.SET or \
           self.current_token.type == TokenType.MAP or \
           self.current_token.type == TokenType.TUPLE or \
           self.current_token.type == TokenType.CONST or \
           self.current_token.type == TokenType.VAR:
            return self.var_declaration()
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        elif self.current_token.type == TokenType.DO:
            return self.do_while_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.for_statement()
        elif self.current_token.type == TokenType.FORIN:
            return self.forin_statement()
        elif self.current_token.type == TokenType.FUN:
            return self.function_declaration()
        elif self.current_token.type == TokenType.CLASS:
            return self.class_declaration()
        elif self.current_token.type == TokenType.INTERFACE:
            return self.interface_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        elif self.current_token.type == TokenType.BREAK:
            return self.break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            return self.continue_statement()
        elif self.current_token.type == TokenType.SWITCH:
            return self.switch_statement()
        elif self.current_token.type == TokenType.MATCH:
            return self.match_statement()
        elif self.current_token.type == TokenType.TRY:
            return self.try_statement()
        elif self.current_token.type == TokenType.THROW:
            return self.throw_statement()
        elif self.current_token.type == TokenType.IMPORT:
            return self.import_statement()
        elif self.current_token.type == TokenType.FLUX:
            return self.flux_declaration()
        elif self.current_token.type == TokenType.ASYNC:
            token = self.eat(TokenType.ASYNC)
            if self.current_token.type == TokenType.FUN:
                return self.function_declaration(is_async=True)
            else:
                self.error("Esperado 'fun' após 'async'")
        else:
            return self.expression_statement()
    
    def var_declaration(self, exported=False):
        """
        var_declaration : type IDENTIFIER ';'
                       | type IDENTIFIER '=' expression ';'
                       | CONST type IDENTIFIER '=' expression ';'
                       | type multiple_declarations ';'
                       | type IDENTIFIER '=' IDENTIFIER '=' expression ';'
        """
        is_const = False
        if self.current_token.type == TokenType.CONST:
            is_const = True
            self.eat(TokenType.CONST)
        
        var_type = self.current_token.value
        self.eat(self.current_token.type)  # Consome o tipo (INT, FLOAT, etc.)
        
        declarations = []
        
        # Primeira variável
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Se tem atribuição
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            
            # Se for um identificador seguido de =, pode ser uma atribuição em cascata
            if self.current_token.type == TokenType.IDENTIFIER and self.lexer.peek() == '=':
                cascade_vars = [var_name]
                while self.current_token.type == TokenType.IDENTIFIER and self.lexer.peek() == '=':
                    cascade_vars.append(self.current_token.value)
                    self.eat(TokenType.IDENTIFIER)
                    self.eat(TokenType.ASSIGN)
                
                # Expressão final que será atribuída a todas variáveis
                value = self.expression()
                
                # Criamos todas as declarações
                for v in reversed(cascade_vars):
                    declarations.append(VarDeclaration(var_type, v, value, is_const, exported))
                    # Na próxima iteração, o valor a ser atribuído será a variável atual
                    value = Variable(v)
            else:
                # Atribuição simples
                value = self.expression()
                declarations.append(VarDeclaration(var_type, var_name, value, is_const, exported))
        else:
            # Sem atribuição
            declarations.append(VarDeclaration(var_type, var_name, None, is_const, exported))
        
        # Se tem vírgula, continua com mais declarações
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            value = None
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                value = self.expression()
            
            declarations.append(VarDeclaration(var_type, var_name, value, is_const, exported))
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        # Se houver mais de uma declaração, retornar um BlockStatement
        if len(declarations) > 1:
            return BlockStatement(declarations)
        else:
            return declarations[0]
    
    def expression_statement(self):
        """
        expression_statement : expression ';'
        """
        expr = self.expression()
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def if_statement(self):
        """
        if_statement : IF '(' expression ')' '{' statement_list '}'
                    | IF '(' expression ')' '{' statement_list '}' ELSE '{' statement_list '}'
                    | IF '(' expression ')' '{' statement_list '}' ELIF '(' expression ')' '{' statement_list '}' [ELSE '{' statement_list '}']
        """
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        then_branch = []
        while self.current_token.type != TokenType.RBRACE:
            then_branch.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        
        # Verifica se há um ELSE ou ELIF
        elif_branches = []
        else_branch = None
        
        if self.current_token.type == TokenType.ELIF:
            while self.current_token.type == TokenType.ELIF:
                self.eat(TokenType.ELIF)
                self.eat(TokenType.LPAREN)
                elif_condition = self.expression()
                self.eat(TokenType.RPAREN)
                self.eat(TokenType.LBRACE)
                
                elif_body = []
                while self.current_token.type != TokenType.RBRACE:
                    elif_body.append(self.statement())
                
                self.eat(TokenType.RBRACE)
                elif_branches.append((elif_condition, elif_body))
        
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            
            else_branch = []
            while self.current_token.type != TokenType.RBRACE:
                else_branch.append(self.statement())
            
            self.eat(TokenType.RBRACE)
        
        return IfStatement(condition, then_branch, elif_branches, else_branch)
    
    def while_statement(self):
        """
        while_statement : WHILE '(' expression ')' '{' statement_list '}'
        """
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        return WhileStatement(condition, body)
    
    def do_while_statement(self):
        """
        do_while_statement : DO '{' statement_list '}' WHILE '(' expression ')' ';'
        """
        self.eat(TokenType.DO)
        self.eat(TokenType.LBRACE)
        
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return DoWhileStatement(body, condition)
    
    def for_statement(self):
        """
        for_statement : FOR '(' expression ';' expression ';' expression ')' '{' statement_list '}'
        """
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        # Inicialização (pode ser uma declaração ou expressão)
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                      TokenType.BOOL, TokenType.DICT, TokenType.CONST):
            init = self.var_declaration()
        else:
            init = self.expression()
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
        
        # Condição
        condition = self.expression()
        self.eat(TokenType.SEMICOLON)
        
        # Incremento/decremento
        update = self.expression()
        self.eat(TokenType.RPAREN)
        
        # Corpo do loop
        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        return ForStatement(init, condition, update, body)
    
    def forin_statement(self):
        """
        forin_statement : FORIN '(' IDENTIFIER IN expression ')' '{' statement_list '}'
        """
        self.eat(TokenType.FORIN)
        self.eat(TokenType.LPAREN)
        
        item = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.IDENTIFIER)  # Consome "in"
        
        iterable = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        return ForInStatement(item, iterable, body)
    
    def function_declaration(self, is_async=False, exported=False):
        """
        function_declaration : FUN IDENTIFIER '(' parameter_list ')' '{' statement_list '}'
                             | FUN IDENTIFIER '(' parameter_list ')' ':' type '{' statement_list '}'
        """
        decorators = []
        while self.current_token.type == TokenType.DECORATOR:
            decorators.append(self.parse_decorator())
        
        if not is_async and self.current_token.type == TokenType.ASYNC:
            self.eat(TokenType.ASYNC)
            is_async = True
        
        self.eat(TokenType.FUN)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parâmetros genéricos
        generic_params = []
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            
            if self.current_token.type == TokenType.IDENTIFIER:
                generic_params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    if self.current_token.type == TokenType.IDENTIFIER:
                        generic_params.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
                    else:
                        self.error("Esperado identificador para parâmetro genérico")
            
            self.eat(TokenType.GT)
        
        self.eat(TokenType.LPAREN)
        parameters = []
        if self.current_token.type != TokenType.RPAREN:
            parameters = self.parameter_list()
        self.eat(TokenType.RPAREN)
        
        # Tipo de retorno opcional
        return_type = None
        if self.current_token.type == TokenType.COLON:
            self.eat(TokenType.COLON)
            return_type = self.current_token.value
            
            if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                           TokenType.DICT, TokenType.LIST, TokenType.VOID, TokenType.ANY,
                                           TokenType.SET, TokenType.MAP, TokenType.TUPLE]:
                self.eat(self.current_token.type)
            else:
                self.eat(TokenType.IDENTIFIER)  # Tipo personalizado
        
        self.eat(TokenType.LBRACE)
        
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        
        func_decl = FunctionDeclaration(name, parameters, body, return_type, is_async, generic_params, exported)
        func_decl.decorators = decorators
        return func_decl
    
    def parameter_list(self):
        """
        parameter_list : parameter
                       | parameter ',' parameter_list
                       | empty
        """
        parameters = []
        
        # Verificar se a lista de parâmetros está vazia (ou seja, se o próximo token é ')')
        if self.current_token.type == TokenType.RPAREN:
            return parameters
            
        param_type = None
        
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                     TokenType.BOOL, TokenType.DICT, TokenType.ANY):
            param_type = self.current_token.value
            self.eat(self.current_token.type)
        
        param_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        parameters.append((param_type, param_name))
        
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            
            param_type = None
            if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                         TokenType.BOOL, TokenType.DICT, TokenType.ANY):
                param_type = self.current_token.value
                self.eat(self.current_token.type)
            
            param_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            parameters.append((param_type, param_name))
        
        return parameters
    
    def return_statement(self):
        """
        return_statement : RETURN [expression] ';'
        """
        self.eat(TokenType.RETURN)
        
        if self.current_token.type in (TokenType.SEMICOLON, TokenType.RBRACE):
            value = None
        else:
            value = self.expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return ReturnStatement(value)
    
    def break_statement(self):
        """
        break_statement : BREAK ';'
        """
        self.eat(TokenType.BREAK)
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return BreakStatement()
    
    def continue_statement(self):
        """
        continue_statement : CONTINUE ';'
        """
        self.eat(TokenType.CONTINUE)
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        return ContinueStatement()
    
    def switch_statement(self):
        """
        switch_statement : SWITCH '(' expression ')' '{' case_list [DEFAULT ':' statement_list] '}'
        """
        self.eat(TokenType.SWITCH)
        self.eat(TokenType.LPAREN)
        value = self.expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        cases = []
        default_case = None
        
        while self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.CASE:
                self.eat(TokenType.CASE)
                case_value = self.expression()
                self.eat(TokenType.COLON)
                
                case_body = []
                while (self.current_token.type != TokenType.CASE and 
                       self.current_token.type != TokenType.DEFAULT and 
                       self.current_token.type != TokenType.RBRACE):
                    case_body.append(self.statement())
                
                cases.append((case_value, case_body))
            
            elif self.current_token.type == TokenType.DEFAULT:
                self.eat(TokenType.DEFAULT)
                self.eat(TokenType.COLON)
                
                default_body = []
                while self.current_token.type != TokenType.RBRACE:
                    default_body.append(self.statement())
                
                default_case = default_body
            
            else:
                self.error(f"Esperado CASE ou DEFAULT, mas encontrado {self.current_token.type}")
        
        self.eat(TokenType.RBRACE)
        return SwitchStatement(value, cases, default_case)
    
    def expression(self):
        """
        expression : assignment_expression
        """
        return self.assignment_expression()
    
    def assignment_expression(self):
        """
        assignment_expression : ternary_expression
                             | variable '=' assignment_expression
                             | variable '+=' assignment_expression
                             | variable '-=' assignment_expression
                             | variable '*=' assignment_expression
                             | variable '/=' assignment_expression
                             | variable '%=' assignment_expression
                             | variable '**=' assignment_expression
        """
        expr = self.ternary_expression()
        
        if isinstance(expr, Variable) and self.current_token.type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, 
                                                                   TokenType.MULTIPLY_ASSIGN, TokenType.DIVIDE_ASSIGN, TokenType.MODULO_ASSIGN,
                                                                   TokenType.POWER_ASSIGN]:
            name = expr.name
            operator = self.current_token.type
            self.eat(operator)
            value = self.assignment_expression()
            
            if operator == TokenType.ASSIGN:
                return Assignment(name, value)
            else:
                return CompoundAssignment(name, operator, value)
        elif isinstance(expr, GetAttr) and self.current_token.type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, 
                                                                     TokenType.MULTIPLY_ASSIGN, TokenType.DIVIDE_ASSIGN, TokenType.MODULO_ASSIGN,
                                                                     TokenType.POWER_ASSIGN]:
            obj = expr.object
            attr = expr.name
            operator = self.current_token.type
            self.eat(operator)
            value = self.assignment_expression()
            
            return Assignment(expr, value)  # Passamos o GetAttr completo
        
        return expr
    
    def ternary_expression(self):
        """
        ternary_expression : logical_or_expression
                          | logical_or_expression '?' expression ':' ternary_expression
        """
        expr = self.logical_or_expression()
        
        if self.current_token.type == TokenType.TERNARY:
            self.eat(TokenType.TERNARY)
            then_expr = self.expression()
            self.eat(TokenType.COLON)
            else_expr = self.ternary_expression()
            return TernaryOperator(expr, then_expr, else_expr)
        
        return expr
    
    def logical_or_expression(self):
        """
        logical_or_expression : logical_and_expression
                             | logical_and_expression '||' logical_or_expression
        """
        left = self.logical_and_expression()
        
        if self.current_token.type == TokenType.OR:
            op = self.current_token.value
            self.eat(TokenType.OR)
            right = self.logical_or_expression()
            return BinaryOperation(left, op, right)
        
        return left
    
    def logical_and_expression(self):
        """
        logical_and_expression : equality_expression
                              | equality_expression '&&' logical_and_expression
        """
        left = self.equality_expression()
        
        if self.current_token.type == TokenType.AND:
            op = self.current_token.value
            self.eat(TokenType.AND)
            right = self.logical_and_expression()
            return BinaryOperation(left, op, right)
        
        return left
    
    def equality_expression(self):
        """
        equality_expression : relational_expression
                           | relational_expression '==' equality_expression
                           | relational_expression '!=' equality_expression
        """
        left = self.relational_expression()
        
        while self.current_token.type in (TokenType.EQ, TokenType.NEQ):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.relational_expression()
            left = BinaryOperation(left, op, right)
        
        return left
    
    def relational_expression(self):
        """
        relational_expression : additive_expression
                             | additive_expression '<' relational_expression
                             | additive_expression '>' relational_expression
                             | additive_expression '<=' relational_expression
                             | additive_expression '>=' relational_expression
        """
        left = self.additive_expression()
        
        while self.current_token.type in (TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.additive_expression()
            left = BinaryOperation(left, op, right)
        
        return left
    
    def additive_expression(self):
        """
        additive_expression : multiplicative_expression
                           | multiplicative_expression '+' additive_expression
                           | multiplicative_expression '-' additive_expression
        """
        left = self.multiplicative_expression()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.multiplicative_expression()
            left = BinaryOperation(left, op, right)
        
        return left
    
    def multiplicative_expression(self):
        """
        multiplicative_expression : power_expression
                                 | power_expression '*' multiplicative_expression
                                 | power_expression '/' multiplicative_expression
                                 | power_expression '%' multiplicative_expression
        """
        left = self.power_expression()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.power_expression()
            left = BinaryOperation(left, op, right)
        
        return left
    
    def power_expression(self):
        """
        power_expression : primary_expression
                        | primary_expression '**' power_expression
        """
        left = self.primary_expression()
        
        if self.current_token.type == TokenType.POWER:
            op = self.current_token.value
            self.eat(TokenType.POWER)
            right = self.power_expression()
            return BinaryOperation(left, op, right)
        
        return left
    
    def primary_expression(self):
        """
        primary_expression : IDENTIFIER
                          | literal
                          | '(' expression ')'
                          | AWAIT expression
                          | function_call
                          | method_call
                          | NEW class_instantiation
                          | THIS
                          | THIS '.' IDENTIFIER
                          | THIS '.' method_call
                          | SUPER
                          | SUPER '.' method_call
                          | SPREAD expression
        """
        token = self.current_token
        
        if token.type == TokenType.AWAIT:
            self.eat(TokenType.AWAIT)
            expr = self.expression()
            return AwaitExpression(expr)
        
        elif token.type == TokenType.THIS:
            self.eat(TokenType.THIS)
            # Verifica se há um acesso a propriedade/método (this.algo)
            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                
                if self.current_token.type != TokenType.IDENTIFIER:
                    self.error(f"Esperado nome de atributo ou método após 'this.', mas encontrado {self.current_token.type}")
                
                # Captura o nome do atributo/método
                attr_or_method_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                
                # Verifica se é uma chamada de método ou acesso a atributo
                if self.current_token.type == TokenType.LPAREN:
                    # Chamada de método: this.método()
                    self.eat(TokenType.LPAREN)
                    args = []
                    
                    if self.current_token.type != TokenType.RPAREN:
                        args.append(self.expression())
                        
                        while self.current_token.type == TokenType.COMMA:
                            self.eat(TokenType.COMMA)
                            args.append(self.expression())
                    
                    self.eat(TokenType.RPAREN)
                    
                    return MethodCall(ThisExpression(), attr_or_method_name, args)
                else:
                    # Acesso a atributo: this.atributo
                    return GetAttr(ThisExpression(), attr_or_method_name)
            
            # Apenas 'this' sem acesso a propriedade
            return ThisExpression()
        
        elif token.type == TokenType.SUPER:
            self.eat(TokenType.SUPER)
            
            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                method = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                
                arguments = []
                if self.current_token.type == TokenType.LPAREN:
                    self.eat(TokenType.LPAREN)
                    if self.current_token.type != TokenType.RPAREN:
                        arguments = self.argument_list()
                    self.eat(TokenType.RPAREN)
                
                return SuperExpression(method, arguments)
            
            return SuperExpression()
        
        elif token.type == TokenType.NEW:
            self.eat(TokenType.NEW)
            return self.class_instantiation()
        
        elif token.type == TokenType.SPREAD:
            self.eat(TokenType.SPREAD)
            expr = self.expression()
            return SpreadExpression(expr)
        
        elif token.type == TokenType.IDENTIFIER or token.type == TokenType.LIST or token.type == TokenType.VECTO:
            # Captura o valor e tipo atual
            name = token.value if token.type == TokenType.IDENTIFIER else token.type.name.lower()
            self.eat(token.type)
            
            # Verifica se é um acesso a atributo ou chamada de método (objeto.atributo ou objeto.método())
            if self.current_token.type == TokenType.DOT:
                self.eat(TokenType.DOT)
                
                if self.current_token.type != TokenType.IDENTIFIER:
                    self.error(f"Esperado nome de atributo ou método após '.', mas encontrado {self.current_token.type}")
                
                attr_or_method_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                
                # Verifica se é uma chamada de método ou acesso a atributo
                if self.current_token.type == TokenType.LPAREN:
                    # Chamada de método: objeto.método() ou módulo.função()
                    self.eat(TokenType.LPAREN)
                    args = []
                    
                    if self.current_token.type != TokenType.RPAREN:
                        args.append(self.expression())
                        
                        while self.current_token.type == TokenType.COMMA:
                            self.eat(TokenType.COMMA)
                            args.append(self.expression())
                    
                    self.eat(TokenType.RPAREN)
                    
                    # Se o nome for simples, é uma chamada de método regular
                    # Se for um nome de módulo, é uma chamada de método de módulo
                    # Simplesmente usamos a classe MethodCall para ambos os casos
                    return MethodCall(Variable(name), attr_or_method_name, args)
                else:
                    # Acesso a atributo: objeto.atributo ou módulo.atributo
                    return GetAttr(Variable(name), attr_or_method_name)
            
            # Verifica se é uma chamada de função
            elif self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                args = []
                
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.expression())
                    
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.append(self.expression())
                
                self.eat(TokenType.RPAREN)
                return FunctionCall(name, args)
            
            return Variable(name)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            # Verificar se é uma expressão de cast do tipo (int)expr
            if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                           TokenType.BOOL, TokenType.ANY, TokenType.DICT, 
                                           TokenType.LIST, TokenType.SET, TokenType.MAP, 
                                           TokenType.TUPLE):
                # É um cast de tipo
                target_type = self.current_token.value
                self.eat(self.current_token.type)
                
                if self.current_token.type == TokenType.RPAREN:
                    self.eat(TokenType.RPAREN)
                    # Avaliamos a expressão que está sendo convertida
                    expr = self.primary_expression()
                    return TypeCast(target_type, expr)
            
            # Não é um cast, é apenas uma expressão entre parênteses
            expr = self.expression()
            self.eat(TokenType.RPAREN)
            return expr
        
        else:
            return self.literal()
    
    def literal(self):
        """
        literal : INTEGER
               | FLOAT_LIT
               | STRING_LIT
               | TRUE
               | FALSE
               | NULL
               | list_literal
               | dict_literal
        """
        token = self.current_token
        
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return IntegerLiteral(token.value)
        
        elif token.type == TokenType.FLOAT_LIT:
            self.eat(TokenType.FLOAT_LIT)
            return FloatLiteral(token.value)
        
        elif token.type == TokenType.STRING_LIT:
            self.eat(TokenType.STRING_LIT)
            return StringLiteral(token.value)
        
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return BooleanLiteral(True)
        
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return BooleanLiteral(False)
        
        elif token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return NullLiteral()
        
        elif token.type == TokenType.LBRACKET:
            return self.list_literal()
        
        elif token.type == TokenType.LBRACE:
            return self.dict_literal()
        
        else:
            self.error(f"Literal inesperado: {token.type}")
    
    def list_literal(self):
        """
        list_literal : '[' [expression_list] ']'
        """
        self.eat(TokenType.LBRACKET)
        elements = []
        
        if self.current_token.type != TokenType.RBRACKET:
            elements.append(self.expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                elements.append(self.expression())
        
        self.eat(TokenType.RBRACKET)
        return ListLiteral(elements)
    
    def dict_literal(self):
        """
        dict_literal : '{' [key_value_list] '}'
        """
        self.eat(TokenType.LBRACE)
        items = []
        
        if self.current_token.type != TokenType.RBRACE:
            # Para simplificar, vamos apenas aceitar uma lista de valores para dicionários
            # Você pode expandir para suportar pares chave-valor
            items.append(self.expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                items.append(self.expression())
        
        self.eat(TokenType.RBRACE)
        return DictLiteral(items)
    
    def import_statement(self):
        """
        import_statement : IMPORT STRING_LIT SEMICOLON
                         | IMPORT LBRACE (IDENTIFIER (COMMA IDENTIFIER)*)? RBRACE FROM STRING_LIT SEMICOLON
                         | IMPORT LBRACE MULTIPLY RBRACE FROM STRING_LIT SEMICOLON
        """
        self.eat(TokenType.IMPORT)
        
        # Verificar se é uma importação seletiva com chaves
        if self.current_token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)
            
            # Verificar se é importação de tudo {*}
            is_import_all = False
            import_items = []
            
            if self.current_token.type == TokenType.MULTIPLY:
                is_import_all = True
                self.eat(TokenType.MULTIPLY)
            else:
                # Lista de itens específicos para importar
                if self.current_token.type != TokenType.RBRACE:
                    import_items.append(self.current_token.value)
                    self.eat(TokenType.IDENTIFIER)
                    
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        import_items.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
            
            self.eat(TokenType.RBRACE)
            
            # Consumir FROM e o nome do módulo
            self.eat(TokenType.FROM)
            
            if self.current_token.type != TokenType.STRING_LIT:
                self.error("String literal esperado após 'from'")
                
            module_name = self.current_token.value
            self.eat(TokenType.STRING_LIT)
            
            # Semicolon opcional
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            return ImportStatement(module_name, import_items, is_import_all)
        else:
            # Importação simples: import "módulo"
            if self.current_token.type != TokenType.STRING_LIT:
                self.error("String literal esperado após 'import'")
            
            module_name = self.current_token.value
            self.eat(TokenType.STRING_LIT)
            
            # Semicolon opcional
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            return ImportStatement(module_name)
    
    def flux_declaration(self):
        """
        flux_declaration : FLUX IDENTIFIER '=' expression ';'
        """
        self.eat(TokenType.FLUX)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.ASSIGN)
        expression = self.expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            
        return FluxDeclaration(name, expression) 
    
    def argument_list(self):
        """
        argument_list : expression (',' expression)*
        """
        arguments = []
        
        # Primeiro argumento
        arguments.append(self.expression())
        
        # Argumentos adicionais separados por vírgula
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            arguments.append(self.expression())
        
        return arguments
    
    def parse_decorator(self):
        """
        decorator : '@' IDENTIFIER ['(' argument_list ')']
        """
        self.eat(TokenType.DECORATOR)  # Consome o @
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        arguments = []
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            if self.current_token.type != TokenType.RPAREN:
                arguments = self.argument_list()
            self.eat(TokenType.RPAREN)
        
        return Decorator(name, arguments)
    
    def class_declaration(self):
        """
        class_declaration : [DECORATOR]* 'class' IDENTIFIER ['<' IDENTIFIER (',' IDENTIFIER)* '>'] ['extends' IDENTIFIER] ['implements' IDENTIFIER (',' IDENTIFIER)*] '{' class_member* '}'
        """
        decorators = []
        while self.current_token.type == TokenType.DECORATOR:
            decorators.append(self.parse_decorator())
        
        self.eat(TokenType.CLASS)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parâmetros genéricos
        generic_params = []
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            
            if self.current_token.type == TokenType.IDENTIFIER:
                generic_params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    if self.current_token.type == TokenType.IDENTIFIER:
                        generic_params.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
                    else:
                        self.error("Esperado identificador para parâmetro genérico")
            
            self.eat(TokenType.GT)
        
        # Herança
        extends = None
        if self.current_token.type == TokenType.EXTENDS:
            self.eat(TokenType.EXTENDS)
            extends = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
        
        # Interfaces implementadas
        implements = []
        if self.current_token.type == TokenType.IMPLEMENTS:
            self.eat(TokenType.IMPLEMENTS)
            implements.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                implements.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.LBRACE)
        
        methods = []
        properties = []
        
        while self.current_token.type != TokenType.RBRACE:
            # Propriedade ou método
            if self.current_token.type in [TokenType.PUBLIC, TokenType.PRIVATE, TokenType.PROTECTED, 
                                         TokenType.STATIC, TokenType.DECORATOR, TokenType.CONSTRUCTOR,
                                         TokenType.ASYNC]:
                member = self.class_member()
                if isinstance(member, PropertyDeclaration):
                    properties.append(member)
                else:
                    methods.append(member)
            elif self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                          TokenType.BOOL, TokenType.DICT, TokenType.LIST, 
                                          TokenType.SET, TokenType.MAP, TokenType.TUPLE,
                                          TokenType.ANY, TokenType.IDENTIFIER]:
                # Assume-se que é uma propriedade
                properties.append(self.property_declaration())
            else:
                self.error(f"Token inesperado {self.current_token.type} na declaração de classe")
        
        self.eat(TokenType.RBRACE)
        
        class_decl = ClassDeclaration(name, methods, properties, extends, implements, generic_params)
        class_decl.decorators = decorators
        return class_decl
    
    def class_member(self):
        """
        class_member : property_declaration | method_declaration | constructor_declaration
        """
        decorators = []
        while self.current_token.type == TokenType.DECORATOR:
            decorators.append(self.parse_decorator())
        
        # Modificadores de acesso e static
        is_static = False
        access_modifier = "public"  # Valor padrão
        
        if self.current_token.type in [TokenType.PUBLIC, TokenType.PRIVATE, TokenType.PROTECTED]:
            access_modifier = self.current_token.value.lower()
            self.eat(self.current_token.type)
        
        if self.current_token.type == TokenType.STATIC:
            is_static = True
            self.eat(TokenType.STATIC)
        
        # Verifique se é um construtor
        if self.current_token.type == TokenType.CONSTRUCTOR:
            self.eat(TokenType.CONSTRUCTOR)
            
            self.eat(TokenType.LPAREN)
            parameters = self.parameter_list()
            self.eat(TokenType.RPAREN)
            
            self.eat(TokenType.LBRACE)
            body = []
            
            while self.current_token.type != TokenType.RBRACE:
                body.append(self.statement())
            
            self.eat(TokenType.RBRACE)
            
            constructor = ConstructorDeclaration(parameters, body, access_modifier)
            constructor.decorators = decorators
            return constructor
        
        # Verifique se é um método assíncrono
        is_async = False
        if self.current_token.type == TokenType.ASYNC:
            is_async = True
            self.eat(TokenType.ASYNC)
        
        # Verifique se é um método
        if self.current_token.type == TokenType.FUN:
            self.eat(TokenType.FUN)
            
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            # Parâmetros genéricos
            generic_params = []
            if self.current_token.type == TokenType.LT:
                self.eat(TokenType.LT)
                
                if self.current_token.type == TokenType.IDENTIFIER:
                    generic_params.append(self.current_token.value)
                    self.eat(TokenType.IDENTIFIER)
                    
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        if self.current_token.type == TokenType.IDENTIFIER:
                            generic_params.append(self.current_token.value)
                            self.eat(TokenType.IDENTIFIER)
                        else:
                            self.error("Esperado identificador para parâmetro genérico")
                
                self.eat(TokenType.GT)
            
            self.eat(TokenType.LPAREN)
            parameters = self.parameter_list()
            self.eat(TokenType.RPAREN)
            
            # Tipo de retorno opcional
            return_type = None
            if self.current_token.type == TokenType.COLON:
                self.eat(TokenType.COLON)
                return_type = self.current_token.value
                
                if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                              TokenType.DICT, TokenType.LIST, TokenType.VOID, TokenType.ANY,
                                              TokenType.SET, TokenType.MAP, TokenType.TUPLE]:
                    self.eat(self.current_token.type)
                else:
                    self.eat(TokenType.IDENTIFIER)  # Tipo personalizado
            
            self.eat(TokenType.LBRACE)
            
            body = []
            while self.current_token.type != TokenType.RBRACE:
                body.append(self.statement())
            
            self.eat(TokenType.RBRACE)
            
            method = MethodDeclaration(name, parameters, body, return_type, access_modifier, is_static, is_async, generic_params)
            method.decorators = decorators
            return method
        
        # Método sem a palavra-chave 'fun'
        # Verifica se o próximo token é um tipo (pode ser um tipo interno ou personalizado)
        if (self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                     TokenType.DICT, TokenType.LIST, TokenType.VOID, TokenType.ANY,
                                     TokenType.SET, TokenType.MAP, TokenType.TUPLE] or 
            self.current_token.type == TokenType.IDENTIFIER):
            
            # Salva o tipo de retorno
            return_type = self.current_token.value
            if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                         TokenType.DICT, TokenType.LIST, TokenType.VOID, TokenType.ANY,
                                         TokenType.SET, TokenType.MAP, TokenType.TUPLE]:
                self.eat(self.current_token.type)
            else:
                self.eat(TokenType.IDENTIFIER)  # Tipo personalizado
            
            # Nome do método
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            # Parâmetros do método
            self.eat(TokenType.LPAREN)
            parameters = self.parameter_list()
            self.eat(TokenType.RPAREN)
            
            # Corpo do método
            self.eat(TokenType.LBRACE)
            body = []
            
            while self.current_token.type != TokenType.RBRACE:
                body.append(self.statement())
            
            self.eat(TokenType.RBRACE)
            
            method = MethodDeclaration(name, parameters, body, return_type, access_modifier, is_static, False, [])
            method.decorators = decorators
            return method
        
        # Se não é nem construtor nem método, deve ser uma propriedade
        return self.property_declaration(decorators, access_modifier, is_static)
    
    def property_declaration(self, decorators=None, access_modifier="public", is_static=False):
        """
        property_declaration : [access_modifier] [STATIC] type IDENTIFIER ['=' expression] ';'
                             | type IDENTIFIER ['=' expression] ';'
        """
        if decorators is None:
            decorators = []
        
        # Já consumimos os modificadores de acesso e static no class_member, se estivermos sendo chamados de lá
        
        # Se a propriedade estiver sendo declarada diretamente na classe (não através de class_member)
        # então podemos ter modificadores aqui
        if self.current_token.type in [TokenType.PUBLIC, TokenType.PRIVATE, TokenType.PROTECTED]:
            access_modifier = self.current_token.value.lower()
            self.eat(self.current_token.type)
        
        if self.current_token.type == TokenType.STATIC:
            is_static = True
            self.eat(TokenType.STATIC)
        
        # Tipo da propriedade
        prop_type = self.current_token.value
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                   TokenType.DICT, TokenType.LIST, TokenType.ANY, TokenType.SET,
                                   TokenType.MAP, TokenType.TUPLE]:
            self.eat(self.current_token.type)
        else:
            self.eat(TokenType.IDENTIFIER)  # Tipo personalizado
        
        # Nome da propriedade
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Inicialização opcional
        value = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        prop = PropertyDeclaration(name, prop_type, access_modifier, value, is_static)
        prop.decorators = decorators
        return prop
    
    def interface_declaration(self):
        """
        interface_declaration : 'interface' IDENTIFIER ['<' IDENTIFIER (',' IDENTIFIER)* '>'] ['extends' IDENTIFIER (',' IDENTIFIER)*] '{' interface_member* '}'
        """
        self.eat(TokenType.INTERFACE)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parâmetros genéricos
        generic_params = []
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            
            if self.current_token.type == TokenType.IDENTIFIER:
                generic_params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    if self.current_token.type == TokenType.IDENTIFIER:
                        generic_params.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
                    else:
                        self.error("Esperado identificador para parâmetro genérico")
            
            self.eat(TokenType.GT)
        
        # Interfaces estendidas
        extends = []
        if self.current_token.type == TokenType.EXTENDS:
            self.eat(TokenType.EXTENDS)
            extends.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                extends.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.LBRACE)
        
        methods = []
        
        while self.current_token.type != TokenType.RBRACE:
            # Em uma interface, apenas métodos são permitidos (sem corpo)
            methods.append(self.interface_method())
        
        self.eat(TokenType.RBRACE)
        
        return InterfaceDeclaration(name, methods, extends, generic_params)
    
    def interface_method(self):
        """
        interface_method : ['async'] 'fun' IDENTIFIER ['<' IDENTIFIER (',' IDENTIFIER)* '>'] '(' parameter_list ')' [':' type] ';'
        """
        # Verifique se é um método assíncrono
        is_async = False
        if self.current_token.type == TokenType.ASYNC:
            is_async = True
            self.eat(TokenType.ASYNC)
        
        self.eat(TokenType.FUN)
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parâmetros genéricos
        generic_params = []
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            
            if self.current_token.type == TokenType.IDENTIFIER:
                generic_params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
                
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    if self.current_token.type == TokenType.IDENTIFIER:
                        generic_params.append(self.current_token.value)
                        self.eat(TokenType.IDENTIFIER)
                    else:
                        self.error("Esperado identificador para parâmetro genérico")
            
            self.eat(TokenType.GT)
        
        self.eat(TokenType.LPAREN)
        parameters = self.parameter_list()
        self.eat(TokenType.RPAREN)
        
        # Tipo de retorno opcional
        return_type = None
        if self.current_token.type == TokenType.COLON:
            self.eat(TokenType.COLON)
            return_type = self.current_token.value
            
            if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                          TokenType.DICT, TokenType.LIST, TokenType.VOID, TokenType.ANY,
                                          TokenType.SET, TokenType.MAP, TokenType.TUPLE]:
                self.eat(self.current_token.type)
            else:
                self.eat(TokenType.IDENTIFIER)  # Tipo personalizado
        
        # Em interfaces, métodos não têm corpo, apenas assinatura seguida de ponto e vírgula
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        # Criamos um MethodDeclaration sem corpo (body = None)
        return MethodDeclaration(name, parameters, None, return_type, "public", False, is_async, generic_params)
    
    def try_statement(self):
        """
        try_statement : 'try' '{' statement_list '}' catch_clause* ['finally' '{' statement_list '}']
        """
        self.eat(TokenType.TRY)
        self.eat(TokenType.LBRACE)
        
        # Bloco try
        try_block = []
        while self.current_token.type != TokenType.RBRACE:
            try_block.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        
        # Cláusulas catch
        catch_clauses = []
        while self.current_token.type == TokenType.CATCH:
            catch_clauses.append(self.catch_clause())
        
        # Bloco finally opcional
        finally_block = None
        if self.current_token.type == TokenType.FINALLY:
            self.eat(TokenType.FINALLY)
            self.eat(TokenType.LBRACE)
            
            finally_block = []
            while self.current_token.type != TokenType.RBRACE:
                finally_block.append(self.statement())
            
            self.eat(TokenType.RBRACE)
        
        return TryStatement(try_block, catch_clauses, finally_block)
    
    def catch_clause(self):
        """
        catch_clause : 'catch' '(' [type] IDENTIFIER ')' '{' statement_list '}'
        """
        self.eat(TokenType.CATCH)
        self.eat(TokenType.LPAREN)
        
        # Tipo da exceção opcional
        exception_type = None
        if self.current_token.type in [TokenType.IDENTIFIER, TokenType.ANY]:
            exception_type = self.current_token.value
            self.eat(self.current_token.type)
        
        # Nome da variável
        variable_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        # Corpo do catch
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        
        return CatchClause(exception_type, variable_name, body)
    
    def throw_statement(self):
        """
        throw_statement : 'throw' expression ';'
        """
        self.eat(TokenType.THROW)
        expression = self.expression()
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return ThrowStatement(expression)
    
    def match_statement(self):
        """
        match_statement : 'match' expression '{' match_case* '}'
        """
        self.eat(TokenType.MATCH)
        expression = self.expression()
        
        self.eat(TokenType.LBRACE)
        
        cases = []
        while self.current_token.type != TokenType.RBRACE:
            cases.append(self.match_case())
        
        self.eat(TokenType.RBRACE)
        
        return MatchStatement(expression, cases)
    
    def match_case(self):
        """
        match_case : expression [WHEN expression] '=>' (expression | '{' statement_list '}') ';'
        """
        pattern = self.expression()
        
        # Condição when opcional
        condition = None
        if self.current_token.type == TokenType.WHEN:
            self.eat(TokenType.WHEN)
            condition = self.expression()
        
        # Operador =>
        self.eat(TokenType.ARROW)
        
        # Corpo do case
        body = None
        if self.current_token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)
            
            body = []
            while self.current_token.type != TokenType.RBRACE:
                body.append(self.statement())
            
            self.eat(TokenType.RBRACE)
        else:
            # Se não for um bloco, é uma única expressão
            body = [ExpressionStatement(self.expression())]
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return MatchCase(pattern, body, condition)
    
    def class_instantiation(self):
        """
        class_instantiation : IDENTIFIER ['<' type_argument_list '>'] '(' [argument_list] ')'
        """
        class_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # Parâmetros de tipo genérico opcionais
        type_arguments = []
        if self.current_token.type == TokenType.LT:
            self.eat(TokenType.LT)
            
            # Lista de argumentos de tipo
            if self.current_token.type != TokenType.GT:
                type_arguments = self.type_argument_list()
            
            self.eat(TokenType.GT)
        
        # Parâmetros do construtor
        self.eat(TokenType.LPAREN)
        arguments = []
        
        if self.current_token.type != TokenType.RPAREN:
            arguments = self.argument_list()
        
        self.eat(TokenType.RPAREN)
        
        return NewExpression(class_name, arguments, type_arguments)
    
    def type_argument_list(self):
        """
        type_argument_list : type (',' type)*
        """
        type_args = []
        
        type_arg = self.parse_type()
        type_args.append(type_arg)
        
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            type_arg = self.parse_type()
            type_args.append(type_arg)
        
        return type_args
    
    def parse_type(self):
        """
        type : INT | FLOAT | STRING | BOOL | DICT | LIST | SET | MAP | TUPLE | ANY | IDENTIFIER
        """
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL, 
                                     TokenType.DICT, TokenType.LIST, TokenType.SET, TokenType.MAP, 
                                     TokenType.TUPLE, TokenType.ANY]:
            type_name = self.current_token.value
            self.eat(self.current_token.type)
            return type_name
        else:
            type_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            return type_name
    
    def export_statement(self):
        """
        export_statement : EXPORT function_declaration
                         | EXPORT var_declaration
                         | EXPORT CONST type IDENTIFIER '=' expression ';'
                         | EXPORT IDENTIFIER ';'
        """
        self.eat(TokenType.EXPORT)
        
        if self.current_token.type == TokenType.FUN:
            return self.function_declaration(exported=True)
        elif self.current_token.type == TokenType.CONST:
            # Nova sintaxe: export const tipo nome = valor;
            is_const = True
            self.eat(TokenType.CONST)
            
            var_type = self.current_token.value
            self.eat(self.current_token.type)  # Consome o tipo (INT, FLOAT, etc.)
            
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            self.eat(TokenType.ASSIGN)
            value = self.expression()
            
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            return VarDeclaration(var_type, var_name, value, is_const, exported=True)
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Nova sintaxe: export identificador;
            # Isso permite exportar uma variável/constante já declarada
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            return ExportStatement(var_name)
        elif self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                        TokenType.BOOL, TokenType.VOID, TokenType.ANY, 
                                        TokenType.DICT, TokenType.LIST, TokenType.VECTO,
                                        TokenType.SET, TokenType.MAP, TokenType.TUPLE,
                                        TokenType.VAR]:
            return self.var_declaration(exported=True)
        else:
            self.error("Expected 'fun', 'const', a type, or an identifier after 'export'") 
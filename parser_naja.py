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
        statement : declaration_statement
                  | expression_statement
                  | if_statement
                  | while_statement
                  | do_while_statement
                  | for_statement
                  | forin_statement
                  | function_declaration
                  | return_statement
                  | break_statement
                  | continue_statement
                  | switch_statement
                  | import_statement
                  | flux_declaration
        """
        if self.current_token.type == TokenType.INT or \
           self.current_token.type == TokenType.FLOAT or \
           self.current_token.type == TokenType.STRING or \
           self.current_token.type == TokenType.BOOL or \
           self.current_token.type == TokenType.DICT or \
           self.current_token.type == TokenType.LIST or \
           self.current_token.type == TokenType.ANY or \
           self.current_token.type == TokenType.CONST:
            return self.declaration_statement()
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
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        elif self.current_token.type == TokenType.BREAK:
            return self.break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            return self.continue_statement()
        elif self.current_token.type == TokenType.SWITCH:
            return self.switch_statement()
        elif self.current_token.type == TokenType.IMPORT:
            return self.import_statement()
        elif self.current_token.type == TokenType.FLUX:
            return self.flux_declaration()
        else:
            return self.expression_statement()
    
    def declaration_statement(self):
        """
        declaration_statement : type IDENTIFIER ';'
                             | type IDENTIFIER '=' expression ';'
                             | CONST type IDENTIFIER '=' expression ';'
        """
        is_const = False
        if self.current_token.type == TokenType.CONST:
            is_const = True
            self.eat(TokenType.CONST)
        
        var_type = self.current_token.value
        self.eat(self.current_token.type)  # Consome o tipo (INT, FLOAT, etc.)
        
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.expression()
        else:
            value = None
        
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
        
        return VarDeclaration(var_type, var_name, value, is_const)
    
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
            init = self.declaration_statement()
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
    
    def function_declaration(self):
        """
        function_declaration : [type] FUN IDENTIFIER '(' [parameter_list] ')' '{' statement_list '}'
        """
        return_type = None
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING, 
                                     TokenType.BOOL, TokenType.DICT, TokenType.VOID, TokenType.ANY):
            return_type = self.current_token.value
            self.eat(self.current_token.type)
        
        self.eat(TokenType.FUN)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.LPAREN)
        parameters = []
        
        if self.current_token.type != TokenType.RPAREN:
            parameters = self.parameter_list()
        
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        
        self.eat(TokenType.RBRACE)
        return FunctionDeclaration(name, parameters, body, return_type)
    
    def parameter_list(self):
        """
        parameter_list : parameter
                       | parameter ',' parameter_list
        """
        parameters = []
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
                             | IDENTIFIER '=' assignment_expression
        """
        expr = self.ternary_expression()
        
        if isinstance(expr, Variable) and self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            right = self.assignment_expression()
            return Assignment(expr.name, right)
        
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
        primary_expression : literal
                          | IDENTIFIER
                          | '(' expression ')'
                          | function_call
                          | IDENTIFIER '.' IDENTIFIER  # Acesso a atributo (módulo.atributo)
                          | IDENTIFIER '.' IDENTIFIER '(' arguments ')'  # Chamada de método (objeto.método() ou módulo.função())
        """
        token = self.current_token
        
        if token.type == TokenType.IDENTIFIER or token.type == TokenType.LIST or token.type == TokenType.VECTO:
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
        """
        self.eat(TokenType.IMPORT)
        
        # O módulo deve ser um literal de string
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, auto

class TokenType(Enum):
    # Palavras-chave
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    DICT = auto()
    NULL = auto()
    VOID = auto()
    CONST = auto()
    FUN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    FOR = auto()
    FORIN = auto()
    WHILE = auto()
    DO = auto()
    BREAK = auto()
    CONTINUE = auto()
    SWITCH = auto()
    CASE = auto()
    DEFAULT = auto()
    VECTO = auto()
    LIST = auto()
    TYPE = auto()
    FLUX = auto()
    ANY = auto()  # Novo token para o tipo any
    
    # Literais
    INTEGER = auto()
    FLOAT_LIT = auto()
    STRING_LIT = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Operadores
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    TERNARY = auto()
    
    # Delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    
    # Outros
    IDENTIFIER = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value=None, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', ln={self.line}, col={self.column})"
    
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, source):
        # Remover BOM UTF-8 se presente
        if source and len(source) >= 1 and source[0] == '\ufeff':
            self.source = source[1:]
            print("BOM UTF-8 detectado e removido")
        else:
            self.source = source
            
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if self.source else None
        
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING,
            'bool': TokenType.BOOL,
            'dict': TokenType.DICT,
            'null': TokenType.NULL,
            'void': TokenType.VOID,
            'const': TokenType.CONST,
            'fun': TokenType.FUN,
            'return': TokenType.RETURN,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'elif': TokenType.ELIF,
            'for': TokenType.FOR,
            'forin': TokenType.FORIN,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'switch': TokenType.SWITCH,
            'case': TokenType.CASE,
            'default': TokenType.DEFAULT,
            'vecto': TokenType.VECTO,
            'list': TokenType.LIST,
            'type': TokenType.TYPE,
            'flux': TokenType.FLUX,
            'any': TokenType.ANY,  # Adicionando any às palavras-chave
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }
    
    def advance(self):
        self.position += 1
        self.column += 1
        
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
    
    def peek(self, n=1):
        peek_pos = self.position + n
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        # Pula comentários de linha única (#)
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def number(self):
        start_column = self.column
        result = ''
        is_float = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:  # Já encontrou um ponto decimal
                    break
                is_float = True
            result += self.current_char
            self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT_LIT, float(result), self.line, start_column)
        else:
            return Token(TokenType.INTEGER, int(result), self.line, start_column)
    
    def string(self):
        start_column = self.column
        result = ''
        quote = self.current_char  # ' ou "
        self.advance()  # Consome a aspa de abertura
        
        while self.current_char is not None and self.current_char != quote:
            # Processar sequências de escape como \n, \t, etc.
            if self.current_char == '\\' and self.peek() is not None:
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == quote:
                    result += quote
                else:
                    result += '\\' + self.current_char
            else:
                result += self.current_char
            self.advance()
        
        if self.current_char is None:
            raise Exception(f"String não fechada na linha {self.line}")
        
        self.advance()  # Consome a aspa de fechamento
        return Token(TokenType.STRING_LIT, result, self.line, start_column)
    
    def identifier(self):
        start_column = self.column
        result = ''
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Palavras-chave especiais que também podem ser identificadores em contextos diferentes
        special_tokens = {
            'list': TokenType.LIST,
            'vecto': TokenType.VECTO
        }
        
        # Verifica se é uma palavra-chave especial ou uma palavra-chave normal
        if result in special_tokens and self.current_char == '(':
            # Se for seguido por parêntese, é uma chamada de função 
            # (list(), vecto())
            return Token(special_tokens[result], result, self.line, start_column)
        elif result in self.keywords:
            # Se for uma palavra-chave normal
            return Token(self.keywords[result], result, self.line, start_column)
        else:
            # Caso contrário é um identificador normal
            return Token(TokenType.IDENTIFIER, result, self.line, start_column)
    
    def get_next_token(self):
        while self.current_char is not None:
            # Espaços em branco
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Comentários
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Identificadores e palavras-chave
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Números
            if self.current_char.isdigit():
                return self.number()
            
            # Strings
            if self.current_char in ('"', "'"):
                return self.string()
            
            # Operadores e delimitadores
            if self.current_char == '+':
                column = self.column
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, column)
            
            if self.current_char == '-':
                column = self.column
                self.advance()
                if self.current_char == '>' and self.peek() == ' ':
                    self.advance()
                    return Token(TokenType.ARROW, '->', self.line, column)
                return Token(TokenType.MINUS, '-', self.line, column)
            
            if self.current_char == '*':
                column = self.column
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    return Token(TokenType.POWER, '**', self.line, column)
                return Token(TokenType.MULTIPLY, '*', self.line, column)
            
            if self.current_char == '/':
                column = self.column
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, column)
            
            if self.current_char == '%':
                column = self.column
                self.advance()
                return Token(TokenType.MODULO, '%', self.line, column)
            
            if self.current_char == '=':
                column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, column)
                return Token(TokenType.ASSIGN, '=', self.line, column)
            
            if self.current_char == '!':
                column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NEQ, '!=', self.line, column)
                raise Exception(f"Caractere inválido '!' na linha {self.line}, coluna {column}")
            
            if self.current_char == '<':
                column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, '<=', self.line, column)
                return Token(TokenType.LT, '<', self.line, column)
            
            if self.current_char == '>':
                column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, '>=', self.line, column)
                return Token(TokenType.GT, '>', self.line, column)
            
            if self.current_char == '?':
                column = self.column
                self.advance()
                return Token(TokenType.TERNARY, '?', self.line, column)
            
            if self.current_char == ':':
                column = self.column
                self.advance()
                return Token(TokenType.COLON, ':', self.line, column)
            
            if self.current_char == '(':
                column = self.column
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, column)
            
            if self.current_char == ')':
                column = self.column
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, column)
            
            if self.current_char == '{':
                column = self.column
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, column)
            
            if self.current_char == '}':
                column = self.column
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, column)
            
            if self.current_char == '[':
                column = self.column
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line, column)
            
            if self.current_char == ']':
                column = self.column
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line, column)
            
            if self.current_char == ';':
                column = self.column
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line, column)
            
            if self.current_char == ',':
                column = self.column
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, column)
            
            if self.current_char == '.':
                column = self.column
                self.advance()
                return Token(TokenType.DOT, '.', self.line, column)
            
            # Se chegarmos aqui, há um caractere desconhecido
            raise Exception(f"Caractere inválido '{self.current_char}' na linha {self.line}, coluna {self.column}")
        
        # Fim do arquivo
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self):
        """Retorna todos os tokens de uma vez"""
        tokens = []
        token = self.get_next_token()
        
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        
        tokens.append(token)  # Adiciona o token EOF
        return tokens 
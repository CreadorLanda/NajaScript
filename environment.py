#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Environment:
    """Ambiente de execução para armazenar variáveis e funções"""
    def __init__(self, enclosing=None):
        self.values = {}  # Armazena valores das variáveis
        self.constants = set()  # Conjunto para rastrear variáveis constantes
        self.enclosing = enclosing  # Ambiente envolvente para escopo
        self.functions = {}  # Armazena funções separadamente
    
    def define(self, name, value, is_const=False, is_flux=False):
        """Define uma variável no ambiente atual"""
        if is_const and name in self.values:
            # Não permite redefinir constantes
            raise RuntimeError(f"Não é possível redefinir a constante '{name}'")
        
        # Se for uma função, armazena separadamente
        if callable(value):
            self.functions[name] = value
        else:
            self.values[name] = (value, is_const, is_flux)
            
            if is_const:
                self.constants.add(name)
    
    def get(self, name):
        """Obtém o valor de uma variável pelo nome"""
        # Primeiro procura nas funções
        if name in self.functions:
            return self.functions[name]
        
        # Depois procura nas variáveis
        if name in self.values:
            return self.values[name][0]  # Retorna apenas o valor
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise RuntimeError(f"Variável '{name}' não definida")
    
    def assign(self, name, value):
        """Atribui um novo valor a uma variável existente"""
        # Não permite atribuir a funções
        if name in self.functions:
            raise RuntimeError(f"Não é possível reatribuir a função '{name}'")
        
        if name in self.values:
            # Verifica se é uma constante
            if name in self.constants:
                raise RuntimeError(f"Não é possível alterar o valor da constante '{name}'")
            
            # Mantém as propriedades (const, flux) da variável
            is_const, is_flux = self.values[name][1:]
            self.values[name] = (value, is_const, is_flux)
            return True
        
        if self.enclosing:
            return self.enclosing.assign(name, value)
        
        raise RuntimeError(f"Variável '{name}' não definida") 
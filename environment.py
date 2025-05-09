#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Environment:
    """Ambiente de execução para armazenar variáveis e funções"""
    def __init__(self, enclosing=None):
        self.values = {}        # Armazena valores diretos
        self.value_info = {}    # Armazena metadados sobre valores (is_const, is_flux)
        self.functions = {}     # {name: Function}
        self.classes = {}       # {name: ClassDefinition}
        self.modules = {}       # {name: Module}
        self.enclosing = enclosing
        self.change_listeners = {}  # {name: [listener_callbacks]}
        self.interpreter = None
    
    def define(self, name, value, is_const=False, is_flux=False):
        """Define uma variável no ambiente atual"""
        # Se for uma Função, armazená-la no dicionário de funções
        if callable(value) and not isinstance(value, (int, float, str, bool)):
            self.functions[name] = value
            return
        
        # Se for um módulo, armazená-lo no dicionário de módulos
        if hasattr(value, 'exports') and hasattr(value, 'get_method'):
            self.modules[name] = value
            self.values[name] = value  # Também armazenamos nos valores para compatibilidade
            return

        # Caso especial para valores flux (identifica pela presença de métodos específicos)
        if hasattr(value, 'evaluate') and hasattr(value, 'notify_change'):
            is_flux = True
            
        # Caso contrário, armazená-la no dicionário de valores
        self.values[name] = value
        self.value_info[name] = (is_const, is_flux)
    
    def define_const(self, name, value):
        """Define uma constante no ambiente atual"""
        # Apenas um wrapper em torno de define com is_const=True
        return self.define(name, value, is_const=True)
    
    def define_class(self, name, class_definition):
        """Define uma classe no ambiente atual"""
        self.classes[name] = class_definition
    
    def get_class_definition(self, name):
        """Obtém a definição de uma classe pelo nome"""
        if name in self.classes:
            return self.classes[name]
        
        if self.enclosing:
            return self.enclosing.get_class_definition(name)
            
        return None
    
    def get(self, name):
        """Obtém o valor de uma variável, função ou módulo pelo nome"""
        # Primeiro verifica nas funções
        if name in self.functions:
            return self.functions[name]
        
        # Depois verifica nos módulos
        if name in self.modules:
            return self.modules[name]
            
        # Depois verifica nos valores
        if name in self.values:
            value = self.values[name]
            is_const, is_flux = self.value_info.get(name, (False, False))
            
            if is_flux:
                # Se for um valor flux, avalia seu valor atual
                return value.evaluate()
            return value
            
        # Se não encontrar no ambiente atual, procura no ambiente pai
        if self.enclosing:
            return self.enclosing.get(name)
        
        # Caso especial para 'this' quando usado fora de um método de classe
        if name == "this":
            return None
            
        raise RuntimeError(f"Variável ou função '{name}' não definida.")
    
    def assign(self, name, value):
        """Atribui um valor a uma variável existente"""
        # Verifica se a variável existe no ambiente atual
        if name in self.values:
            current_value = self.values[name]
            is_const, is_flux = self.value_info.get(name, (False, False))
            
            # Verifica se é uma constante
            if is_const:
                raise RuntimeError(f"Não é possível reatribuir valor à constante '{name}'.")
                
            # Se for um valor flux, notifica os listeners sobre a mudança
            if is_flux:
                old_value = current_value.evaluate()
                self.values[name] = value
                new_value = value
                
                # Notifica os listeners
                self._notify_change_listeners(name, old_value, new_value)
                
                return value
                
            # Armazena o novo valor
            old_value = current_value
            self.values[name] = value
            
            # Notifica os listeners sobre a mudança
            self._notify_change_listeners(name, old_value, value)
            
            return value
            
        # Se não existir no ambiente atual, procura no ambiente pai
        if self.enclosing:
            return self.enclosing.assign(name, value)
            
        raise RuntimeError(f"Variável '{name}' não definida.")
    
    def is_defined(self, name):
        """Verifica se uma variável, função ou módulo está definida"""
        return (name in self.values or name in self.functions 
                or name in self.modules
                or (self.enclosing and self.enclosing.is_defined(name)))
    
    def add_change_listener(self, name, callback):
        """Adiciona um listener para mudanças em uma variável"""
        if name not in self.change_listeners:
            self.change_listeners[name] = []
        self.change_listeners[name].append(callback)
    
    def _notify_change_listeners(self, name, old_value, new_value):
        """Notifica todos os listeners sobre uma mudança em uma variável"""
        if name in self.change_listeners:
            for callback in self.change_listeners[name]:
                callback(name, old_value, new_value)
    
    def mark_as_exported(self, name):
        """Marca um símbolo como exportado para que possa ser importado por outros módulos"""
        # Se for uma função, marcar o atributo exported na declaração
        if name in self.functions:
            func = self.functions[name]
            if hasattr(func, 'declaration'):
                func.declaration.exported = True
        
        # Criar um registro de exports se ainda não existir
        if not hasattr(self, 'exports'):
            self.exports = set()
        
        # Adicionar o nome ao conjunto de exports
        self.exports.add(name)
    
    def can_access(self, property_name, access_modifier, current_class, accessing_class):
        """Verifica se uma propriedade/método pode ser acessada com base no modificador de acesso"""
        if access_modifier == "public":
            return True
        elif access_modifier == "protected":
            # Protected pode ser acessado pela própria classe ou subclasses
            if current_class == accessing_class:
                return True
                
            # Verifica se accessing_class é subclasse de current_class
            class_def = self.get_class_definition(accessing_class)
            while class_def and class_def.extends:
                if class_def.extends == current_class:
                    return True
                class_def = self.get_class_definition(class_def.extends)
                
            return False
        elif access_modifier == "private":
            # Private só pode ser acessado pela própria classe
            return current_class == accessing_class
        
        # Por padrão, considerar como public
        return True 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o método problemático
content = content.replace(
    'def execute_WhileStatement(self, stmt):\n        """Executa uma declaração while"""\n        result = None\n        \n        try:\n        while self.is_truthy(self.evaluate(stmt.condition)):',
    'def execute_WhileStatement(self, stmt):\n        """Executa uma declaração while"""\n        result = None\n        \n        try:\n            while self.is_truthy(self.evaluate(stmt.condition)):'
)

# Escreve o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Método execute_WhileStatement corrigido!") 
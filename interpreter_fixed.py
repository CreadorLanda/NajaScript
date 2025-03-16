#!/usr/bin/env python3

# Métodos corrigidos para substituir no arquivo original
metodos_corrigidos = {
    'execute_DoWhileStatement': '''    def execute_DoWhileStatement(self, stmt):
        """Executa uma declaração do-while"""
        result = None
        
        try:
            # Executa o bloco pelo menos uma vez
            result = self.execute_block(stmt.body, Environment(self.environment))
            
            # Continua executando enquanto a condição for verdadeira
            while self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    result = self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    continue
                except BreakException:
                    break
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise
        
        return result''',
    
    'execute_ForStatement': '''    def execute_ForStatement(self, stmt):
        """Executa uma declaração for"""
        # Cria um novo ambiente para o escopo do for
        env = Environment(self.environment)
        result = None
        
        # Salva o ambiente atual
        old_env = self.environment
        self.environment = env
        
        try:
            # Inicialização
            if stmt.init:
                self.execute(stmt.init)
            
            # Loop principal
            while not stmt.condition or self.is_truthy(self.evaluate(stmt.condition)):
                try:
                    result = self.execute_block(stmt.body, Environment(self.environment))
                except ContinueException:
                    # Continua para a próxima iteração
                    pass
                except BreakException:
                    # Sai do loop
                    break
                
                # Atualização no final de cada iteração
                if stmt.update:
                    self.evaluate(stmt.update)
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise
        finally:
            # Restaura o ambiente original
            self.environment = old_env
        
        return result''',
    
    'execute_ForInStatement': '''    def execute_ForInStatement(self, stmt):
        """Executa uma declaração forin"""
        result = None
        
        # Avalia o iterável
        iterable = self.evaluate(stmt.iterable)
        
        # Verifica se é um tipo iterável suportado
        if isinstance(iterable, NajaList) or isinstance(iterable, NajaDict) or isinstance(iterable, NajaVector) or isinstance(iterable, list) or isinstance(iterable, dict):
            # Cria um novo ambiente para o escopo do loop
            env = Environment(self.environment)
            old_env = self.environment
            self.environment = env
            
            try:
                # Para listas e vetores
                if isinstance(iterable, NajaList) or isinstance(iterable, NajaVector) or isinstance(iterable, list):
                    if isinstance(iterable, list):
                        items = iterable
                    else:
                        items = iterable.elements
                    
                    for item in items:
                        # Define a variável de item no ambiente do loop
                        self.environment.define(stmt.item, item)
                        
                        try:
                            # Executa o corpo do loop
                            result = self.execute_block(stmt.body, Environment(self.environment))
                        except ContinueException:
                            # Continua para a próxima iteração
                            continue
                        except BreakException:
                            # Sai do loop
                            break
                
                # Para dicionários
                elif isinstance(iterable, NajaDict) or isinstance(iterable, dict):
                    if isinstance(iterable, dict):
                        items = iterable.keys()
                    else:
                        items = iterable.items.keys()
                    
                    for key in items:
                        # Define a variável de item no ambiente do loop
                        self.environment.define(stmt.item, key)
                        
                        try:
                            # Executa o corpo do loop
                            result = self.execute_block(stmt.body, Environment(self.environment))
                        except ContinueException:
                            # Continua para a próxima iteração
                            continue
                        except BreakException:
                            # Sai do loop
                            break
            except Exception as e:
                if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                    raise
            finally:
                # Restaura o ambiente original
                self.environment = old_env
        else:
            self.error(f"Tipo não iterável: {type(iterable)}")
        
        return result''',
    
    'evaluate_FunctionCall': '''    def evaluate_FunctionCall(self, expr):
        """Avalia uma chamada de função"""
        # Obtém a função
        callee = self.environment.get(expr.name)
        
        # Avalia os argumentos
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        
        # Verifica se é uma função nativa (Python) ou uma função NajaScript
        if callable(callee):
            try:
                # Tenta chamar a função com os argumentos
                return callee(*arguments)
            except TypeError as e:
                # Se houver erro de tipo, pode ser uma função que espera um interpretador
                if isinstance(callee, Function):
                    return callee(self, arguments)
                else:
                    raise e
        else:
            raise RuntimeError(f"Não é possível chamar '{expr.name}' como função")'''
}

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as file:
    conteudo = file.read()

# Substitui cada método
import re
for nome_metodo, codigo_corrigido in metodos_corrigidos.items():
    padrao = rf'def {nome_metodo}.*?raise'
    conteudo = re.sub(padrao, codigo_corrigido.strip(), conteudo, flags=re.DOTALL)

# Salva o arquivo corrigido
with open('interpreter.py', 'w', encoding='utf-8') as file:
    file.write(conteudo)

print("Arquivo interpreter.py corrigido com sucesso.") 
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Union, Any
from ast_nodes import FunctionCall, Assignment
import sys

# Aumenta o limite de recursão
sys.setrecursionlimit(10000)

class OpCode(Enum):
    # Operações de pilha
    PUSH = auto()      # Empilha um valor
    POP = auto()       # Desempilha um valor
    DUP = auto()       # Duplica o valor no topo da pilha
    
    # Operações aritméticas
    ADD = auto()       # Soma os dois valores do topo da pilha
    SUB = auto()       # Subtrai os dois valores do topo da pilha
    MUL = auto()       # Multiplica os dois valores do topo da pilha
    DIV = auto()       # Divide os dois valores do topo da pilha
    
    # Operações de controle de fluxo
    JMP = auto()       # Salta para um endereço específico
    JMP_IF = auto()    # Salta se a condição for verdadeira
    CALL = auto()      # Chama uma função
    RET = auto()       # Retorna de uma função
    
    # Operações de memória
    LOAD = auto()      # Carrega uma variável
    STORE = auto()     # Armazena em uma variável
    
    # Operações de comparação
    EQ = auto()        # Igual
    LT = auto()        # Menor que
    GT = auto()        # Maior que
    LE = auto()        # Menor ou igual
    GE = auto()        # Maior ou igual
    NE = auto()        # Diferente

@dataclass
class Instruction:
    opcode: OpCode
    operands: List[Any] = None
    
    def __init__(self, opcode: OpCode, *operands):
        self.opcode = opcode
        self.operands = list(operands) if operands else []

class Frame:
    def __init__(self, variables, instructions, return_address=None):
        self.variables = variables  # Variáveis locais do frame
        self.instructions = instructions
        self.pc = 0  # Program counter
        self.return_address = return_address

class NajaBytecodeCompiler:
    """Compila AST NajaScript para bytecode"""
    
    def __init__(self):
        self.code = []
        self.constants = []
        self.names = []
        self.current_scope = None
        self.scopes = []
        self.interpreter = None
        self.debug = False  # Desabilitando depuração
        
    def debug_print(self, msg):
        """Imprime mensagens de depuração, se habilitado"""
        if self.debug:
            print(f"DEBUG: {msg}")
            
    def compile(self, ast_node) -> List[Instruction]:
        """Compila um nó AST para uma lista de instruções bytecode"""
        method = f"compile_{ast_node.__class__.__name__.lower()}"
        if hasattr(self, method):
            result = getattr(self, method)(ast_node)
            if self.debug:
                print(f"\nCompilando {ast_node.__class__.__name__}:")
                for i, instr in enumerate(result):
                    print(f"{i}: {instr.opcode.name} {instr.operands}")
            return result
        raise NotImplementedError(f"Compilação não implementada para {ast_node.__class__.__name__}")
    
    def compile_program(self, node):
        """Compila o nó raiz Program"""
        instructions = []
        for statement in node.statements:
            instructions.extend(self.compile(statement))
        return instructions
    
    def compile_functiondeclaration(self, node):
        """Compila uma declaração de função"""
        # Compila o corpo da função
        func_instructions = []
        
        # Carrega os parâmetros da função
        for i, (param_type, param_name) in enumerate(node.parameters):
            func_instructions.append(Instruction(OpCode.LOAD, f"arg{i}"))
            func_instructions.append(Instruction(OpCode.STORE, param_name))
        
        # Compila o corpo da função
        for stmt in node.body:
            func_instructions.extend(self.compile(stmt))
            
        # Adiciona retorno implícito se necessário
        if not func_instructions or func_instructions[-1].opcode != OpCode.RET:
            func_instructions.append(Instruction(OpCode.PUSH, 0))  # Valor padrão de retorno
            func_instructions.append(Instruction(OpCode.RET))
        
        # Armazena a função no interpretador
        if hasattr(self, 'interpreter'):
            self.interpreter.functions[node.name] = func_instructions
        else:
            # Se não tiver interpretador, cria um dicionário temporário
            if not hasattr(self, '_functions'):
                self._functions = {}
            self._functions[node.name] = func_instructions
        
        return []  # Não gera instruções no escopo atual
    
    def compile_binaryoperation(self, node):
        """Compila uma operação binária"""
        instructions = []
        
        # Compila operandos
        instructions.extend(self.compile(node.left))
        instructions.extend(self.compile(node.right))
        
        # Mapeia operador para opcode
        op_map = {
            "+": OpCode.ADD,
            "-": OpCode.SUB,
            "*": OpCode.MUL,
            "/": OpCode.DIV,
            "==": OpCode.EQ,
            "<": OpCode.LT,
            ">": OpCode.GT,
            "<=": OpCode.LE,
            ">=": OpCode.GE,
            "!=": OpCode.NE
        }
        
        if node.operator in op_map:
            instructions.append(Instruction(op_map[node.operator]))
        else:
            raise ValueError(f"Operador não suportado: {node.operator}")
            
        return instructions
    
    def compile_integerliteral(self, node):
        """Compila um literal inteiro"""
        return [Instruction(OpCode.PUSH, node.value)]
    
    def compile_stringliteral(self, node):
        """Compila um literal string"""
        return [Instruction(OpCode.PUSH, node.value)]
    
    def compile_identifier(self, node):
        """Compila um identificador"""
        return [Instruction(OpCode.LOAD, node.name)]
    
    def compile_returnstatement(self, node):
        """Compila uma instrução return"""
        instructions = []
        if node.value:
            instructions.extend(self.compile(node.value))
        instructions.append(Instruction(OpCode.RET))
        return instructions
        
    def compile_ifstatement(self, node):
        """Compila uma instrução if"""
        instructions = []
        
        # Compila a condição
        instructions.extend(self.compile(node.condition))
        
        # Reserva espaço para o salto (será preenchido depois)
        jmp_if_idx = len(instructions)
        instructions.append(Instruction(OpCode.JMP_IF, 0))  # placeholder
        
        # Compila o bloco then
        then_instructions = []
        for stmt in node.then_branch:
            then_instructions.extend(self.compile(stmt))
            
        # Adiciona salto para o fim do if
        end_idx = len(instructions) + len(then_instructions)
        if node.else_branch:
            # Se houver else, precisamos pular ele também
            else_instructions = []
            for stmt in node.else_branch:
                else_instructions.extend(self.compile(stmt))
            end_idx += len(else_instructions)
            instructions.append(Instruction(OpCode.JMP, end_idx))
        
        # Atualiza o endereço do salto condicional
        if node.else_branch:
            instructions[jmp_if_idx].operands[0] = len(instructions) + len(then_instructions)
        else:
            instructions[jmp_if_idx].operands[0] = end_idx
        
        # Adiciona as instruções do bloco then
        instructions.extend(then_instructions)
        
        # Se houver else, compila também
        if node.else_branch:
            else_instructions = []
            for stmt in node.else_branch:
                else_instructions.extend(self.compile(stmt))
            instructions.extend(else_instructions)
            
        return instructions
        
    def compile_whilestatement(self, node):
        """Compila uma instrução while"""
        instructions = []
        
        # Marca o início do loop
        loop_start = len(instructions)
        
        # Compila a condição
        condition_instructions = self.compile(node.condition)
        instructions.extend(condition_instructions)
        
        # Reserva espaço para o salto (será preenchido depois)
        jmp_if_idx = len(instructions)
        instructions.append(Instruction(OpCode.JMP_IF, 0))  # placeholder
        
        # Compila o corpo do loop
        body_instructions = []
        for stmt in node.body:
            body_instructions.extend(self.compile(stmt))
            
        # Adiciona as instruções do corpo
        instructions.extend(body_instructions)
        
        # Adiciona salto de volta para o início
        instructions.append(Instruction(OpCode.JMP, loop_start))
        
        # Atualiza o endereço do salto condicional para pular todo o corpo se a condição for falsa
        instructions[jmp_if_idx].operands[0] = len(instructions)
        
        return instructions
        
    def compile_functioncall(self, node):
        """Compila uma chamada de função"""
        instructions = []
        
        # Compila os argumentos
        for arg in node.arguments:
            instructions.extend(self.compile(arg))
            
        # Adiciona a chamada da função
        instructions.append(Instruction(OpCode.CALL, node.name, len(node.arguments)))
        
        return instructions

    def compile_variable(self, node):
        """Compila uma referência a variável"""
        return [Instruction(OpCode.LOAD, node.name)]

    def compile_expressionstatement(self, node):
        """Compila uma expressão como statement"""
        instructions = self.compile(node.expression)
        # Não descarta o resultado de chamadas de função ou atribuições
        if not isinstance(node.expression, (FunctionCall, Assignment)):
            instructions.append(Instruction(OpCode.POP))
        return instructions

    def compile_vardeclaration(self, node):
        """Compila uma declaração de variável"""
        instructions = []
        if node.value:
            instructions.extend(self.compile(node.value))
        else:
            # Se não houver valor inicial, usa 0 como valor padrão
            instructions.append(Instruction(OpCode.PUSH, 0))
        instructions.append(Instruction(OpCode.STORE, node.name))
        return instructions

    def compile_assignment(self, node):
        """Compila uma atribuição de variável"""
        instructions = []
        
        # Compila o valor a ser atribuído
        instructions.extend(self.compile(node.value))
        
        # Duplica o valor no topo da pilha para que possamos retorná-lo após a atribuição
        instructions.append(Instruction(OpCode.DUP))
        
        # Armazena o valor na variável
        instructions.append(Instruction(OpCode.STORE, node.name))
        
        # O valor duplicado permanece na pilha como resultado da expressão
        return instructions

    def compile_listliteral(self, node):
        """Compila um literal de lista"""
        instructions = []
        
        # Compila cada elemento da lista
        for element in node.elements:
            instructions.extend(self.compile(element))
        
        # Cria a lista com os elementos compilados
        instructions.append(Instruction(OpCode.PUSH, len(node.elements)))
        instructions.append(Instruction(OpCode.CALL, "list", len(node.elements)))
        
        return instructions

    def set_interpreter(self, interpreter):
        """Define o interpretador e transfere as funções compiladas"""
        self.interpreter = interpreter
        if hasattr(self, '_functions'):
            for name, instructions in self._functions.items():
                interpreter.functions[name] = instructions
            delattr(self, '_functions')

class BytecodeInterpreter:
    def __init__(self):
        self.stack = []  # Pilha de valores
        self.frames = []  # Pilha de frames de execução
        self.functions = {
            'println': self.native_println
        }  # Funções definidas
        self.current_frame = None
    
    def execute(self, instructions):
        """Executa uma sequência de instruções"""
        # Cria o frame inicial com variáveis globais
        self.current_frame = Frame({}, instructions)
        self.frames.append(self.current_frame)
        
        # Contador de instruções para evitar loops infinitos
        max_instructions = 1000000  # Limite máximo de instruções
        instruction_count = 0
        
        # Loop principal de execução
        try:
            while self.frames and instruction_count < max_instructions:
                # Obtém o frame atual
                frame = self.frames[-1]
                
                # Verifica se chegamos ao fim das instruções
                if frame.pc >= len(frame.instructions):
                    old_frame = self.frames.pop()
                    print(f"\nFrame finalizado: {old_frame.variables}")
                    if self.frames:
                        self.current_frame = self.frames[-1]
                        print(f"Retornando para frame: {self.current_frame.variables}")
                    else:
                        print("Execução finalizada")
                        break
                
                # Obtém a próxima instrução
                instruction = frame.instructions[frame.pc]
                old_pc = frame.pc
                frame.pc += 1
                instruction_count += 1
                
                # Debug: imprime a instrução atual e estado
                print(f"\nFrame {len(self.frames)-1}, PC: {old_pc}")
                print(f"Executando: {instruction.opcode.name} {instruction.operands}")
                print(f"Variáveis locais: {frame.variables}")
                print(f"Pilha antes: {self.stack}")
                
                # Executa a instrução
                method = f"execute_{instruction.opcode.name.lower()}"
                should_stop = getattr(self, method)(instruction)
                
                # Se a instrução retornou True, terminamos a execução
                if should_stop:
                    print("Execução finalizada por retorno")
                    break
                
                # Debug: imprime o estado após execução
                print(f"Pilha depois: {self.stack}")
                print(f"PC após execução: {frame.pc}")
                
            if instruction_count >= max_instructions:
                raise RuntimeError("Limite máximo de instruções excedido - possível loop infinito")
                
        except Exception as e:
            print(f"\nErro durante a execução: {e}")
            print(f"Estado final:")
            print(f"- Frames ativos: {len(self.frames)}")
            print(f"- Pilha: {self.stack}")
            print(f"- Variáveis do frame atual: {self.current_frame.variables}")
            raise
    
    def execute_load(self, instruction):
        """Carrega uma variável"""
        name = instruction.operands[0]
        # Procura a variável no frame atual
        value = self.current_frame.variables.get(name)
        if value is None:
            # Se não encontrar no frame atual, procura nos frames anteriores
            for frame in reversed(self.frames[:-1]):
                value = frame.variables.get(name)
                if value is not None:
                    break
            # Se ainda não encontrou, usa 0 como padrão
            if value is None:
                value = 0
        self.stack.append(value)
    
    def execute_store(self, instruction):
        """Armazena em uma variável"""
        name = instruction.operands[0]
        value = self.stack.pop()
        # Armazena no frame atual
        self.current_frame.variables[name] = value
    
    def execute_call(self, instruction):
        """Executa uma chamada de função"""
        # Obtém o nome da função e número de argumentos
        func_name = instruction.operands[0]
        num_args = instruction.operands[1]
        
        # Obtém os argumentos da pilha
        args = []
        for _ in range(num_args):
            if not self.stack:
                raise IndexError("Pilha vazia ao tentar obter argumentos da função")
            args.insert(0, self.stack.pop())
            
        # Procura a função
        func = self.functions.get(func_name)
        if func is None:
            raise ValueError(f"Função não encontrada: {func_name}")
            
        if callable(func):
            # Se for uma função nativa
            result = func(*args)
            if result is not None:
                self.stack.append(result)
        else:
            # Se for uma função compilada
            # Cria novo escopo para a função
            new_variables = {f"arg{i}": arg for i, arg in enumerate(args)}
            
            # Cria um novo frame para a função
            new_frame = Frame(new_variables, func)
            self.frames.append(new_frame)
            self.current_frame = new_frame
            self.current_frame.pc = 0  # Garante que começamos do início da função

    def execute_return(self, instruction):
        """Executa uma instrução de retorno"""
        # Se houver um valor de retorno, ele já está na pilha
        return_value = None
        if self.stack:
            return_value = self.stack.pop()
        
        # Remove o frame atual
        if self.frames:
            old_frame = self.frames.pop()
            print(f"\nFrame finalizado: {old_frame.variables}")
            
            if self.frames:
                # Restaura o frame anterior
                self.current_frame = self.frames[-1]
                # Empilha o valor de retorno no frame anterior
                if return_value is not None:
                    self.stack.append(return_value)
                print(f"Retornando para frame: {self.current_frame.variables}")
            else:
                # Se não houver mais frames, terminamos a execução
                print("Execução finalizada")
                return True  # Indica que a execução deve terminar
        return False  # Indica que a execução deve continuar

    def native_println(self, *args):
        """Função nativa println"""
        print(*args)
        return None
        
    def execute_push(self, instruction):
        """Empilha um valor"""
        self.stack.append(instruction.operands[0])
        
    def execute_pop(self, instruction):
        """Desempilha um valor"""
        if self.stack:  # Só remove se houver algo na pilha
            return self.stack.pop()
        return None
        
    def execute_add(self, instruction):
        """Soma os dois valores do topo da pilha"""
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)
        
    def execute_sub(self, instruction):
        """Subtrai os dois valores do topo da pilha"""
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)
        
    def execute_mul(self, instruction):
        """Multiplica os dois valores do topo da pilha"""
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)
        
    def execute_div(self, instruction):
        """Divide os dois valores do topo da pilha"""
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a / b)
        
    def execute_ret(self, instruction):
        """Retorna um valor"""
        if self.stack:
            return self.stack.pop()
        return None
        
    def execute_jmp(self, instruction):
        """Salta para um endereço específico"""
        target = instruction.operands[0]
        if target >= 0 and target < len(self.current_frame.instructions):
            self.current_frame.pc = target
            print(f"Saltando para instrução {target}")
        else:
            raise ValueError(f"Endereço de salto inválido: {target}")
        
    def execute_jmp_if(self, instruction):
        """Salta se a condição for falsa"""
        if not self.stack:
            raise IndexError("Pilha vazia ao tentar avaliar condição de salto")
            
        condition = self.stack.pop()
        target = instruction.operands[0]
        
        print(f"Avaliando salto condicional: condição = {condition}, alvo = {target}")
        
        if condition == 0:  # Se a condição for falsa
            if target >= 0 and target < len(self.current_frame.instructions):
                self.current_frame.pc = target
                print(f"Condição falsa, saltando para {target}")
            else:
                raise ValueError(f"Endereço de salto inválido: {target}")
        else:
            print("Condição verdadeira, continuando sequencialmente")

    def execute_le(self, instruction):
        """Compara se o primeiro valor é menor ou igual ao segundo"""
        if len(self.stack) < 2:
            raise IndexError("Pilha não tem elementos suficientes para comparação")
            
        b = self.stack.pop()
        a = self.stack.pop()
        result = 1 if a <= b else 0
        print(f"Comparando {a} <= {b} = {result}")
        self.stack.append(result)

    def execute_dup(self, instruction):
        """Duplica o valor no topo da pilha"""
        if not self.stack:
            raise IndexError("Pilha vazia ao tentar duplicar o topo")
        value = self.stack[-1]  # Obtém o valor do topo sem remover
        self.stack.append(value)  # Adiciona uma cópia na pilha
        return None 
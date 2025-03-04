from typing import List, Dict, Any
from llvmlite import ir
from naja_bytecode import OpCode, Instruction

class NajaLLVMGenerator:
    """Gera LLVM IR a partir do bytecode NajaScript"""
    
    def __init__(self):
        # Inicializa o módulo LLVM
        self.module = ir.Module(name="naja_module")
        self.builder = None
        
        # Tipos LLVM comuns
        self.void_t = ir.VoidType()
        self.int32_t = ir.IntType(32)
        self.float_t = ir.DoubleType()
        self.bool_t = ir.IntType(1)
        
        # Estado da geração
        self.functions: Dict[str, ir.Function] = {}
        self.blocks: List[ir.Block] = []
        self.variables: Dict[str, ir.AllocaInstr] = {}
        self.stack: List[ir.Value] = []
        
    def generate(self, instructions: List[Instruction]) -> ir.Module:
        """Gera LLVM IR a partir de uma lista de instruções bytecode"""
        # Cria a função main
        func_type = ir.FunctionType(self.int32_t, [])
        main_func = ir.Function(self.module, func_type, name="main")
        
        # Cria o bloco de entrada
        block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        # Processa cada instrução
        for instruction in instructions:
            self._process_instruction(instruction)
            
        # Retorna 0 por padrão
        self.builder.ret(ir.Constant(self.int32_t, 0))
        
        return self.module
        
    def _process_instruction(self, instruction: Instruction):
        """Processa uma única instrução bytecode"""
        opcode = instruction.opcode
        
        if opcode == OpCode.PUSH:
            value = instruction.operands[0]
            if isinstance(value, int):
                const = ir.Constant(self.int32_t, value)
            elif isinstance(value, float):
                const = ir.Constant(self.float_t, value)
            elif isinstance(value, bool):
                const = ir.Constant(self.bool_t, int(value))
            else:
                raise ValueError(f"Tipo não suportado: {type(value)}")
            self.stack.append(const)
            
        elif opcode == OpCode.POP:
            self.stack.pop()
            
        elif opcode == OpCode.ADD:
            right = self.stack.pop()
            left = self.stack.pop()
            result = self.builder.add(left, right)
            self.stack.append(result)
            
        elif opcode == OpCode.SUB:
            right = self.stack.pop()
            left = self.stack.pop()
            result = self.builder.sub(left, right)
            self.stack.append(result)
            
        elif opcode == OpCode.MUL:
            right = self.stack.pop()
            left = self.stack.pop()
            result = self.builder.mul(left, right)
            self.stack.append(result)
            
        elif opcode == OpCode.DIV:
            right = self.stack.pop()
            left = self.stack.pop()
            result = self.builder.sdiv(left, right)  # Divisão com sinal
            self.stack.append(result)
            
        elif opcode == OpCode.LOAD:
            name = instruction.operands[0]
            if name not in self.variables:
                # Aloca variável se não existir
                alloca = self.builder.alloca(self.int32_t, name=name)
                self.variables[name] = alloca
                self.builder.store(ir.Constant(self.int32_t, 0), alloca)
            
            # Carrega valor da variável
            value = self.builder.load(self.variables[name])
            self.stack.append(value)
            
        elif opcode == OpCode.STORE:
            name = instruction.operands[0]
            value = self.stack.pop()
            
            if name not in self.variables:
                # Aloca variável se não existir
                alloca = self.builder.alloca(self.int32_t, name=name)
                self.variables[name] = alloca
                
            # Armazena valor na variável
            self.builder.store(value, self.variables[name])
            
        elif opcode == OpCode.RET:
            if self.stack:
                value = self.stack.pop()
                self.builder.ret(value)
            else:
                self.builder.ret(ir.Constant(self.int32_t, 0))
                
        elif opcode == OpCode.CALL:
            func_name = instruction.operands[0]
            arg_count = instruction.operands[1]
            
            # Obtém argumentos da pilha
            args = []
            for _ in range(arg_count):
                args.insert(0, self.stack.pop())
                
            # Obtém ou cria a função
            if func_name not in self.functions:
                # Cria tipo da função (todos os args são int32 por enquanto)
                func_type = ir.FunctionType(self.int32_t, [self.int32_t] * arg_count)
                func = ir.Function(self.module, func_type, name=func_name)
                self.functions[func_name] = func
                
            # Chama a função
            result = self.builder.call(self.functions[func_name], args)
            self.stack.append(result)
            
        else:
            raise NotImplementedError(f"Operação LLVM não implementada: {opcode}")
            
    def optimize(self):
        """Aplica otimizações no código LLVM IR gerado"""
        # TODO: Implementar otimizações usando o LLVM optimization pass manager
        pass 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import platform
import tempfile
import subprocess
from enum import Enum, auto

import llvmlite.binding as llvm
import llvmlite.ir as ir
from ast_nodes import *

# Inicializa o LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class DataType(Enum):
    """Tipos de dados suportados pelo compilador AOT"""
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    VOID = auto()

class AOTCompiler:
    """
    Compilador AOT (Ahead-of-Time) para NajaScript usando LLVM
    """
    def __init__(self, target_triple=None):
        self.target_triple = target_triple or self._get_default_triple()
        self.module = None
        self.builder = None
        self.function = None
        self.local_vars = {}
        self.global_vars = {}
        self.func_symtab = {}
        
    def _get_default_triple(self):
        """Obtém o triple padrão para a plataforma atual"""
        return llvm.get_default_triple()
        
    def compile(self, ast_program, output_file=None, optimize=True):
        """
        Compila um programa AST para código nativo
        """
        # Cria um novo módulo LLVM
        self.module = ir.Module(name="najascript_module")
        self.module.triple = self.target_triple
        
        # Processa as declarações de função e variáveis globais
        self._declare_functions(ast_program)
        
        # Compila as funções
        for statement in ast_program.statements:
            if isinstance(statement, FunctionDeclaration):
                self._compile_function(statement)
        
        # Adiciona função main se não existir
        if "main" not in self.func_symtab:
            self._create_main_function(ast_program)
        
        # Verifica o módulo LLVM
        llvm_module = llvm.parse_assembly(str(self.module))
        llvm_module.verify()
        
        # Otimiza o código LLVM se solicitado
        if optimize:
            self._optimize_module(llvm_module)
        
        # Gera código objeto ou executável
        if output_file:
            return self._generate_output(llvm_module, output_file)
        else:
            return str(self.module)
    
    def _declare_functions(self, ast_program):
        """
        Declara todas as funções e variáveis globais
        """
        for statement in ast_program.statements:
            if isinstance(statement, FunctionDeclaration):
                # Cria a declaração da função no LLVM
                func_name = statement.name
                return_type = self._convert_type(statement.return_type)
                
                # Determina os tipos dos parâmetros
                param_types = [self._convert_type(param.var_type) for param in statement.parameters]
                
                # Cria o tipo de função
                func_type = ir.FunctionType(return_type, param_types)
                
                # Declara a função no módulo
                func = ir.Function(self.module, func_type, name=func_name)
                
                # Armazena a função na tabela de símbolos
                self.func_symtab[func_name] = func
                
            elif isinstance(statement, VarDeclaration) and not isinstance(statement.value, FunctionDeclaration):
                # Declara variáveis globais
                var_name = statement.name
                var_type = self._convert_type(statement.var_type)
                
                # Cria uma variável global
                global_var = ir.GlobalVariable(self.module, var_type, name=var_name)
                global_var.linkage = 'common'
                global_var.initializer = ir.Constant(var_type, None)
                
                # Armazena na tabela de símbolos globais
                self.global_vars[var_name] = global_var
    
    def _compile_function(self, ast_function):
        """
        Compila uma função AST para código LLVM
        """
        # Obtém a função LLVM
        func_name = ast_function.name
        func = self.func_symtab[func_name]
        
        # Cria um bloco de entrada
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)
        
        # Parâmetros da função
        for i, param in enumerate(ast_function.parameters):
            param_name = param.name
            param_value = func.args[i]
            param_value.name = param_name
            
            # Aloca espaço na stack para o parâmetro
            alloca = self.builder.alloca(param_value.type, name=param_name)
            self.builder.store(param_value, alloca)
            self.local_vars[param_name] = alloca
        
        # Compila o corpo da função
        for statement in ast_function.body:
            self._compile_statement(statement)
        
        # Adiciona retorno se não houver
        if not self.builder.block.is_terminated:
            ret_type = func.return_value.type
            if ret_type == ir.VoidType():
                self.builder.ret_void()
            else:
                self.builder.ret(ir.Constant(ret_type, None))
    
    def _create_main_function(self, ast_program):
        """
        Cria uma função main que executa o código no nível global
        """
        # Tipo da função main: int main(void)
        func_type = ir.FunctionType(ir.IntType(32), [])
        func = ir.Function(self.module, func_type, name="main")
        
        # Cria o bloco de entrada
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)
        
        # Armazena a função atual
        self.function = func
        
        # Compila as declarações globais
        for statement in ast_program.statements:
            if not isinstance(statement, FunctionDeclaration):
                self._compile_statement(statement)
        
        # Adiciona retorno 0 para sucesso
        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        
        # Adiciona à tabela de símbolos
        self.func_symtab["main"] = func
    
    def _compile_statement(self, statement):
        """
        Compila uma declaração para código LLVM
        """
        # Implementa para cada tipo de declaração
        if isinstance(statement, VarDeclaration):
            self._compile_var_declaration(statement)
        elif isinstance(statement, ExpressionStatement):
            self._compile_expression(statement.expression)
        elif isinstance(statement, ReturnStatement):
            self._compile_return(statement)
        elif isinstance(statement, IfStatement):
            self._compile_if_statement(statement)
        elif isinstance(statement, WhileStatement):
            self._compile_while_statement(statement)
        # Outros tipos de declarações serão implementados conforme necessário
    
    def _compile_var_declaration(self, statement):
        """
        Compila uma declaração de variável
        """
        var_name = statement.name
        var_type = self._convert_type(statement.var_type)
        
        # Aloca espaço na stack
        alloca = self.builder.alloca(var_type, name=var_name)
        
        # Compila e armazena o valor inicial, se houver
        if statement.value:
            value = self._compile_expression(statement.value)
            self.builder.store(value, alloca)
        
        # Armazena na tabela de símbolos local
        self.local_vars[var_name] = alloca
    
    def _compile_expression(self, expression):
        """
        Compila uma expressão para código LLVM
        """
        if isinstance(expression, IntegerLiteral):
            return ir.Constant(ir.IntType(32), expression.value)
        elif isinstance(expression, FloatLiteral):
            return ir.Constant(ir.FloatType(), expression.value)
        elif isinstance(expression, BooleanLiteral):
            return ir.Constant(ir.IntType(1), 1 if expression.value else 0)
        elif isinstance(expression, Variable):
            return self._compile_variable(expression)
        elif isinstance(expression, BinaryOperation):
            return self._compile_binary_operation(expression)
        elif isinstance(expression, UnaryOperation):
            return self._compile_unary_operation(expression)
        elif isinstance(expression, FunctionCall):
            return self._compile_function_call(expression)
        # Outros tipos de expressões serão implementados conforme necessário
    
    def _compile_variable(self, expression):
        """
        Compila o acesso a uma variável
        """
        var_name = expression.name
        
        # Procura na tabela de símbolos local primeiro
        if var_name in self.local_vars:
            # Carrega o valor da variável local
            return self.builder.load(self.local_vars[var_name], name=var_name)
        # Depois procura nas variáveis globais
        elif var_name in self.global_vars:
            # Carrega o valor da variável global
            return self.builder.load(self.global_vars[var_name], name=var_name)
        else:
            raise ValueError(f"Variável '{var_name}' não encontrada")
    
    def _compile_binary_operation(self, expression):
        """
        Compila uma operação binária
        """
        left = self._compile_expression(expression.left)
        right = self._compile_expression(expression.right)
        
        # Verifica se os operandos são do mesmo tipo
        if left.type != right.type:
            # Implementar conversão de tipos, se necessário
            pass
        
        # Implementa cada operador
        if expression.operator == "+":
            if isinstance(left.type, ir.IntType):
                return self.builder.add(left, right, "addtmp")
            elif isinstance(left.type, ir.FloatType):
                return self.builder.fadd(left, right, "addtmp")
        elif expression.operator == "-":
            if isinstance(left.type, ir.IntType):
                return self.builder.sub(left, right, "subtmp")
            elif isinstance(left.type, ir.FloatType):
                return self.builder.fsub(left, right, "subtmp")
        elif expression.operator == "*":
            if isinstance(left.type, ir.IntType):
                return self.builder.mul(left, right, "multmp")
            elif isinstance(left.type, ir.FloatType):
                return self.builder.fmul(left, right, "multmp")
        elif expression.operator == "/":
            if isinstance(left.type, ir.IntType):
                return self.builder.sdiv(left, right, "divtmp")
            elif isinstance(left.type, ir.FloatType):
                return self.builder.fdiv(left, right, "divtmp")
        elif expression.operator == "<":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed("<", left, right, "cmptmp")
            elif isinstance(left.type, ir.FloatType):
                return self.builder.fcmp_ordered("<", left, right, "cmptmp")
        # Outros operadores serão implementados conforme necessário
        
        raise ValueError(f"Operador binário '{expression.operator}' não implementado")
    
    def _compile_unary_operation(self, expression):
        """
        Compila uma operação unária
        """
        operand = self._compile_expression(expression.operand)
        
        # Implementa cada operador unário
        if expression.operator == "-":
            if isinstance(operand.type, ir.IntType):
                return self.builder.neg(operand, "negtmp")
            elif isinstance(operand.type, ir.FloatType):
                return self.builder.fneg(operand, "negtmp")
        elif expression.operator == "!":
            # Para negação lógica, converte para boolean (i1) e nega
            if operand.type != ir.IntType(1):
                operand = self.builder.icmp_signed("!=", operand, 
                                               ir.Constant(operand.type, 0), "booltmp")
            return self.builder.not_(operand, "nottmp")
        
        raise ValueError(f"Operador unário '{expression.operator}' não implementado")
    
    def _compile_function_call(self, expression):
        """
        Compila uma chamada de função
        """
        func_name = expression.name
        
        # Verifica se a função existe
        if func_name not in self.func_symtab:
            # Para funções nativas, crie declarações apropriadas
            if func_name == "print" or func_name == "println":
                self._declare_print_function()
            else:
                raise ValueError(f"Função '{func_name}' não encontrada")
        
        # Obtém a função
        func = self.func_symtab[func_name]
        
        # Compila os argumentos
        args = []
        if expression.arguments:
            for arg in expression.arguments:
                args.append(self._compile_expression(arg))
        
        # Chama a função
        return self.builder.call(func, args, "calltmp")
    
    def _compile_return(self, statement):
        """
        Compila uma declaração de retorno
        """
        # Se tiver um valor para retornar
        if statement.value:
            value = self._compile_expression(statement.value)
            self.builder.ret(value)
        else:
            self.builder.ret_void()
    
    def _compile_if_statement(self, statement):
        """
        Compila uma declaração if
        """
        # Compila a condição
        condition = self._compile_expression(statement.condition)
        
        # Converte para boolean se necessário
        if condition.type != ir.IntType(1):
            condition = self.builder.icmp_signed("!=", condition, 
                                           ir.Constant(condition.type, 0), "ifcond")
        
        # Cria blocos para then, else e merge
        then_block = self.function.append_basic_block("then")
        else_block = self.function.append_basic_block("else")
        merge_block = self.function.append_basic_block("ifcont")
        
        # Cria o branch condicional
        self.builder.cbranch(condition, then_block, else_block)
        
        # Compila o bloco then
        self.builder.position_at_end(then_block)
        for stmt in statement.then_branch:
            self._compile_statement(stmt)
        
        # Adiciona jump para o bloco merge se necessário
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        
        # Salva o bloco then para PHI (se necessário)
        then_end = self.builder.block
        
        # Compila o bloco else
        self.builder.position_at_end(else_block)
        if statement.else_branch:
            for stmt in statement.else_branch:
                self._compile_statement(stmt)
        
        # Adiciona jump para o bloco merge se necessário
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        
        # Salva o bloco else para PHI (se necessário)
        else_end = self.builder.block
        
        # Posiciona no bloco merge
        self.builder.position_at_end(merge_block)
    
    def _compile_while_statement(self, statement):
        """
        Compila uma declaração while
        """
        # Cria blocos para condição, corpo e continuação
        cond_block = self.function.append_basic_block("while.cond")
        body_block = self.function.append_basic_block("while.body")
        end_block = self.function.append_basic_block("while.end")
        
        # Branch para o bloco de condição
        self.builder.branch(cond_block)
        
        # Compila o bloco de condição
        self.builder.position_at_end(cond_block)
        condition = self._compile_expression(statement.condition)
        
        # Converte para boolean se necessário
        if condition.type != ir.IntType(1):
            condition = self.builder.icmp_signed("!=", condition, 
                                           ir.Constant(condition.type, 0), "whilecond")
        
        # Branch condicional
        self.builder.cbranch(condition, body_block, end_block)
        
        # Compila o corpo do loop
        self.builder.position_at_end(body_block)
        for stmt in statement.body:
            self._compile_statement(stmt)
        
        # Branch de volta para a condição
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)
        
        # Posiciona no final do loop
        self.builder.position_at_end(end_block)
    
    def _declare_print_function(self):
        """
        Declara a função print do sistema
        """
        # Declara a função printf do C
        printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        printf_func = ir.Function(self.module, printf_type, name="printf")
        self.func_symtab["printf"] = printf_func
        
        # Cria uma função de wrapper para print
        print_type = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        print_func = ir.Function(self.module, print_type, name="print")
        
        # Cria o corpo da função
        block = print_func.append_basic_block("entry")
        builder = ir.IRBuilder(block)
        
        # Chama printf com o argumento
        builder.call(printf_func, [print_func.args[0]], "printf_call")
        builder.ret_void()
        
        # Adiciona à tabela de símbolos
        self.func_symtab["print"] = print_func
        
        # Também adiciona println
        println_func = ir.Function(self.module, print_type, name="println")
        block = println_func.append_basic_block("entry")
        builder = ir.IRBuilder(block)
        
        # Format string com quebra de linha
        format_str = ir.Constant(ir.ArrayType(ir.IntType(8), 3), bytearray("%s\n\0", "utf-8"))
        format_str_ptr = builder.bitcast(format_str, ir.IntType(8).as_pointer())
        
        # Chama printf com o argumento e quebra de linha
        builder.call(printf_func, [format_str_ptr, println_func.args[0]], "printf_call")
        builder.ret_void()
        
        # Adiciona à tabela de símbolos
        self.func_symtab["println"] = println_func
    
    def _convert_type(self, type_name):
        """
        Converte um tipo NajaScript para um tipo LLVM
        """
        if type_name == "int":
            return ir.IntType(32)
        elif type_name == "float":
            return ir.FloatType()
        elif type_name == "bool":
            return ir.IntType(1)
        elif type_name == "string":
            return ir.IntType(8).as_pointer()
        elif type_name == "void" or type_name is None:
            return ir.VoidType()
        else:
            # Para tipos não suportados, use um ponteiro genérico
            return ir.IntType(8).as_pointer()
    
    def _optimize_module(self, llvm_module):
        """
        Otimiza o módulo LLVM
        """
        # Cria um pass manager
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 3  # Nível de otimização (0-3)
        pm = llvm.create_module_pass_manager()
        
        # Adiciona passes de otimização comuns
        pmb.populate(pm)
        
        # Executa as otimizações
        pm.run(llvm_module)
    
    def _generate_output(self, llvm_module, output_file):
        """
        Gera um arquivo objeto ou executável
        """
        # Determina o tipo de saída com base na extensão
        _, ext = os.path.splitext(output_file)
        
        # Seleciona o alvo para a plataforma atual
        target = llvm.Target.from_triple(self.target_triple)
        target_machine = target.create_target_machine()
        
        # Gera código objeto
        obj_file = output_file if ext == '.o' else output_file + '.o'
        with open(obj_file, 'wb') as f:
            f.write(target_machine.emit_object(llvm_module))
        
        # Se não for apenas um objeto, cria um executável
        if ext != '.o':
            self._link_executable(obj_file, output_file)
            # Limpa o arquivo objeto intermediário
            if output_file != obj_file:
                os.remove(obj_file)
        
        return output_file
    
    def _link_executable(self, obj_file, exe_file):
        """
        Vincula o arquivo objeto em um executável
        """
        # Determina o compilador C para vincular
        if platform.system() == "Windows":
            cc = "cl"
            exe_flag = "/Fe:"
        else:
            cc = "gcc"
            exe_flag = "-o"
        
        # Constrói a linha de comando para o linker
        cmd = [cc, obj_file, exe_flag + exe_file]
        
        # Executa o comando de vinculação
        subprocess.check_call(cmd) 
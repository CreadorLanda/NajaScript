#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lê o arquivo original
with open('interpreter.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura pelo método execute_IfStatement
for i in range(len(lines)):
    if 'def execute_IfStatement(self, stmt):' in lines[i]:
        # Encontra o final do método
        end_line = i
        for j in range(i+1, len(lines)):
            if lines[j].startswith('    def '):
                end_line = j
                break
        
        # Adiciona o método execute_ImportStatement após o método execute_IfStatement
        import_method = [
            '    def execute_ImportStatement(self, stmt):\n',
            '        """Executa uma instrução de importação"""\n',
            '        module_name = stmt.module_name\n',
            '        \n',
            '        # Remove aspas se presentes\n',
            '        if module_name.startswith(\'"\'): module_name = module_name[1:]\n',
            '        if module_name.endswith(\'"\'): module_name = module_name[:-1]\n',
            '        if module_name.startswith("\'"): module_name = module_name[1:]\n',
            '        if module_name.endswith("\'"): module_name = module_name[:-1]\n',
            '        \n',
            '        # Verifica se o módulo já foi importado\n',
            '        if module_name in self.imported_modules:\n',
            '            return self.imported_modules[module_name]\n',
            '        \n',
            '        # Procura o módulo nos caminhos definidos\n',
            '        module_found = False\n',
            '        module_path = None\n',
            '        \n',
            '        for path in self.module_paths:\n',
            '            # Tenta encontrar o módulo como arquivo .naja\n',
            '            potential_path = os.path.join(path, module_name + ".naja")\n',
            '            if os.path.exists(potential_path):\n',
            '                module_path = potential_path\n',
            '                module_found = True\n',
            '                break\n',
            '            \n',
            '            # Tenta encontrar o módulo como arquivo .py\n',
            '            potential_path = os.path.join(path, module_name + ".py")\n',
            '            if os.path.exists(potential_path):\n',
            '                module_path = potential_path\n',
            '                module_found = True\n',
            '                break\n',
            '            \n',
            '            # Tenta encontrar o módulo como diretório com __init__.naja\n',
            '            potential_path = os.path.join(path, module_name, "__init__.naja")\n',
            '            if os.path.exists(potential_path):\n',
            '                module_path = potential_path\n',
            '                module_found = True\n',
            '                break\n',
            '        \n',
            '        if not module_found:\n',
            '            # Tenta importar um módulo Python nativo\n',
            '            try:\n',
            '                if module_name == "NajaGame":\n',
            '                    # Importa o módulo pygame_bridge\n',
            '                    import importlib.util\n',
            '                    spec = importlib.util.spec_from_file_location("pygame_bridge", "modules/pygame_bridge.py")\n',
            '                    pygame_bridge = importlib.util.module_from_spec(spec)\n',
            '                    spec.loader.exec_module(pygame_bridge)\n',
            '                    \n',
            '                    # Registra as funções exportadas no ambiente global\n',
            '                    for name, func in pygame_bridge.naja_exports.items():\n',
            '                        self.environment.define(name, func)\n',
            '                    \n',
            '                    self.imported_modules[module_name] = True\n',
            '                    return True\n',
            '                else:\n',
            '                    raise Exception(f"Módulo não encontrado: {module_name}")\n',
            '            except Exception as e:\n',
            '                raise Exception(f"Erro ao importar módulo {module_name}: {str(e)}")\n',
            '        \n',
            '        # Carrega e executa o módulo\n',
            '        try:\n',
            '            with open(module_path, "r", encoding="utf-8") as f:\n',
            '                module_source = f.read()\n',
            '            \n',
            '            # Cria um novo ambiente para o módulo\n',
            '            module_env = Environment(self.globals)\n',
            '            \n',
            '            # Analisa e executa o código do módulo\n',
            '            lexer = Lexer(module_source)\n',
            '            parser = Parser(lexer)\n',
            '            ast = parser.parse()\n',
            '            \n',
            '            # Salva o ambiente atual\n',
            '            previous_env = self.environment\n',
            '            self.environment = module_env\n',
            '            \n',
            '            try:\n',
            '                # Executa o módulo\n',
            '                self.interpret(ast)\n',
            '                \n',
            '                # Registra o módulo como importado\n',
            '                self.imported_modules[module_name] = module_env\n',
            '                \n',
            '                # Exporta as definições do módulo para o ambiente atual\n',
            '                for name, value in module_env.values.items():\n',
            '                    if not name.startswith("_"):  # Não exporta variáveis privadas\n',
            '                        self.globals.define(name, value)\n',
            '                \n',
            '                return module_env\n',
            '            finally:\n',
            '                # Restaura o ambiente original\n',
            '                self.environment = previous_env\n',
            '        except Exception as e:\n',
            '            raise Exception(f"Erro ao carregar módulo {module_name}: {str(e)}")\n',
            '    \n'
        ]
        
        # Insere o método execute_ImportStatement
        lines = lines[:end_line] + import_method + lines[end_line:]
        break

# Escreve o arquivo modificado
with open('interpreter.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Método execute_ImportStatement adicionado!") 
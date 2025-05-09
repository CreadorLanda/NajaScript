#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Package Manager
Gerenciador de pacotes para NajaScript
Use: naja comando [opções]
Comandos: add, remove, install, init, search, remote, create
"""

import sys
import os
import argparse
import json
from naja_package_manager import NajaPackageManager
from naja_repository_manager import NajaRepositoryManager

def main():
    parser = argparse.ArgumentParser(description="NajaScript Package Manager")
    
    # Comandos principais
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando add 
    add_parser = subparsers.add_parser("add", help="Adicionar um pacote")
    add_parser.add_argument("package", help="Nome do pacote para instalar")
    add_parser.add_argument("--version", "-v", default="latest", help="Versão do pacote")
    add_parser.add_argument("--dev", "-d", action="store_true", help="Instalar como dependência de desenvolvimento")
    add_parser.add_argument("--local", "-l", action="store_true", help="Apenas buscar no repositório local")
    
    # Comando remove
    remove_parser = subparsers.add_parser("remove", help="Remover um pacote")
    remove_parser.add_argument("package", help="Nome do pacote a remover")
    remove_parser.add_argument("--dev", "-d", action="store_true", help="Remover de dependências de desenvolvimento")
    
    # Comando install
    install_parser = subparsers.add_parser("install", help="Instalar todos os pacotes do naja_packages.json")
    
    # Comando init
    init_parser = subparsers.add_parser("init", help="Inicializar um arquivo naja_packages.json")
    
    # Comando search
    search_parser = subparsers.add_parser("search", help="Buscar pacotes")
    search_parser.add_argument("query", nargs="?", default="", help="Termo de busca")
    
    # Comando create
    create_parser = subparsers.add_parser("create", help="Criar um novo pacote")
    create_parser.add_argument("name", help="Nome do pacote")
    create_parser.add_argument("--type", "-t", choices=["module", "game"], default="module", 
                              help="Tipo de pacote (module ou game)")
    create_parser.add_argument("--version", "-v", default="1.0.0", help="Versão inicial do pacote")
    create_parser.add_argument("--description", "-d", default="", help="Descrição do pacote")
    
    # Comando remote (substitui naja_remote.py)
    remote_parser = subparsers.add_parser("remote", help="Gerenciar repositórios remotos")
    remote_parser.add_argument("action", choices=["add", "remove", "list", "use", "publish"], 
                               help="Ação a executar com repositórios")
    remote_parser.add_argument("name", nargs="?", help="Nome do repositório")
    remote_parser.add_argument("url", nargs="?", help="URL do repositório")
    remote_parser.add_argument("--package", "-p", help="Pacote a publicar")
    remote_parser.add_argument("--version", "-v", help="Versão do pacote")
    
    args = parser.parse_args()
    
    # Inicializar gerenciadores
    package_manager = NajaPackageManager()
    repo_manager = NajaRepositoryManager()
    
    # Se não houver comando explícito, mostrar ajuda
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execução dos comandos
    if args.command == "search":
        repo_manager.search(args.query)
    
    elif args.command == "add":
        package_name = args.package
        version = args.version
        dev = args.dev
        local = args.local
        
        # Tentar instalar do repositório, a menos que --local esteja especificado
        if not local:
            result = repo_manager.install_from_repo(package_name, version, dev)
            if result:
                print(f"Instalado com sucesso {package_name}@{version}")
                return
            else:
                print(f"Pacote {package_name} não encontrado em repositórios.")
        
        # Se --local especificado ou repositório falhou, perguntar se deseja criar localmente
        if local or not result:
            create_local = input(f"Deseja criar um pacote local para {package_name}? (s/N): ")
            if create_local.lower() == 's':
                print(f"Criando pacote local {package_name}...")
                if package_manager.add_package(package_name, version, dev):
                    print(f"Criado pacote local {package_name}@{version}")
                else:
                    print(f"Falha ao instalar {package_name}")
                    sys.exit(1)
            else:
                print("Operação cancelada.")
                sys.exit(1)
    
    elif args.command == "remove":
        package_name = args.package
        dev = args.dev
        
        if package_manager.remove_package(package_name, dev):
            print(f"Pacote {package_name} removido com sucesso.")
        else:
            print(f"Falha ao remover pacote {package_name}.")
            sys.exit(1)
    
    elif args.command == "install":
        print("Instalando todas as dependências...")
        package_manager.install()
    
    elif args.command == "init":
        # Verificar se o arquivo já existe
        if os.path.exists("naja_packages.json"):
            overwrite = input("O arquivo naja_packages.json já existe. Sobrescrever? (s/N): ")
            if overwrite.lower() != 's':
                print("Operação cancelada.")
                return
        
        # Criar arquivo package.json com valores padrão
        package_data = {
            "name": os.path.basename(os.getcwd()),
            "version": "1.0.0",
            "description": "Projeto NajaScript",
            "author": "",
            "license": "MIT",
            "dependencies": {},
            "devDependencies": {}
        }
        
        with open("naja_packages.json", 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print("Arquivo naja_packages.json criado com sucesso.")
        
        # Criar pasta naja_modules se não existir
        if not os.path.exists("naja_modules"):
            os.makedirs("naja_modules")
            print("Diretório naja_modules criado com sucesso.")
    
    elif args.command == "create":
        package_name = args.name
        package_type = args.type
        version = args.version
        description = args.description or f"Pacote {package_name} para NajaScript"
        
        # Criar diretório do pacote
        package_dir = os.path.join("naja_repository", "modules", package_name, version)
        
        if os.path.exists(package_dir):
            overwrite = input(f"O pacote {package_name}@{version} já existe. Sobrescrever? (s/N): ")
            if overwrite.lower() != 's':
                print("Operação cancelada.")
                return
            
        # Criar estrutura de diretórios
        os.makedirs(package_dir, exist_ok=True)
        
        # Criar arquivo index.naja com template adequado
        index_path = os.path.join(package_dir, "index.naja")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            if package_type == "module":
                f.write(f"// {package_name} package for NajaScript\n\n")
                
                # Escrever algumas funções de exemplo
                f.write("// Basic functions\n")
                f.write("export fun hello() {\n")
                f.write('    println("Hello from ' + package_name + '");\n')
                f.write("    return \"Hello World\";\n")
                f.write("}\n\n")
                
                f.write("// Package information\n")
                f.write("export fun info() {\n")
                f.write(f'    return "{package_name} package v{version} - {description}";\n')
                f.write("}\n\n")
                
                f.write(f"// Initialize\nprintln(\"{package_name} package initialized\");\n")
            
            else:  # game
                f.write(f"// {package_name} - A NajaScript Game\n\n")
                
                # Importar pygame bridge
                f.write("import PyGame from \"pygame_bridge\";\n\n")
                
                # Configurações iniciais do jogo
                f.write("// Game settings\n")
                f.write("const WIDTH = 800;\n")
                f.write("const HEIGHT = 600;\n")
                f.write("const TITLE = \"" + package_name + "\";\n\n")
                
                # Função de inicialização
                f.write("// Initialize game\n")
                f.write("PyGame.init_game(WIDTH, HEIGHT, TITLE);\n\n")
                
                # Game loop
                f.write("// Game loop\n")
                f.write("fun game_loop() {\n")
                f.write("    // Clear screen\n")
                f.write("    PyGame.fill_background(0, 0, 0);\n\n")
                
                f.write("    // Draw game elements\n")
                f.write("    PyGame.draw_rect(WIDTH/2 - 50, HEIGHT/2 - 50, 100, 100, 255, 0, 0);\n\n")
                
                f.write("    // Text display\n")
                f.write("    PyGame.draw_text(\"" + package_name + "\", WIDTH/2, 50, 24, 255, 255, 255);\n\n")
                
                f.write("    // Update display\n")
                f.write("    PyGame.update_window();\n")
                f.write("}\n\n")
                
                # Função principal
                f.write("// Main function\n")
                f.write("fun main() {\n")
                f.write("    println(\"Starting game...\");\n")
                f.write("    while (true) {\n")
                f.write("        // Check for quit event\n")
                f.write("        if (PyGame.should_quit()) {\n")
                f.write("            break;\n")
                f.write("        }\n\n")
                
                f.write("        // Run game loop\n")
                f.write("        game_loop();\n")
                f.write("        \n")
                f.write("        // Control frame rate\n")
                f.write("        PyGame.wait(30);\n")
                f.write("    }\n")
                f.write("    PyGame.quit_game();\n")
                f.write("}\n\n")
                
                f.write("// Run the game\n")
                f.write("main();\n")
        
        # Atualizar o arquivo index.json no repositório
        repo_index_path = os.path.join("naja_repository", "index.json")
        
        if os.path.exists(repo_index_path):
            try:
                with open(repo_index_path, 'r', encoding='utf-8') as f:
                    repo_index = json.load(f)
            except json.JSONDecodeError:
                repo_index = {"name": "NajaScript Official Repository", "description": "Repositório oficial de módulos para NajaScript", "modules": {}}
        else:
            # Criar índice base se não existir
            repo_index = {
                "name": "NajaScript Official Repository",
                "description": "Repositório oficial de módulos para NajaScript",
                "modules": {}
            }
        
        # Adicionar ou atualizar o pacote no índice
        if package_name not in repo_index.get("modules", {}):
            repo_index["modules"][package_name] = {
                "description": description,
                "versions": {}
            }
        
        repo_index["modules"][package_name]["versions"][version] = {
            "description": description,
            "dependencies": {}
        }
        
        # Salvar o índice atualizado
        os.makedirs(os.path.dirname(repo_index_path), exist_ok=True)
        with open(repo_index_path, 'w', encoding='utf-8') as f:
            json.dump(repo_index, f, indent=2, ensure_ascii=False)
        
        print(f"Pacote {package_name}@{version} criado com sucesso no repositório local.")
        print(f"Caminho: {os.path.abspath(package_dir)}")
    
    elif args.command == "remote":
        # Implementação básica do comando remote (substituindo naja_remote.py)
        if args.action == "list":
            print("Repositórios configurados:")
            for name, url in repo_manager.config.get("repositories", {}).items():
                active = " (ativo)" if repo_manager.config.get("use_remote", False) else ""
                print(f"  - {name}: {url}{active}")
        
        elif args.action == "add":
            if not args.name or not args.url:
                print("Erro: É necessário fornecer nome e URL do repositório")
                sys.exit(1)
                
            repo_manager.config["repositories"][args.name] = args.url
            repo_manager._write_config(repo_manager.config)
            print(f"Repositório {args.name} adicionado: {args.url}")
            
        elif args.action == "remove":
            if not args.name:
                print("Erro: É necessário fornecer o nome do repositório")
                sys.exit(1)
                
            if args.name in repo_manager.config.get("repositories", {}):
                del repo_manager.config["repositories"][args.name]
                repo_manager._write_config(repo_manager.config)
                print(f"Repositório {args.name} removido")
            else:
                print(f"Repositório {args.name} não encontrado")
                
        elif args.action == "use":
            if not args.name:
                print("Erro: É necessário fornecer o nome do repositório")
                sys.exit(1)
                
            if args.name in repo_manager.config.get("repositories", {}):
                repo_manager.config["remote"] = repo_manager.config["repositories"][args.name]
                repo_manager.config["use_remote"] = True
                repo_manager._write_config(repo_manager.config)
                print(f"Usando repositório {args.name}: {repo_manager.config['repositories'][args.name]}")
            else:
                print(f"Repositório {args.name} não encontrado")
        
        elif args.action == "publish":
            print("Para publicar pacotes, use o comando 'naja_remote publish' ou atualize para a nova versão")

if __name__ == "__main__":
    main() 
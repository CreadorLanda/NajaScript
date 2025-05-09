#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Package Manager
Gerenciador de pacotes para NajaScript
Use: naja comando [opções]
Comandos: add, remove, install, init, search, remote
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
        if not local and repo_manager.install_from_repo(package_name, version, dev):
            print(f"Instalado com sucesso {package_name}@{version}")
            return
        
        # Se repositório falhar ou --local especificado, criar localmente
        if local:
            print(f"Opção --local especificada. Criando pacote local para {package_name}...")
        else:
            print(f"Pacote {package_name} não encontrado em repositórios. Criando pacote local...")
            
        # Adicionar o pacote localmente
        if package_manager.add_package(package_name, version, dev):
            print(f"Criado pacote local {package_name}@{version}")
            print(f"Atenção: Este é apenas um template básico. Você precisará implementar as funcionalidades do pacote.")
            print(f"O pacote foi criado em: naja_modules/{package_name}/")
        else:
            print(f"Falha ao instalar {package_name}")
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript GitHub Package Manager
Sistema completo de gerenciamento de pacotes usando GitHub como registry central
"""

import os
import sys
import json
import shutil
import argparse
import urllib.request
import urllib.error
import tempfile
import zipfile
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Constants
NAJA_PACKAGES_DIR = "naja_modules"
NAJA_PACKAGE_FILE = "naja_packages.json"
NAJA_CONFIG_FILE = ".naja_config"
GITHUB_REGISTRY_URL = "https://github.com/NajaScript/Naja"
GITHUB_API_BASE = "https://api.github.com/repos/NajaScript/Naja"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/NajaScript/Naja"

class NajaGitHubPackageManager:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.packages_dir = self.project_dir / NAJA_PACKAGES_DIR
        self.package_file = self.project_dir / NAJA_PACKAGE_FILE
        self.config_file = self.project_dir / NAJA_CONFIG_FILE
        
        # Criar diretórios necessários
        self._ensure_directories()
        
        # Carregar configuração
        self.config = self._load_config()
        
    def _ensure_directories(self):
        """Garantir que todos os diretórios necessários existem"""
        if not self.packages_dir.exists():
            self.packages_dir.mkdir(parents=True)
            
        if not self.package_file.exists():
            self._write_package_file({
                "name": "naja-project",
                "version": "1.0.0",
                "description": "NajaScript project",
                "dependencies": {},
                "devDependencies": {}
            })
    
    def _load_config(self):
        """Carregar configuração do sistema"""
        default_config = {
            "registry": {
                "url": GITHUB_REGISTRY_URL,
                "api": GITHUB_API_BASE,
                "raw": GITHUB_RAW_BASE
            },
            "cache_dir": str(self.project_dir / ".naja_cache"),
            "user": {
                "name": "",
                "email": "",
                "github_token": ""
            }
        }
        
        if not self.config_file.exists():
            self._write_config(default_config)
            return default_config
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Mesclar com defaults para garantir que tudo está presente
                return {**default_config, **config}
        except (json.JSONDecodeError, FileNotFoundError):
            return default_config
    
    def _write_config(self, config):
        """Salvar configuração"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _read_package_file(self):
        """Ler arquivo de pacotes do projeto"""
        try:
            with open(self.package_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {
                "name": "naja-project",
                "version": "1.0.0", 
                "description": "NajaScript project",
                "dependencies": {},
                "devDependencies": {}
            }
    
    def _write_package_file(self, data):
        """Salvar arquivo de pacotes do projeto"""
        with open(self.package_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _fetch_registry_index(self):
        """Buscar índice de pacotes do GitHub"""
        try:
            # Tentar buscar o index.json do repositório principal
            index_url = f"{self.config['registry']['raw']}/main/registry/index.json"
            
            print(f"Buscando índice de pacotes de {index_url}...")
            
            request = urllib.request.Request(index_url)
            request.add_header('User-Agent', 'NajaScript Package Manager')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    return json.loads(content)
                else:
                    print(f"Erro ao buscar índice: HTTP {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("Índice de pacotes não encontrado. O registry pode estar vazio.")
                return {"packages": {}}
            else:
                print(f"Erro HTTP ao buscar índice: {e.code}")
                return None
        except Exception as e:
            print(f"Erro ao buscar índice de pacotes: {e}")
            return None
    
    def _download_package_version(self, package_name, version):
        """Baixar uma versão específica de um pacote"""
        try:
            # URL para baixar o arquivo específico do pacote
            package_url = f"{self.config['registry']['raw']}/main/packages/{package_name}/{version}/index.naja"
            
            print(f"Baixando {package_name}@{version}...")
            
            request = urllib.request.Request(package_url)
            request.add_header('User-Agent', 'NajaScript Package Manager')
            
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    
                    # Criar diretório do pacote
                    package_dir = self.packages_dir / package_name
                    package_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Salvar arquivo principal
                    main_file = package_dir / "index.naja"
                    with open(main_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Tentar baixar package.json se existir
                    try:
                        package_json_url = f"{self.config['registry']['raw']}/main/packages/{package_name}/{version}/package.json"
                        json_request = urllib.request.Request(package_json_url)
                        json_request.add_header('User-Agent', 'NajaScript Package Manager')
                        
                        with urllib.request.urlopen(json_request, timeout=10) as json_response:
                            if json_response.status == 200:
                                json_content = json_response.read().decode('utf-8')
                                package_json_file = package_dir / "package.json"
                                with open(package_json_file, 'w', encoding='utf-8') as f:
                                    f.write(json_content)
                    except:
                        # package.json é opcional
                        pass
                    
                    return True
                else:
                    print(f"Erro ao baixar pacote: HTTP {response.status}")
                    return False
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"Pacote {package_name}@{version} não encontrado no registry")
            else:
                print(f"Erro HTTP ao baixar pacote: {e.code}")
            return False
        except Exception as e:
            print(f"Erro ao baixar pacote: {e}")
            return False
    
    def install(self, package_name, version="latest", dev=False):
        """Instalar um pacote"""
        print(f"Instalando {package_name}@{version}...")
        
        # Buscar informações do registry
        registry_index = self._fetch_registry_index()
        if not registry_index:
            print("Não foi possível acessar o registry. Tentando instalação offline...")
            return self._install_offline_template(package_name, version, dev)
        
        packages = registry_index.get("packages", {})
        
        if package_name not in packages:
            print(f"Pacote '{package_name}' não encontrado no registry.")
            print("Criando template básico...")
            return self._install_offline_template(package_name, version, dev)
        
        package_info = packages[package_name]
        available_versions = package_info.get("versions", [])
        
        # Resolver versão
        if version == "latest":
            if not available_versions:
                print(f"Nenhuma versão disponível para {package_name}")
                return False
            version = max(available_versions)  # Versão mais alta
        
        if version not in available_versions:
            print(f"Versão {version} não disponível para {package_name}")
            print(f"Versões disponíveis: {', '.join(available_versions)}")
            return False
        
        # Baixar e instalar
        if self._download_package_version(package_name, version):
            # Atualizar package.json
            package_data = self._read_package_file()
            dependency_type = "devDependencies" if dev else "dependencies"
            package_data[dependency_type][package_name] = version
            self._write_package_file(package_data)
            
            print(f"✅ {package_name}@{version} instalado com sucesso!")
            return True
        else:
            print(f"❌ Falha ao instalar {package_name}@{version}")
            return False
    
    def _install_offline_template(self, package_name, version, dev):
        """Criar template básico quando não conseguir baixar do registry"""
        package_dir = self.packages_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar arquivo principal com template
        main_file = package_dir / "index.naja"
        template_content = f"""// Pacote {package_name}
// Versão {version}
// Gerado automaticamente pelo NajaScript Package Manager

classe {package_name.replace('-', '_').title()} {{
    funcao construtor() {{
        // Inicialização do módulo
    }}
    
    funcao info() {{
        return "Módulo {package_name} versão {version}";
    }}
    
    // Adicione suas funcionalidades aqui
}}

// Exportar instância
var {package_name.replace('-', '_')} = {package_name.replace('-', '_').title()}();
"""
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # Criar package.json
        package_json = {
            "name": package_name,
            "version": version,
            "description": f"Módulo {package_name} para NajaScript",
            "main": "index.naja",
            "author": "NajaScript Community",
            "license": "MIT"
        }
        
        package_json_file = package_dir / "package.json"
        with open(package_json_file, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        
        # Atualizar package.json do projeto
        package_data = self._read_package_file()
        dependency_type = "devDependencies" if dev else "dependencies"
        package_data[dependency_type][package_name] = version
        self._write_package_file(package_data)
        
        print(f"✅ Template para {package_name}@{version} criado localmente!")
        return True
    
    def uninstall(self, package_name):
        """Desinstalar um pacote"""
        print(f"Desinstalando {package_name}...")
        
        # Remover do package.json
        package_data = self._read_package_file()
        removed = False
        
        if package_name in package_data.get("dependencies", {}):
            del package_data["dependencies"][package_name]
            removed = True
        
        if package_name in package_data.get("devDependencies", {}):
            del package_data["devDependencies"][package_name]
            removed = True
        
        if not removed:
            print(f"Pacote {package_name} não está instalado")
            return False
        
        # Remover diretório
        package_dir = self.packages_dir / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        # Salvar package.json atualizado
        self._write_package_file(package_data)
        
        print(f"✅ {package_name} desinstalado com sucesso!")
        return True
    
    def list_packages(self):
        """Listar pacotes instalados"""
        package_data = self._read_package_file()
        
        print("📦 Pacotes Instalados")
        print("=" * 40)
        
        deps = package_data.get("dependencies", {})
        dev_deps = package_data.get("devDependencies", {})
        
        if deps:
            print("\n📋 Dependências:")
            for pkg, version in deps.items():
                status = "✅" if (self.packages_dir / pkg).exists() else "❌"
                print(f"  {status} {pkg}@{version}")
        
        if dev_deps:
            print("\n🔧 Dependências de Desenvolvimento:")
            for pkg, version in dev_deps.items():
                status = "✅" if (self.packages_dir / pkg).exists() else "❌"
                print(f"  {status} {pkg}@{version}")
        
        if not deps and not dev_deps:
            print("Nenhum pacote instalado")
    
    def search(self, query):
        """Pesquisar pacotes no registry"""
        print(f"🔍 Procurando pacotes: '{query}'")
        
        registry_index = self._fetch_registry_index()
        if not registry_index:
            print("❌ Não foi possível acessar o registry")
            return
        
        packages = registry_index.get("packages", {})
        found = []
        
        # Pesquisar por nome e descrição
        for pkg_name, pkg_info in packages.items():
            if (query.lower() in pkg_name.lower() or 
                query.lower() in pkg_info.get("description", "").lower()):
                found.append((pkg_name, pkg_info))
        
        if found:
            print(f"\n📦 Encontrados {len(found)} pacote(s):")
            print("-" * 60)
            for pkg_name, pkg_info in found:
                description = pkg_info.get("description", "Sem descrição")
                versions = pkg_info.get("versions", [])
                latest = max(versions) if versions else "N/A"
                print(f"📦 {pkg_name}@{latest}")
                print(f"   {description}")
                print(f"   Versões: {', '.join(versions)}")
                print()
        else:
            print("❌ Nenhum pacote encontrado")
    
    def publish(self, package_path="."):
        """Publicar um pacote (requer configuração do GitHub)"""
        print("🚀 Publicando pacote...")
        
        # Verificar se existe package.json no diretório
        pkg_path = Path(package_path)
        package_json_file = pkg_path / "package.json"
        
        if not package_json_file.exists():
            print("❌ package.json não encontrado")
            print("Execute 'naja init' para criar um projeto")
            return False
        
        # Ler package.json
        try:
            with open(package_json_file, 'r', encoding='utf-8') as f:
                package_info = json.load(f)
        except Exception as e:
            print(f"❌ Erro ao ler package.json: {e}")
            return False
        
        package_name = package_info.get("name")
        version = package_info.get("version")
        
        if not package_name or not version:
            print("❌ package.json deve conter 'name' e 'version'")
            return False
        
        print(f"📦 Preparando para publicar {package_name}@{version}")
        print("⚠️  Publicação automática ainda não implementada")
        print("📝 Instruções manuais:")
        print(f"   1. Fork do repositório: {GITHUB_REGISTRY_URL}")
        print(f"   2. Criar diretório: packages/{package_name}/{version}/")
        print(f"   3. Adicionar seus arquivos .naja")
        print(f"   4. Atualizar registry/index.json")
        print(f"   5. Criar Pull Request")
        
        return True
    
    def init(self, name=None):
        """Inicializar um novo projeto NajaScript"""
        if not name:
            name = input("Nome do projeto: ").strip() or "meu-projeto-naja"
        
        package_data = {
            "name": name,
            "version": "1.0.0",
            "description": f"Projeto NajaScript: {name}",
            "main": "main.naja",
            "scripts": {
                "start": f"najascript main.naja"
            },
            "keywords": ["najascript"],
            "author": self.config.get("user", {}).get("name", ""),
            "license": "MIT",
            "dependencies": {},
            "devDependencies": {}
        }
        
        self._write_package_file(package_data)
        
        # Criar main.naja se não existir
        main_file = self.project_dir / "main.naja"
        if not main_file.exists():
            main_content = f"""// {name}
// Projeto NajaScript gerado automaticamente

fun main() {{
    println("Olá do {name}!");
    println("Projeto criado com NajaScript Package Manager");
}}

main();
"""
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(main_content)
        
        # Criar .gitignore se não existir
        gitignore_file = self.project_dir / ".gitignore"
        if not gitignore_file.exists():
            gitignore_content = """# NajaScript
naja_modules/
.naja_cache/
*.log

# Sistema
.DS_Store
Thumbs.db
"""
            with open(gitignore_file, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
        
        print(f"✅ Projeto '{name}' inicializado!")
        print(f"📄 Arquivos criados:")
        print(f"   - naja_packages.json")
        print(f"   - main.naja")
        print(f"   - .gitignore")
        print(f"\n🚀 Para começar:")
        print(f"   najascript main.naja")
    
    def update(self):
        """Atualizar todos os pacotes"""
        print("🔄 Atualizando pacotes...")
        
        package_data = self._read_package_file()
        deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
        
        if not deps:
            print("Nenhum pacote para atualizar")
            return
        
        for pkg_name in deps:
            print(f"\n🔄 Atualizando {pkg_name}...")
            self.install(pkg_name, "latest", pkg_name in package_data.get("devDependencies", {}))
        
        print("✅ Atualização concluída!")


def main():
    parser = argparse.ArgumentParser(description="NajaScript GitHub Package Manager")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Install
    install_parser = subparsers.add_parser("install", help="Instalar pacote")
    install_parser.add_argument("package", nargs="?", help="Nome do pacote")
    install_parser.add_argument("--version", "-v", default="latest", help="Versão específica")
    install_parser.add_argument("--dev", "-D", action="store_true", help="Instalar como dependência de desenvolvimento")
    
    # Uninstall
    uninstall_parser = subparsers.add_parser("uninstall", help="Desinstalar pacote")
    uninstall_parser.add_argument("package", help="Nome do pacote")
    
    # List
    subparsers.add_parser("list", help="Listar pacotes instalados")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Pesquisar pacotes")
    search_parser.add_argument("query", help="Termo de pesquisa")
    
    # Init
    init_parser = subparsers.add_parser("init", help="Inicializar projeto")
    init_parser.add_argument("name", nargs="?", help="Nome do projeto")
    
    # Update
    subparsers.add_parser("update", help="Atualizar todos os pacotes")
    
    # Publish
    publish_parser = subparsers.add_parser("publish", help="Publicar pacote")
    publish_parser.add_argument("path", nargs="?", default=".", help="Caminho do pacote")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Criar instância do gerenciador
    pm = NajaGitHubPackageManager()
    
    # Executar comando
    if args.command == "install":
        if args.package:
            pm.install(args.package, args.version, args.dev)
        else:
            # Instalar todas as dependências
            package_data = pm._read_package_file()
            deps = package_data.get("dependencies", {})
            dev_deps = package_data.get("devDependencies", {})
            
            for pkg, version in deps.items():
                pm.install(pkg, version, False)
            
            for pkg, version in dev_deps.items():
                pm.install(pkg, version, True)
    
    elif args.command == "uninstall":
        pm.uninstall(args.package)
    
    elif args.command == "list":
        pm.list_packages()
    
    elif args.command == "search":
        pm.search(args.query)
    
    elif args.command == "init":
        pm.init(args.name)
    
    elif args.command == "update":
        pm.update()
    
    elif args.command == "publish":
        pm.publish(args.path)


if __name__ == "__main__":
    main() 
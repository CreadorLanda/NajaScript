#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import argparse
import urllib.request
from pathlib import Path

# Constants
NAJA_PACKAGES_DIR = "naja_modules"
NAJA_PACKAGE_FILE = "naja_packages.json"
NAJA_REGISTRY_URL = "https://example.com/naja-registry"  # Placeholder for future remote registry

class NajaPackageManager:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.packages_dir = self.project_dir / NAJA_PACKAGES_DIR
        self.package_file = self.project_dir / NAJA_PACKAGE_FILE
        
        # Create packages directory if it doesn't exist
        if not self.packages_dir.exists():
            self.packages_dir.mkdir(parents=True)
            
        # Create package file if it doesn't exist
        if not self.package_file.exists():
            self._write_package_file({"dependencies": {}, "devDependencies": {}})
    
    def _read_package_file(self):
        try:
            with open(self.package_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"dependencies": {}, "devDependencies": {}}
    
    def _write_package_file(self, data):
        with open(self.package_file, 'w', encoding='utf-8') as f:
            json.dump(data, sort_keys=True, indent=2, ensure_ascii=False, fp=f)
    
    def add_package(self, package_name, version="latest", dev=False):
        """Add a package to the project"""
        print(f"Adding package {package_name}@{version}...")
        
        # Update package file
        package_data = self._read_package_file()
        dependency_type = "devDependencies" if dev else "dependencies"
        
        if package_name in package_data[dependency_type]:
            print(f"Package {package_name} is already installed. Updating...")
        
        package_data[dependency_type][package_name] = version
        self._write_package_file(package_data)
        
        # Create package directory
        package_dir = self.packages_dir / package_name
        if not package_dir.exists():
            package_dir.mkdir(parents=True)
        
        # Aqui deveria tentar baixar o pacote do repositório
        # Em vez de apenas criar um arquivo com uma função info
        
        # Tentar baixar o pacote (implementação básica)
        package_downloaded = self._download_package(package_name, version, package_dir)
        
        # Se não conseguir baixar, criar um template básico
        if not package_downloaded:
            print(f"Não foi possível baixar o pacote {package_name}. Criando um template básico.")
            module_file = package_dir / "index.naja"
            with open(module_file, 'w', encoding='utf-8') as f:
                # Usar o formato do gerenciador_ficheiros.naja como exemplo
                f.write(f"// Módulo {package_name}\n")
                f.write(f"// Versão {version}\n\n")
                
                # Criar uma classe com nome baseado no pacote
                class_name = ''.join(word.capitalize() for word in package_name.split('_'))
                
                f.write(f"classe {class_name} {{\n")
                f.write("    funcao construtor() {\n")
                f.write("        // Inicialização do módulo\n")
                f.write("    }\n\n")
                
                f.write("    // Função de exemplo\n")
                f.write("    funcao info() {\n")
                f.write(f"        retornar \"Módulo {package_name} versão {version}\";\n")
                f.write("    }\n\n")
                
                f.write("    // Adicione seus métodos aqui\n")
                f.write("    // ...\n")
                f.write("}\n\n")
                
                f.write(f"// Exportar uma instância da classe\n")
                f.write(f"var instancia = {class_name}();\n")
        
        print(f"Successfully added {package_name}@{version}")
        return True
    
    def _download_package(self, package_name, version, dest_dir):
        """Tenta baixar um pacote do repositório configurado"""
        try:
            # Tentar importar e usar o NajaRepositoryManager
            try:
                from naja_repository_manager import NajaRepositoryManager
                repo_manager = NajaRepositoryManager(self.project_dir)
                
                # Se conseguir, tentar instalar do repositório
                # Não chamamos o install_from_repo diretamente porque já estamos 
                # processando o pacote no add_package
                
                # Tentar primeiro o repositório local
                local_repo = repo_manager.config.get("repositories", {}).get("local")
                if local_repo:
                    try:
                        repo_path = Path(local_repo)
                        if repo_manager._install_from_local(repo_path, package_name, version, False):
                            return True
                    except Exception as e:
                        print(f"Erro ao buscar do repositório local: {e}")
                
                # Se falhar e o repositório remoto estiver habilitado, tentar remote
                if repo_manager.config.get("use_remote", False):
                    try:
                        if repo_manager._install_from_remote(package_name, version, False):
                            return True
                    except Exception as e:
                        print(f"Erro ao buscar do repositório remoto: {e}")
                
                return False
                
            except ImportError:
                print("NajaRepositoryManager não disponível. Impossível baixar pacotes automáticamente.")
                return False
        except Exception as e:
            print(f"Erro ao baixar o pacote: {e}")
            return False
    
    def remove_package(self, package_name, dev=False):
        """Remove a package from the project"""
        print(f"Removing package {package_name}...")
        
        # Update package file
        package_data = self._read_package_file()
        dependency_type = "devDependencies" if dev else "dependencies"
        
        if package_name not in package_data[dependency_type]:
            print(f"Package {package_name} is not installed.")
            return False
        
        # Remove from package file
        del package_data[dependency_type][package_name]
        self._write_package_file(package_data)
        
        # Remove package directory
        package_dir = self.packages_dir / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        print(f"Successfully removed {package_name}")
        return True
    
    def list_packages(self):
        """List all installed packages"""
        package_data = self._read_package_file()
        
        print("=== Installed Packages ===")
        
        print("\nDependencies:")
        if package_data["dependencies"]:
            for pkg, version in package_data["dependencies"].items():
                print(f"  - {pkg}@{version}")
        else:
            print("  No dependencies installed")
        
        print("\nDev Dependencies:")
        if package_data["devDependencies"]:
            for pkg, version in package_data["devDependencies"].items():
                print(f"  - {pkg}@{version}")
        else:
            print("  No dev dependencies installed")
    
    def install(self):
        """Install all packages listed in the package file"""
        package_data = self._read_package_file()
        
        print("Installing dependencies...")
        for pkg, version in package_data["dependencies"].items():
            self.add_package(pkg, version)
        
        print("\nInstalling dev dependencies...")
        for pkg, version in package_data["devDependencies"].items():
            self.add_package(pkg, version, dev=True)
        
        print("\nAll packages installed successfully!")

def main():
    parser = argparse.ArgumentParser(description="NajaScript Package Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a package")
    add_parser.add_argument("package", help="Package name")
    add_parser.add_argument("--version", "-v", default="latest", help="Package version")
    add_parser.add_argument("--dev", "-d", action="store_true", help="Add as dev dependency")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a package")
    remove_parser.add_argument("package", help="Package name")
    remove_parser.add_argument("--dev", "-d", action="store_true", help="Remove from dev dependencies")
    
    # List command
    subparsers.add_parser("list", help="List installed packages")
    
    # Install command
    subparsers.add_parser("install", help="Install all packages in package file")
    
    args = parser.parse_args()
    
    npm = NajaPackageManager()
    
    if args.command == "add":
        npm.add_package(args.package, args.version, args.dev)
    elif args.command == "remove":
        npm.remove_package(args.package, args.dev)
    elif args.command == "list":
        npm.list_packages()
    elif args.command == "install":
        npm.install()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
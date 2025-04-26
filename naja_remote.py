#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Remote Package Publisher
Publica pacotes NajaScript diretamente no repositório remoto
"""

import os
import sys
import json
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path
from naja_package_manager import NajaPackageManager, NAJA_PACKAGES_DIR
from naja_repository_manager import NajaRepositoryManager

# Constantes
TEMP_DIR = tempfile.gettempdir() + "/naja_remote"
DEFAULT_REMOTE_REPO = "https://github.com/CreadorLanda/naja-packages.git"

class NajaRemotePublisher:
    def __init__(self, repo_url=None):
        self.repo_url = repo_url or DEFAULT_REMOTE_REPO
        self.temp_path = Path(TEMP_DIR)
        self.repo_manager = NajaRepositoryManager()
        
        # Garantir que o diretório temporário exista
        if not self.temp_path.exists():
            self.temp_path.mkdir(parents=True)
            
    def _clone_or_pull_repo(self):
        """Clona ou atualiza o repositório remoto"""
        repo_dir = self.temp_path / "naja-packages"
        
        if repo_dir.exists():
            print(f"Atualizando repositório em {repo_dir}...")
            try:
                # Pull para atualizar
                subprocess.run(["git", "pull"], cwd=repo_dir, check=True)
                return repo_dir
            except subprocess.CalledProcessError:
                print("Erro ao atualizar o repositório. Tentando novamente...")
                shutil.rmtree(repo_dir)
        
        # Clonar o repositório
        print(f"Clonando repositório {self.repo_url}...")
        try:
            subprocess.run(["git", "clone", self.repo_url, str(repo_dir)], check=True)
            return repo_dir
        except subprocess.CalledProcessError as e:
            print(f"Erro ao clonar o repositório: {e}")
            return None
    
    def _initialize_repo_structure(self, repo_dir):
        """Inicializa a estrutura do repositório se necessário"""
        modules_dir = repo_dir / "modules"
        index_file = repo_dir / "index.json"
        
        # Criar diretório de módulos se não existir
        if not modules_dir.exists():
            modules_dir.mkdir(parents=True)
        
        # Criar arquivo de índice se não existir
        if not index_file.exists():
            index = {
                "name": "NajaScript Module Repository",
                "description": "Repositório público de módulos NajaScript",
                "modules": {}
            }
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
        
        return modules_dir, index_file
    
    def _read_index(self, index_file):
        """Lê o arquivo de índice do repositório"""
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"name": "NajaScript Module Repository", "modules": {}}
    
    def _write_index(self, index_file, data):
        """Escreve no arquivo de índice do repositório"""
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def publish_package(self, package_name, version=None, description=None):
        """Publica um pacote no repositório remoto"""
        # Verificar se o pacote existe localmente
        project_dir = Path.cwd()
        package_dir = project_dir / NAJA_PACKAGES_DIR / package_name
        
        if not package_dir.exists():
            print(f"Erro: O pacote {package_name} não existe localmente em {package_dir}")
            return False
        
        # Obter a versão e descrição do pacote
        if not version:
            # Tentar obter a versão do package.json
            package_json = project_dir / "naja_packages.json"
            if package_json.exists():
                try:
                    with open(package_json, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Procurar nas dependências e devDependencies
                    deps = data.get("dependencies", {})
                    dev_deps = data.get("devDependencies", {})
                    
                    if package_name in deps:
                        version = deps[package_name]
                    elif package_name in dev_deps:
                        version = dev_deps[package_name]
                    else:
                        version = "1.0.0"  # Versão padrão
                except:
                    version = "1.0.0"  # Em caso de erro, usar versão padrão
            else:
                version = "1.0.0"  # Se não encontrar o arquivo, usar versão padrão
        
        # Descrição padrão se não for fornecida
        if not description:
            description = f"Módulo NajaScript: {package_name}"
        
        # Clonar ou atualizar o repositório remoto
        repo_dir = self._clone_or_pull_repo()
        if not repo_dir:
            return False
        
        # Inicializar estrutura do repositório
        modules_dir, index_file = self._initialize_repo_structure(repo_dir)
        
        # Ler índice atual
        index = self._read_index(index_file)
        
        # Preparar o diretório do módulo no repositório
        module_dir = modules_dir / package_name / version
        if module_dir.exists():
            shutil.rmtree(module_dir)
        module_dir.mkdir(parents=True)
        
        # Copiar arquivos do módulo
        try:
            shutil.copytree(package_dir, module_dir, dirs_exist_ok=True)
            print(f"Copiados arquivos do módulo para {module_dir}")
        except Exception as e:
            print(f"Erro ao copiar arquivos: {e}")
            return False
        
        # Atualizar o índice
        if package_name not in index.get("modules", {}):
            index["modules"][package_name] = {
                "description": description,
                "versions": {}
            }
        
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        index["modules"][package_name]["versions"][version] = {
            "added": timestamp,
            "description": description
        }
        
        # Salvar índice atualizado
        self._write_index(index_file, index)
        
        # Commitar e enviar mudanças
        try:
            # Adicionar arquivos
            subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
            
            # Commitar
            commit_msg = f"Adicionar/atualizar {package_name}@{version}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir, check=True)
            
            # Push
            subprocess.run(["git", "push"], cwd=repo_dir, check=True)
            
            print(f"Módulo {package_name}@{version} publicado com sucesso no repositório remoto!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao enviar mudanças para o repositório: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="NajaScript Remote Package Publisher")
    parser.add_argument("package", help="Nome do pacote para publicar")
    parser.add_argument("--version", "-v", help="Versão do pacote")
    parser.add_argument("--description", "-d", help="Descrição do pacote")
    parser.add_argument("--repo", "-r", help="URL do repositório remoto")
    
    args = parser.parse_args()
    
    publisher = NajaRemotePublisher(args.repo)
    publisher.publish_package(args.package, args.version, args.description)

if __name__ == "__main__":
    main() 
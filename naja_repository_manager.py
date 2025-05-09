#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Repository Manager
Connects the package manager with a central repository
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
from pathlib import Path
from naja_package_manager import NajaPackageManager, NAJA_PACKAGES_DIR

# Constants
NAJA_CONFIG_FILE = ".naja_config"
NAJA_REGISTRY_URL = "https://github.com/CreadorLanda/naja-packages"  # GitHub repository
LOCAL_REPO_DEFAULT = "naja_repository"

class NajaRepositoryManager:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.config_file = self.project_dir / NAJA_CONFIG_FILE
        self.config = self._read_config()
        self.package_manager = NajaPackageManager(project_dir)
        
    def _read_config(self):
        """Read the configuration file"""
        if not self.config_file.exists():
            # Default configuration
            default_config = {
                "repositories": {
                    "local": str(Path(LOCAL_REPO_DEFAULT).resolve()),
                    "remote": NAJA_REGISTRY_URL
                },
                "use_remote": True  # Enable remote by default
            }
            self._write_config(default_config)
            return default_config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"repositories": {}, "use_remote": False}
    
    def _write_config(self, config):
        """Write to the configuration file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def set_local_repo(self, path):
        """Set the local repository path"""
        abs_path = Path(path).resolve()
        self.config["repositories"]["local"] = str(abs_path)
        self._write_config(self.config)
        print(f"Local repository set to: {abs_path}")
    
    def set_remote_repo(self, url):
        """Set the remote repository URL"""
        self.config["repositories"]["remote"] = url
        self._write_config(self.config)
        print(f"Remote repository set to: {url}")
    
    def use_remote(self, enabled=True):
        """Enable or disable remote repository"""
        self.config["use_remote"] = enabled
        self._write_config(self.config)
        status = "enabled" if enabled else "disabled"
        print(f"Remote repository access {status}")
    
    def install_from_repo(self, package_name, version="latest", dev=False):
        """Install a package from the repository"""
        # First try local repository
        local_repo = Path(self.config["repositories"]["local"])
        
        if self._install_from_local(local_repo, package_name, version, dev):
            return True
        
        # If local fails and remote is enabled, try remote repository
        if self.config["use_remote"]:
            print(f"Package {package_name} not found locally, trying remote repository...")
            if self._install_from_remote(package_name, version, dev):
                return True
        
        print(f"Package {package_name}@{version} not found in any repository")
        return False
    
    def _install_from_local(self, repo_path, package_name, version, dev):
        """Install a package from the local repository"""
        # Check if the local repository exists
        if not repo_path.exists():
            print(f"Local repository {repo_path} does not exist")
            return False
        
        # Check if the package exists
        index_file = repo_path / "index.json"
        if not index_file.exists():
            print(f"Repository index not found at {index_file}")
            return False
        
        # Read the index
        with open(index_file, 'r', encoding='utf-8') as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                print("Invalid repository index format")
                return False
        
        # Check if the package exists
        if package_name not in index.get("modules", {}):
            print(f"Package {package_name} not found in local repository")
            return False
        
        package_info = index["modules"][package_name]
        versions = package_info.get("versions", {})
        
        # Handle the version
        if version == "latest":
            # Find the latest version - this is a simple implementation
            if not versions:
                print(f"No versions available for {package_name}")
                return False
            
            # Sort versions by string, not ideal but simple for now
            version = sorted(versions.keys())[-1]
        
        if version not in versions:
            print(f"Version {version} not found for package {package_name}")
            return False
        
        # Source and destination paths
        src_path = repo_path / "modules" / package_name / version
        dst_path = self.project_dir / NAJA_PACKAGES_DIR / package_name
        
        if not src_path.exists():
            print(f"Package files not found at {src_path}")
            return False
        
        # Check if destination exists and remove it
        if dst_path.exists():
            shutil.rmtree(dst_path)
        
        # Copy the package
        try:
            shutil.copytree(src_path, dst_path)
        except Exception as e:
            print(f"Error copying package: {e}")
            return False
        
        # Update the package.json
        self.package_manager.add_package(package_name, version, dev)
        
        print(f"Successfully installed {package_name}@{version} from local repository")
        return True
    
    def _install_from_remote(self, package_name, version, dev):
        """Install a package from the remote repository (GitHub)"""
        
        print(f"Buscando pacote {package_name}@{version} no repositório remoto...")
        
        try:
            import tqdm
            has_tqdm = True
        except ImportError:
            has_tqdm = False
            print("******* anim not installed ")
        
        # Default repository URL (can be changed in config)
        repo_url = self.config.get("repositories", {}).get("remote", "https://github.com/CreadorLanda/naja-packages")
        
        # Ensure the URL is the full GitHub repo URL
        if not repo_url.startswith("https://github.com/"):
            repo_url = f"https://github.com/{repo_url}"
        
        # Extract the org/repo from the URL
        if repo_url.startswith("https://github.com/"):
            parts = repo_url[19:].split('/')
            if len(parts) >= 2:
                org_name = parts[0]
                repo_name = parts[1]
            else:
                # If URL format is just org name
                org_name = repo_url[19:]
                repo_name = "naja-packages"
        else:
            org_name = repo_url
            repo_name = "naja-packages"
        
        # Determine version tag/branch
        version_tag = version if version != "latest" else "main"
        
        print(f"Acessando {org_name}/{repo_name} (branch/tag: {version_tag})")
        
        # Diretório temporário para trabalhar
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Criar diretório para o pacote
                package_dir = os.path.join(temp_dir, package_name)
                os.makedirs(package_dir, exist_ok=True)
                
                # URLs para acesso direto aos arquivos no GitHub
                base_raw_url = f"https://raw.githubusercontent.com/{org_name}/{repo_name}/{version_tag}"
                base_api_url = f"https://api.github.com/repos/{org_name}/{repo_name}/contents"
                
                # Verificar se o diretório do pacote existe usando a API do GitHub
                api_url = f"{base_api_url}/modules/{package_name}?ref={version_tag}"
                
                print(f"Verificando existência do pacote via: {api_url}")
                
                try:
                    # Configurar um request com headers apropriados para a API do GitHub
                    request = urllib.request.Request(api_url)
                    request.add_header('Accept', 'application/vnd.github.v3+json')
                    request.add_header('User-Agent', 'NajaScript Package Manager')
                    
                    with urllib.request.urlopen(request) as response:
                        if response.getcode() == 200:
                            package_info = json.loads(response.read().decode('utf-8'))
                        else:
                            print(f"Erro ao acessar o pacote: código {response.getcode()}")
                            return False
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        print(f"Pacote {package_name} não encontrado no GitHub (erro 404)")
                        print(f"Verifique se o pacote existe em: https://github.com/{org_name}/{repo_name}/tree/{version_tag}/modules/{package_name}")
                        return False
                    else:
                        print(f"Erro HTTP: {e.code} - {e.reason}")
                        return False
                except Exception as e:
                    print(f"Erro ao verificar pacote: {e}")
                    return False
                
                # Verificar versões disponíveis
                version_to_use = version
                
                # Encontrar diretórios de versão (itens que são diretórios)
                available_versions = []
                for item in package_info:
                    if item['type'] == 'dir':
                        available_versions.append(item['name'])
                
                if not available_versions:
                    print(f"Nenhuma versão disponível para {package_name}")
                    return False
                
                print(f"Versões disponíveis: {', '.join(available_versions)}")
                
                # Determinar qual versão usar
                if version == "latest":
                    # Use a versão mais recente (ordenação simples)
                    version_to_use = sorted(available_versions)[-1]
                    print(f"Usando versão mais recente: {version_to_use}")
                else:
                    # Verificar se a versão específica existe
                    if version not in available_versions:
                        print(f"Versão {version} não encontrada para {package_name}")
                        print(f"Versões disponíveis: {', '.join(available_versions)}")
                        return False
                
                # Obter os arquivos da versão escolhida
                version_api_url = f"{base_api_url}/modules/{package_name}/{version_to_use}?ref={version_tag}"
                
                print(f"Buscando arquivos da versão {version_to_use}...")
                
                try:
                    request = urllib.request.Request(version_api_url)
                    request.add_header('Accept', 'application/vnd.github.v3+json')
                    request.add_header('User-Agent', 'NajaScript Package Manager')
                    
                    with urllib.request.urlopen(request) as response:
                        if response.getcode() == 200:
                            version_files = json.loads(response.read().decode('utf-8'))
                        else:
                            print(f"Erro ao acessar a versão: código {response.getcode()}")
                            return False
                except Exception as e:
                    print(f"Erro ao verificar versão: {e}")
                    return False
                
                # Criar diretório para a versão
                version_dir = os.path.join(package_dir, version_to_use)
                os.makedirs(version_dir, exist_ok=True)
                
                # Baixar cada arquivo da versão
                found_index_naja = False
                found_index_ns = False
                
                # Mostrar uma barra de progresso para o download se tqdm estiver disponível
                if has_tqdm:
                    progress_bar = tqdm.tqdm(total=len(version_files), desc="Downloading files", unit="file")
                
                for file_info in version_files:
                    file_name = file_info['name']
                    if file_name == "index.naja":
                        found_index_naja = True
                    elif file_name == "index.ns":
                        found_index_ns = True
                    
                    # Usar download_url diretamente da resposta da API
                    if 'download_url' in file_info and file_info['download_url']:
                        raw_file_url = file_info['download_url']
                    else:
                        # Fallback para URL direta
                        raw_file_url = f"{base_raw_url}/modules/{package_name}/{version_to_use}/{file_name}"
                    
                    file_path = os.path.join(version_dir, file_name)
                    
                    if not has_tqdm:
                        print(f"Baixando arquivo: {file_name}")
                    
                    try:
                        # Criar request para obter o conteúdo do arquivo
                        file_request = urllib.request.Request(raw_file_url)
                        file_request.add_header('User-Agent', 'NajaScript Package Manager')
                        file_request.add_header('Accept', 'application/vnd.github.v3.raw')
                        
                        # Baixar o conteúdo do arquivo
                        with urllib.request.urlopen(file_request) as file_response:
                            file_content = file_response.read()
                            
                            # Verificar se o conteúdo é válido para arquivos .naja ou .ns
                            if file_name.endswith(('.naja', '.ns')):
                                try:
                                    text_content = file_content.decode('utf-8')
                                    if len(text_content.strip().splitlines()) < 3 and "export fun info()" in text_content:
                                        print(f"AVISO: O arquivo {file_name} parece ser um stub/placeholder.")
                                except UnicodeDecodeError:
                                    # Se não conseguir decodificar como texto, provavelmente é binário
                                    pass
                            
                            # Escrever o conteúdo no arquivo local
                            with open(file_path, 'wb') as f:
                                f.write(file_content)
                                if not has_tqdm:
                                    print(f"Arquivo {file_name} salvo com {len(file_content)} bytes")
                    except Exception as e:
                        print(f"Erro ao baixar {file_name}: {e}")
                        if has_tqdm:
                            progress_bar.close()
                        return False
                    
                    if has_tqdm:
                        progress_bar.update(1)
                
                if has_tqdm:
                    progress_bar.close()
                
                # Verificar se existe um arquivo index (naja ou ns)
                if not (found_index_naja or found_index_ns):
                    print(f"Arquivo index.naja ou index.ns não encontrado na versão {version_to_use}")
                    print(f"Verifique se o arquivo existe em: https://github.com/{org_name}/{repo_name}/blob/{version_tag}/modules/{package_name}/{version_to_use}")
                    
                    # Se não existe, criar um index.ns padrão
                    print("Criando arquivo index.ns padrão...")
                    index_file_path = os.path.join(version_dir, "index.ns")
                    with open(index_file_path, 'w', encoding='utf-8') as f:
                        f.write(f"// {package_name} package index file\n\n")
                        f.write(f"// Auto-generated for version {version_to_use}\n\n")
                        f.write("// Export functions\n")
                        f.write("export fun info() {\n")
                        f.write(f'    return "Package {package_name} version {version_to_use}";\n')
                        f.write("}\n")
                    
                    print(f"Arquivo index.ns criado com sucesso")
                    found_index_ns = True
                
                # Verificar que pelo menos um dos arquivos index foi encontrado ou criado
                if not (found_index_naja or found_index_ns):
                    print(f"Falha ao criar arquivo index para o pacote")
                    return False
                
                # Criar e preparar o diretório de destino
                dst_path = self.project_dir / NAJA_PACKAGES_DIR / package_name
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                
                # Copiar conteúdo para o destino
                try:
                    shutil.copytree(version_dir, dst_path)
                    print(f"Arquivos do pacote copiados para {dst_path}")
                except Exception as e:
                    print(f"Erro ao copiar arquivos do pacote: {e}")
                    return False
                
                # Atualizar o package.json com a versão atual
                self.package_manager.add_package(package_name, version_to_use, dev)
                
                print(f"✅ Pacote {package_name}@{version_to_use} instalado com sucesso do GitHub")
                return True
                
            except Exception as e:
                print(f"Erro durante instalação: {e}")
                import traceback
                traceback.print_exc()
                return False
    
    def search(self, query):
        """Search for packages in repositories"""
        print(f"Searching for packages matching '{query}'...")
        
        # Search local repository
        local_repo = Path(self.config["repositories"]["local"])
        local_results = self._search_local(local_repo, query)
        
        # Display results
        if local_results:
            print("\nLocal Repository Results:")
            for name, info in local_results.items():
                print(f"  {name}: {info['description']}")
                print(f"    Latest: {info['latest']}")
        else:
            print("\nNo local results found")
        
        # Search remote repository if enabled
        if self.config["use_remote"]:
            print("\nRemote repository search not implemented yet")
        
        return local_results
    
    def _search_local(self, repo_path, query):
        """Search the local repository"""
        results = {}
        
        if not repo_path.exists():
            return results
        
        # Read the index
        index_file = repo_path / "index.json"
        if not index_file.exists():
            return results
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        except json.JSONDecodeError:
            return results
        
        # Search for packages matching the query
        for name, info in index.get("modules", {}).items():
            if query.lower() in name.lower() or query.lower() in info.get("description", "").lower():
                # Get latest version
                versions = info.get("versions", {})
                latest = sorted(versions.keys())[-1] if versions else "N/A"
                
                results[name] = {
                    "description": info.get("description", ""),
                    "latest": latest
                }
        
        return results

def main():
    parser = argparse.ArgumentParser(description="NajaScript Repository Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Set local repository command
    local_parser = subparsers.add_parser("set-local", help="Set local repository path")
    local_parser.add_argument("path", help="Path to local repository")
    
    # Set remote repository command
    remote_parser = subparsers.add_parser("set-remote", help="Set remote repository URL")
    remote_parser.add_argument("url", help="URL of remote repository")
    
    # Toggle remote repository usage
    remote_toggle = subparsers.add_parser("use-remote", help="Enable/disable remote repository")
    remote_toggle.add_argument("--enable", action="store_true", help="Enable remote repository")
    remote_toggle.add_argument("--disable", action="store_true", help="Disable remote repository")
    
    # Install from repository
    install_parser = subparsers.add_parser("install", help="Install package from repository")
    install_parser.add_argument("package", help="Package name")
    install_parser.add_argument("--version", "-v", default="latest", help="Package version")
    install_parser.add_argument("--dev", "-d", action="store_true", help="Install as dev dependency")
    
    # Search repositories
    search_parser = subparsers.add_parser("search", help="Search for packages")
    search_parser.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    # Create repository manager
    repo_manager = NajaRepositoryManager()
    
    if args.command == "set-local":
        repo_manager.set_local_repo(args.path)
    elif args.command == "set-remote":
        repo_manager.set_remote_repo(args.url)
    elif args.command == "use-remote":
        if args.enable:
            repo_manager.use_remote(True)
        elif args.disable:
            repo_manager.use_remote(False)
        else:
            print("Please specify --enable or --disable")
    elif args.command == "install":
        repo_manager.install_from_repo(args.package, args.version, args.dev)
    elif args.command == "search":
        repo_manager.search(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
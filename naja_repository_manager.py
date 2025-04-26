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
NAJA_REGISTRY_URL = "https://example.com/naja-registry"  # Placeholder
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
                "use_remote": False
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
        
        print(f"Fetching package {package_name}@{version} from GitHub...")
        
        # Default repository URL (can be changed in config)
        repo_url = self.config.get("repositories", {}).get("remote", "https://github.com/NajaScript")
        
        # Remove 'https://github.com/' if present
        if repo_url.startswith("https://github.com/"):
            org_name = repo_url[19:]
        else:
            org_name = repo_url
        
        # Default package naming convention: naja-[package_name]
        repo_name = f"naja-{package_name.lower()}"
        
        # Determine version tag/branch
        version_tag = version if version != "latest" else "main"
        
        # GitHub ZIP URL
        zip_url = f"https://github.com/{org_name}/{repo_name}/archive/refs/heads/{version_tag}.zip"
        
        # If version is specified and not "latest", try tag URL instead of branch
        if version != "latest":
            zip_url = f"https://github.com/{org_name}/{repo_name}/archive/refs/tags/v{version}.zip"
        
        # Use temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, f"{package_name}.zip")
            
            try:
                # Download the zip file
                print(f"Downloading from {zip_url}...")
                urllib.request.urlretrieve(zip_url, zip_path)
                
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # If version tag wasn't found, try the main branch
                    if version != "latest" and version_tag != "main":
                        print(f"Version {version} not found, trying main branch...")
                        zip_url = f"https://github.com/{org_name}/{repo_name}/archive/refs/heads/main.zip"
                        try:
                            urllib.request.urlretrieve(zip_url, zip_path)
                        except urllib.error.HTTPError:
                            print(f"Package {package_name} not found on GitHub")
                            return False
                    else:
                        print(f"Package {package_name} not found on GitHub")
                        return False
                else:
                    print(f"HTTP Error: {e.code} - {e.reason}")
                    return False
            except Exception as e:
                print(f"Error downloading package: {e}")
                return False
            
            # Create extraction directory
            extract_dir = os.path.join(temp_dir, "extract")
            os.makedirs(extract_dir, exist_ok=True)
            
            # Extract the ZIP file
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            except Exception as e:
                print(f"Error extracting package: {e}")
                return False
            
            # Find the extracted directory (it might include the branch/tag name)
            extracted_dirs = os.listdir(extract_dir)
            if not extracted_dirs:
                print("No files extracted from ZIP")
                return False
            
            src_dir = os.path.join(extract_dir, extracted_dirs[0])
            
            # Create and prepare the destination directory
            dst_path = self.project_dir / NAJA_PACKAGES_DIR / package_name
            if dst_path.exists():
                shutil.rmtree(dst_path)
            
            # Look for a src or lib directory within the package
            package_src = None
            for dir_name in ["src", "lib", "naja"]:
                candidate = os.path.join(src_dir, dir_name)
                if os.path.isdir(candidate):
                    package_src = candidate
                    break
            
            # If no src/lib directory, use the root
            if package_src is None:
                package_src = src_dir
            
            # Copy contents to the destination
            try:
                shutil.copytree(package_src, dst_path)
                print(f"Package files copied to {dst_path}")
            except Exception as e:
                print(f"Error copying package files: {e}")
                return False
            
            # Ensure an index.naja file exists
            index_file = dst_path / "index.naja"
            if not index_file.exists():
                # Create a basic index.naja if missing
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(f"// {package_name} module\n\n")
                    f.write(f"export fun info() {{\n")
                    f.write(f"    return \"Package {package_name} version {version} from GitHub\";\n")
                    f.write("}\n")
            
            # Update the package.json
            self.package_manager.add_package(package_name, version, dev)
            
            print(f"Successfully installed {package_name}@{version} from GitHub")
            return True
    
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
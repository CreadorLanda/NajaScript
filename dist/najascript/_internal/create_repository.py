#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Module Repository Creator
This script sets up a basic repository structure for NajaScript modules.
"""

import os
import json
import argparse
import shutil
from pathlib import Path

# Constants
REPO_ROOT = "naja_repository"
MODULES_DIR = "modules"
INDEX_FILE = "index.json"

class NajaRepository:
    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path or REPO_ROOT).resolve()
        self.modules_path = self.repo_path / MODULES_DIR
        self.index_path = self.repo_path / INDEX_FILE
        
    def create_repository(self):
        """Create the basic repository structure"""
        print(f"Creating repository at {self.repo_path}")
        
        # Create main directories
        if not self.repo_path.exists():
            self.repo_path.mkdir(parents=True)
        
        if not self.modules_path.exists():
            self.modules_path.mkdir(parents=True)
        
        # Create initial index file
        index = {
            "name": "NajaScript Module Repository",
            "description": "Repository for NajaScript modules",
            "modules": {}
        }
        
        self._write_json(self.index_path, index)
        
        print("Repository structure created successfully!")
        
    def add_module(self, name, version, description, source_path):
        """Add a module to the repository"""
        source_path = Path(source_path).resolve()
        
        if not source_path.exists():
            print(f"Error: Source path {source_path} does not exist")
            return False
        
        # Create module directory
        module_dir = self.modules_path / name / version
        if module_dir.exists():
            print(f"Warning: Module {name}@{version} already exists. Overwriting...")
            shutil.rmtree(module_dir)
        
        module_dir.mkdir(parents=True)
        
        # Copy module files
        if source_path.is_file():
            # Single file module
            shutil.copy(source_path, module_dir / "index.naja")
        else:
            # Directory module
            shutil.copytree(source_path, module_dir, dirs_exist_ok=True)
        
        # Update index
        index = self._read_json(self.index_path)
        
        if name not in index["modules"]:
            index["modules"][name] = {
                "description": description,
                "versions": {}
            }
        
        index["modules"][name]["versions"][version] = {
            "added": self._get_timestamp(),
            "description": description
        }
        
        # Update the index file
        self._write_json(self.index_path, index)
        
        print(f"Added module {name}@{version} to repository")
        return True
    
    def list_modules(self):
        """List all modules in the repository"""
        if not self.index_path.exists():
            print("Repository index not found")
            return
        
        index = self._read_json(self.index_path)
        modules = index["modules"]
        
        if not modules:
            print("No modules in repository")
            return
        
        print("\n=== NajaScript Modules ===\n")
        for name, info in modules.items():
            print(f"{name}: {info['description']}")
            print("  Versions:")
            for version, version_info in info["versions"].items():
                print(f"    - {version}: {version_info['description']}")
            print()
    
    def _read_json(self, path):
        """Read JSON from a file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_json(self, path, data):
        """Write JSON to a file"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_timestamp(self):
        """Get current timestamp as string"""
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    parser = argparse.ArgumentParser(description="NajaScript Module Repository Creator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new repository")
    init_parser.add_argument("--path", help="Repository path")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a module to the repository")
    add_parser.add_argument("name", help="Module name")
    add_parser.add_argument("version", help="Module version")
    add_parser.add_argument("source", help="Source path (file or directory)")
    add_parser.add_argument("--description", "-d", default="", help="Module description")
    add_parser.add_argument("--repo-path", help="Repository path")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List modules in the repository")
    list_parser.add_argument("--repo-path", help="Repository path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create repository instance
    repo = NajaRepository(args.repo_path if hasattr(args, 'repo_path') and args.repo_path else None)
    
    if args.command == "init":
        repo.create_repository()
    elif args.command == "add":
        repo.add_module(args.name, args.version, args.description, args.source)
    elif args.command == "list":
        repo.list_modules()

if __name__ == "__main__":
    main() 
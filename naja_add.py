#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from naja_package_manager import NajaPackageManager
from naja_repository_manager import NajaRepositoryManager

def main():
    parser = argparse.ArgumentParser(description="NajaScript Package Installer")
    parser.add_argument("package", nargs="?", help="Package name to install")
    parser.add_argument("--version", "-v", default="latest", help="Package version")
    parser.add_argument("--dev", "-d", action="store_true", help="Install as dev dependency")
    parser.add_argument("--local", "-l", action="store_true", help="Only search local repository")
    parser.add_argument("--search", "-s", action="store_true", help="Search for packages")
    
    args = parser.parse_args()
    
    if not args.package and not args.search:
        parser.print_help()
        sys.exit(1)
    
    if args.search:
        # Search mode
        repo_manager = NajaRepositoryManager()
        repo_manager.search(args.package or "")
        return
    
    # Install mode
    package_name = args.package
    version = args.version
    dev = args.dev
    
    # First try to install from repository
    repo_manager = NajaRepositoryManager()
    
    if repo_manager.install_from_repo(package_name, version, dev):
        print(f"Successfully installed {package_name}@{version}")
        return
    
    # If repository install fails, fall back to local installation
    print(f"Package {package_name} not found in repositories. Attempting local installation...")
    
    # Initialize package manager for local install
    manager = NajaPackageManager()
    
    # Add the package
    if manager.add_package(package_name, version, dev):
        print(f"Created local package {package_name}@{version}")
    else:
        print(f"Failed to install {package_name}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
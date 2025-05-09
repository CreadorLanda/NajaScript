#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NajaScript Online Package Registry Server
Simple HTTP server to host and manage NajaScript packages
"""

import os
import sys
import json
import shutil
import datetime
import zipfile
import io
from pathlib import Path
import argparse

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Constants
REGISTRY_DIR = "naja_registry"
VERSION = "0.1.0"
DEFAULT_PORT = 8765
PACKAGE_INDEX_FILE = "package_index.json"

class NajaRegistryServer:
    def __init__(self, registry_dir=REGISTRY_DIR):
        self.registry_dir = Path(registry_dir)
        self.ensure_registry_structure()
    
    def ensure_registry_structure(self):
        """Ensure the registry directory structure exists"""
        if not self.registry_dir.exists():
            self.registry_dir.mkdir(parents=True)
            print(f"Created registry directory at {self.registry_dir}")
        
        # Create package index file if it doesn't exist
        index_path = self.registry_dir / PACKAGE_INDEX_FILE
        if not index_path.exists():
            initial_index = {
                "name": "NajaScript Package Registry",
                "description": "Central registry for NajaScript packages",
                "version": VERSION,
                "created": datetime.datetime.now().isoformat(),
                "packages": {}
            }
            self.save_index(initial_index)
            print(f"Created initial package index at {index_path}")
    
    def load_index(self):
        """Load the package index from disk"""
        index_path = self.registry_dir / PACKAGE_INDEX_FILE
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading package index: {e}")
            return {
                "name": "NajaScript Package Registry",
                "description": "Central registry for NajaScript packages",
                "version": VERSION,
                "created": datetime.datetime.now().isoformat(),
                "packages": {}
            }
    
    def save_index(self, index_data):
        """Save the package index to disk"""
        index_path = self.registry_dir / PACKAGE_INDEX_FILE
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    def list_packages(self):
        """List all packages in the registry"""
        index = self.load_index()
        return index.get("packages", {})
    
    def search_packages(self, query):
        """Search for packages by name or description"""
        packages = self.list_packages()
        if not query:
            return packages
        
        query = query.lower()
        results = {}
        
        for name, info in packages.items():
            name_match = query in name.lower()
            desc_match = query in info.get("description", "").lower()
            
            if name_match or desc_match:
                results[name] = info
        
        return results
    
    def get_package_info(self, package_name):
        """Get information about a specific package"""
        packages = self.list_packages()
        return packages.get(package_name)
    
    def get_package_version(self, package_name, version):
        """Get information about a specific package version"""
        package_info = self.get_package_info(package_name)
        if not package_info:
            return None
        
        versions = package_info.get("versions", {})
        if version == "latest":
            # Use semantic versioning to find the latest version
            if not versions:
                return None
            version = sorted(versions.keys(), key=lambda v: [int(x) for x in v.split('.')])[-1]
        
        return versions.get(version)
    
    def publish_package(self, package_name, version, description, author, files):
        """Publish a new package or update an existing one"""
        # Load current index
        index = self.load_index()
        packages = index.get("packages", {})
        
        # Create package directory
        package_dir = self.registry_dir / package_name / version
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(parents=True)
        
        # Save files
        file_list = []
        for file_name, file_content in files.items():
            file_path = package_dir / file_name
            with open(file_path, 'wb') as f:
                f.write(file_content)
            file_list.append(file_name)
        
        # Update index
        timestamp = datetime.datetime.now().isoformat()
        
        if package_name not in packages:
            packages[package_name] = {
                "name": package_name,
                "description": description,
                "author": author,
                "created": timestamp,
                "versions": {}
            }
        
        # Update version information
        packages[package_name]["versions"][version] = {
            "version": version,
            "published": timestamp,
            "files": file_list
        }
        
        # Update last modified time
        packages[package_name]["updated"] = timestamp
        
        # Save updated index
        index["packages"] = packages
        self.save_index(index)
        
        return True
    
    def create_package_archive(self, package_name, version="latest"):
        """Create a zip archive of a package"""
        package_info = self.get_package_info(package_name)
        if not package_info:
            return None
        
        versions = package_info.get("versions", {})
        if version == "latest" and versions:
            version = sorted(versions.keys(), key=lambda v: [int(x) for x in v.split('.')])[-1]
        
        if version not in versions:
            return None
        
        package_dir = self.registry_dir / package_name / version
        if not package_dir.exists():
            return None
        
        # Create in-memory zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in package_dir.glob('**/*'):
                if file_path.is_file():
                    rel_path = file_path.relative_to(package_dir)
                    zip_file.write(file_path, arcname=rel_path)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

class NajaRegistryHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, registry=None, **kwargs):
        self.registry = registry
        super().__init__(*args, **kwargs)
    
    def _set_response(self, content_type='application/json', status=200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def _send_json(self, data, status=200):
        self._set_response(status=status)
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _send_error(self, message, status=404):
        self._send_json({"error": message}, status=status)
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # API Routes
        if path == "/":
            # Registry home
            self._send_json({
                "name": "NajaScript Package Registry",
                "version": VERSION,
                "endpoints": [
                    "/packages",
                    "/package/{name}",
                    "/package/{name}/{version}",
                    "/download/{name}/{version}",
                    "/search?q={query}"
                ]
            })
        
        elif path == "/packages":
            # List all packages
            packages = self.registry.list_packages()
            self._send_json({"packages": packages})
        
        elif path.startswith("/package/"):
            # Get package info
            parts = path.strip("/").split("/")
            if len(parts) < 2:
                self._send_error("Invalid package path")
                return
            
            package_name = parts[1]
            package_info = self.registry.get_package_info(package_name)
            
            if not package_info:
                self._send_error(f"Package {package_name} not found")
                return
            
            if len(parts) >= 3:
                # Get specific version
                version = parts[2]
                version_info = self.registry.get_package_version(package_name, version)
                
                if not version_info:
                    self._send_error(f"Version {version} not found for package {package_name}")
                    return
                
                self._send_json({
                    "package": package_name,
                    "version": version,
                    "info": version_info
                })
            else:
                # Get all package info
                self._send_json(package_info)
        
        elif path.startswith("/download/"):
            # Download package
            parts = path.strip("/").split("/")
            if len(parts) < 3:
                self._send_error("Invalid download path")
                return
            
            package_name = parts[1]
            version = parts[2]
            
            package_data = self.registry.create_package_archive(package_name, version)
            if not package_data:
                self._send_error(f"Package {package_name}@{version} not found")
                return
            
            self._set_response('application/zip')
            self.wfile.write(package_data)
        
        elif path == "/search":
            # Search packages
            query_params = parse_qs(parsed_url.query)
            query = query_params.get("q", [""])[0]
            
            results = self.registry.search_packages(query)
            self._send_json({"query": query, "results": results})
        
        else:
            self._send_error("Endpoint not found", 404)
    
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Get content length
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length <= 0:
            self._send_error("No content provided", 400)
            return
        
        # Read request body
        post_data = self.rfile.read(content_length)
        
        # Handle publish endpoint
        if path == "/publish":
            try:
                # Check if it's a multipart form request for package upload
                content_type = self.headers.get('Content-Type', '')
                
                if content_type.startswith('multipart/form-data'):
                    self._send_error("Multipart form uploads not yet supported", 501)
                    return
                
                # Assume JSON payload
                try:
                    data = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError:
                    self._send_error("Invalid JSON data", 400)
                    return
                
                # Validate required fields
                required_fields = ['name', 'version', 'description', 'author', 'files']
                for field in required_fields:
                    if field not in data:
                        self._send_error(f"Missing required field: {field}", 400)
                        return
                
                # Process files (they should be base64 encoded)
                files = {}
                for filename, content_base64 in data['files'].items():
                    import base64
                    try:
                        file_content = base64.b64decode(content_base64)
                        files[filename] = file_content
                    except Exception as e:
                        self._send_error(f"Failed to decode file {filename}: {e}", 400)
                        return
                
                # Publish package
                result = self.registry.publish_package(
                    data['name'],
                    data['version'],
                    data['description'],
                    data['author'],
                    files
                )
                
                if result:
                    self._send_json({
                        "success": True,
                        "message": f"Published {data['name']}@{data['version']}"
                    })
                else:
                    self._send_error("Failed to publish package", 500)
            
            except Exception as e:
                self._send_error(f"Error processing request: {e}", 500)
        else:
            self._send_error("Endpoint not found", 404)

def run_server(port=DEFAULT_PORT, registry_dir=REGISTRY_DIR):
    registry = NajaRegistryServer(registry_dir)
    
    # Create a custom handler class with the registry instance
    def handler_class(*args, **kwargs):
        return NajaRegistryHandler(*args, registry=registry, **kwargs)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    
    print(f"Starting NajaScript Package Registry server on port {port}")
    print(f"Registry directory: {registry_dir}")
    print("Press Ctrl+C to stop server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

def main():
    parser = argparse.ArgumentParser(description="NajaScript Package Registry Server")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, 
                        help=f"Port to run the server on (default: {DEFAULT_PORT})")
    parser.add_argument("--dir", "-d", default=REGISTRY_DIR,
                        help=f"Directory to store registry data (default: {REGISTRY_DIR})")
    
    args = parser.parse_args()
    run_server(args.port, args.dir)

if __name__ == "__main__":
    main() 
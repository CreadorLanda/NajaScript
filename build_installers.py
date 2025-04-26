#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if required tools are installed"""
    try:
        import PyInstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check other requirements
    try:
        import llvmlite
        print("llvmlite is installed.")
    except ImportError:
        print("llvmlite is not installed. Installing...")
        subprocess.call([sys.executable, "-m", "pip", "install", "llvmlite"])

def build_windows():
    """Build Windows installer"""
    print("Building Windows installer...")
    
    # Build with PyInstaller
    pyinstaller_result = subprocess.call([
        sys.executable, 
        "-m", "PyInstaller", 
        "najascript_win.spec",
        "--clean"
    ])
    
    # Verificar se o build foi bem-sucedido
    if pyinstaller_result != 0:
        print("Erro ao executar PyInstaller. Verifique os logs acima.")
        return
    
    # Verificar se o arquivo executável foi criado
    exe_path = os.path.join("dist", "najascript", "najascript.exe")
    if not os.path.exists(exe_path):
        print(f"ERRO: O executável {exe_path} não foi criado pelo PyInstaller.")
        print("Verifique os logs acima para mais detalhes.")
        return
    
    print(f"PyInstaller concluído com sucesso. Executável criado: {exe_path}")
    
    # Check if Inno Setup is installed
    inno_setup = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if os.path.exists(inno_setup):
        print("Building Windows installer with Inno Setup...")
        inno_result = subprocess.call([inno_setup, "setup_windows.iss"])
        
        if inno_result == 0:
            print("Windows installer created successfully!")
        else:
            print("Error creating Windows installer. Check the logs above.")
    else:
        print("Inno Setup not found. Please install Inno Setup to build the Windows installer.")
        print("You can download it from: https://jrsoftware.org/isdl.php")
        print("After installation, run this script again or manually run the Inno Setup script: setup_windows.iss")

def build_linux():
    """Build Linux installer"""
    print("Building Linux installer...")
    
    # Build with PyInstaller
    subprocess.call([
        sys.executable, 
        "-m", "PyInstaller", 
        "najascript_linux.spec",
        "--clean"
    ])
    
    # Create a .deb package
    print("Creating .deb package...")
    try:
        # First ensure fpm is installed
        if subprocess.call(["which", "fpm"]) != 0:
            print("FPM (Effing Package Management) is not installed.")
            print("On Ubuntu/Debian, install with: sudo apt-get install ruby ruby-dev && sudo gem install fpm")
            print("On Fedora/RHEL/CentOS: sudo yum install ruby ruby-devel && sudo gem install fpm")
            print("Please install FPM and run this script again to build the .deb package.")
        else:
            # Create directory structure
            os.makedirs("deb_package/usr/local/bin", exist_ok=True)
            os.makedirs("deb_package/usr/share/applications", exist_ok=True)
            os.makedirs("deb_package/usr/share/najascript/assets", exist_ok=True)
            os.makedirs("deb_package/usr/share/najascript/modules", exist_ok=True)
            
            # Copy files
            subprocess.call(["cp", "-r", "dist/najascript/najascript", "deb_package/usr/local/bin/"])
            subprocess.call(["cp", "najascript.desktop", "deb_package/usr/share/applications/"])
            subprocess.call(["cp", "-r", "assets/*", "deb_package/usr/share/najascript/assets/"])
            subprocess.call(["cp", "-r", "modules/*", "deb_package/usr/share/najascript/modules/"])
            
            # Build the package
            subprocess.call([
                "fpm", "-s", "dir", "-t", "deb",
                "-n", "najascript",
                "-v", "1.0.0",
                "--architecture", "all",
                "--description", "NajaScript Programming Language Interpreter",
                "--maintainer", "NajaScript Team <contact@najascript.com>",
                "--url", "https://najascript.com",
                "--license", "MIT",
                "-C", "deb_package",
                "usr"
            ])
            
            print("Linux .deb package created successfully!")
    except Exception as e:
        print(f"Error creating .deb package: {e}")
        print("You can still use the PyInstaller output in dist/najascript/")

def main():
    """Main function"""
    check_requirements()
    
    # Check if LICENSE file exists
    if not os.path.exists("LICENSE"):
        print("Creating license file...")
        with open("LICENSE", "w") as f:
            f.write("""MIT License

Copyright (c) 2023 NajaScript Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    
    system = platform.system()
    if system == "Windows":
        build_windows()
    elif system == "Linux":
        build_linux()
    else:
        print(f"Unsupported platform: {system}")
        print("This script can build installers for Windows and Linux platforms.")
        choice = input("Do you want to build for Windows or Linux? (w/l): ").lower()
        if choice.startswith('w'):
            build_windows()
        elif choice.startswith('l'):
            build_linux()
        else:
            print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para gerar instalador Linux do NajaScript
Este script pode ser executado em sistemas Windows ou Linux para preparar 
o pacote de instalação Linux.
"""

import os
import sys
import shutil
import subprocess
import platform
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime

# Diretórios do projeto
SCRIPT_DIR = Path(__file__).parent.absolute()
DIST_DIR = SCRIPT_DIR / "dist"
OUTPUT_DIR = SCRIPT_DIR / "install_packages" / "linux"

# Versão do instalador
VERSION = "1.0.0"

def check_requirements():
    """Verificar requisitos de build"""
    try:
        import PyInstaller
        print("PyInstaller está instalado.")
    except ImportError:
        print("PyInstaller não está instalado. Instalando...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_spec_file():
    """Criar arquivo .spec para o PyInstaller específico para Linux"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree

block_cipher = None

# Análise principal para o najascript.py
a = Analysis(
    ['najascript.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('modules', 'modules'),
        ('LICENSE', '.'),
        ('naja_add.py', '.'),
        ('naja_add.sh', '.'),
        ('naja_remote.py', '.'),
        ('naja_remote.sh', '.'),
        ('naja_package_manager.py', '.'),
        ('naja_repository_manager.py', '.'),
        ('create_repository.py', '.'),
        ('README_naja_repo.md', '.'),
    ],
    hiddenimports=[
        'lexer', 
        'parser_naja', 
        'interpreter', 
        'naja_bytecode', 
        'naja_llvm', 
        'ast_nodes',
        'llvmlite',
        'json',
        'shutil',
        'subprocess',
        'tempfile',
        'datetime',
        'argparse'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executável principal do najascript
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='najascript',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Análise para o gerenciador de pacotes
naja_a = Analysis(
    ['naja.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'naja_package_manager',
        'naja_repository_manager',
        'json',
        'shutil',
        'argparse'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

naja_pyz = PYZ(naja_a.pure, naja_a.zipped_data, cipher=block_cipher)

naja_exe = EXE(
    naja_pyz,
    naja_a.scripts,
    [],
    exclude_binaries=True,
    name='naja',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Análise para o publicador remoto
naja_remote_a = Analysis(
    ['naja_remote.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'naja_package_manager',
        'naja_repository_manager',
        'json',
        'shutil',
        'subprocess',
        'tempfile',
        'datetime',
        'argparse'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

naja_remote_pyz = PYZ(naja_remote_a.pure, naja_remote_a.zipped_data, cipher=block_cipher)

naja_remote_exe = EXE(
    naja_remote_pyz,
    naja_remote_a.scripts,
    [],
    exclude_binaries=True,
    name='naja_remote',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

collect = COLLECT(
    exe,
    naja_exe,
    naja_remote_exe,
    a.binaries,
    naja_a.binaries,
    naja_remote_a.binaries,
    a.zipfiles,
    naja_a.zipfiles,
    naja_remote_a.zipfiles,
    a.datas,
    naja_a.datas,
    naja_remote_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='najascript',
)
"""
    
    # Escrever arquivo spec
    spec_path = SCRIPT_DIR / "najascript_linux.spec"
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    return spec_path

def create_desktop_file():
    """Criar arquivo .desktop para integração com ambiente Linux"""
    desktop_content = """[Desktop Entry]
Name=NajaScript
Comment=NajaScript Programming Language
Exec=najascript %f
Icon=/usr/share/najascript/assets/najascript_icon.png
Terminal=true
Type=Application
Categories=Development;Education;
MimeType=text/x-najascript;
Keywords=najascript;programming;education;
"""
    
    desktop_path = SCRIPT_DIR / "najascript.desktop"
    with open(desktop_path, "w", encoding="utf-8") as f:
        f.write(desktop_content)
    
    return desktop_path

def create_shell_scripts():
    """Criar scripts shell para Linux"""
    # Criar naja_add.sh
    naja_add_path = SCRIPT_DIR / "naja_add.sh"
    with open(naja_add_path, "w", encoding="utf-8") as f:
        f.write("""#!/bin/bash
python3 "$(dirname "$0")/naja_add.py" "$@"
""")
    
    # Criar naja_remote.sh
    naja_remote_path = SCRIPT_DIR / "naja_remote.sh"
    with open(naja_remote_path, "w", encoding="utf-8") as f:
        f.write("""#!/bin/bash
python3 "$(dirname "$0")/naja_remote.py" "$@"
""")
    
    # Tornar executáveis
    os.chmod(naja_add_path, 0o755)
    os.chmod(naja_remote_path, 0o755)

def create_deb_control_files(temp_dir):
    """Criar arquivos de controle para pacote .deb"""
    control_dir = Path(temp_dir) / "DEBIAN"
    control_dir.mkdir(exist_ok=True)
    
    # Arquivo control
    control_content = f"""Package: najascript
Version: {VERSION}
Section: devel
Priority: optional
Architecture: all
Depends: python3 (>= 3.8)
Maintainer: NajaScript Team <contato@najascript.org>
Description: NajaScript Programming Language
 NajaScript é uma linguagem de programação educacional,
 projetada para ser simples e intuitiva para iniciantes,
 especialmente falantes de português.
"""
    
    with open(control_dir / "control", "w", encoding="utf-8") as f:
        f.write(control_content)
    
    # Script postinst
    postinst_content = """#!/bin/bash
set -e

# Atualizar cache de aplicações
update-desktop-database -q || true

# Associar extensão .naja
if [ -f /usr/bin/xdg-mime ]; then
    xdg-mime install --novendor /usr/share/mime/packages/najascript.xml
fi

# Mensagem final
echo "NajaScript foi instalado com sucesso!"
echo "Você pode executar 'najascript' no terminal para iniciar o interpretador."
"""
    
    with open(control_dir / "postinst", "w", encoding="utf-8") as f:
        f.write(postinst_content)
    
    # Tornar executável
    os.chmod(control_dir / "postinst", 0o755)
    
    # Arquivo para associação de tipo MIME
    mime_dir = Path(temp_dir) / "usr/share/mime/packages"
    mime_dir.mkdir(parents=True, exist_ok=True)
    
    mime_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
   <mime-type type="text/x-najascript">
     <comment>NajaScript source code</comment>
     <glob pattern="*.naja"/>
     <glob pattern="*.ns"/>
   </mime-type>
</mime-info>
"""
    
    with open(mime_dir / "najascript.xml", "w", encoding="utf-8") as f:
        f.write(mime_content)

def prepare_deb_package():
    """Preparar estrutura para pacote .deb"""
    if not is_linux():
        print("Preparando estrutura de pacote .deb a partir do Windows...")
        print("Nota: Este pacote .deb precisará ser finalizado em um sistema Linux.")
    
    # Criar diretório temporário
    temp_dir = tempfile.mkdtemp(prefix="najascript_deb_")
    
    try:
        # Criar diretórios necessários
        bin_dir = Path(temp_dir) / "usr/bin"
        share_dir = Path(temp_dir) / "usr/share/najascript"
        desktop_dir = Path(temp_dir) / "usr/share/applications"
        
        bin_dir.mkdir(parents=True, exist_ok=True)
        share_dir.mkdir(parents=True, exist_ok=True)
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivos
        # Simular a saída do PyInstaller
        os.makedirs(share_dir / "assets", exist_ok=True)
        os.makedirs(share_dir / "modules", exist_ok=True)
        
        # Copiar assets e modules
        shutil.copytree(SCRIPT_DIR / "assets", share_dir / "assets", dirs_exist_ok=True)
        shutil.copytree(SCRIPT_DIR / "modules", share_dir / "modules", dirs_exist_ok=True)
        
        # Copiar arquivo .desktop
        desktop_file = create_desktop_file()
        shutil.copy(desktop_file, desktop_dir / "najascript.desktop")
        
        # Criar arquivos do shell script para serem usados como binários
        with open(bin_dir / "najascript", "w", encoding="utf-8") as f:
            f.write("""#!/bin/bash
/usr/share/najascript/najascript "$@"
""")
        
        with open(bin_dir / "naja", "w", encoding="utf-8") as f:
            f.write("""#!/bin/bash
/usr/share/najascript/naja "$@"
""")
        
        with open(bin_dir / "naja_remote", "w", encoding="utf-8") as f:
            f.write("""#!/bin/bash
/usr/share/najascript/naja_remote "$@"
""")
        
        # Tornar executáveis
        os.chmod(bin_dir / "najascript", 0o755)
        os.chmod(bin_dir / "naja", 0o755)
        os.chmod(bin_dir / "naja_remote", 0o755)
        
        # Criar arquivos de controle
        create_deb_control_files(temp_dir)
        
        # Criar arquivo de estrutura para referência
        structure_file = OUTPUT_DIR / "estrutura_deb.txt"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        with open(structure_file, "w", encoding="utf-8") as f:
            f.write(f"Estrutura do pacote .deb para NajaScript v{VERSION}\n")
            f.write("Gerado em: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            
            for root, dirs, files in os.walk(temp_dir):
                level = root.replace(temp_dir, "").count(os.sep)
                indent = "  " * level
                f.write(f"{indent}{os.path.basename(root)}/\n")
                for file in files:
                    f.write(f"{indent}  {file}\n")
        
        # Criar arquivo tar.gz com a estrutura
        package_file = OUTPUT_DIR / f"najascript-{VERSION}-linux-structure.tar.gz"
        
        make_tarfile(package_file, temp_dir)
        
        print(f"Estrutura do pacote .deb criada em: {package_file}")
        print(f"Descrição da estrutura salva em: {structure_file}")
        
        # Incluir instruções para finalizar em Linux
        instructions_file = OUTPUT_DIR / "instrucoes_instalador_linux.txt"
        with open(instructions_file, "w", encoding="utf-8") as f:
            f.write("""Instruções para finalizar o pacote .deb no Linux:

1. Descompacte o arquivo najascript-*-linux-structure.tar.gz
   $ tar -xzf najascript-*-linux-structure.tar.gz -C /tmp/

2. Copie os executáveis compilados para a estrutura:
   $ mkdir -p /tmp/najascript_deb_*/usr/share/najascript/
   $ cp -r dist/najascript/* /tmp/najascript_deb_*/usr/share/najascript/

3. Crie o pacote .deb:
   $ cd /tmp/
   $ dpkg-deb --build najascript_deb_* najascript.deb

4. O pacote najascript.deb estará pronto para instalação com:
   $ sudo dpkg -i najascript.deb
   $ sudo apt-get install -f  # Para resolver dependências

Alternativamente, instale FPM e crie o pacote .deb diretamente:
  $ sudo apt-get install ruby ruby-dev build-essential
  $ sudo gem install fpm
  $ cd /caminho/para/NajaScript
  $ python3 build_installers.py
""")
        print(f"Instruções para finalizar o instalador Linux salvas em: {instructions_file}")
        
        return package_file
    
    finally:
        if is_linux():
            # Em Linux, podemos limpar diretamente
            shutil.rmtree(temp_dir)
        else:
            # Em Windows, pode haver problemas para excluir, então apenas informamos
            print(f"Arquivos temporários em: {temp_dir}")
            print("Você pode excluir manualmente após o uso.")

def make_tarfile(output_filename, source_dir):
    """Criar arquivo tar.gz a partir de um diretório"""
    import tarfile
    with tarfile.open(output_filename, "w:gz") as tar:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                archive_name = os.path.relpath(full_path, source_dir)
                tar.add(full_path, arcname=archive_name)

def is_linux():
    """Verificar se estamos em um sistema Linux"""
    return platform.system() == "Linux"

def main():
    """Função principal"""
    print("=== Criação de Instalador Linux para NajaScript ===")
    
    # Verificar requisitos
    check_requirements()
    
    # Criar diretório de saída
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if is_linux():
        print("Ambiente Linux detectado. Preparando para build nativo...")
        create_spec_file()
        create_shell_scripts()
        # TODO: Implementar build completo em ambiente Linux
        print("Este script não executa a compilação completa em Linux ainda.")
        print("Por favor, execute o build_installers.py diretamente em Linux.")
    else:
        print("Ambiente Windows detectado. Preparando estrutura de arquivos para Linux...")
        package_file = prepare_deb_package()
        print("\nPacote preparado com sucesso!")
        print(f"Arquivo: {package_file}")
    
    print("\nProcesso concluído!")

if __name__ == "__main__":
    main() 
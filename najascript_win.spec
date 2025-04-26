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
        ('naja_add.bat', '.'),
        ('naja_remote.py', '.'),
        ('naja_remote.bat', '.'),
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
    icon='assets/najascript_icon.ico'
)

# Análise para o gerenciador de pacotes
naja_add_a = Analysis(
    ['naja_add.py'],
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

naja_add_pyz = PYZ(naja_add_a.pure, naja_add_a.zipped_data, cipher=block_cipher)

naja_add_exe = EXE(
    naja_add_pyz,
    naja_add_a.scripts,
    [],
    exclude_binaries=True,
    name='naja_add',
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
    naja_add_exe,
    naja_remote_exe,
    a.binaries,
    naja_add_a.binaries,
    naja_remote_a.binaries,
    a.zipfiles,
    naja_add_a.zipfiles,
    naja_remote_a.zipfiles,
    a.datas,
    naja_add_a.datas,
    naja_remote_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='najascript',
) 
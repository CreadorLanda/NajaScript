#!/usr/bin/env python3
"""
Script para criar instalador Windows do NajaScript v1.2.0
Gera arquivo .iss para Inno Setup
"""

import os
import shutil
from datetime import datetime

VERSION = "1.2.0"
APP_NAME = "NajaScript"

def create_inno_setup_script():
    """Cria script .iss para Inno Setup"""
    
    iss_content = f"""[Setup]
AppId={{{{B8C9A1F2-8D5E-4A3B-9C7F-1E6D4B2A8F5C}}}}
AppName={APP_NAME}
AppVersion={VERSION}
AppVerName={APP_NAME} {VERSION}
AppPublisher=NajaScript Team
AppPublisherURL=https://najascript.github.io
AppSupportURL=https://github.com/NajaScript/Naja/issues
AppUpdatesURL=https://najascript.github.io
DefaultDirName={{autopf}}\\{APP_NAME}
DefaultGroupName={APP_NAME}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoAfterFile=POST_INSTALL.txt
OutputDir=output
OutputBaseFilename=NajaScript_Setup_v{VERSION}
SetupIconFile=assets\\najascript_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "addtopath"; Description: "Adicionar NajaScript ao PATH do sistema"; GroupDescription: "Opções do Sistema"

[Files]
; Arquivos principais
Source: "najascript.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "interpreter.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "lexer.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "parser_naja.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "ast_nodes.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "environment.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "fs_module.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "http_module.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "naja_github_package_manager.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "naja_bytecode.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "jit_compiler.py"; DestDir: "{{app}}"; Flags: ignoreversion

; Assets
Source: "assets\\*"; DestDir: "{{app}}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Módulos
Source: "modules\\*"; DestDir: "{{app}}\\modules"; Flags: ignoreversion recursesubdirs createallsubdirs

; Pacotes
Source: "packages\\*"; DestDir: "{{app}}\\packages"; Flags: ignoreversion recursesubdirs createallsubdirs

; Registry
Source: "registry\\*"; DestDir: "{{app}}\\registry"; Flags: ignoreversion recursesubdirs createallsubdirs

; Exemplos
Source: "exemplos\\hello_world.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion
Source: "exemplos\\calculator.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion
Source: "exemplos\\teste_class.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion
Source: "exemplos\\teste_najahack.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion
Source: "exemplos\\flappy_bird_completo.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion
Source: "complete_math_test.naja"; DestDir: "{{app}}\\examples"; Flags: ignoreversion

; Scripts de execução
Source: "najascript.bat"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "naja.bat"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "naja_pkg.bat"; DestDir: "{{app}}"; Flags: ignoreversion

; Documentação
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "FUNCIONALIDADES_IMPLEMENTADAS.md"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\{APP_NAME}"; Filename: "{{app}}\\najascript.bat"; IconFilename: "{{app}}\\assets\\najascript_icon.ico"
Name: "{{group}}\\{APP_NAME} Package Manager"; Filename: "{{app}}\\naja_pkg.bat"; IconFilename: "{{app}}\\assets\\najascript_icon.ico"
Name: "{{group}}\\Exemplos"; Filename: "{{app}}\\examples"
Name: "{{group}}\\Documentação"; Filename: "{{app}}\\README.md"
Name: "{{group}}\\{{cm:UninstallProgram,{APP_NAME}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{APP_NAME}"; Filename: "{{app}}\\najascript.bat"; IconFilename: "{{app}}\\assets\\najascript_icon.ico"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{APP_NAME}"; Filename: "{{app}}\\najascript.bat"; IconFilename: "{{app}}\\assets\\najascript_icon.ico"; Tasks: quicklaunchicon

[Registry]
; Associação de arquivos .naja
Root: HKCR; Subkey: ".naja"; ValueType: string; ValueName: ""; ValueData: "NajaScript.File"
Root: HKCR; Subkey: "NajaScript.File"; ValueType: string; ValueName: ""; ValueData: "NajaScript Source File"
Root: HKCR; Subkey: "NajaScript.File\\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{{app}}\\assets\\najascript_icon.ico"
Root: HKCR; Subkey: "NajaScript.File\\shell\\open\\command"; ValueType: string; ValueName: ""; ValueData: "\"{{app}}\\najascript.bat\" \"%1\""

; Adicionar ao PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{{olddata}};{{app}}"; Tasks: addtopath; Check: NeedsAddPath('{{app}}')

[Run]
Filename: "{{app}}\\najascript.bat"; Parameters: "--version"; StatusMsg: "Verificando instalação..."; Flags: runhidden waituntilterminated
Filename: "{{app}}\\README.md"; Description: "{{cm:LaunchProgram,Ver documentação}}"; Flags: postinstall nowait skipifsilent shellexec

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

[CustomMessages]
portuguese.CreateDesktopIcon=Criar ícone na área de trabalho
portuguese.CreateQuickLaunchIcon=Criar ícone na barra de acesso rápido
portuguese.LaunchProgram=Executar %1
portuguese.UninstallProgram=Desinstalar %1
"""
    
    with open("najascript_setup.iss", "w", encoding="utf-8") as f:
        f.write(iss_content)
    
    print("✅ Script Inno Setup criado: najascript_setup.iss")

def create_batch_files():
    """Cria arquivos .bat para Windows"""
    
    # najascript.bat
    najascript_bat = f"""@echo off
REM NajaScript v{VERSION} - Launcher
setlocal enabledelayedexpansion

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.6+ de https://python.org
    pause
    exit /b 1
)

REM Definir diretório do NajaScript
set "NAJA_DIR=%~dp0"

REM Adicionar ao PYTHONPATH
set "PYTHONPATH=%NAJA_DIR%;%PYTHONPATH%"

REM Executar NajaScript
if "%1"=="" (
    python "%NAJA_DIR%\\najascript.py" --help
) else (
    python "%NAJA_DIR%\\najascript.py" %*
)
"""
    
    # naja.bat (alias)
    naja_bat = f"""@echo off
REM NajaScript v{VERSION} - Alias
call "%~dp0najascript.bat" %*
"""
    
    # naja_pkg.bat
    naja_pkg_bat = f"""@echo off
REM NajaScript Package Manager v{VERSION}
setlocal enabledelayedexpansion

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.6+ de https://python.org
    pause
    exit /b 1
)

REM Definir diretório do NajaScript
set "NAJA_DIR=%~dp0"

REM Adicionar ao PYTHONPATH
set "PYTHONPATH=%NAJA_DIR%;%PYTHONPATH%"

REM Executar Package Manager
python "%NAJA_DIR%\\naja_github_package_manager.py" %*
"""
    
    # Escrever arquivos
    with open("najascript.bat", "w", encoding="utf-8") as f:
        f.write(najascript_bat)
    
    with open("naja.bat", "w", encoding="utf-8") as f:
        f.write(naja_bat)
    
    with open("naja_pkg.bat", "w", encoding="utf-8") as f:
        f.write(naja_pkg_bat)
    
    print("✅ Arquivos .bat criados")

def create_license_file():
    """Cria arquivo de licença"""
    
    license_content = """MIT License

Copyright (c) 2024 NajaScript Team

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
"""
    
    with open("LICENSE.txt", "w", encoding="utf-8") as f:
        f.write(license_content)
    
    print("✅ Arquivo LICENSE.txt criado")

def create_post_install_info():
    """Cria arquivo de informações pós-instalação"""
    
    post_install_content = f"""INSTALAÇÃO CONCLUÍDA COM SUCESSO!

NajaScript v{VERSION} foi instalado em seu sistema.

🚀 COMO USAR:

1. Abra o Prompt de Comando ou PowerShell
2. Digite: najascript --help
3. Para executar um programa: najascript meu_programa.naja

📦 PACKAGE MANAGER:

- Listar pacotes: naja_pkg list
- Instalar pacote: naja_pkg install nome-do-pacote
- Buscar pacotes: naja_pkg search palavra-chave

🧮 BIBLIOTECA MATH-UTILS:

A biblioteca math-utils com 24 funções matemáticas está incluída!

Exemplo de uso:
```
import {{ pi, sqrt, factorial }} from "math-utils";

fun teste() {{
    println("Pi: " + pi());
    println("√16: " + sqrt(16.0));
    println("5! = " + factorial(5));
}}

teste();
```

📚 EXEMPLOS:

Vários exemplos estão disponíveis na pasta examples do NajaScript.

🔗 LINKS ÚTEIS:

- Documentação: https://najascript.github.io
- Repositório: https://github.com/NajaScript/Naja
- Issues: https://github.com/NajaScript/Naja/issues

PRÓXIMOS PASSOS:

1. Teste a instalação: najascript --version
2. Execute um exemplo: najascript examples\\hello_world.naja
3. Explore a documentação online

Obrigado por usar NajaScript! 🎉
"""
    
    with open("POST_INSTALL.txt", "w", encoding="utf-8") as f:
        f.write(post_install_content)
    
    print("✅ Arquivo POST_INSTALL.txt criado")

def create_windows_readme():
    """Cria README específico para Windows"""
    
    readme_content = f"""# NajaScript v{VERSION} - Windows

## 🚀 Instalação Concluída!

NajaScript foi instalado com sucesso em seu sistema Windows.

## 🎯 Como Usar

### Executar Programas
```cmd
# Executar um arquivo .naja
najascript meu_programa.naja

# Ver ajuda
najascript --help

# Verificar versão
najascript --version
```

### Package Manager
```cmd
# Listar pacotes disponíveis
naja_pkg list

# Instalar um pacote
naja_pkg install math-utils

# Buscar pacotes
naja_pkg search matemática

# Ver ajuda do package manager
naja_pkg --help
```

## 🧮 Biblioteca Math-Utils Incluída

A biblioteca math-utils com 24 funções matemáticas está pré-instalada:

```naja
import {{ pi, sqrt, sin, cos, factorial }} from "math-utils";

fun exemplo_matematica() {{
    // Constantes
    println("Pi: " + pi());
    
    // Funções básicas
    println("√25: " + sqrt(25.0));
    
    // Trigonometria
    println("sin(90°): " + sin(deg2rad(90.0)));
    
    // Funções especiais
    println("5! = " + factorial(5));
}}

exemplo_matematica();
```

## 📁 Estrutura de Arquivos

```
C:\\Program Files\\NajaScript\\
├── najascript.py          # Interpretador principal
├── najascript.bat         # Launcher Windows
├── naja_pkg.bat          # Package manager
├── modules\\              # Módulos padrão
├── packages\\             # Pacotes instalados
├── examples\\             # Exemplos de código
└── assets\\               # Recursos e ícones
```

## 📚 Exemplos Incluídos

Na pasta `examples\\`:
- `hello_world.naja` - Primeiro programa
- `calculator.naja` - Calculadora simples
- `teste_class.naja` - Programação orientada a objetos
- `complete_math_test.naja` - Teste da biblioteca matemática
- `flappy_bird_completo.naja` - Jogo completo

## 🔧 Resolução de Problemas

### "Python não encontrado"
1. Instale Python 3.6+ de https://python.org
2. Certifique-se de marcar "Add to PATH" durante a instalação
3. Reinicie o Prompt de Comando

### "Comando não reconhecido"
1. Verifique se NajaScript está no PATH do sistema
2. Reinicie o Prompt de Comando
3. Execute como Administrador se necessário

### Problemas com Pacotes
```cmd
# Verificar configuração
naja_pkg info

# Limpar cache
naja_pkg clear-cache

# Reinstalar math-utils
naja_pkg install math-utils --force
```

## 🆘 Suporte

- **Documentação**: https://najascript.github.io
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Discussões**: https://github.com/NajaScript/Naja/discussions

## 📝 Changelog v{VERSION}

- ✅ Sistema de package manager funcional
- ✅ Biblioteca math-utils com 24 funções
- ✅ Melhorias na sintaxe e performance
- ✅ Novos exemplos e documentação
- ✅ Suporte aprimorado para Windows

---

**Desenvolvido com ❤️ pela comunidade NajaScript**
"""
    
    with open("README_WINDOWS.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README Windows criado")

def create_build_instructions():
    """Cria instruções para compilar o instalador"""
    
    instructions = f"""# Instruções para Criar Instalador Windows

## Pré-requisitos

1. **Inno Setup 6.x**
   - Baixar: https://jrsoftware.org/isdl.php
   - Instalar com todas as opções

2. **Arquivos Preparados**
   - najascript_setup.iss ✅
   - Todos os arquivos .py ✅
   - Arquivos .bat ✅
   - Assets e módulos ✅

## Passos para Compilar

### 1. Preparar Ambiente
```cmd
# Verificar se todos os arquivos estão presentes
dir najascript.py
dir najascript.bat
dir najascript_setup.iss
```

### 2. Compilar com Inno Setup
```cmd
# Método 1: Interface gráfica
"C:\\Program Files (x86)\\Inno Setup 6\\Compil32.exe" najascript_setup.iss

# Método 2: Linha de comando
"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" najascript_setup.iss
```

### 3. Resultado
- Arquivo gerado: `output\\NajaScript_Setup_v{VERSION}.exe`
- Tamanho esperado: ~5-8 MB
- Inclui todos os módulos e bibliotecas

## Teste do Instalador

### 1. Instalação
1. Executar `NajaScript_Setup_v{VERSION}.exe` como Admin
2. Seguir assistente de instalação
3. Marcar "Adicionar ao PATH"

### 2. Verificação
```cmd
# Testar comando básico
najascript --version

# Testar package manager
naja_pkg list

# Testar math-utils
echo 'import {{ pi }} from "math-utils"; println("Pi: " + pi());' > teste.naja
najascript teste.naja
```

### 3. Problemas Comuns

**"Python não encontrado"**
- Usuário precisa instalar Python 3.6+
- Verificar se Python está no PATH

**"Arquivo não encontrado"**
- Verificar se todos os arquivos foram incluídos no .iss
- Conferir permissões de arquivo

## Upload para Release

### 1. GitHub Release
```bash
# Criar nova release
gh release create v{VERSION} \\
  --title "NajaScript v{VERSION}" \\
  --notes "Release notes here"

# Upload do instalador
gh release upload v{VERSION} output/NajaScript_Setup_v{VERSION}.exe
```

### 2. Documentação
- Atualizar link de download no site
- Adicionar changelog
- Testar link de download

## Estrutura Final

```
output/
└── NajaScript_Setup_v{VERSION}.exe  # Instalador final

Inclui:
✅ Interpretador NajaScript
✅ Package Manager
✅ Biblioteca math-utils
✅ Módulos padrão (NajaGame, NajaHack, etc.)
✅ Exemplos de código
✅ Documentação
✅ Associação de arquivos .naja
✅ Ícones e recursos
```

---

**Total estimado**: ~5-8 MB
**Versão**: {VERSION}
**Build**: Windows x64
"""
    
    with open("BUILD_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Instruções de build criadas")

def main():
    """Função principal"""
    
    print(f"🪟 Criando instalador Windows NajaScript v{VERSION}")
    print("=" * 50)
    
    # Criar arquivos necessários
    create_inno_setup_script()
    create_batch_files()
    create_license_file()
    create_post_install_info()
    create_windows_readme()
    create_build_instructions()
    
    print("=" * 50)
    print("✅ Arquivos do instalador Windows criados!")
    print("")
    print("📁 Arquivos gerados:")
    print("  - najascript_setup.iss (Script Inno Setup)")
    print("  - najascript.bat (Launcher principal)")
    print("  - naja.bat (Alias)")
    print("  - naja_pkg.bat (Package manager)")
    print("  - LICENSE.txt")
    print("  - POST_INSTALL.txt")
    print("  - README_WINDOWS.md")
    print("  - BUILD_INSTRUCTIONS.md")
    print("")
    print("🎯 Próximos passos:")
    print("1. Instalar Inno Setup 6.x")
    print("2. Compilar: ISCC.exe najascript_setup.iss")
    print("3. Testar instalador gerado")
    print("4. Upload para GitHub Releases")

if __name__ == "__main__":
    main() 
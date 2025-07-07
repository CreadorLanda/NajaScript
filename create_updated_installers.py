#!/usr/bin/env python3
"""
Script para criar instaladores atualizados do NajaScript v1.2.0
Inclui: math-utils library, package manager, e todas as funcionalidades novas
"""

import os
import shutil
import tarfile
import json
from datetime import datetime

# Versão atualizada
VERSION = "1.2.0"
PACKAGE_NAME = f"najascript-{VERSION}"

def create_directory_structure():
    """Cria a estrutura de diretórios para o instalador Linux"""
    
    base_dir = f"{PACKAGE_NAME}-updated"
    linux_dir = f"{base_dir}/linux/{PACKAGE_NAME}-linux-structure"
    
    # Estrutura Linux
    directories = [
        f"{linux_dir}/DEBIAN",
        f"{linux_dir}/usr/bin",
        f"{linux_dir}/usr/share/najascript/assets",
        f"{linux_dir}/usr/share/najascript/modules", 
        f"{linux_dir}/usr/share/najascript/packages",
        f"{linux_dir}/usr/share/najascript/registry",
        f"{linux_dir}/usr/share/najascript/examples",
        f"{linux_dir}/usr/share/applications",
        f"{linux_dir}/usr/share/mime/packages"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Criado: {directory}")
    
    return base_dir, linux_dir

def create_debian_control_file(linux_dir):
    """Cria o arquivo control para o pacote Debian"""
    
    control_content = f"""Package: najascript
Version: {VERSION}
Section: devel
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-pip
Maintainer: NajaScript Team <team@najascript.dev>
Description: NajaScript Programming Language
 NajaScript é uma linguagem de programação moderna e intuitiva
 com suporte a programação orientada a objetos, módulos,
 sistema de pacotes, e biblioteca matemática completa.
 .
 Funcionalidades incluem:
 - Sintaxe intuitiva e fácil de aprender
 - Sistema de módulos e pacotes
 - Biblioteca math-utils com 24 funções matemáticas
 - Suporte a POO com classes e herança
 - Sistema de eventos e programação reativa
 - Desenvolvimento de jogos com NajaGame2D
 - Ferramentas de segurança com NajaHack
 - Package manager integrado
"""
    
    with open(f"{linux_dir}/DEBIAN/control", "w", encoding="utf-8") as f:
        f.write(control_content)
    
    print("✅ Arquivo control criado")

def create_postinst_script(linux_dir):
    """Cria script de pós-instalação"""
    
    postinst_content = """#!/bin/bash
# Post-installation script for NajaScript

echo "🚀 Configurando NajaScript..."

# Tornar executáveis acessíveis
chmod +x /usr/bin/najascript
chmod +x /usr/bin/naja
chmod +x /usr/bin/naja_pkg

# Atualizar banco de dados MIME
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database /usr/share/mime
fi

# Atualizar cache de aplicações
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications
fi

echo "✅ NajaScript v1.2.0 instalado com sucesso!"
echo "📦 Package manager disponível: naja_pkg"
echo "📚 Biblioteca math-utils incluída"
echo ""
echo "Para começar:"
echo "  najascript --help"
echo "  naja_pkg list"
echo ""
echo "Documentação: https://najascript.github.io"

exit 0
"""
    
    with open(f"{linux_dir}/DEBIAN/postinst", "w", encoding="utf-8") as f:
        f.write(postinst_content)
    
    os.chmod(f"{linux_dir}/DEBIAN/postinst", 0o755)
    print("✅ Script postinst criado")

def create_executable_scripts(linux_dir):
    """Cria scripts executáveis"""
    
    # Script najascript principal
    najascript_content = """#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/share/najascript')
from najascript import main

if __name__ == "__main__":
    main()
"""
    
    # Script naja (alias)
    naja_content = """#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/share/najascript')
from najascript import main

if __name__ == "__main__":
    main()
"""
    
    # Script package manager
    naja_pkg_content = """#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/share/najascript')
from naja_github_package_manager import main

if __name__ == "__main__":
    main()
"""
    
    # Escrever scripts
    with open(f"{linux_dir}/usr/bin/najascript", "w", encoding="utf-8") as f:
        f.write(najascript_content)
    
    with open(f"{linux_dir}/usr/bin/naja", "w", encoding="utf-8") as f:
        f.write(naja_content)
        
    with open(f"{linux_dir}/usr/bin/naja_pkg", "w", encoding="utf-8") as f:
        f.write(naja_pkg_content)
    
    # Tornar executáveis
    os.chmod(f"{linux_dir}/usr/bin/najascript", 0o755)
    os.chmod(f"{linux_dir}/usr/bin/naja", 0o755)
    os.chmod(f"{linux_dir}/usr/bin/naja_pkg", 0o755)
    
    print("✅ Scripts executáveis criados")

def create_desktop_file(linux_dir):
    """Cria arquivo .desktop para o menu"""
    
    desktop_content = """[Desktop Entry]
Name=NajaScript
Comment=NajaScript Programming Language IDE
Comment[pt]=Linguagem de Programação NajaScript
Exec=najascript
Icon=najascript
Terminal=true
Type=Application
Categories=Development;IDE;Programming;
MimeType=text/x-najascript;
Keywords=programming;development;najascript;naja;
StartupNotify=true
"""
    
    with open(f"{linux_dir}/usr/share/applications/najascript.desktop", "w", encoding="utf-8") as f:
        f.write(desktop_content)
    
    print("✅ Arquivo .desktop criado")

def create_mime_type(linux_dir):
    """Cria tipo MIME para arquivos .naja"""
    
    mime_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="text/x-najascript">
        <comment>NajaScript source code</comment>
        <comment xml:lang="pt">Código fonte NajaScript</comment>
        <icon name="text-x-script"/>
        <glob pattern="*.naja"/>
        <glob pattern="*.ns"/>
    </mime-type>
</mime-info>
"""
    
    with open(f"{linux_dir}/usr/share/mime/packages/najascript.xml", "w", encoding="utf-8") as f:
        f.write(mime_content)
    
    print("✅ Tipo MIME criado")

def copy_najascript_files(linux_dir):
    """Copia arquivos do NajaScript para o instalador"""
    
    share_dir = f"{linux_dir}/usr/share/najascript"
    
    # Arquivos principais
    main_files = [
        "najascript.py", "interpreter.py", "lexer.py", "parser_naja.py",
        "ast_nodes.py", "environment.py", "fs_module.py", "http_module.py",
        "naja_github_package_manager.py", "naja_bytecode.py", "jit_compiler.py"
    ]
    
    for file in main_files:
        if os.path.exists(file):
            shutil.copy2(file, share_dir)
            print(f"✅ Copiado: {file}")
    
    # Copiar assets
    if os.path.exists("assets"):
        shutil.copytree("assets", f"{share_dir}/assets", dirs_exist_ok=True)
        print("✅ Assets copiados")
    
    # Copiar módulos
    if os.path.exists("modules"):
        shutil.copytree("modules", f"{share_dir}/modules", dirs_exist_ok=True)
        print("✅ Módulos copiados")
    
    # Copiar registry
    if os.path.exists("registry"):
        shutil.copytree("registry", f"{share_dir}/registry", dirs_exist_ok=True)
        print("✅ Registry copiado")
    
    # Copiar pacotes
    if os.path.exists("packages"):
        shutil.copytree("packages", f"{share_dir}/packages", dirs_exist_ok=True)
        print("✅ Pacotes copiados")
    
    # Copiar exemplos selecionados
    examples_dir = f"{share_dir}/examples"
    example_files = [
        "hello_world.naja", "calculator.naja", "complete_math_test.naja",
        "teste_class.naja", "teste_najahack.naja", "flappy_bird_completo.naja"
    ]
    
    for example in example_files:
        if os.path.exists(f"exemplos/{example}"):
            shutil.copy2(f"exemplos/{example}", examples_dir)
            print(f"✅ Exemplo copiado: {example}")

def create_readme(base_dir):
    """Cria README para o instalador"""
    
    readme_content = f"""# NajaScript v{VERSION} - Instaladores Atualizados

## 🚀 Novidades da Versão {VERSION}

### ✅ Novas Funcionalidades:
- **🧮 Biblioteca math-utils**: 24 funções matemáticas completas
- **📦 Package Manager**: Sistema completo de gerenciamento de pacotes
- **🔧 Ferramentas aprimoradas**: Novos módulos e exemplos
- **📚 Documentação atualizada**: Guias completos e exemplos práticos

### 📦 Biblioteca Math Utils:
- Constantes matemáticas: pi(), e(), phi()
- Funções básicas: abs(), max(), min(), pow(), sqrt()
- Trigonometria: sin(), cos(), tan(), deg2rad(), rad2deg()
- Estatística: mean(), sum()
- Funções especiais: factorial(), fibonacci(), gcd(), lcm(), isPrime()
- Arredondamento: floor(), ceil(), round()

### 🛠️ Package Manager:
- Instalação de pacotes: `naja_pkg install package-name`
- Busca de pacotes: `naja_pkg search keyword`
- Listagem: `naja_pkg list`
- Registry integrado com GitHub

## 📥 Instalação

### Linux (Ubuntu/Debian):
```bash
# Baixar e instalar
wget https://github.com/NajaScript/Naja/releases/download/v{VERSION}/najascript-{VERSION}-linux.deb
sudo dpkg -i najascript-{VERSION}-linux.deb

# Resolver dependências se necessário
sudo apt-get install -f
```

### Windows:
1. Baixar `NajaScript_Setup_v{VERSION}.exe`
2. Executar como administrador
3. Seguir instruções do instalador

## 🎯 Uso Rápido

```bash
# Verificar instalação
najascript --version

# Executar programa
najascript meu_programa.naja

# Gerenciar pacotes
naja_pkg list
naja_pkg install math-utils

# Usar biblioteca math-utils
```

```naja
import {{ pi, sqrt, factorial }} from "math-utils";

fun exemplo() {{
    float area = pi() * pow(5.0, 2);
    int fat = factorial(5);
    println("Área: " + area);
    println("5! = " + fat);
}}
```

## 🔗 Links Úteis

- **Documentação**: https://najascript.github.io
- **Repositório**: https://github.com/NajaScript/Naja
- **Issues**: https://github.com/NajaScript/Naja/issues

## 📝 Changelog v{VERSION}

- ✅ Adicionada biblioteca math-utils completa
- ✅ Sistema de package manager funcional
- ✅ Registry de pacotes integrado
- ✅ Novos exemplos e documentação
- ✅ Melhorias na sintaxe e performance
- ✅ Suporte aprimorado para Linux e Windows

---

**Feito com ❤️ pela comunidade NajaScript**
"""
    
    with open(f"{base_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README criado")

def create_linux_tarball(base_dir, linux_dir):
    """Cria arquivo tar.gz para Linux"""
    
    tarball_name = f"{base_dir}/linux/{PACKAGE_NAME}-linux-structure.tar.gz"
    
    with tarfile.open(tarball_name, "w:gz") as tar:
        tar.add(linux_dir, arcname=f"{PACKAGE_NAME}-linux-structure")
    
    print(f"✅ Tarball criado: {tarball_name}")
    
    # Informações do pacote
    size = os.path.getsize(tarball_name)
    print(f"📦 Tamanho: {size:,} bytes ({size/1024/1024:.1f} MB)")

def create_installation_guide(base_dir):
    """Cria guia de instalação detalhado"""
    
    guide_content = f"""# Guia de Instalação - NajaScript v{VERSION}

## 🐧 Linux (Ubuntu/Debian)

### Método 1: Instalação via .deb (Recomendado)

```bash
# 1. Baixar o pacote
wget https://github.com/NajaScript/Naja/releases/download/v{VERSION}/najascript-{VERSION}-linux.deb

# 2. Instalar
sudo dpkg -i najascript-{VERSION}-linux.deb

# 3. Resolver dependências (se necessário)
sudo apt-get install -f

# 4. Verificar instalação
najascript --version
naja_pkg --help
```

### Método 2: Instalação manual

```bash
# 1. Extrair arquivos
tar -xzf najascript-{VERSION}-linux-structure.tar.gz

# 2. Copiar arquivos
sudo cp -r najascript-{VERSION}-linux-structure/usr/* /usr/

# 3. Atualizar permissões
sudo chmod +x /usr/bin/najascript
sudo chmod +x /usr/bin/naja
sudo chmod +x /usr/bin/naja_pkg

# 4. Atualizar MIME types
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## 🪟 Windows

### Instalação Automática

1. **Baixar**: `NajaScript_Setup_v{VERSION}.exe`
2. **Executar como Administrador**
3. **Seguir o assistente de instalação**
4. **Reiniciar o sistema** (se solicitado)

### Verificação

```cmd
# Prompt de Comando ou PowerShell
najascript --version
naja_pkg list
```

## 🧪 Teste da Instalação

### Teste Básico
```bash
# Criar arquivo de teste
echo 'println("Olá, NajaScript v{VERSION}!");' > teste.naja

# Executar
najascript teste.naja
```

### Teste do Package Manager
```bash
# Listar pacotes disponíveis
naja_pkg list

# Instalar math-utils
naja_pkg install math-utils

# Testar biblioteca
echo 'import {{ pi, sqrt }} from "math-utils"; println("Pi: " + pi()); println("√16: " + sqrt(16.0));' > teste_math.naja
najascript teste_math.naja
```

## 🔧 Resolução de Problemas

### Linux

**Erro: "comando não encontrado"**
```bash
# Verificar se está no PATH
echo $PATH | grep -q "/usr/bin" && echo "PATH OK" || echo "Adicionar /usr/bin ao PATH"

# Adicionar ao PATH (se necessário)
echo 'export PATH="/usr/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Erro de dependências**
```bash
# Instalar Python 3.6+
sudo apt-get update
sudo apt-get install python3 python3-pip

# Verificar versão
python3 --version
```

### Windows

**Erro: "não é reconhecido como comando"**
1. Verificar se NajaScript está no PATH do sistema
2. Reiniciar o Prompt de Comando
3. Executar como Administrador

**Erro de permissões**
1. Executar Prompt como Administrador
2. Verificar antivírus (pode bloquear)
3. Adicionar exceção para NajaScript

## 📚 Primeiros Passos

### 1. Hello World
```naja
fun main() {{
    println("Olá, mundo!");
}}

main();
```

### 2. Usando math-utils
```naja
import {{ pi, factorial, isPrime }} from "math-utils";

fun demonstracao() {{
    // Constantes
    println("Pi: " + pi());
    
    // Fatorial
    println("5! = " + factorial(5));
    
    // Números primos
    println("17 é primo: " + isPrime(17));
}}

demonstracao();
```

### 3. Package Manager
```bash
# Ver pacotes instalados
naja_pkg list

# Procurar pacotes
naja_pkg search math

# Instalar pacote
naja_pkg install nome-do-pacote

# Informações do sistema
naja_pkg info
```

## 🆘 Suporte

- **Documentação**: https://najascript.github.io
- **Issues**: https://github.com/NajaScript/Naja/issues
- **Discussões**: https://github.com/NajaScript/Naja/discussions

---

**NajaScript v{VERSION} - Desenvolvido com ❤️ pela comunidade**
"""
    
    with open(f"{base_dir}/INSTALLATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Guia de instalação criado")

def main():
    """Função principal"""
    
    print(f"🚀 Criando instaladores atualizados NajaScript v{VERSION}")
    print("=" * 60)
    
    # Criar estrutura
    base_dir, linux_dir = create_directory_structure()
    
    # Criar arquivos de configuração
    create_debian_control_file(linux_dir)
    create_postinst_script(linux_dir)
    create_executable_scripts(linux_dir)
    create_desktop_file(linux_dir)
    create_mime_type(linux_dir)
    
    # Copiar arquivos do NajaScript
    copy_najascript_files(linux_dir)
    
    # Criar documentação
    create_readme(base_dir)
    create_installation_guide(base_dir)
    
    # Criar tarball
    create_linux_tarball(base_dir, linux_dir)
    
    print("=" * 60)
    print(f"✅ Instaladores criados com sucesso!")
    print(f"📁 Diretório: {base_dir}")
    print(f"📦 Versão: {VERSION}")
    print(f"🐧 Linux: {base_dir}/linux/")
    print(f"📚 Docs: {base_dir}/README.md")
    print(f"🔧 Guia: {base_dir}/INSTALLATION_GUIDE.md")
    
    print("\n🎯 Próximos passos:")
    print("1. Testar instalador Linux")
    print("2. Criar executável Windows")
    print("3. Fazer upload para GitHub Releases")
    print("4. Atualizar site de documentação")

if __name__ == "__main__":
    main() 
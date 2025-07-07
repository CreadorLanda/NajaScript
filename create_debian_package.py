#!/usr/bin/env python3
"""
Script para finalizar o pacote Debian do NajaScript v1.2.0
"""

import os
import shutil
import tarfile
import subprocess
from datetime import datetime

VERSION = "1.2.0"
PACKAGE_NAME = f"najascript-{VERSION}"

def calculate_package_size(directory):
    """Calcula o tamanho total do pacote em KB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size // 1024  # Converter para KB

def update_control_file():
    """Atualiza o arquivo control com informações precisas"""
    
    linux_dir = f"najascript-1.2.0-updated/linux/najascript-1.2.0-linux-structure"
    control_file = f"{linux_dir}/DEBIAN/control"
    
    # Calcular tamanho instalado
    installed_size = calculate_package_size(f"{linux_dir}/usr")
    
    # Ler conteúdo atual
    with open(control_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Adicionar tamanho instalado
    if "Installed-Size:" not in content:
        content = content.replace(
            "Architecture: all", 
            f"Architecture: all\nInstalled-Size: {installed_size}"
        )
    
    # Escrever de volta
    with open(control_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Control file atualizado (Tamanho: {installed_size} KB)")

def create_checksums():
    """Cria arquivo de checksums md5sums"""
    
    linux_dir = f"najascript-1.2.0-updated/linux/najascript-1.2.0-linux-structure"
    
    try:
        import hashlib
        
        md5sums = []
        
        # Percorrer todos os arquivos em usr/
        for root, dirs, files in os.walk(f"{linux_dir}/usr"):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, linux_dir)
                
                # Calcular MD5
                with open(file_path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                md5sums.append(f"{file_hash}  {relative_path}")
        
        # Escrever arquivo md5sums
        with open(f"{linux_dir}/DEBIAN/md5sums", "w", encoding="utf-8") as f:
            f.write("\n".join(md5sums) + "\n")
        
        print(f"✅ Checksums criados ({len(md5sums)} arquivos)")
        
    except Exception as e:
        print(f"⚠️  Erro ao criar checksums: {e}")

def create_debian_tarball():
    """Cria tarball pronto para conversão em .deb"""
    
    source_dir = "najascript-1.2.0-updated/linux/najascript-1.2.0-linux-structure"
    target_name = f"najascript_{VERSION}_all.tar.gz"
    
    with tarfile.open(target_name, "w:gz") as tar:
        tar.add(source_dir, arcname=f"najascript_{VERSION}_all")
    
    size = os.path.getsize(target_name)
    print(f"✅ Tarball Debian criado: {target_name}")
    print(f"📦 Tamanho: {size:,} bytes ({size/1024/1024:.1f} MB)")
    
    return target_name

def create_installation_script():
    """Cria script para instalação manual no Linux"""
    
    install_script = f"""#!/bin/bash
# Script de instalação manual do NajaScript v{VERSION}

set -e

echo "🚀 Instalando NajaScript v{VERSION}..."

# Verificar permissões
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo $0"
    exit 1
fi

# Verificar dependências
echo "📦 Verificando dependências..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Instale com: apt-get update && apt-get install python3 python3-pip"
    exit 1
fi

# Extrair arquivos
echo "📁 Extraindo arquivos..."
tar -xzf najascript_{VERSION}_all.tar.gz

# Copiar arquivos
echo "📋 Copiando arquivos do sistema..."
cp -r najascript_{VERSION}_all/usr/* /usr/

# Definir permissões
echo "🔧 Configurando permissões..."
chmod +x /usr/bin/najascript
chmod +x /usr/bin/naja
chmod +x /usr/bin/naja_pkg

# Atualizar bancos de dados
echo "🔄 Atualizando bancos de dados..."
if command -v update-mime-database &> /dev/null; then
    update-mime-database /usr/share/mime
fi

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

# Limpar arquivos temporários
rm -rf najascript_{VERSION}_all

echo "✅ Instalação concluída!"
echo ""
echo "🎯 Teste a instalação:"
echo "  najascript --version"
echo "  naja_pkg list"
echo ""
echo "📚 Documentação: https://najascript.github.io"
"""
    
    with open("install_najascript.sh", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    # Tornar executável (se no Linux)
    try:
        os.chmod("install_najascript.sh", 0o755)
    except:
        pass
    
    print("✅ Script de instalação criado: install_najascript.sh")

def create_uninstall_script():
    """Cria script de desinstalação"""
    
    uninstall_script = f"""#!/bin/bash
# Script de desinstalação do NajaScript v{VERSION}

set -e

echo "🗑️  Desinstalando NajaScript v{VERSION}..."

# Verificar permissões
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo $0"
    exit 1
fi

# Remover executáveis
echo "🗑️  Removendo executáveis..."
rm -f /usr/bin/najascript
rm -f /usr/bin/naja
rm -f /usr/bin/naja_pkg

# Remover arquivos do programa
echo "🗑️  Removendo arquivos do programa..."
rm -rf /usr/share/najascript

# Remover arquivos de sistema
echo "🗑️  Removendo configurações do sistema..."
rm -f /usr/share/applications/najascript.desktop
rm -f /usr/share/mime/packages/najascript.xml

# Atualizar bancos de dados
echo "🔄 Atualizando bancos de dados..."
if command -v update-mime-database &> /dev/null; then
    update-mime-database /usr/share/mime
fi

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

echo "✅ NajaScript removido com sucesso!"
"""
    
    with open("uninstall_najascript.sh", "w", encoding="utf-8") as f:
        f.write(uninstall_script)
    
    # Tornar executável (se no Linux)
    try:
        os.chmod("uninstall_najascript.sh", 0o755)
    except:
        pass
    
    print("✅ Script de desinstalação criado: uninstall_najascript.sh")

def create_conversion_instructions():
    """Cria instruções para converter em .deb no Linux"""
    
    instructions = f"""# Conversão para .deb no Linux

## Método 1: Usando dpkg-deb (Recomendado)

```bash
# No sistema Linux com dpkg:
cd najascript-1.2.0-updated/linux/
dpkg-deb --build najascript-1.2.0-linux-structure najascript_{VERSION}_all.deb

# Verificar pacote criado
dpkg-deb --info najascript_{VERSION}_all.deb
dpkg-deb --contents najascript_{VERSION}_all.deb
```

## Método 2: Instalação Manual

```bash
# Usar o script de instalação
chmod +x install_najascript.sh
sudo ./install_najascript.sh

# Para desinstalar
chmod +x uninstall_najascript.sh
sudo ./uninstall_najascript.sh
```

## Método 3: Usando o Tarball

```bash
# Extrair e instalar manualmente
tar -xzf najascript_{VERSION}_all.tar.gz
sudo cp -r najascript_{VERSION}_all/usr/* /usr/
sudo chmod +x /usr/bin/najascript /usr/bin/naja /usr/bin/naja_pkg
sudo update-mime-database /usr/share/mime
sudo update-desktop-database /usr/share/applications
```

## Teste da Instalação

```bash
# Verificar instalação
najascript --version

# Testar package manager
naja_pkg list

# Testar math-utils
echo 'import {{ pi }} from "math-utils"; println("Pi: " + pi());' > test.naja
najascript test.naja
```

## Estrutura do Pacote

- **Package**: najascript
- **Version**: {VERSION}
- **Architecture**: all
- **Depends**: python3 (>= 3.6), python3-pip
- **Maintainer**: NajaScript Team
- **Size**: ~4 MB

## Upload para Repositório

```bash
# Após criar o .deb:
# 1. Testar instalação em sistema limpo
# 2. Verificar dependências
# 3. Upload para GitHub Releases
# 4. Atualizar documentação
```
"""
    
    with open("DEB_CONVERSION.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Instruções de conversão criadas: DEB_CONVERSION.md")

def main():
    """Função principal"""
    
    print(f"📦 Finalizando pacote Debian NajaScript v{VERSION}")
    print("=" * 55)
    
    # Verificar se a estrutura existe
    if not os.path.exists("najascript-1.2.0-updated/linux"):
        print("❌ Estrutura do pacote não encontrada!")
        print("Execute primeiro: python create_updated_installers.py")
        return
    
    # Atualizar arquivos de controle
    update_control_file()
    create_checksums()
    
    # Criar tarball
    tarball = create_debian_tarball()
    
    # Criar scripts de instalação
    create_installation_script()
    create_uninstall_script()
    create_conversion_instructions()
    
    print("=" * 55)
    print("✅ Pacote Debian finalizado!")
    print("")
    print("📁 Arquivos criados:")
    print(f"  - {tarball} (Tarball principal)")
    print("  - install_najascript.sh (Instalação manual)")
    print("  - uninstall_najascript.sh (Desinstalação)")
    print("  - DEB_CONVERSION.md (Instruções)")
    print("")
    print("🎯 Para criar .deb no Linux:")
    print("1. Transferir arquivos para sistema Linux")
    print("2. Executar: dpkg-deb --build najascript-1.2.0-linux-structure")
    print("3. Testar: dpkg -i najascript_1.2.0_all.deb")
    print("")
    print("💡 Alternativa: usar install_najascript.sh para instalação manual")

if __name__ == "__main__":
    main() 
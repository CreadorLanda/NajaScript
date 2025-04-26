#!/bin/bash

# Script para construir o instalador do NajaScript para Linux

# Verifica requisitos
check_requirements() {
    echo "Verificando requisitos..."
    
    # Verifica Python
    python3 --version >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Python 3 não encontrado. Por favor, instale o Python 3."
        exit 1
    fi
    
    # Verifica PyInstaller
    python3 -c "import PyInstaller" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "PyInstaller não encontrado. Instalando..."
        pip3 install pyinstaller
    fi
    
    # Verifica llvmlite
    python3 -c "import llvmlite" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "llvmlite não encontrado. Instalando..."
        pip3 install llvmlite
    fi
    
    # Verifica FPM
    which fpm >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "FPM não encontrado. Por favor, instale o FPM:"
        echo "Para Ubuntu/Debian: sudo apt-get install ruby ruby-dev && sudo gem install fpm"
        echo "Para Fedora/RHEL/CentOS: sudo yum install ruby ruby-devel && sudo gem install fpm"
        exit 1
    fi
}

# Construir com PyInstaller
build_with_pyinstaller() {
    echo "Construindo com PyInstaller..."
    python3 -m PyInstaller najascript_linux.spec --clean --noconfirm
    
    if [ ! -f "dist/najascript/najascript" ]; then
        echo "ERRO: Falha ao criar o executável."
        exit 1
    fi
    
    echo "PyInstaller executado com sucesso."
}

# Criar pacote DEB
create_deb_package() {
    echo "Criando pacote .deb..."
    
    # Cria estrutura de diretórios
    mkdir -p deb_package/usr/local/bin
    mkdir -p deb_package/usr/share/applications
    mkdir -p deb_package/usr/share/najascript/assets
    mkdir -p deb_package/usr/share/najascript/modules
    
    # Cria o arquivo .desktop
    cat > najascript.desktop << EOF
[Desktop Entry]
Name=NajaScript
Comment=NajaScript Programming Language Interpreter
Exec=najascript
Icon=/usr/share/najascript/assets/najascript_icon.png
Terminal=true
Type=Application
Categories=Development;IDE;
EOF
    
    # Copia arquivos
    cp -r dist/najascript/najascript deb_package/usr/local/bin/
    cp najascript.desktop deb_package/usr/share/applications/
    cp -r assets/* deb_package/usr/share/najascript/assets/
    cp -r modules/* deb_package/usr/share/najascript/modules/
    
    # Constrói o pacote
    fpm -s dir -t deb \
        -n najascript \
        -v 1.0.0 \
        --architecture all \
        --description "NajaScript Programming Language Interpreter" \
        --maintainer "NajaScript Team <contact@najascript.com>" \
        --url "https://najascript.com" \
        --license "MIT" \
        -C deb_package \
        usr
    
    echo "Pacote .deb criado com sucesso: najascript_1.0.0_all.deb"
}

# Criar tarball
create_tarball() {
    echo "Criando tarball..."
    
    mkdir -p dist/najascript-1.0.0
    cp -r dist/najascript/* dist/najascript-1.0.0/
    
    # Criar scripts auxiliares
    cat > dist/najascript-1.0.0/install.sh << EOF
#!/bin/bash
# Instalador simples para NajaScript
echo "Instalando NajaScript..."
mkdir -p ~/.local/bin
cp najascript ~/.local/bin/
mkdir -p ~/.local/share/najascript
cp -r assets modules ~/.local/share/najascript/
echo "NajaScript instalado em ~/.local/bin/najascript"
echo "Para usar, adicione ~/.local/bin ao seu PATH se ainda não estiver."
echo "export PATH=\$HOME/.local/bin:\$PATH"
EOF
    
    chmod +x dist/najascript-1.0.0/install.sh
    
    # Criar tarball
    cd dist
    tar -czf najascript-1.0.0.tar.gz najascript-1.0.0
    cd ..
    
    echo "Tarball criado com sucesso: dist/najascript-1.0.0.tar.gz"
}

# Função principal
main() {
    check_requirements
    
    # Verifica se LICENSE existe
    if [ ! -f "LICENSE" ]; then
        echo "Criando arquivo de licença..."
        cat > LICENSE << EOF
MIT License

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
EOF
    fi
    
    build_with_pyinstaller
    create_deb_package
    create_tarball
    
    echo "Construção do Linux concluída com sucesso!"
    echo "Arquivos gerados:"
    echo "  - dist/najascript (diretório com executável e dependências)"
    echo "  - najascript_1.0.0_all.deb (pacote Debian/Ubuntu)"
    echo "  - dist/najascript-1.0.0.tar.gz (tarball para outras distribuições)"
}

# Executar função principal
main 
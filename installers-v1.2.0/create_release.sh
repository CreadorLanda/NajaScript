#!/bin/bash
# Script para fazer release do NajaScript v1.2.0

set -e

VERSION="1.2.0"
RELEASE_NAME="NajaScript v$VERSION"
RELEASE_TAG="v$VERSION"

echo "🚀 Criando release $RELEASE_NAME..."

# Verificar se gh CLI está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI não encontrado!"
    echo "Instale: https://cli.github.com/"
    exit 1
fi

# Verificar se estamos no repositório correto
if ! git remote get-url origin | grep -q "NajaScript/Naja"; then
    echo "❌ Execute no repositório NajaScript/Naja"
    exit 1
fi

# Criar tag se não existir
if ! git tag | grep -q "^$RELEASE_TAG$"; then
    echo "📝 Criando tag $RELEASE_TAG..."
    git tag $RELEASE_TAG
    git push origin $RELEASE_TAG
fi

# Criar release notes
cat > release_notes.md << 'EOF'
## 🚀 NajaScript v1.2.0 - Release Atualizada

### ✅ Novidades Principais:
- **🧮 Biblioteca math-utils**: 24 funções matemáticas completas (pi, sqrt, sin, cos, factorial, etc.)
- **📦 Package Manager**: Sistema completo de gerenciamento de pacotes com GitHub registry
- **🔧 Melhorias no interpretador**: Performance e estabilidade aprimoradas
- **📚 Documentação renovada**: Guias completos e exemplos práticos

### 📥 Downloads:

#### 🐧 Linux (Ubuntu/Debian):
- **najascript_1.2.0_all.tar.gz**: Pacote principal com script de instalação automática
- **install_najascript.sh**: Script de instalação standalone

#### 🪟 Windows:
- **NajaScript_Setup_v1.2.0.exe**: Instalador automático com Inno Setup
- **najascript_setup.iss**: Código fonte do instalador

### 🧮 Biblioteca Math-Utils Incluída:

```naja
import { pi, sqrt, sin, cos, factorial, isPrime } from "math-utils";

fun exemplo() {
    println("Pi: " + pi());
    println("√25: " + sqrt(25.0));
    println("sin(90°): " + sin(deg2rad(90.0)));
    println("5! = " + factorial(5));
    println("17 é primo: " + isPrime(17));
}
```

### 📦 Package Manager:

```bash
# Listar pacotes disponíveis
naja_pkg list

# Instalar pacote
naja_pkg install math-utils

# Buscar pacotes
naja_pkg search matematica
```

### 🛠️ Instalação Rápida:

**Linux:**
```bash
wget https://github.com/NajaScript/Naja/releases/download/v1.2.0/najascript_1.2.0_all.tar.gz
tar -xzf najascript_1.2.0_all.tar.gz
chmod +x install_najascript.sh
sudo ./install_najascript.sh
```

**Windows:**
1. Baixar `NajaScript_Setup_v1.2.0.exe`
2. Executar como Administrador
3. Seguir instruções do instalador

### 🔧 Verificação:
```bash
najascript --version
naja_pkg list
echo 'import { pi } from "math-utils"; println(pi());' > test.naja
najascript test.naja
```

### 📚 Links:
- **Documentação**: https://najascript.github.io
- **Getting Started**: https://najascript.github.io/documentation/getting-started
- **Package Manager**: https://najascript.github.io/documentation/package-manager

---

**Total de arquivos**: Interpretador + 24 funções matemáticas + Package manager + Módulos + Exemplos
**Compatibilidade**: Python 3.6+ | Linux (Ubuntu/Debian) | Windows 7+
EOF

# Criar release
echo "📦 Criando GitHub Release..."
gh release create $RELEASE_TAG \
    --title "$RELEASE_NAME" \
    --notes-file release_notes.md \
    --latest

# Upload dos arquivos
echo "📤 Fazendo upload dos arquivos..."

# Linux
if [ -f "linux/najascript_1.2.0_all.tar.gz" ]; then
    gh release upload $RELEASE_TAG "linux/najascript_1.2.0_all.tar.gz"
    echo "✅ Uploaded: najascript_1.2.0_all.tar.gz"
fi

if [ -f "linux/install_najascript.sh" ]; then
    gh release upload $RELEASE_TAG "linux/install_najascript.sh"
    echo "✅ Uploaded: install_najascript.sh"
fi

# Windows (se compilado)
if [ -f "windows/output/NajaScript_Setup_v1.2.0.exe" ]; then
    gh release upload $RELEASE_TAG "windows/output/NajaScript_Setup_v1.2.0.exe"
    echo "✅ Uploaded: NajaScript_Setup_v1.2.0.exe"
fi

# Documentação
if [ -f "documentation/README.md" ]; then
    gh release upload $RELEASE_TAG "documentation/README.md"
    echo "✅ Uploaded: README.md"
fi

echo ""
echo "✅ Release criado com sucesso!"
echo "🔗 URL: https://github.com/NajaScript/Naja/releases/tag/$RELEASE_TAG"
echo ""
echo "🎯 Próximos passos:"
echo "1. Verificar release no GitHub"
echo "2. Testar downloads"
echo "3. Atualizar site de documentação"
echo "4. Anunciar nas redes sociais"

# Limpar
rm -f release_notes.md

echo ""
echo "🎉 Release v1.2.0 publicado!"

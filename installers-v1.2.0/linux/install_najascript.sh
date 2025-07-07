#!/bin/bash
# Script de instalação manual do NajaScript v1.2.0

set -e

echo "🚀 Instalando NajaScript v1.2.0..."

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
tar -xzf najascript_1.2.0_all.tar.gz

# Copiar arquivos
echo "📋 Copiando arquivos do sistema..."
cp -r najascript_1.2.0_all/usr/* /usr/

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
rm -rf najascript_1.2.0_all

echo "✅ Instalação concluída!"
echo ""
echo "🎯 Teste a instalação:"
echo "  najascript --version"
echo "  naja_pkg list"
echo ""
echo "📚 Documentação: https://najascript.github.io"

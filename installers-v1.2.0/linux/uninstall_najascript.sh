#!/bin/bash
# Script de desinstalação do NajaScript v1.2.0

set -e

echo "🗑️  Desinstalando NajaScript v1.2.0..."

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

# Instruções para Criar Instalador Windows

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
"C:\Program Files (x86)\Inno Setup 6\Compil32.exe" najascript_setup.iss

# Método 2: Linha de comando
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" najascript_setup.iss
```

### 3. Resultado
- Arquivo gerado: `output\NajaScript_Setup_v1.2.0.exe`
- Tamanho esperado: ~5-8 MB
- Inclui todos os módulos e bibliotecas

## Teste do Instalador

### 1. Instalação
1. Executar `NajaScript_Setup_v1.2.0.exe` como Admin
2. Seguir assistente de instalação
3. Marcar "Adicionar ao PATH"

### 2. Verificação
```cmd
# Testar comando básico
najascript --version

# Testar package manager
naja_pkg list

# Testar math-utils
echo 'import { pi } from "math-utils"; println("Pi: " + pi());' > teste.naja
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
gh release create v1.2.0 \
  --title "NajaScript v1.2.0" \
  --notes "Release notes here"

# Upload do instalador
gh release upload v1.2.0 output/NajaScript_Setup_v1.2.0.exe
```

### 2. Documentação
- Atualizar link de download no site
- Adicionar changelog
- Testar link de download

## Estrutura Final

```
output/
└── NajaScript_Setup_v1.2.0.exe  # Instalador final

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
**Versão**: 1.2.0
**Build**: Windows x64

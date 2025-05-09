# Guia de Instalação - Extensão NajaScript para VS Code

Este guia explica como instalar e configurar a extensão NajaScript no Visual Studio Code de forma simplificada.

## Requisitos

Antes de começar, certifique-se de ter:

- [Node.js](https://nodejs.org/) (versão 14 ou superior)
- [Visual Studio Code](https://code.visualstudio.com/)
- NajaScript instalado e configurado no PATH do sistema

## Passo 1: Instalar as dependências da extensão

1. Abra um terminal (Prompt de Comando ou PowerShell)
2. Navegue até a pasta da extensão:
   ```
   cd caminho/para/najascript-vscode
   ```
3. Instale as dependências principais:
   ```
   npm install
   ```
4. Instale as dependências do servidor de linguagem:
   ```
   cd server
   npm install
   cd ..
   ```

## Passo 2: Empacotar a extensão

1. Instale a ferramenta VSCE globalmente (se ainda não tiver):
   ```
   npm install -g @vscode/vsce
   ```
2. Empacote a extensão:
   ```
   vsce package
   ```
3. Isso gerará um arquivo `najascript-0.1.0.vsix` (ou versão similar) na pasta da extensão

## Passo 3: Instalar a extensão no VS Code

### Método 1: Via interface gráfica

1. Abra o VS Code
2. Acesse a aba de extensões (Ctrl+Shift+X)
3. Clique nos três pontos (...) no topo da aba de extensões
4. Selecione "Install from VSIX..."
5. Navegue até o arquivo .vsix gerado e selecione-o

### Método 2: Via linha de comando

```
code --install-extension najascript-0.1.0.vsix
```

## Passo 4: Verificar a instalação

1. Reinicie o VS Code
2. Abra um arquivo .naja
3. Verifique se o destaque de sintaxe está funcionando
4. Verifique se o botão "Executar NajaScript" aparece na barra de status

## Passo 5: Configurar a extensão

1. Acesse as configurações do VS Code (Ctrl+,)
2. Pesquise por "NajaScript"
3. Configure as opções disponíveis:
   - **NajaScript: Use Terminal**: Defina como `true` para executar scripts no terminal integrado
   - **NajaScript: Enable Autocomplete**: Defina como `true` para habilitar sugestões de código

## Solução de problemas

### O botão de execução não aparece
- Certifique-se de que o arquivo aberto tem a extensão `.naja`
- Verifique se a extensão está instalada e ativa

### O autocomplete não funciona
- Verifique se a opção "Enable Autocomplete" está habilitada nas configurações
- Reinicie o VS Code após a instalação

### Erro ao executar scripts
- Certifique-se de que o interpretador NajaScript está instalado e configurado no PATH
- Verifique se o caminho para o executável do NajaScript está correto

## Executando manualmente

Se preferir, você pode executar a extensão em modo de desenvolvimento:

1. Abra a pasta da extensão no VS Code
2. Pressione F5 para iniciar a depuração
3. Uma nova janela do VS Code será aberta com a extensão carregada 
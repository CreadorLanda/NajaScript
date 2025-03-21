# Como criar o instalador do NajaScript Editor e Interpretador

Este documento descreve os passos finais para criar um instalador para o NajaScript Editor e Interpretador.

## Passos já concluídos

1. ✅ Criação dos executáveis com PyInstaller:
   - Editor: `dist/NajaScriptEditor.exe`
   - Interpretador: `dist/najascript.exe`
2. ✅ Criação do ícone para os aplicativos
3. ✅ Criação do script para o Inno Setup com opções avançadas:
   - Associação de arquivos .naja
   - Adição do interpretador ao PATH

## Passos pendentes

### 1. Instalar o Inno Setup

1. Baixe o Inno Setup em: [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)
2. Execute o instalador e siga as instruções de instalação

### 2. Compilar o instalador

1. Abra o Inno Setup
2. Abra o arquivo `najascript_setup.iss` que criamos
3. Clique em "Build" > "Compile" (ou pressione F9)
4. O instalador será criado na pasta `Instalador` com o nome `NajaScriptEditor_Setup.exe`

## Distribuição

Após criar o instalador, você pode distribuí-lo para que as pessoas possam usar o NajaScript Editor e Interpretador sem precisar instalar o Python. O instalador:

- Instala o editor e o interpretador com todas as dependências
- Permite associar arquivos .naja ao interpretador (opcional)
- Permite adicionar o interpretador ao PATH do sistema (opcional)
- Cria atalhos no Menu Iniciar e no Desktop (opcional)
- Permite desinstalação fácil pelo Painel de Controle

## Como usar o interpretador

Após a instalação, o interpretador poderá ser usado de diferentes formas:

1. **Através do editor**: Execute scripts diretamente do editor usando o botão "Executar"
2. **Pela linha de comando**: Se adicionar ao PATH, execute `najascript arquivo.naja`
3. **Por associação de arquivo**: Dê duplo clique em qualquer arquivo .naja para executá-lo

## Notas adicionais

- Os executáveis criados pelo PyInstaller contêm o Python e todas as bibliotecas necessárias
- O tamanho do instalador pode ser grande (geralmente entre 30-60 MB)
- É possível personalizar mais o instalador, como adicionar termos de licença, telas de boas-vindas, etc.

## Resolução de problemas

Se encontrar erros durante a compilação com o Inno Setup:

1. Verifique se todos os caminhos no script estão corretos
2. Certifique-se de que os executáveis foram criados corretamente pelo PyInstaller
3. Confirme se os arquivos adicionais (ícone, exemplos) existem nos caminhos especificados 
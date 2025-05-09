# NajaScript Extension for VS Code

This extension provides language support for the NajaScript programming language, including syntax highlighting, code completion, and execution in the integrated terminal.

## Features

- Syntax highlighting for NajaScript (`.naja` and `.ns` files)
- Code execution via the integrated VS Code terminal
- Code autocompletion for language keywords and functions
- Module autocompletion for imports
  - Autocompletes modules in `naja_modules` directory
  - Recognizes local modules with exported functions
  - Provides autocompletion for exported functions, classes, and variables
- Execution button in the editor title and context menu
- Default keyboard shortcuts for running code (F4)
- JSON syntax highlighting for `.naja_config` files

## Module Autocompletion

The extension now provides intelligent autocompletion for modules when writing import statements:

- Type `import "` to get autocompletion for available modules
- Modules in the `naja_modules` directory are suggested automatically
- If you create a directory with `.ns` files containing exports, it will be recognized as a module
- After importing a module, you can access its exported functions with autocompletion:
  ```
  import "mymodule";
  mymodule.exportedFunction(); // exportedFunction will be suggested
  ```

## Special Files

- `.ns` - New, shorter extension for NajaScript files
- `.naja` - Traditional NajaScript files
- `.naja_config` - Configuration files with JSON syntax highlighting

## Installation / Instalação

### English
1. Download the latest `.vsix` package from the GitHub releases
2. In VS Code, go to the Extensions view (Ctrl+Shift+X)
3. Click on the "..." menu in the top right corner
4. Select "Install from VSIX..."
5. Choose the downloaded `.vsix` file

### Português
1. Abra o Visual Studio Code
2. Pressione `Ctrl+Shift+X` para abrir a aba de extensões
3. Pesquise por "NajaScript"
4. Clique em "Instalar"

Ou instale o arquivo VSIX manualmente:
1. Baixe o arquivo `.vsix` da extensão
2. No VS Code, vá em Extensions (Ctrl+Shift+X)
3. Clique no ícone "..." e selecione "Install from VSIX..."
4. Selecione o arquivo baixado

## Usage / Uso

### English
#### Running NajaScript Code
- Open a `.naja` or `.ns` file
- Press F4 or click the run button in the editor title
- The code will execute in the integrated terminal

#### Portuguese Mode
- Use Shift+F4 to run in Portuguese mode
- Or select "Executar NajaScript (Português)" from the context menu

### Português
#### Executar código NajaScript
1. Abra um arquivo `.naja` ou `.ns`
2. Use o botão "Executar NajaScript" na barra de status
3. Alternativamente, pressione F4 ou use o menu de contexto do editor

## Configuration / Configurações

### English
The following settings are available:
- `najascript.useTerminal`: Execute NajaScript code in the integrated terminal (default: true)
- `najascript.enableAutocomplete`: Enable code suggestions and autocomplete (default: true)

### Português
Para personalizar o comportamento da extensão, acesse as configurações do VS Code (`Ctrl+,`) e procure por "NajaScript":
- **NajaScript: Use Terminal** - Execute código no terminal integrado (permite interação com input)
- **NajaScript: Enable Autocomplete** - Habilita/desabilita sugestões de código

## Development Features / Recursos de Desenvolvimento

### Autocompletar
- Palavras-chave da linguagem (`if`, `for`, `while`, `fun`, `export`, etc.)
- Tipos de dados (`int`, `string`, `bool`, etc.)
- Funções integradas (`println`, `input`, etc.)
- Métodos de objetos (`.length()`, `.add()`, etc.)
- Módulos em contextos de import
- Funções exportadas de módulos

## Keyboard Shortcuts / Atalhos de Teclado
- **F4** - Execute current NajaScript file / Executar arquivo NajaScript atual
- **Shift+F4** - Execute current NajaScript file in Portuguese mode / Executar arquivo com suporte a português

## Requirements / Requisitos
- Visual Studio Code 1.50.0 or higher / ou superior
- NajaScript installed and configured in PATH / instalado e configurado no PATH

## Packaging / Empacotamento

To create a VSIX file that can be shared and installed / Para criar um arquivo VSIX que pode ser compartilhado e instalado:

1. Install vsce / Instale o vsce:
   ```
   npm install -g @vscode/vsce
   ```

2. In the extension directory, run / No diretório da extensão, execute:
   ```
   vsce package
   ```

3. A `.vsix` file will be generated / Um arquivo `.vsix` será gerado 
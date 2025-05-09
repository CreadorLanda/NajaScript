// Servidor de linguagem para NajaScript
const {
    createConnection,
    TextDocuments,
    Diagnostic,
    DiagnosticSeverity,
    ProposedFeatures,
    InitializeParams,
    DidChangeConfigurationNotification,
    CompletionItem,
    CompletionItemKind,
    TextDocumentPositionParams,
    TextDocumentSyncKind
} = require('vscode-languageserver/node');

const { TextDocument } = require('vscode-languageserver-textdocument');
const fs = require('fs');
const path = require('path');

// Criar uma conexão para o cliente
const connection = createConnection(ProposedFeatures.all);

// Criar um gerenciador simples para os documentos de texto
const documents = new TextDocuments(TextDocument);

// Definir capacidades ao inicializar
connection.onInitialize((params) => {
    // Armazenar o rootPath para uso posterior
    connection.workspaceRoot = params.rootPath || params.rootUri;
    
    return {
        capabilities: {
            textDocumentSync: TextDocumentSyncKind.Incremental,
            // Habilitar auto-complete
            completionProvider: {
                resolveProvider: true,
                triggerCharacters: ['.', '(', '"', "'"]
            }
        }
    };
});

// Palavras-chave da linguagem NajaScript
const keywords = [
    // Tipos
    { label: 'int', kind: CompletionItemKind.Keyword, detail: 'Tipo inteiro', documentation: 'Tipo de dado inteiro' },
    { label: 'float', kind: CompletionItemKind.Keyword, detail: 'Tipo ponto flutuante', documentation: 'Tipo de dado ponto flutuante' },
    { label: 'string', kind: CompletionItemKind.Keyword, detail: 'Tipo string', documentation: 'Tipo de dado texto' },
    { label: 'bool', kind: CompletionItemKind.Keyword, detail: 'Tipo booleano', documentation: 'Tipo de dado booleano (true/false)' },
    { label: 'list', kind: CompletionItemKind.Keyword, detail: 'Tipo lista', documentation: 'Tipo de dado lista ordenada de elementos' },
    { label: 'dict', kind: CompletionItemKind.Keyword, detail: 'Tipo dicionário', documentation: 'Tipo de dado de pares chave-valor' },
    { label: 'any', kind: CompletionItemKind.Keyword, detail: 'Tipo qualquer', documentation: 'Aceita qualquer tipo de dados' },
    
    // Declarações
    { label: 'fun', kind: CompletionItemKind.Keyword, detail: 'Declaração de função', documentation: 'Define uma função' },
    { label: 'class', kind: CompletionItemKind.Keyword, detail: 'Declaração de classe', documentation: 'Define uma classe' },
    { label: 'const', kind: CompletionItemKind.Keyword, detail: 'Constante', documentation: 'Define uma constante' },
    { label: 'var', kind: CompletionItemKind.Keyword, detail: 'Variável', documentation: 'Define uma variável' },
    
    // Controle de fluxo
    { label: 'if', kind: CompletionItemKind.Keyword, detail: 'Condicional if', documentation: 'Estrutura condicional if' },
    { label: 'else', kind: CompletionItemKind.Keyword, detail: 'Condicional else', documentation: 'Bloco else para um if' },
    { label: 'elif', kind: CompletionItemKind.Keyword, detail: 'Condicional elif', documentation: 'Condicional else if' },
    { label: 'for', kind: CompletionItemKind.Keyword, detail: 'Loop for', documentation: 'Loop for' },
    { label: 'while', kind: CompletionItemKind.Keyword, detail: 'Loop while', documentation: 'Loop while' },
    { label: 'break', kind: CompletionItemKind.Keyword, detail: 'Break', documentation: 'Sai do loop atual' },
    { label: 'continue', kind: CompletionItemKind.Keyword, detail: 'Continue', documentation: 'Pula para a próxima iteração do loop' },
    { label: 'return', kind: CompletionItemKind.Keyword, detail: 'Return', documentation: 'Retorna um valor de uma função' },
    
    // Importação
    { label: 'import', kind: CompletionItemKind.Keyword, detail: 'Import', documentation: 'Importa um módulo' },
    { label: 'from', kind: CompletionItemKind.Keyword, detail: 'From', documentation: 'Especifica a origem de uma importação' },
    { label: 'export', kind: CompletionItemKind.Keyword, detail: 'Export', documentation: 'Exporta uma função ou variável' },
    
    // Membros e modificadores
    { label: 'public', kind: CompletionItemKind.Keyword, detail: 'Modificador public', documentation: 'Torna um membro acessível de qualquer lugar' },
    { label: 'private', kind: CompletionItemKind.Keyword, detail: 'Modificador private', documentation: 'Restringe acesso a membros apenas internamente' },
    { label: 'protected', kind: CompletionItemKind.Keyword, detail: 'Modificador protected', documentation: 'Restringe acesso a classe e subclasses' },
    { label: 'static', kind: CompletionItemKind.Keyword, detail: 'Modificador static', documentation: 'Define um membro pertencente à classe, não às instâncias' },
    
    // Outros
    { label: 'constructor', kind: CompletionItemKind.Constructor, detail: 'Construtor', documentation: 'Método construtor de uma classe' },
    { label: 'this', kind: CompletionItemKind.Keyword, detail: 'This', documentation: 'Referência ao objeto atual' },
    { label: 'super', kind: CompletionItemKind.Keyword, detail: 'Super', documentation: 'Referência à classe pai' },
    { label: 'true', kind: CompletionItemKind.Value, detail: 'True', documentation: 'Valor booleano verdadeiro' },
    { label: 'false', kind: CompletionItemKind.Value, detail: 'False', documentation: 'Valor booleano falso' },
    { label: 'null', kind: CompletionItemKind.Value, detail: 'Null', documentation: 'Valor nulo' }
];

// Funções internas do NajaScript 
const standardFunctions = [
    { label: 'println', kind: CompletionItemKind.Function, detail: 'println(texto)', documentation: 'Imprime um texto com quebra de linha' },
    { label: 'print', kind: CompletionItemKind.Function, detail: 'print(texto)', documentation: 'Imprime um texto sem quebra de linha' },
    { label: 'input', kind: CompletionItemKind.Function, detail: 'input(mensagem)', documentation: 'Lê entrada do usuário' },
    { label: 'len', kind: CompletionItemKind.Function, detail: 'len(objeto)', documentation: 'Retorna o tamanho de uma string, lista ou dicionário' },
    { label: 'str', kind: CompletionItemKind.Function, detail: 'str(valor)', documentation: 'Converte um valor para string' },
    { label: 'int', kind: CompletionItemKind.Function, detail: 'int(valor)', documentation: 'Converte um valor para inteiro' },
    { label: 'float', kind: CompletionItemKind.Function, detail: 'float(valor)', documentation: 'Converte um valor para ponto flutuante' },
    { label: 'bool', kind: CompletionItemKind.Function, detail: 'bool(valor)', documentation: 'Converte um valor para booleano' },
    { label: 'type', kind: CompletionItemKind.Function, detail: 'type(valor)', documentation: 'Retorna o tipo de um valor' },
    { label: 'range', kind: CompletionItemKind.Function, detail: 'range(inicio, fim, passo)', documentation: 'Cria uma sequência de números' },
    { label: 'main', kind: CompletionItemKind.Function, detail: 'main()', documentation: 'Função principal' }
];

// Armazenar módulos e suas funções exportadas
const moduleExports = new Map();

// Função para obter módulos disponíveis (tanto naja_modules quanto pastas com arquivos .ns)
function getAvailableModules(workspaceRoot) {
    if (!workspaceRoot) return [];
    
    const modules = [];
    
    try {
        // Verificar se existe diretório naja_modules
        const najaModulesPath = path.join(workspaceRoot, 'naja_modules');
        if (fs.existsSync(najaModulesPath) && fs.statSync(najaModulesPath).isDirectory()) {
            const moduleDirs = fs.readdirSync(najaModulesPath);
            
            for (const dir of moduleDirs) {
                const fullPath = path.join(najaModulesPath, dir);
                if (fs.statSync(fullPath).isDirectory()) {
                    const moduleItem = {
                        label: dir,
                        kind: CompletionItemKind.Module,
                        detail: `Módulo instalado: ${dir}`,
                        documentation: `Módulo disponível em naja_modules/${dir}`
                    };
                    modules.push(moduleItem);
                    
                    // Escanear este módulo para funções exportadas
                    scanModuleForExportedFunctions(fullPath, dir);
                }
            }
        }
        
        // Encontrar pastas no workspace que contenham arquivos .ns com export
        scanDirectoryForModules(workspaceRoot, '', modules);
        
    } catch (error) {
        console.error(`Erro ao listar módulos: ${error.message}`);
    }
    
    return modules;
}

// Expressão regular para encontrar funções exportadas
const exportedFunctionRegex = /export\s+fun\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g;
const exportedClassRegex = /export\s+class\s+([a-zA-Z_][a-zA-Z0-9_]*)/g;
const exportedVarRegex = /export\s+(var|const)\s+([a-zA-Z_][a-zA-Z0-9_]*)/g;

// Escanear um módulo para encontrar funções exportadas
function scanModuleForExportedFunctions(modulePath, moduleName) {
    const exportedItems = [];
    
    try {
        // Procurar por index.ns ou index.naja
        const indexPaths = [
            path.join(modulePath, 'index.ns'),
            path.join(modulePath, 'index.naja')
        ];
        
        let files = [];
        
        // Verificar arquivos index primeiro
        for (const indexPath of indexPaths) {
            if (fs.existsSync(indexPath)) {
                files.push(indexPath);
                break; // Usar apenas o primeiro arquivo index encontrado
            }
        }
        
        // Se não encontrou index, procurar todos os arquivos .ns/.naja
        if (files.length === 0) {
            const allFiles = getAllFiles(modulePath);
            files = allFiles.filter(file => file.endsWith('.ns') || file.endsWith('.naja'));
        }
        
        // Processar cada arquivo
        for (const file of files) {
            try {
                const content = fs.readFileSync(file, 'utf8');
                
                // Buscar funções exportadas
                let match;
                while ((match = exportedFunctionRegex.exec(content)) !== null) {
                    const functionName = match[1];
                    exportedItems.push({
                        label: functionName,
                        kind: CompletionItemKind.Function,
                        detail: `${functionName}() - Função exportada de ${moduleName}`,
                        documentation: `Função exportada do módulo ${moduleName}`
                    });
                }
                
                // Reset regex
                exportedFunctionRegex.lastIndex = 0;
                
                // Buscar classes exportadas
                while ((match = exportedClassRegex.exec(content)) !== null) {
                    const className = match[1];
                    exportedItems.push({
                        label: className,
                        kind: CompletionItemKind.Class,
                        detail: `${className} - Classe exportada de ${moduleName}`,
                        documentation: `Classe exportada do módulo ${moduleName}`
                    });
                }
                
                // Reset regex
                exportedClassRegex.lastIndex = 0;
                
                // Buscar variáveis exportadas
                while ((match = exportedVarRegex.exec(content)) !== null) {
                    const varName = match[2];
                    exportedItems.push({
                        label: varName,
                        kind: CompletionItemKind.Variable,
                        detail: `${varName} - Variável exportada de ${moduleName}`,
                        documentation: `Variável exportada do módulo ${moduleName}`
                    });
                }
                
                // Reset regex
                exportedVarRegex.lastIndex = 0;
                
            } catch (err) {
                console.error(`Erro ao ler arquivo ${file}: ${err.message}`);
            }
        }
        
        // Salvar no mapa de exportações de módulos
        if (exportedItems.length > 0) {
            moduleExports.set(moduleName, exportedItems);
        }
        
    } catch (error) {
        console.error(`Erro ao escanear módulo ${moduleName}: ${error.message}`);
    }
}

// Obter todos os arquivos recursivamente em um diretório
function getAllFiles(dirPath, arrayOfFiles = []) {
    const files = fs.readdirSync(dirPath);
    
    files.forEach(file => {
        const filePath = path.join(dirPath, file);
        if (fs.statSync(filePath).isDirectory()) {
            // Ignorar pastas node_modules e .git
            if (file !== 'node_modules' && file !== '.git') {
                arrayOfFiles = getAllFiles(filePath, arrayOfFiles);
            }
        } else {
            arrayOfFiles.push(filePath);
        }
    });
    
    return arrayOfFiles;
}

// Função recursiva para escanear diretórios em busca de módulos
function scanDirectoryForModules(baseDir, relativePath, modules) {
    try {
        const currentDir = path.join(baseDir, relativePath);
        const items = fs.readdirSync(currentDir);
        
        // Verificar se este diretório contém arquivos .ns com export
        let hasExportFile = false;
        
        for (const item of items) {
            const itemPath = path.join(currentDir, item);
            const itemRelativePath = relativePath ? path.join(relativePath, item) : item;
            
            if (fs.statSync(itemPath).isDirectory()) {
                // É um diretório, continuar recursão
                if (item !== 'node_modules' && item !== '.git' && item !== 'naja_modules') {
                    scanDirectoryForModules(baseDir, itemRelativePath, modules);
                }
            } else if (item.endsWith('.ns') || item.endsWith('.naja')) {
                // Verificar se o arquivo contém 'export'
                try {
                    const content = fs.readFileSync(itemPath, 'utf8');
                    if (content.includes('export ')) {
                        hasExportFile = true;
                    }
                } catch (err) {
                    console.error(`Erro ao ler arquivo ${itemPath}: ${err.message}`);
                }
            }
        }
        
        // Se este diretório possui arquivos com export, adicionar como módulo
        if (hasExportFile && relativePath) {
            const moduleName = path.basename(relativePath);
            
            // Evitar duplicatas
            if (!modules.some(m => m.label === moduleName)) {
                const moduleItem = {
                    label: moduleName,
                    kind: CompletionItemKind.Module,
                    detail: `Módulo local: ${moduleName}`,
                    documentation: `Módulo definido em ${relativePath}`
                };
                
                modules.push(moduleItem);
                
                // Escanear este módulo para funções exportadas
                scanModuleForExportedFunctions(path.join(baseDir, relativePath), moduleName);
            }
        }
    } catch (error) {
        console.error(`Erro ao escanear diretório ${relativePath}: ${error.message}`);
    }
}

// Cache de módulos para não ter que escanear o workspace em cada autocompletar
let modulesCache = null;
let modulesCacheTimestamp = 0;

// Fornecer auto-complete
connection.onCompletion((textDocumentPosition) => {
    // Obter o texto até a posição atual
    const document = documents.get(textDocumentPosition.textDocument.uri);
    if (!document) {
        return null;
    }

    const text = document.getText();
    const position = textDocumentPosition.position;
    const offset = document.offsetAt(position);
    
    // Verificar se estamos em um contexto específico
    const line = text.substring(text.lastIndexOf('\n', offset) + 1, offset);
    
    // Itens de conclusão padrão
    let items = [...keywords, ...standardFunctions];
    
    // Verificar contexto de importação de módulo
    const importMatch = line.match(/\b(import|importar)\s+["']([^"']*)$/);
    if (importMatch) {
        // Atualizar cache de módulos se necessário (no máximo a cada 10 segundos)
        const now = Date.now();
        if (!modulesCache || now - modulesCacheTimestamp > 10000) {
            modulesCache = getAvailableModules(connection.workspaceRoot);
            modulesCacheTimestamp = now;
        }
        
        return modulesCache;
    }
    
    // Verificar contexto de acesso a um módulo
    const moduleAccessMatch = line.match(/\b(import|importar)\s+["']([^"']+)["']\s*;\s*$/);
    if (moduleAccessMatch) {
        const moduleName = moduleAccessMatch[2];
        const moduleItems = moduleExports.get(moduleName) || [];
        return moduleItems;
    }
    
    // Verificar contexto de uso de módulo importado
    const moduleUsageMatch = line.match(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\.\s*$/);
    if (moduleUsageMatch) {
        const moduleName = moduleUsageMatch[1];
        const moduleItems = moduleExports.get(moduleName) || [];
        return moduleItems;
    }
    
    // Se estiver digitando após um '.', tente fornecer membros
    if (line.endsWith('.')) {
        // TODO: Detectar o tipo do objeto e oferecer seus métodos
        // Por enquanto, adicione alguns métodos comuns
        if (line.includes('list') || line.match(/\[\s*\w+/)) {
            items = [
                { label: 'add', kind: CompletionItemKind.Method, detail: 'add(elemento)', documentation: 'Adiciona um elemento à lista' },
                { label: 'get', kind: CompletionItemKind.Method, detail: 'get(indice)', documentation: 'Obtém um elemento pelo índice' },
                { label: 'remove', kind: CompletionItemKind.Method, detail: 'remove(elemento)', documentation: 'Remove um elemento da lista' },
                { label: 'length', kind: CompletionItemKind.Method, detail: 'length()', documentation: 'Retorna o tamanho da lista' }
            ];
        } else if (line.includes('dict') || line.match(/\{\s*\w+/)) {
            items = [
                { label: 'add', kind: CompletionItemKind.Method, detail: 'add(chave, valor)', documentation: 'Adiciona um par chave-valor' },
                { label: 'get', kind: CompletionItemKind.Method, detail: 'get(chave)', documentation: 'Obtém o valor associado à chave' },
                { label: 'remove', kind: CompletionItemKind.Method, detail: 'remove(chave)', documentation: 'Remove um par chave-valor' },
                { label: 'keys', kind: CompletionItemKind.Method, detail: 'keys()', documentation: 'Retorna as chaves do dicionário' }
            ];
        } else if (line.includes('string') || line.match(/["']/)) {
            items = [
                { label: 'length', kind: CompletionItemKind.Method, detail: 'length()', documentation: 'Retorna o tamanho da string' },
                { label: 'substring', kind: CompletionItemKind.Method, detail: 'substring(inicio, fim)', documentation: 'Retorna uma substring' },
                { label: 'toUpper', kind: CompletionItemKind.Method, detail: 'toUpper()', documentation: 'Converte para maiúsculas' },
                { label: 'toLower', kind: CompletionItemKind.Method, detail: 'toLower()', documentation: 'Converte para minúsculas' }
            ];
        }
    }
    
    return items;
});

// Implementar resolveCompletion para fornecer mais detalhes sob demanda
connection.onCompletionResolve((item) => {
    return item;
});

// Iniciar o servidor de linguagem
documents.listen(connection);
connection.listen(); 
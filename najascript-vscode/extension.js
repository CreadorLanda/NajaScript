// The module 'vscode' contains the VS Code extensibility API
const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

let statusBarItem;
let outputChannel;
let terminal;
let client;

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('NajaScript extension is now active!');

    // Register the command to run NajaScript
    const runCommand = vscode.commands.registerCommand('najascript.run', () => {
        runNajaScript(false);
    });

    // Register the command to run NajaScript in Portuguese
    const runPortugueseCommand = vscode.commands.registerCommand('najascript.runPortuguese', () => {
        runNajaScript(true);
    });

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'najascript.run';
    statusBarItem.text = "$(play) Executar NajaScript";
    statusBarItem.tooltip = "Executar arquivo NajaScript atual";
    
    // Show status bar item only when a .naja file is open
    context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor(updateStatusBarVisibility));
    updateStatusBarVisibility(vscode.window.activeTextEditor);

    // Initialize language server if autocomplete is enabled
    const config = vscode.workspace.getConfiguration('najascript');
    if (config.get('enableAutocomplete')) {
        initLanguageServer(context);
    }

    // Add all disposables to the context
    context.subscriptions.push(runCommand);
    context.subscriptions.push(runPortugueseCommand);
    context.subscriptions.push(statusBarItem);
}

function updateStatusBarVisibility(editor) {
    if (editor && editor.document.languageId === 'najascript') {
        statusBarItem.show();
    } else {
        statusBarItem.hide();
    }
}

/**
 * Initializes the language server for autocomplete
 * @param {vscode.ExtensionContext} context 
 */
function initLanguageServer(context) {
    // Path to the server module 
    const serverModule = context.asAbsolutePath(
        path.join('server', 'server.js')
    );

    // Create the server options
    const serverOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: {
            module: serverModule,
            transport: TransportKind.ipc,
            options: { execArgv: ['--nolazy', '--inspect=6009'] }
        }
    };

    // Client options define the documents handled by the server
    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'najascript' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.naja{modules,packages.json}')
        }
    };

    // Create and start the client
    client = new LanguageClient(
        'najascriptLanguageServer',
        'NajaScript Language Server',
        serverOptions,
        clientOptions
    );

    // Start the client, which will also start the server
    client.start();
}

/**
 * Executa o arquivo NajaScript atual
 * @param {boolean} inPortuguese - Se deve ser executado em modo português
 */
function runNajaScript(inPortuguese) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('Nenhum editor ativo encontrado.');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'najascript') {
        vscode.window.showErrorMessage('O arquivo atual não é um arquivo NajaScript.');
        return;
    }

    // Save the current file before running
    document.save().then(() => {
        const filePath = document.uri.fsPath;

        if (!fs.existsSync(filePath)) {
            vscode.window.showErrorMessage(`Arquivo não encontrado: ${filePath}`);
            return;
        }

        // Get configuration
        const config = vscode.workspace.getConfiguration('najascript');
        const useTerminal = config.get('useTerminal');
        
        // Build the command to run NajaScript
        // Usando python para garantir que o input funcione corretamente
        const pythonCmd = "python";
        const najascriptPath = "najascript.py"; // Caminho para o script Python do NajaScript
        
        const command = inPortuguese
            ? `${pythonCmd} ${najascriptPath} --pt "${filePath}"`
            : `${pythonCmd} ${najascriptPath} "${filePath}"`;
        
        // Comando alternativo (comando direto)
        const directCommand = inPortuguese
            ? `najascript --pt "${filePath}"`
            : `najascript "${filePath}"`;
        
        if (useTerminal) {
            // Create or show terminal
            if (!terminal || terminal.exitStatus !== undefined) {
                terminal = vscode.window.createTerminal('NajaScript');
            }
            
            terminal.show(true);
            
            // Tentar encontrar o executável do NajaScript no sistema
            // Se najascript.py não estiver no PATH, usar o comando direto
            terminal.sendText(`echo "Executando ${filePath}..."`);
            terminal.sendText(directCommand);
        } else {
            // Use output channel (original implementation)
            const outputChannel = getOutputChannel();
            outputChannel.clear();
            outputChannel.show(true);
    
            outputChannel.appendLine(`Executando: ${filePath}`);
            outputChannel.appendLine('----------------------------');
    
            // Execute the command
            exec(directCommand, { cwd: path.dirname(filePath) }, (error, stdout, stderr) => {
                if (stdout) {
                    outputChannel.appendLine(stdout);
                }
                
                if (stderr) {
                    outputChannel.appendLine(`ERRO: ${stderr}`);
                }
                
                if (error) {
                    outputChannel.appendLine(`Erro de execução: ${error.message}`);
                    vscode.window.showErrorMessage(`Erro ao executar NajaScript: ${error.message}`);
                } else {
                    outputChannel.appendLine('----------------------------');
                    outputChannel.appendLine('Execução concluída com sucesso!');
                }
            });
        }
    });
}

/**
 * Retorna o canal de saída para a extensão
 */
function getOutputChannel() {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('NajaScript');
    }
    return outputChannel;
}

// Função chamada quando a extensão é desativada
function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
    if (outputChannel) {
        outputChannel.dispose();
    }
    if (terminal) {
        terminal.dispose();
    }
    
    // Stop the language client
    if (client) {
        return client.stop();
    }
    
    return undefined;
}

module.exports = {
    activate,
    deactivate
}; 
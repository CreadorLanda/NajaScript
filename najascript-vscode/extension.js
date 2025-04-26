// The module 'vscode' contains the VS Code extensibility API
const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

let statusBarItem;
let outputChannel;

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

        const outputChannel = getOutputChannel();
        outputChannel.clear();
        outputChannel.show(true);

        outputChannel.appendLine(`Executando: ${filePath}`);
        outputChannel.appendLine('----------------------------');

        // Build the command to run NajaScript
        const command = inPortuguese
            ? `najascript --pt "${filePath}"`
            : `najascript "${filePath}"`;

        // Execute the command
        exec(command, { cwd: path.dirname(filePath) }, (error, stdout, stderr) => {
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
}

module.exports = {
    activate,
    deactivate
}; 
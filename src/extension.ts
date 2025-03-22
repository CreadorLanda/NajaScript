import * as vscode from 'vscode';
import * as path from 'path';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    console.log('Extensão NajaScript está ativa!');

    // Registrar comando para executar arquivo NajaScript
    let disposable = vscode.commands.registerCommand('najascript.executar', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            if (document.languageId === 'najascript') {
                const filePath = document.uri.fsPath;
                const terminal = vscode.window.createTerminal('NajaScript');
                terminal.sendText(`python najascript.py "${filePath}"`);
                terminal.show();
            } else {
                vscode.window.showErrorMessage('Este arquivo não é um arquivo NajaScript!');
            }
        }
    });

    context.subscriptions.push(disposable);

    // Registrar comando para criar novo arquivo NajaScript
    let newFileDisposable = vscode.commands.registerCommand('najascript.novoArquivo', () => {
        vscode.window.showInputBox({
            prompt: 'Digite o nome do arquivo',
            placeHolder: 'exemplo.naja'
        }).then(fileName => {
            if (fileName) {
                if (!fileName.endsWith('.naja')) {
                    fileName += '.naja';
                }
                const workspaceFolders = vscode.workspace.workspaceFolders;
                if (workspaceFolders) {
                    const filePath = path.join(workspaceFolders[0].uri.fsPath, fileName);
                    const content = '// Novo arquivo NajaScript\n\nfuncao principal() {\n    imprimir("Olá, Mundo!");\n}\n\nprincipal();';
                    vscode.workspace.fs.writeFile(vscode.Uri.file(filePath), Buffer.from(content));
                    vscode.window.showInformationMessage(`Arquivo ${fileName} criado com sucesso!`);
                }
            }
        });
    });

    context.subscriptions.push(newFileDisposable);
}

export function deactivate() {} 
[Setup]
AppId={{B8C9A1F2-8D5E-4A3B-9C7F-1E6D4B2A8F5C}}
AppName=NajaScript
AppVersion=1.2.0
AppVerName=NajaScript 1.2.0
AppPublisher=NajaScript Team
AppPublisherURL=https://najascript.vercel.app
AppSupportURL=https://github.com/NajaScript/Naja/issues
AppUpdatesURL=https://najascript.vercel.app
DefaultDirName={autopf}\NajaScript
DefaultGroupName=NajaScript
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoAfterFile=POST_INSTALL.txt
OutputDir=output
OutputBaseFilename=NajaScript_Setup_v1.2.0
SetupIconFile=najascript_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "addtopath"; Description: "Adicionar NajaScript ao PATH do sistema"; GroupDescription: "Opções do Sistema"

[Files]
; Arquivos principais
Source: "najascript.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "interpreter.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "lexer.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "parser_naja.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "ast_nodes.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "environment.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "fs_module.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "http_module.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja_github_package_manager.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja_bytecode.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "jit_compiler.py"; DestDir: "{app}"; Flags: ignoreversion

; Assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Módulos
Source: "modules\*"; DestDir: "{app}\modules"; Flags: ignoreversion recursesubdirs createallsubdirs

; Pacotes
Source: "packages\*"; DestDir: "{app}\packages"; Flags: ignoreversion recursesubdirs createallsubdirs

; Registry
Source: "registry\*"; DestDir: "{app}\registry"; Flags: ignoreversion recursesubdirs createallsubdirs

; Exemplos
Source: "exemplos\hello_world.naja"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "exemplos\calculator.naja"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "exemplos\teste_class.naja"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "exemplos\teste_najahack.naja"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "exemplos\flappy_bird_completo.naja"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "complete_math_test.naja"; DestDir: "{app}\examples"; Flags: ignoreversion

; Scripts de execução
Source: "najascript.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja_pkg.bat"; DestDir: "{app}"; Flags: ignoreversion

; Documentação
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "FUNCIONALIDADES_IMPLEMENTADAS.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\NajaScript"; Filename: "{app}\najascript.bat"; IconFilename: "{app}\assets\najascript_icon.ico"
Name: "{group}\NajaScript Package Manager"; Filename: "{app}\naja_pkg.bat"; IconFilename: "{app}\assets\najascript_icon.ico"
Name: "{group}\Exemplos"; Filename: "{app}\examples"
Name: "{group}\Documentação"; Filename: "{app}\README.md"
Name: "{group}\{cm:UninstallProgram,NajaScript}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NajaScript"; Filename: "{app}\najascript.bat"; IconFilename: "{app}\assets\najascript_icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\NajaScript"; Filename: "{app}\najascript.bat"; IconFilename: "{app}\assets\najascript_icon.ico"; Tasks: quicklaunchicon

[Registry]
; Associação de arquivos .naja
Root: HKCR; Subkey: ".naja"; ValueType: string; ValueName: ""; ValueData: "NajaScript.File"
Root: HKCR; Subkey: "NajaScript.File"; ValueType: string; ValueName: ""; ValueData: "NajaScript Source File"
Root: HKCR; Subkey: "NajaScript.File\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\najascript_icon.ico"
Root: HKCR; Subkey: "NajaScript.File\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\najascript.bat"" ""%1"""

; Adicionar ao PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath('{app}')

[Run]
Filename: "{app}\najascript.bat"; Parameters: "--version"; StatusMsg: "Verificando instalação..."; Flags: runhidden waituntilterminated
Filename: "{app}\README.md"; Description: "{cm:LaunchProgram,Ver documentação}"; Flags: postinstall nowait skipifsilent shellexec

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

[CustomMessages]
portuguese.CreateDesktopIcon=Criar ícone na área de trabalho
portuguese.CreateQuickLaunchIcon=Criar ícone na barra de acesso rápido
portuguese.LaunchProgram=Executar %1
portuguese.UninstallProgram=Desinstalar %1

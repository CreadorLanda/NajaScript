#define MyAppName "NajaScript"
#define MyAppVersion "0.1"
#define MyAppPublisher "NajaScript Team"
#define MyAppExeName "naja_repl.py"

[Setup]
AppId={{A1B2C3D4-E5F6-4747-8899-AABBCCDDEEFF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=Instalador
OutputBaseFilename=NajaScript_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "naja_repl.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "najascript.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "lexer.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "parser_naja.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "interpreter.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "ast_nodes.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja_bytecode.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "environment.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "modules\*"; DestDir: "{app}\modules"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "post_install.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\naja.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\naja.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{sys}\cmd.exe"; Parameters: "/c python -m venv ""{app}\venv"""; Description: "Criando ambiente virtual"; Flags: runhidden
Filename: "{app}\venv\Scripts\python.exe"; Parameters: """{app}\post_install.py"""; Description: "Configurando ambiente"; Flags: runhidden
Filename: "{app}\naja.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  PythonPath: String;
begin
  Result := True;
  
  // Verifica se o Python está instalado
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Python\PythonCore\3.13\InstallPath',
    '', PythonPath) then
  begin
    Result := True;
  end
  else
  begin
    MsgBox('Python 3.13 não está instalado. Por favor, instale o Python 3.13 antes de continuar.',
      mbError, MB_OK);
    Result := False;
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}" 
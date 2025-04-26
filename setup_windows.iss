#define MyAppName "NajaScript"
#define MyAppVersion "1.0"
#define MyAppPublisher "NajaScript Team"
#define MyAppURL "https://najascript.com"
#define MyAppExeName "najascript.exe"

[Setup]
AppId={{B2BBB89A-4F60-46E5-A7CE-3CF4AAB1D0FC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename=NajaScript_Setup
SetupIconFile=assets\najascript_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "addtopath"; Description: "Adicionar ao PATH do sistema"; GroupDescription: "Opções adicionais:"

[Files]
Source: "dist\najascript\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\najascript\naja_add.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\najascript\naja_remote.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\najascript\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "modules\*"; DestDir: "{app}\modules"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "naja_add.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "naja_remote.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README_naja_repo.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "README_Pacotes.md"
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\najascript_icon.ico"
Name: "{group}\Gerenciador de Pacotes"; Filename: "{app}\naja_add.exe"; Parameters: "--help"
Name: "{group}\Publicador de Módulos"; Filename: "{app}\naja_remote.exe"; Parameters: "--help"
Name: "{group}\Documentação de Pacotes"; Filename: "{app}\README_Pacotes.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\najascript_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\README_Pacotes.md"; Description: "Ver documentação do gerenciador de pacotes"; Flags: postinstall shellexec skipifsilent

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath('{app}')
Root: HKCR; Subkey: ".naja"; ValueType: string; ValueName: ""; ValueData: "NajaScriptFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "NajaScriptFile"; ValueType: string; ValueName: ""; ValueData: "Arquivo NajaScript"; Flags: uninsdeletekey
Root: HKCR; Subkey: "NajaScriptFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\assets\najascript_icon.ico,0"
Root: HKCR; Subkey: "NajaScriptFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKLM, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', OrigPath) then
  begin
    Result := True;
    exit;
  end;
  // verifica se o caminho já existe
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

// Adicionar um comando de finalizaçao para notificar o usuário sobre o gerenciador de pacotes
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('O NajaScript foi instalado com sucesso!' + #13#10 + #13#10 +
           'Você pode usar os seguintes comandos a partir de qualquer terminal:' + #13#10 + #13#10 +
           '  naja_add - Para instalar pacotes' + #13#10 +
           '  naja_remote - Para publicar seus módulos no repositório central' + #13#10 + #13#10 +
           'Para mais informações, consulte o arquivo README_Pacotes.md.', mbInformation, MB_OK);
  end;
end; 
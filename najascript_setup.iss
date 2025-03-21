#define MyAppName "NajaScript Editor"
#define MyAppVersion "1.0"
#define MyAppPublisher "NajaScript"
#define MyAppURL "https://github.com/seu-usuario/najascript"
#define MyAppExeName "NajaScriptEditor.exe"
#define MyInterpreterExeName "najascript.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{0BF56438-9F2D-4E8A-B3D2-0A84D754E328}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=.\Instalador
OutputBaseFilename=NajaScriptEditor_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
ChangesEnvironment=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "associatenaja"; Description: "Associar arquivos .naja ao interpretador"; GroupDescription: "Associações de arquivo"
Name: "addtopath"; Description: "Adicionar o interpretador ao PATH do sistema"; GroupDescription: "Opções avançadas"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\{#MyInterpreterExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "exemplo.naja"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\Interpretador NajaScript"; Filename: "{app}\{#MyInterpreterExeName}"; IconFilename: "{app}\icon.ico"; Parameters: "--help"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Registry]
Root: HKCR; Subkey: ".naja"; ValueType: string; ValueName: ""; ValueData: "NajaScriptFile"; Tasks: associatenaja; Flags: uninsdeletevalue
Root: HKCR; Subkey: "NajaScriptFile"; ValueType: string; ValueName: ""; ValueData: "Arquivo NajaScript"; Tasks: associatenaja; Flags: uninsdeletekey
Root: HKCR; Subkey: "NajaScriptFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icon.ico,0"; Tasks: associatenaja
Root: HKCR; Subkey: "NajaScriptFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyInterpreterExeName}"" ""%1"""; Tasks: associatenaja
Root: HKCR; Subkey: "NajaScriptFile\shell\edit"; ValueType: string; ValueName: ""; ValueData: "Editar com NajaScript Editor"; Tasks: associatenaja
Root: HKCR; Subkey: "NajaScriptFile\shell\edit\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: associatenaja

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  Path, NewPath: String;
  AppDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    if IsTaskSelected('addtopath') then
    begin
      AppDir := ExpandConstant('{app}');
      RegQueryStringValue(HKLM, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path);
      NewPath := Path;
      if Pos(AppDir, NewPath) = 0 then
      begin
        if Copy(NewPath, Length(NewPath), 1) <> ';' then
          NewPath := NewPath + ';';
        NewPath := NewPath + AppDir;
        RegWriteStringValue(HKLM, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', NewPath);
      end;
    end;
  end;
end; 
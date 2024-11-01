[Setup]
AppName=Muerta DOS
AppVersion=1.0
DefaultDirName={pf}\Muerta
DefaultGroupName=Muerta DOS
OutputDir=.\Output
OutputBaseFilename=MuertaInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\muerta.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Muerta DOS"; Filename: "{app}\muerta.exe"
Name: "{userdesktop}\Muerta DOS"; Filename: "{app}\muerta.exe"; Tasks: createappshortcut

[Tasks]
Name: createappshortcut; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительно"

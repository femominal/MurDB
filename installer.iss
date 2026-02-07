[Setup]
AppName=MurDB
AppVersion=1.0
DefaultDirName={pf}\MurDB
DefaultGroupName=MurDB
OutputDir=installer
OutputBaseFilename=MurDB_Setup
Compression=lzma
SolidCompression=yes
ChangesEnvironment=yes

[Files]
Source: "dist\murdb.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MurDB CLI"; Filename: "{app}\murdb.exe"
Name: "{commondesktop}\MurDB CLI"; Filename: "{app}\murdb.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: string; ValueName: "PATH"; \
ValueData: "{olddata};{app}"; Flags: preservestringtype
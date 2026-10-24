[Setup]
AppName=BiTTuRK Sunum Hazırlama Aracı
AppVersion=1.0
DefaultDirName={pf}\BiTTuRK_SunumAraci
DefaultGroupName=BiTTuRK Sunum Aracı
OutputBaseFilename=BiTTuRK_SunumAraci_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=no

[Files]
Source: "dist\BiTTuRK_SunumAraci\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\BiTTuRK Sunum Aracı"; Filename: "{app}\BiTTuRK_SunumAraci.exe"
Name: "{commondesktop}\BiTTuRK Sunum Aracı"; Filename: "{app}\BiTTuRK_SunumAraci.exe"

[Run]
Filename: "{app}\BiTTuRK_SunumAraci.exe"; Description: "Launch application"; Flags: nowait postinstall skipifsilent

[Setup]
AppName=BiTTuRK.NeT Sunum Hazırlama Aracı 5.0
AppPublisher=Mcilve
AppVersion=
DefaultDirName={pf}\BiTTuRK_SunumAraci
DefaultGroupName=BiTTuRK.NeT Sunum Hazırlama Aracı
OutputBaseFilename=BiTTuRK_SunumAraci_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=no
OutputDir=.
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\BiTTuRK_SunumAraci.exe

[Files]
Source: "dist\BiTTuRK_SunumAraci\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\BiTTuRK.NeT Sunum Hazırlama Aracı 5.0"; Filename: "{app}\BiTTuRK_SunumAraci.exe"; IconFilename: "{app}\BiTTuRK_SunumAraci.exe"
Name: "{commondesktop}\BiTTuRK.NeT Sunum Hazırlama Aracı 5.0"; Filename: "{app}\BiTTuRK_SunumAraci.exe"; IconFilename: "{app}\BiTTuRK_SunumAraci.exe"

[Run]
Filename: "{app}\BiTTuRK_SunumAraci.exe"; Description: "Launch application"; Flags: nowait postinstall skipifsilent

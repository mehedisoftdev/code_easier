[Setup]
AppName=Code Easier
AppVersion=1.0.1
DefaultDirName={pf}\CodeEasier
DefaultGroupName=Code Easier
OutputBaseFilename=code_easier_installer
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\icon.ico 

[Files]
Source: "dist\code_easier.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Code Easier"; Filename: "{app}\code_easier.exe"

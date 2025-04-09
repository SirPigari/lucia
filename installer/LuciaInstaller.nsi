Var Version

!include "MUI2.nsh"

Outfile "../installer/LuciaInstaller.exe"
InstallDir "$LOCALAPPDATA\Programs\LuciaAPL"
RequestExecutionLevel admin
Icon "../env/assets/installer2.ico"  ; Fixed icon path
SetOverwrite on


Function .onInit
    StrCpy $Version "1.1.2"  ; Set version dynamically
    InitPluginsDir
    File /oname=$PLUGINSDIR\\options.ini "options.ini"  ; Updated relative path for options.ini
FunctionEnd

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_ABORTWARNING
!define MUI_ICON "../env/assets/installer2.ico"
!define MUI_TITLE "Lucia - $Version"  ; Use the version in the installer title
Name "Lucia-$Version"  ; Use the version in the installer name

!define MUI_UNICON "../env/assets/installer3.ico"
!define MUI_UNTITLE "Lucia - $Version"  ; Use the version in the installer title

!define MUI_UNTEXT "LuciaAPL by SirPigari, v$Version"
!define MUI_TEXT "LuciaAPL by SirPigari, v$Version"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom InstallOptionsPage
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Install Lucia"
    IfFileExists "$INSTDIR\env\bin\lucia.exe" 0 +2
    Delete "$INSTDIR\env\bin\lucia.exe"


    SetOutPath "$INSTDIR"

    ; Exclude specific files and directories (relative paths)
    File /r /x .venv /x .git /x tests/test.lucia /x build /x dist /x *.spec \
         /x env/config.json /x AdditionalLibs /x .idea /x __pycache__ \
         /x env/Lib/Builtins/__pycache__ /x *.pyc /x tests \
         /x env/assets/fake_temp.zip /x env/assets/python_installer.exe \
         /x installer.py /x env/build /x env/bin/lucia_installer.exe \
         /x installer "C:\Users\sirpigari\Desktop\Projects\LuciaAPL\*.*"

    ; Run lucia.exe after installation if the user selected the "Run Lucia" option
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 3" "State"
        StrCmp $0 "1" 0 +2
        nsExec::ExecToStack "where wt"
        Pop $0

        StrCmp $0 "" 0 +2

        MessageBox MB_OK 'cmd.exe /C "$INSTDIR\env\bin\lucia.exe"'
        ExecWait 'cmd.exe /C "$INSTDIR\env\bin\lucia.exe"'
        Goto Done2

        MessageBox MB_OK 'wt ""$INSTDIR\env\bin\lucia.exe""'
        ExecWait 'wt ""$INSTDIR\env\bin\lucia.exe""'

        Done2:

    ; Add to PATH if checkbox is selected
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 1" "State"
        StrCmp $0 "1" 0 +3
        Push "$INSTDIR\env\bin"
        Call AddToPath

    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Function InstallOptionsPage
    InstallOptions::dialog "$PLUGINSDIR\\options.ini"
FunctionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR\\*.*"
    RMDir "$INSTDIR"

    ; Remove the PATH entry if it was added
    ReadRegStr $0 HKCU "Environment" "Path"
    StrCmp $0 "" done

    StrCpy $1 ""  ; Variable for new PATH
    StrCpy $2 $0  ; Copy of the PATH to process

    loop:
        ; Find the next semicolon separator
        StrCpy $3 $2 1
        StrCmp $3 ";" foundSeparator
        StrCmp $2 "" done
        StrCpy $1 "$1$3"  ; Append character to new PATH
        StrCpy $2 $2 "" 1  ; Remove first character
        Goto loop

    foundSeparator:
        ; Extract the first entry
        StrCpy $4 $1
        StrCpy $1 ""  ; Reset new PATH

        ; Compare with our install directory
        StrCmp $4 "$INSTDIR\\env\\bin" skip
        StrCmp $4 "" skip
        StrCpy $1 "$1;$4"  ; Add back to the new PATH

    skip:
        StrCpy $2 $2 "" 1  ; Remove the processed part
        StrCmp $2 "" done
        Goto loop

    done:
        WriteRegStr HKCU "Environment" "Path" $1  ; Write the new PATH value

    ; Remove the uninstaller itself
    Delete "$INSTDIR\\uninstall.exe"
SectionEnd

Function AddToPath
    Exch $0              ; $0 = path to add
    ReadRegStr $1 HKCU "Environment" "Path"

    ; Check if it's already in PATH
    Push $0              ; Save $0 for later use
    Push $1              ; Save original PATH
    Push $2
    Push $3
    Push $4
    Push $5

    StrCpy $2 $1         ; Copy of PATH to search through

CheckLoop:
    StrCpy $3 $2 1
    StrCmp $2 "" DoneChecking
    StrCmp $3 ";" NextChar
    StrCpy $4 ""         ; Reset $4 to hold a segment

    ; Extract the next path segment
    GetNextSegment:
        StrCpy $3 $2 1
        StrCmp $3 ";" FoundSegment
        StrCmp $2 "" FoundSegment
        StrCpy $4 "$4$3"
        StrCpy $2 $2 "" 1
        Goto GetNextSegment

FoundSegment:
    ; Compare segment to $0
    StrCmp $4 $0 AlreadyExists
    StrCpy $2 $2 "" 1  ; Skip the semicolon
    Goto CheckLoop

NextChar:
    ; Move to the next segment in PATH
    StrCpy $2 $2 "" 1
    Goto CheckLoop

AlreadyExists:
    Pop $5
    Pop $4
    Pop $3
    Pop $2
    Pop $1
    Pop $0
    Goto End

DoneChecking:
    Pop $5
    Pop $4
    Pop $3
    Pop $2
    Pop $1
    Pop $0

    ; Add the path because it doesn't exist
    ReadRegStr $1 HKCU "Environment" "Path"
    StrCmp $1 "" 0 +2
    WriteRegStr HKCU "Environment" "Path" "$0"
    StrCmp $1 "" End
    WriteRegStr HKCU "Environment" "Path" "$1;$0"

End:
    Pop $0
FunctionEnd

Function .onInstSuccess
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 3" "State"
    StrCmp $0 "1" 0 +2

    nsExec::ExecToStack "where wt"
    Pop $0

    StrCmp $0 "" 0 RunWithCMD

    MessageBox MB_OK 'wt "$INSTDIR\env\bin\lucia.exe"'
    ExecShell "" "wt" '""$INSTDIR\env\bin\lucia.exe""'
    Goto EndLaunch

RunWithCMD:
    MessageBox MB_OK 'cmd.exe /c "$INSTDIR\env\bin\lucia.exe"'
    ExecShell "" "cmd.exe" '/C "$INSTDIR\env\bin\lucia.exe"'

EndLaunch:
FunctionEnd

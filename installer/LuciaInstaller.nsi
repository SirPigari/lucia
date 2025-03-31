Var Version

!include "MUI2.nsh"

Outfile "../installer/LuciaInstaller.exe"
InstallDir "$LOCALAPPDATA\\Programs\\LuciaAPL"
RequestExecutionLevel admin
Icon "../env/assets/installer2.ico"  ; Fixed icon path

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

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
Page custom InstallOptionsPage
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Install Lucia"
    SetOutPath "$INSTDIR"

    ; Exclude specific files and directories (relative paths)
    File /r /x .venv /x .git /x tests/test.lucia /x build /x dist /x *.spec \
         /x env/config.json /x AdditionalLibs /x .idea /x __pycache__ \
         /x env/Lib/Builtins/__pycache__ /x *.pyc /x tests \
         /x env/assets/fake_temp.zip /x env/assets/python_installer.exe \
         /x installer.py /x env/build /x env/bin/lucia_installer.exe \
         /x installer "E:\\LuciaAPL\\*.*"

    ; Run lucia.exe with --activate if the user selected the "Activate" option
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 2" "State"
    StrCmp $0 "1" 0 +2
    Exec '\"$INSTDIR\\env\\bin\\lucia.exe" --activate'

    ; Run lucia.exe after installation if the user selected the "Run Lucia" option
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 3" "State"
    StrCmp $0 "1" 0 +2
    Exec '\"$INSTDIR\\env\\bin\\lucia.exe"'
    Exec '\"$INSTDIR\\env\\bin\\lucia.exe"'

    ; Add to PATH if checkbox is selected
    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 1" "State"
    StrCmp $0 "1" 0 +2
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
    Exch $0
    ReadRegStr $1 HKCU "Environment" "Path"
    StrCmp $1 "" 0 +2
    WriteRegStr HKCU "Environment" "Path" "$0"
    StrCmp $1 "" exit
    WriteRegStr HKCU "Environment" "Path" "$1;$0"
exit:
    Pop $0
FunctionEnd

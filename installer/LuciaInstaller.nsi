Var Version

!include "MUI2.nsh"

Outfile "../installer/LuciaInstaller.exe"
InstallDir "$LOCALAPPDATA\Programs\LuciaAPL"
RequestExecutionLevel admin
Icon "../env/assets/installer2.ico"
SetOverwrite on


Function .onInit
    StrCpy $Version "1.3.1"
    InitPluginsDir
    File /oname=$PLUGINSDIR\\options.ini "options.ini"
FunctionEnd

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_ABORTWARNING
!define MUI_ICON "../env/assets/installer2.ico"
!define MUI_TITLE "Lucia - $Version"
!define MUI_BANNERIMAGE_BITMAP "../env/assets/lucia_logo_banner_fill.bmp"
!define MUI_BANNERIMAGE "..\env\assets\lucia_logo_banner_fill.bmp"
!define MUI_BANNER_TRANSPARENT_TEXT
Name "Lucia-$Version"

!define MUI_UNICON "../env/assets/installer3.ico"
!define MUI_UNTITLE "Lucia - $Version"

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

    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 5" "State"
        StrCmp $0 "1" 0 +2
        Pop $0

        RMDir /r "$INSTDIR\"

        Delete $2

    SetOutPath "$INSTDIR"

    File /r /x .venv /x .git /x tests/test.lucia /x build /x dist /x *.spec \
         /x env/config.json /x AdditionalLibs /x .idea /x __pycache__ \
         /x env/Lib/Builtins/__pycache__ /x *.pyc /x tests \
         /x env/assets/fake_temp.zip /x env/assets/python_installer.exe \
         /x installer.py /x env/build /x env/bin/lucia_installer.exe \
         /x installer "C:\Users\sirpigari\Desktop\Projects\LuciaAPL\*.*"

    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 6" "State"
        StrCmp $0 "1" 0 CopyConfig
        Goto AfterConfig

    CopyConfig:
        SetOutPath "$INSTDIR\env"
        File "C:\Users\sirpigari\Desktop\Projects\LuciaAPL\env\config.json"

    AfterConfig:


    IfErrors 0 +3
    MessageBox MB_OK|MB_ICONSTOP "Error: Failed to copy files."
    Abort


    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 2" "State"
        StrCmp $0 "1" 0 +2
        Pop $0

        ExecWait 'cmd.exe /C ""$INSTDIR\env\bin\lucia.exe" --no-color --activate"'

    ReadINIStr $0 "$PLUGINSDIR\\options.ini" "Field 4" "State"
        StrCmp $0 "1" 0 +2
        Pop $0

        ExecWait 'cmd.exe /C ""$INSTDIR\env\bin\lucia.exe" --no-color --timer $INSTDIR\env\Docs\examples\testAll.lc"'

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

    ReadRegStr $0 HKCU "Environment" "Path"
    StrCmp $0 "" done

    StrCpy $1 ""
    StrCpy $2 $0

    loop:
        StrCpy $3 $2 1
        StrCmp $3 ";" foundSeparator
        StrCmp $2 "" done
        StrCpy $1 "$1$3"
        StrCpy $2 $2 "" 1
        Goto loop

    foundSeparator:
        StrCpy $4 $1
        StrCpy $1 ""

        StrCmp $4 "$INSTDIR\\env\\bin" skip
        StrCmp $4 "" skip
        StrCpy $1 "$1;$4"

    skip:
        StrCpy $2 $2 "" 1
        StrCmp $2 "" done
        Goto loop

    done:
        WriteRegStr HKCU "Environment" "Path" $1

    Delete "$INSTDIR\\uninstall.exe"
SectionEnd

Function AddToPath
    Exch $0
    ReadRegStr $1 HKCU "Environment" "Path"

    Push $0
    Push $1
    Push $2
    Push $3
    Push $4
    Push $5

    StrCpy $2 $1

CheckLoop:
    StrCpy $3 $2 1
    StrCmp $2 "" DoneChecking
    StrCmp $3 ";" NextChar
    StrCpy $4 ""

    GetNextSegment:
        StrCpy $3 $2 1
        StrCmp $3 ";" FoundSegment
        StrCmp $2 "" FoundSegment
        StrCpy $4 "$4$3"
        StrCpy $2 $2 "" 1
        Goto GetNextSegment

FoundSegment:
    StrCmp $4 $0 AlreadyExists
    StrCpy $2 $2 "" 1
    Goto CheckLoop

NextChar:
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
    Pop $0
    StrCmp $0 "" 0 RunWithCMD
    Goto EndLaunch

RunWithCMD:
    ExecShell "" "cmd.exe" '/C ""$INSTDIR\env\bin\lucia.exe" --no-color"'

EndLaunch:
FunctionEnd
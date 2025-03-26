!include "MUI2.nsh"         ; Modern UI
!include "LogicLib.nsh"     ; For if-else logic
!include "inetc.nsh"        ; Include the inetc plugin (make sure it's in your NSIS plugins folder)
!include "nsisunz.nsh"      ; Include nsisunz for unzipping

Name "Lucia Installer"
Outfile "LuciaInstaller.exe"
InstallDir $PROGRAMFILES\LuciaAPL

Var AddToPath               ; Variable to store if checkbox is selected
Var GitHubRepoURL           ; The URL for downloading the zip from GitHub
Var Version                 ; The version string, default to "1.1"
Var TempZipFile             ; The temporary zip file

Function AddToPath
    # Adding path to the system environment variables
    WriteRegExpandStr HKCU "Environment" "Path" "$0"
    MessageBox MB_OK "Successfully added to PATH!"
FunctionEnd

Function DownloadFromGitHub
    Exch $0   ; GitHub URL passed in $0
    Push $1   ; Temporary file path for the downloaded zip

    StrCpy $1 $INSTDIR\temp.zip
    ; Download the zip from GitHub using the inetc plugin
    inetc::get /TIMEOUT=600 /OUTPUT=$1 $0

    Pop $1
    Exch $0   ; Restore URL
FunctionEnd

Function SetGitHubURL
    ; Set the GitHub URL using the version
    StrCpy $GitHubRepoURL "https://github.com/SirPigari/lucia/archive/refs/tags/Release${Version}.zip"
FunctionEnd

Function ExtractLuciaMain
    ; Extract only the lucia-main folder from the downloaded zip to the parent directory
    DetailPrint "Extracting lucia-main from zip..."
    nsisunz::UnzipToLog $INSTDIR\temp.zip $INSTDIR\lucia-main\*

    ; Move all extracted files from "lucia-main" to the parent folder (INSTALLDIR)
    DetailPrint "Moving lucia-main files to INSTALLDIR..."
    Rename $INSTDIR\lucia-main\* $INSTDIR\*

    ; Remove the temporary lucia-main folder after moving files
    RMDir /r $INSTDIR\lucia-main
FunctionEnd

Section "Install Lucia"
    ; Step 1: Set the GitHub URL with the correct version
    StrCpy $Version "1.1"  ; Set the desired version here
    Call SetGitHubURL

    ; Step 2: Download the zip file from GitHub
    Call DownloadFromGitHub $GitHubRepoURL

    ; Step 3: Extract the `lucia-main` directory and move its contents
    Call ExtractLuciaMain

    ; Step 4: Delete the temporary zip file
    Delete $INSTDIR\temp.zip

    ; Step 5: Add to PATH if checkbox is selected
    ${If} $AddToPath == 1
        Push "$INSTDIR\env\bin"
        Call AddToPath
    ${EndIf}

    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir /r $INSTDIR
SectionEnd

Page directory
Page instfiles

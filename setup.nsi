; Accept external parameters
!define Build_VERSION_MAJOR "${I_VERSION_MAJOR}"
!define Build_VERSION_MINOR "${I_VERSION_MINOR}"
!define Build_APP_NAME "${I_APP_NAME}"
!define Build_AUTHOR "${I_AUTHOR}"
!define Build_ICON "${I_ICON}"
!define Build_ICON_NAME "${I_ICON_NAME}"
!define Build_LICENSE "${I_LICENSE}"

; Installer.nsi
; Use Modern UI 2
!include "MUI2.nsh"

; Define the name of the installer
Name "${Build_APP_NAME}Installer"

; Define the output file for the installer
OutFile ".\build\${Build_APP_NAME}Installer.exe"

; Use unicode
; Unicode true

; Use best compressor
; SetCompressor /FINAL /SOLID lzma
; SetCompressorDictSize 64
; SetDatablockOptimize ON

; Set the icon for the installer
Icon "${Build_ICON}"

; Request execution level for 64-bit installation
RequestExecutionLevel admin

; Define the default installation directory
InstallDir "$PROGRAMFILES64\${Build_APP_NAME}"
; InstallDir "$APPDATA\${Build_APP_NAME}"

; Define the directory from where to install files
InstallDirRegKey HKCU "Software\${Build_APP_NAME}" "InstallPath"

; Specify the license file to show
LicenseData "${Build_LICENSE}"

; Modern UI settings
!define MUI_ABORTWARNING
!define MUI_ICON "${Build_ICON}"
!define MUI_UNICON "${Build_ICON}"

; Install Pages
!insertmacro MUI_PAGE_WELCOME

!if "${Build_LICENSE}" != ""
  !insertmacro MUI_PAGE_LICENSE "${Build_LICENSE}"
!endif

!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstall Pages
; !insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "SimpChinese"

; Reserve files (use nsDialogs as recommended)
ReserveFile /plugin nsDialogs.dll

; Define the section for installing the application
Section "${Build_APP_NAME} (required)" InstallExeutable
  SectionIn RO

  ; Set the output path to the installation directory
  SetOutPath $INSTDIR

  ; Recursively copy all files and folders from the source directory to the installation directory
  File /r ".\build\out\*"

  ; Create a shortcut for the main executable on the desktop
  CreateShortcut "$DESKTOP\${Build_APP_NAME}.lnk" "$INSTDIR\${Build_APP_NAME}.exe" "" "$INSTDIR\${Build_ICON_NAME}"

  ; Write the installation path into the registry
  WriteRegStr HKCU "Software\${Build_APP_NAME}" "InstallPath" "$INSTDIR"

  ; Write the uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Create the application data directory and set the environment variable
  StrCpy $0 "%APPDATA%\${Build_APP_NAME}\${Build_APP_NAME}_${Build_VERSION_MAJOR}_${Build_VERSION_MINOR}"
  CreateDirectory "$0"

  ; EnVar::AddValue "${Build_APP_NAME}Data" "$0"
  ; EnVar::Delete "${Build_APP_NAME}Data"
  ; EnVar::AddValue "${Build_APP_NAME}Data" "$0"
  ; DetailPrint "Added ${Build_APP_NAME}Data to the environment variables"

  ; User
  ; WriteRegExpandStr HKCU "Environment" "${Build_APP_NAME}Data" "$0"

  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "${Build_APP_NAME}Data" "$0"

  ; Add to "Add or Remove Programs" in Control Panel
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "DisplayName" "${Build_APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "DisplayIcon" "$INSTDIR\${Build_APP_NAME}.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "Publisher" "${Build_AUTHOR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "DisplayVersion" "${Build_VERSION_MAJOR}.${Build_VERSION_MINOR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "VersionMajor" "${Build_VERSION_MAJOR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "VersionMinor" "${Build_VERSION_MINOR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "NoModify" "1"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}" "NoRepair" "1"

  ; Show a ok message box
  MessageBox MB_OK|MB_ICONINFORMATION "${Build_APP_NAME} has been successfully installed."

SectionEnd

; Define the section for Enable LongPath
Section "Enable LongPath" EnableLongPath
  WriteRegDWORD HKLM "SYSTEM\CurrentControlSet\Control\FileSystem" "LongPathsEnabled" 1
SectionEnd

; Define the language strings
LangString DESC_InstallExeutable ${LANG_SimpChinese} "安装${Build_APP_NAME}到您的计算机。"
LangString DESC_EnableLongPath ${LANG_SimpChinese} "启用长路径。"

; Assign language strings to sections
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${InstallExeutable} $(DESC_InstallExeutable)
!insertmacro MUI_DESCRIPTION_TEXT ${EnableLongPath}   $(DESC_EnableLongPath)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Define the section for uninstalling the application
Section "Uninstall"

  ; Remove the files and shortcuts
  Delete "$INSTDIR\${Build_APP_NAME}.exe"
  Delete "$DESKTOP\${Build_APP_NAME}.lnk"

  ; Remove all files in the installation directory
  Delete "$INSTDIR\*.*"
  RmDir /r "$INSTDIR"

  ; Remove the uninstaller
  Delete "$INSTDIR\Uninstall.exe"

  ; Remov environment variables
  DeleteRegValue HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "${Build_APP_NAME}Data"

  ; Remove the installation path from the registry
  DeleteRegKey HKCU "Software\${Build_APP_NAME}"

  ; Remove from "Add or Remove Programs" in Control Panel
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${Build_APP_NAME}"

  ; Show a ok message box
  MessageBox MB_OK|MB_ICONINFORMATION "${Build_APP_NAME} has been successfully uninstalled."

SectionEnd

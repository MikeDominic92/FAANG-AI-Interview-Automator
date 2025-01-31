$SourceExe = "C:\Users\sleep\CascadeProjects\interview-ai\dist\Interview AI Assistant.exe"
$DesktopPath = [System.Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Interview AI Assistant.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $SourceExe
$Shortcut.WorkingDirectory = "C:\Users\sleep\CascadeProjects\interview-ai\dist"
$Shortcut.Save()

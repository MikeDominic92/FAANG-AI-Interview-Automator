$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Interview AI Assistant.lnk")
$Shortcut.TargetPath = "C:\Users\sleep\CascadeProjects\interview-ai\start_interview_assistant.bat"
$Shortcut.WorkingDirectory = "C:\Users\sleep\CascadeProjects\interview-ai"
$Shortcut.IconLocation = "C:\Windows\System32\SHELL32.dll,76"
$Shortcut.Save()

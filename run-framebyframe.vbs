
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

strFolder = objFSO.GetParentFolderName(WScript.ScriptFullName)
strPython = strFolder & "\fbfenv\Scripts\pythonw.exe"
strScript = strFolder & "\src\FrameByFrame.py"
strFfmpeg = strFolder & "\ffmpeg\bin"

If Not objFSO.FileExists(strPython) Then
    MsgBox "FrameByFrame is not installed. Run install.bat first.", vbExclamation, "FrameByFrame"
    WScript.Quit 1
End If

If Not objFSO.FileExists(strScript) Then
    MsgBox "FrameByFrame.py could not be found.", vbExclamation, "FrameByFrame"
    WScript.Quit 1
End If

If Not objFSO.FileExists(strFfmpeg & "\ffmpeg.exe") Then
    MsgBox "FFmpeg is missing. Run install-windows.bat again.", vbExclamation, "FrameByFrame"
    WScript.Quit 1
End If

' Add the bundled FFmpeg directory to this application's PATH only.
Set objEnv = objShell.Environment("Process")
objEnv("PATH") = strFfmpeg & ";" & objEnv("PATH")

objShell.CurrentDirectory = strFolder
objShell.Run """" & strPython & """ """ & strScript & """", 0, False

' This script runs the batch file "run_bgr_file_sorter.bat" silently without showing the command prompt window.
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c run_bgr_file_sorter.bat", 0, False


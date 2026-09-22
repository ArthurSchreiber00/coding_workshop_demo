@echo off
REM Startet quickstart.ps1 ohne Aenderung der PowerShell Execution Policy.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0quickstart.ps1" %*

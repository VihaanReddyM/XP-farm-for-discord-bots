@echo off

REM Terminate the program with window title "My Bot"
taskkill /F /FI "WINDOWTITLE eq Main token*"
echo Program has been terminated.

REM Terminate extra.py
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Extra token*"
echo extra.py has been terminated.

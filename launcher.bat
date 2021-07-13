@echo off

reg query "hkcu\software\Python"
if ERRORLEVEL 1 GOTO NOPYTHON	

GOTO :continue

:NOPYTHON (
	reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
	if %OS%==32BIT START /WAIT Installers/python-3.8.5.exe
	if %OS%==64BIT START /Wait Installers/python-3.8.5-amd64.exe
	GOTO :continue)

:continue
REM call venv\Scripts\activate.bat
REM call DuckHuntAIEdition.py
py -m pip install --upgrade pip
py -m pip install numpy
py -m pip install pywin32-ctypes
py -m pip install pygame
py -m pip install pygame_gui
py -m pip install scipy
py DuckHuntAIEdition.py


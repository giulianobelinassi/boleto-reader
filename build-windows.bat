@echo off

rmdir /S /Q dist
pyinstaller --onefile --noconsole boleto-reader.py
xcopy win32 dist\win32 /E /H /C /I /Y

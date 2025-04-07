@echo off
cd /d "%~dp0"
powershell -Command "Start-Process python 'registration-helper-gui.py' -Verb RunAs"

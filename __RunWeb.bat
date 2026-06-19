@echo off
%~d0
cd %~dp0

python main.py
rem --verbose
if %ERRORLEVEL% neq 0 pause
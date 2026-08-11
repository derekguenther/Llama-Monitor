@echo off
%~d0
cd %~dp0

python llamamonitor.py --port 8081
rem --verbose
if %ERRORLEVEL% neq 0 pause
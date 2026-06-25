@echo off
%~d0
cd %~dp0

python llamamonitor.py
rem --verbose
if %ERRORLEVEL% neq 0 pause
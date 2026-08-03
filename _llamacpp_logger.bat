@echo off

%~d0
cd %~dp0

python _llamacpp_logger.py
if "%ERRORLEVEL%" GTR "0" PAUSE
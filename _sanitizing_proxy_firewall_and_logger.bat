@echo off

%~d0
cd %~dp0

python _sanitizing_proxy_firewall_and_logger.py
if "%ERRORLEVEL%" GTR "0" PAUSE
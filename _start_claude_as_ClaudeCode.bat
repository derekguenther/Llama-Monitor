@echo off

%~d0
cd %~dp0

runas /user:ClaudeCode /savecred "%~dp0_start_claude_as_ClaudeCode2.bat"
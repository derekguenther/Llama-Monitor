@echo off

:: Disable the hidden header that trashes the cache
set CLAUDE_CODE_ATTRIBUTION_HEADER=0

:: 1. Point to your local llama-server
set ANTHROPIC_BASE_URL=http://localhost:8000
set ANTHROPIC_API_KEY=12345
rem set ANTHROPIC_AUTH_TOKEN=local
set ANTHROPIC_MODEL=qwen3-coder-next
set ANTHROPIC_SMALL_FAST_MODEL=qwen3-coder-next
set CLAUDE_SONNET=qwen3-coder-next
set CLAUDE_OPUS=qwen3-coder-next
set CLAUDE_HAIKU=qwen3-coder-next
set EPISODIC_MEMORY_API_MODEL=qwen3-coder-next
set EPISODIC_MEMORY_API_MODEL_FALLBACK=qwen3-coder-next
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set CLAUDE_CODE_USE_POWERSHELL_TOOL=0
set CLAUDE_CODE_MAX_CONTEXT_TOKENS=131072
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=131072
set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=85
set CLAUDE_CODE_BYPASS_ALL_PERMISSIONS=1
set IS_SANDBOX=1
set CLAUDE_CODE_SUPPRESS_UI_PROMPTS=1
set ANTHROPIC_DISABLE_SAFETY_CHECKS=1

rem for Gemma 4 12B
rem set CLAUDE_CODE_MAX_CONTEXT_TOKENS=50000
rem set CLAUDE_CODE_AUTO_COMPACT_WINDOW=50000
rem set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80


set CLAUDE_CODE_MAX_CONTEXT_TOKENS=131072
set CLAUDE_CODE_AUTO_COMPACT_WINDOW=131072
set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=85

rem set CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1


set "PATH=C:\Users\ClaudeCode\.local\bin;C:\Users\ClaudeCode\AppData\Local\Programs\Python\Python312;C:\Users\ClaudeCode\AppData\Local\Programs\Python\Python312\Scripts;C:\Users\ClaudeCode\AppData\Local\Programs\node-v24.15.0\node-v24.15.0-win-x64;C:\Users\ClaudeCode\AppData\Local\Programs\node-v24.15.0\node-v24.15.0-win-x64\node_modules\.bin;C:\Users\ClaudeCode\AppData\Local\Programs\node-v24.15.0\node-v24.15.0-win-x64\node_modules\@beads\bd\bin;C:\Program Files\GitHub CLI;C:\Program Files\Git\mingw64\bin\;C:\Program Files\Godot;C:\Program Files\dotnet;C:\Windows\System32;C:\Windows;C:\Users\ClaudeCode\AppData\Local\Microsoft\WindowsApps;C:\Program Files\Ollama"


%~d0
cd %~dp0

:: 2. Launch Claude Code
claude --update

:claudelaunch
set /p continue=Would you like to continue from your last session? y/n (default y): 
cls
if "%continue%" equ "y" goto :claudecontinue
if "%continue%" equ "" goto :claudecontinue
if "%continue%" equ "n" goto :claudenocontinue
goto :claudelaunch

:claudecontinue
claude --continue --permission-mode acceptEdits
if %ERRORLEVEL% NEQ 0 pause
goto :EOF

:claudenocontinue
claude --permission-mode acceptEdits
if %ERRORLEVEL% NEQ 0 pause
goto :EOF


rem This is the original command to include a baseline prompt.
rem claude --system-prompt "You are a professional Godot 4 developer. We are working on a C# project. Follow the project guidelines in CLAUDE.md. Be concise and prioritize working code."

rem Since your log showed you were very close to your VRAM limit (only 1,363 MiB free), if you notice any crashes, you can add --fit-target 512M. This tells the server to leave exactly 512MB of "breathing room" for the actual math calculations so it doesn't choke.
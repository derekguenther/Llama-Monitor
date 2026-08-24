@echo off

:: Anthropic API Emulation / Claude Code Environment
set ANTHROPIC_BASE_URL=http://127.0.0.1:8000
set ANTHROPIC_AUTH_TOKEN=
set ANTHROPIC_API_KEY=12345
set ANTHROPIC_MODEL=qwen3-coder-next
set ANTHROPIC_SMALL_FAST_MODEL=qwen3-coder-next
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set API_TIMEOUT_MS=600000

:: Conda Environment Setup
call conda activate llama.cpp

:: Executable & Model Paths
set SERVER_BIN=C:\Users\ClaudeCode\Documents\windows_llama.cpp\vendor\llama.cpp\build\bin\llama-server.exe
set MODEL_PATH=D:\AI\LLMs\General Use\DeepSeek v4\DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf
set SLOT_PATH=D:\AI\LLMs\General Use\DeepSeek v4\llama.cpp save slots
set JINJATEMPLATE_PATH=D:\AI\LLMs\General Use\DeepSeek v4\chat_template.jinja

REM Get date and time in a safe format (YYYYMMDD_HHMMSS)
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set mm=%%a
    set dd=%%b
    set yyyy=%%c
)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set hh=%%a
    set nn=%%b
    set ss=%%c
)
set logfilename=llama-server_%yyyy%%mm%%dd%_%hh%%nn%%ss%.log

:: Launch Mainline llama-server
start /affinity FFFF /b /wait "" "%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --chat-template-file "%JINJATEMPLATE_PATH%" ^
    --alias qwen3-coder-next ^
    --host 0.0.0.0 ^
    --port 8001 ^
    --jinja ^
    --reasoning on ^
    --reasoning-format deepseek ^
    --metrics ^
    --ctx-size 262144 ^
    --parallel 5 ^
    --cache-prompt ^
    --cache-reuse 256 ^
    --kv-unified ^
    --cache-type-k q8_0 ^
    --cache-type-v q8_0 ^
    --cont-batching ^
    --flash-attn on ^
    --load-mode none ^
    --n-gpu-layers all ^
    --n-cpu-moe 43 ^
    --temp 1.0 ^
    --top-p 1.0 ^
    --min-p 0.05 ^
    --top-k 0 ^
    --repeat-penalty 1.0 ^
    --threads 8 ^
    --threads-batch 16 ^
    --batch-size 4096 ^
    --ubatch-size 1024 ^
    --log-file %logfilename%^
    --log-prefix ^
    --log-timestamps ^
    -lv 5

if %ERRORLEVEL% NEQ 0 pause

rem    --load-mode mlock ^
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
set SERVER_BIN=C:\Users\ClaudeCode\Documents\windows_llama.cpp - special build for inkling-small\vendor\llama.cpp\build\bin\Release\llama-server.exe
set MODEL_PATH=D:\AI\LLMs\General Use\Inkling-Small\Inkling-Small-UD-IQ3_XXS-00001-of-00003.gguf
set MMPROJ_PATH=D:\AI\LLMs\General Use\Inkling-Small\mmproj-F16.gguf
rem set SLOT_PATH=D:\AI\LLMs\General Use\Inkling-Small\llama.cpp save slots
rem set JINJATEMPLATE_PATH=D:\AI\LLMs\General Use\Inkling-Small\chat_template.jinja

:: Launch Mainline llama-server
start /affinity FFFF /b /wait "" "%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --mmproj "%MMPROJ_PATH%" ^
    --no-mmproj-offload ^
    --alias qwen3-coder-next ^
    --host 0.0.0.0 ^
    --port 8000 ^
    --jinja ^
    --reasoning on ^
    --reasoning-preserve ^
    --metrics ^
    --ctx-size 196608 ^
    --parallel 1 ^
    --cont-batching ^
    --flash-attn on ^
    --load-mode none ^
    --n-gpu-layers all ^
    --n-cpu-moe 41 ^
    --temp 0.7 ^
    --top-p 0.9 ^
    --min-p 0.05 ^
    --top-k 40 ^
    --repeat-penalty 1.0 ^
    --threads 8 ^
    --threads-batch 16 ^
    --batch-size 2048 ^
    --ubatch-size 256

if %ERRORLEVEL% NEQ 0 pause

rem    --load-mode mlock ^
rem    --n-gpu-layers all ^
rem    --n-cpu-moe 999 ^
rem    --mmproj "%MMPROJ_PATH%" ^
rem    --no-mmproj-offload ^
rem    --cache-type-k q8_0 ^
rem    --cache-type-v q8_0 ^
rem ctx-size 131072
rem ctx-size 196608
rem ctx-size 262144
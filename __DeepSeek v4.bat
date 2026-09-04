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

:: Launch Mainline llama-server
rem start /affinity FFFF /b /wait "" 
"%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --chat-template-file "%JINJATEMPLATE_PATH%" ^
    --alias qwen3-coder-next ^
    --host 0.0.0.0 ^
    --port 8000 ^
    --jinja ^
    --reasoning on ^
    --reasoning-format deepseek ^
    --metrics ^
    --ctx-size 185000 ^
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
    --n-cpu-moe 42 ^
    --temp 1.0 ^
    --top-p 1.0 ^
    --min-p 0.05 ^
    --top-k 0 ^
    --repeat-penalty 1.0 ^
    --threads 24 ^
    --threads-batch 16 ^
    --batch-size 4096 ^
    --ubatch-size 2048 ^
    --cache-ram 0

if %ERRORLEVEL% NEQ 0 pause

rem    --load-mode mlock ^
rem    --cache-ram 0
rem 131072 262144
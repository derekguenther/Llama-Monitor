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
set MODEL_PATH=D:\AI\LLMs\General Use\Qwen3.8-Flash-Next\Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf
set MMPROJ_PATH=D:\AI\LLMs\General Use\Qwen3.8-Flash-Next\mmproj-F16.gguf
rem set JINJATEMPLATE_PATH=D:\AI\LLMs\General Use\Qwen3.8-Flash-Next\chat_template.jinja

:: Launch Mainline llama-server
start /affinity FFFF /b /wait "" "%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --mmproj "%MMPROJ_PATH%" ^
    --no-mmproj-offload ^
    --alias qwen3.8-flash-next ^
    --host 0.0.0.0 ^
    --port 8000 ^
    --jinja ^
    --ctx-size 131072 ^
    --parallel 2 ^
    --cache-type-k q8_0 ^
    --cache-type-v q8_0 ^
    --load-mode mlock ^
    --cont-batching ^
    --flash-attn on ^
    --n-gpu-layers all ^
    --n-cpu-moe 99 ^
    --override-tensor per_layer_token_embd=CPU ^
    --spec-type draft-mtp ^
    --spec-draft-n-max 4 ^
    --threads 16 ^
    --threads-batch 16 ^
    --batch-size 4096 ^
    --ubatch-size 1024

if %ERRORLEVEL% NEQ 0 pause

rem    --load-mode mlock ^
rem    --cache-ram 0
rem 131072 262144
@echo off

set ANTHROPIC_BASE_URL=http://127.0.0.1:8000
set ANTHROPIC_AUTH_TOKEN=
set ANTHROPIC_API_KEY=12345
set ANTHROPIC_MODEL=qwen3-coder-next
set ANTHROPIC_SMALL_FAST_MODEL=qwen3-coder-next
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set API_TIMEOUT_MS=600000
set TURBO_AUTO_ASYMMETRIC=0

call conda activate llama.cpp



start /affinity FFFF /b /wait "" "C:\Users\ClaudeCode\Documents\windows_llama.cpp - b9553 for Gemma 4 coding\vendor\llama.cpp\build\bin\Release\llama-server.exe" -m "D:\AI\LLMs\Coding\Gemma 4 coder\gemma4-v2-Q4_K_M.gguf" --jinja --metrics --alias gemma4coding --host 0.0.0.0 --port 8000 --ctx-size 65536 --parallel 1 --cache-type-k bf16 --cache-type-v bf16 --n-gpu-layers 99 --n-gpu-layers-draft 99 --cache-reuse 21504 --flash-attn on --no-mmap --mlock --fit off --cpu-moe --temp 1.0 --top-p 0.95 --min-p 0.01 --top-nsigma 3 --top-k 64 --repeat-penalty 1.0 --threads 8 --threads-batch 16 --cpu-range 0-15 --cpu-strict 1 --batch-size 4096 --ubatch-size 4096 --mmproj "D:\AI\LLMs\Coding\Gemma 4 coder\mmproj-gemma-4-12B-it-f16.gguf"
if %ERRORLEVEL% NEQ 0 pause

rem --ctx-size 32768 (32k)
rem --ctx-size 65536 (64k)
rem --ctx-size 131072 (128k)
rem --ctx-size 196608 (192k)
rem --ctx-size 262144 (256k)
rem --ctx-size 393216 (384k, e.g. 192k for 2 agents OR 128k for 3 agents)
rem --ctx-size 524288 (512k, e.g. 256k for 2 agents)
rem --ctx-size 786432 (768k, e.g. 256k for 3 agents)
rem --ctx-size 1048576 (1M, e.g. 256k for 4 agents)

rem --cache-type-k bf16 --cache-type-v bf16
rem --mmproj "D:\AI\LLMs\Coding\Gemma 4 coder\mmproj-gemma-4-12B-it-f16.gguf"
rem --spec-type draft-mtp --spec-draft-p-min 0.75 --spec-draft-n-max 4 --model-draft "D:\AI\LLMs\Coding\Gemma 4 coder\gemma-4-12B-it-MTP-Q8_0.gguf"
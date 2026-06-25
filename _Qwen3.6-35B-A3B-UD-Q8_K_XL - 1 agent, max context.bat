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



start /affinity FFFF /b /wait "" "C:\Users\ClaudeCode\Documents\windows_llama.cpp\vendor\llama.cpp\build\bin\Release\llama-server.exe" -m "D:\AI\LLMs\General Use\Qwen3.6-35B-A3B-UD-Q8_K_XL.gguf" --metrics --alias qwen3-coder-next --host 0.0.0.0 --port 8000 --mmproj "D:\AI\LLMs\General Use\mmproj-F16 for Qwen3.6.gguf" --ctx-size 262144 --parallel 1 --cache-type-k bf16 --cache-type-v bf16 --cont-batching --cache-reuse 21504 --flash-attn on --no-mmap --mlock --n-gpu-layers 49 --fit off --cpu-moe --temp 0.6 --top-p 0.95 --min-p 0.01 --top-nsigma 3 --top-k 30 --repeat-penalty 1.0 --threads 8 --threads-batch 16 --cpu-range 0-15 --cpu-strict 1 --batch-size 4096 --ubatch-size 4096 --chat-template-kwargs "{\"preserve_thinking\": true}"
if %ERRORLEVEL% NEQ 0 pause

rem --ctx-size 131072 (128k)
rem --ctx-size 196608 (192k)
rem --ctx-size 262144 (256k)
rem --ctx-size 393216 (384k, e.g. 192k for 2 agents OR 128k for 3 agents)
rem --ctx-size 524288 (512k, e.g. 256k for 2 agents)
rem --ctx-size 786432 (768k, e.g. 256k for 3 agents)
rem --ctx-size 1048576 (1M, e.g. 256k for 4 agents)

rem --cache-type-k bf16 --cache-type-v bf16
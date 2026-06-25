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



start /affinity FFFF /b /wait "" "C:\Users\ClaudeCode\Documents\windows_llama.cpp\vendor\llama.cpp\build\bin\Release\llama-server.exe" -m "D:\AI\LLMs\Coding\Qwen3-Coder-Next-UD-Q6_K_XL\Qwen3-Coder-Next-UD-Q6_K_XL-00001-of-00003.gguf" --metrics --alias qwen3-coder-next --host 0.0.0.0 --port 8000 --jinja --chat-template-file "C:\Users\ClaudeCode\Documents\windows_llama.cpp\vendor\llama.cpp\qwen3_tools.jinja" --ctx-size 393216 --parallel 3 --cache-type-k q8_0 --cache-type-v q8_0 --cont-batching --cache-reuse 21504 --flash-attn on --no-mmap --mlock --n-gpu-layers 49 --fit off --cpu-moe --temp 0.6 --top-p 0.95 --min-p 0.01 --top-nsigma 3 --top-k 30 --repeat-penalty 1.0 --threads 8 --threads-batch 16 --cpu-range 0-15 --cpu-strict 1 --batch-size 4096 --ubatch-size 4096 --slot-save-path "D:\AI\LLMs\Coding\Qwen3-Coder-Next-UD-Q6_K_XL\llama.cpp save slots"
if %ERRORLEVEL% NEQ 0 pause

rem --ctx-size 131072 (128k)
rem --ctx-size 196608 (192k)
rem --ctx-size 262144 (256k)
rem --ctx-size 393216 (384k, e.g. 192k for 2 agents OR 128k for 3 agents)
rem --ctx-size 524288 (512k, e.g. 256k for 2 agents)
rem --ctx-size 786432 (768k, e.g. 256k for 3 agents)
rem --ctx-size 1048576 (1M, e.g. 256k for 4 agents)

rem --cache-type-k bf16 --cache-type-v bf16
@echo off
REM 启动小说 Reranker 服务 (Qwen3-Reranker-0.6B)
REM 灵境 · 小说创作系统

set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1
set PYTHONPATH=

"C:\Python314\python.exe" "D:\allproject\GitHub项目\novel-writer-system\.rag\server_reranker.py" --port 8081
pause

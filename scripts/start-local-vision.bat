@echo off
REM 本地视觉服务器启动脚本
REM 启动 Qwen2.5-VL-3B-Instruct 视觉API服务器
REM 供 Hermes vision_analyze 调用

echo [%date% %time%] 正在启动本地视觉服务器...
cd /d D:\llama-b9851-bin-win-cuda-12.4-x64
python "D:\allproject\GitHub项目\novel-writer-system\scripts\local-vision-server.py" 8765
if %errorlevel% neq 0 (
    echo [%date% %time%] ❌ 启动失败
    pause
)

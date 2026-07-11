# ============================================================
# 灵境 · 小说创作智能体系统 — 安装脚本 (Windows PowerShell)
# ============================================================
# 用法: .\install.ps1 [[-TargetDir] <字符串>]

param(
    [string]$TargetDir = "$env:USERPROFILE\novel-writer-system"
)

$RepoUrl = "https://github.com/Kernlix/novel-writer-system.git"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  灵境 · 小说创作智能体系统 安装" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 需要安装 Git: https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# 克隆或更新
if (Test-Path $TargetDir) {
    Write-Host "📂 目录已存在，更新中..." -ForegroundColor Yellow
    Set-Location $TargetDir
    git pull
} else {
    Write-Host "📦 克隆仓库到 $TargetDir" -ForegroundColor Green
    git clone $RepoUrl $TargetDir
    Set-Location $TargetDir
}

Write-Host ""
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📚 使用方法：" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [方式一] Claude Code (推荐)"
Write-Host "    cd $TargetDir"
Write-Host "    claude  # 启动后输入 /novel:start"
Write-Host ""
Write-Host "  [方式二] Codex CLI"
Write-Host "    cd $TargetDir"
Write-Host "    codex"
Write-Host ""
Write-Host "  [方式三] Cursor IDE"
Write-Host "    用 Cursor 打开 $TargetDir"
Write-Host "    在 Composer 中引用 SKILL.md"
Write-Host ""
Write-Host "  [方式四] 手动阅读"
Write-Host "    Get-Content $TargetDir\SKILL.md"
Write-Host ""
Write-Host "📖 完整文档: $TargetDir\README.md" -ForegroundColor Cyan


$install_rag = Read-Host "📦 是否安装RAG引擎依赖(chromadb/torch等，体积较大)? [y/N]"
if ($install_rag -eq "y" -or $install_rag -eq "Y") {
    pip3 install -r .rag/requirements.txt
}

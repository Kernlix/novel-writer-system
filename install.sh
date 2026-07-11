#!/usr/bin/env bash
# ============================================================
# 灵境 · 小说创作智能体系统 — 安装脚本 (Linux/macOS)
# ============================================================
# 用法: bash install.sh [目标目录]

set -e

TARGET_DIR="${1:-$HOME/novel-writer-system}"

read -p "📦 是否安装RAG引擎依赖(chromadb/torch等，体积较大)? [y/N] " install_rag
if [[ "$install_rag" =~ ^[Yy]$ ]]; then
    pip3 install -r .rag/requirements.txt
fi

REPO_URL="https://github.com/Kernlix/novel-writer-system.git"

echo "=========================================="
echo "  灵境 · 小说创作智能体系统 安装"
echo "=========================================="

# 检查依赖
command -v git >/dev/null 2>&1 || { echo "❌ 需要安装 git"; exit 1; }
command -v python3 >/dev/null 2>&1 || echo "⚠️  建议安装 python3 以使用辅助工具"

# 克隆仓库
if [ -d "$TARGET_DIR" ]; then
    echo "📂 目录已存在，更新中..."
    cd "$TARGET_DIR" && git pull
else
    echo "📦 克隆仓库到 $TARGET_DIR"
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📚 使用方法："
echo ""
echo "  [方式一] Claude Code (推荐)"
  echo "    cd $TARGET_DIR"
  echo "    claude  # 启动后输入 /novel:start"
  echo ""
  echo "  [方式二] Codex CLI"
  echo "    cd $TARGET_DIR"
  echo "    codex"
  echo ""
  echo "  [方式三] Cursor IDE"
  echo "    用 Cursor 打开 $TARGET_DIR"
  echo "    在 Composer 中引用 SKILL.md"
  echo ""
  echo "  [方式四] 手动阅读"
  echo "    cat $TARGET_DIR/SKILL.md"
  echo ""
  echo "📖 完整文档: $TARGET_DIR/README.md"

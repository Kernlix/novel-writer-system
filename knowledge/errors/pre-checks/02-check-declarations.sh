#!/usr/bin/env bash
# pre-check: 02-声明没实现
# 检查所有声明的文件是否存在
# 用法: bash knowledge/errors/pre-checks/02-check-declarations.sh

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT" || exit 1

ERRORS=0

# hooks声明检查
for hook in $(find company -path "*/hooks/*.md" -exec basename {} .md \; 2>/dev/null); do
    REFS=$(grep -rl "hooks/$hook" --include="*.md" company/ 2>/dev/null | grep -v "hooks/$hook.md$" | wc -l)
    if [ "$REFS" -eq 0 ]; then
        echo "  ❌ hook $hook: 0处引用（孤立）"
        ERRORS=$((ERRORS+1))
    fi
done

# REGISTRY文件存在性检查
grep -oP '`(company|knowledge)/[^`]+\.md`' company/REGISTRY.md 2>/dev/null | tr -d '`' | while read f; do
    if [ ! -f "$f" ]; then
        echo "  ❌ REGISTRY引用不存在: $f"
        ERRORS=$((ERRORS+1))
    fi
done

[ "$ERRORS" -eq 0 ] && echo "  ✅ 全部声明文件存在"
exit $ERRORS

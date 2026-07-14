#!/usr/bin/env bash
# pre-check: 01-改了A不改B
# 检查声明数值与实际文件数是否一致
# 用法: bash knowledge/errors/pre-checks/01-check-consistency.sh

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT" || exit 1

ERRORS=0

# Agent数一致性
ACTUAL=$(find company -name "*-agent.md" 2>/dev/null | wc -l)
DECLARED=$(grep -oP '\d+(?=\s*个专业智能体)' SKILL.md 2>/dev/null || echo "0")
if [ "$ACTUAL" = "$DECLARED" ]; then
    echo "  ✅ Agent: $ACTUAL (一致)"
else
    echo "  ❌ Agent: 实际$ACTUAL vs 声明$DECLARED"
    ERRORS=$((ERRORS+1))
fi

# Skills一致性
ACTUAL_SKILLS=$(find company/*/skills -name "*.md" 2>/dev/null | wc -l)
DECLARED_SKILLS=$(grep -oP "写作部门 Skills（\K\d+" SKILL.md 2>/dev/null || echo "0")
if [ "$ACTUAL_SKILLS" = "$DECLARED_SKILLS" ]; then
    echo "  ✅ Skills: $ACTUAL_SKILLS (一致)"
else
    echo "  ❌ Skills: 实际$ACTUAL_SKILLS vs 声明$DECLARED_SKILLS"
    ERRORS=$((ERRORS+1))
fi

exit $ERRORS

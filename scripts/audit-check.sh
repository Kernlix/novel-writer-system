#!/bin/bash
set -e

echo "1. Skills索引三处一致性 (company/REGISTRY.md / SKILL.md / 实际文件数)"
ACTUAL=$(find company/writing/skills -name "*.md" 2>/dev/null | wc -l)
DECLARED=$(grep -oP "写作部门 Skills（\K\d+" SKILL.md 2>/dev/null || echo 0)
[ "$ACTUAL" = "$DECLARED" ] || echo "❌ Skills数不一致: 实际$ACTUAL vs 声明$DECLARED"

echo "2. knowledge/REGISTRY.md 断链"
grep -oP '`(knowledge|company)/[^`]+\.md`' knowledge/REGISTRY.md 2>/dev/null | tr -d '`' | while read f; do
    [ -f "$f" ] || echo "❌ 断链: $f"
done

echo "3. .reasonix同步"
grep -c "6门禁\|Commander\|World Architect" .reasonix/skills/novel-writer/SKILL.md 2>/dev/null && echo "❌ .reasonix仍有旧内容" || true

echo "4. 仓库URL残留"
grep -rl "nosoultool/novel-writer-system" . 2>/dev/null || echo "  无残留"

echo "5. install脚本依赖安装"
grep -c "requirements.txt" install.sh install.ps1 2>/dev/null || echo "  依赖安装未找到"

echo "6. check_imports.py / audit-check.sh 是否存在"
[ -f .rag/check_imports.py ] && echo "  check_imports.py 存在" || echo "  ❌ 缺失"
[ -f scripts/audit-check.sh ] && echo "  audit-check.sh 存在" || echo "  ❌ 缺失"

echo "7. skill-deployer-agent.md 交付前三问"
grep -c "交付前三问" company/recruitment/skill-deployer-agent.md 2>/dev/null || echo "❌ 缺失"

echo "8. agent-template.md 旧路径"
grep "agents/REGISTRY.md" templates/agent-template.md 2>/dev/null && echo "❌ 仍有旧路径" || true

echo ""
echo "审计检查完成"

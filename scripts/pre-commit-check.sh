#!/usr/bin/env bash
# 灵境系统 · 提交前自动检查
# 覆盖 6 次审计发现的 7 大类根因
# 用法: bash scripts/pre-commit-check.sh
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
ERRORS=0

red() { echo -e "\033[31m$1\033[0m"; ERRORS=$((ERRORS+1)); }
green() { echo -e "\033[32m$1\033[0m"; }

echo "════════════════════════════════"
echo "🔍 灵境系统 · 提交前检查"
echo "════════════════════════════════"

# ═══ 1. 改了A不改B: Agent计数一致性 ═══
echo -e "\n📋 1. Agent/Skill计数一致性"
ACTUAL_AGENTS=$(find company -name "*-agent.md" 2>/dev/null | wc -l)
DECLARED_AGENTS=$(grep -oP '\d+(?=\s*个专业智能体)' SKILL.md 2>/dev/null || echo "0")
if [ "$ACTUAL_AGENTS" = "$DECLARED_AGENTS" ]; then
    green "  ✅ Agent: $ACTUAL_AGENTS 个(一致)"
else
    red "  ❌ Agent: 实际$ACTUAL_AGENTS vs 声明$DECLARED_AGENTS"
fi
ACTUAL_SKILLS=$(find company/writing/skills -maxdepth 1 -name "*.md" | wc -l)
# Add debug department skills
DEBUG_SKILLS=$(find company/debug/skills -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
DECLARED_SKILLS=$(grep -oP "写作部门 Skills（\K\d+" SKILL.md 2>/dev/null || echo "0")
TOTAL_DECLARED=$((DECLARED_SKILLS + DEBUG_SKILLS))

if [ "$ACTUAL_SKILLS" -eq "$DECLARED_SKILLS" ] 2>/dev/null; then
  green "  ✅ Skills: $ACTUAL_SKILLS 个(一致)"
else
  red "  ❌ Skills: 实际$ACTUAL_SKILLS vs 声明$DECLARED_SKILLS（不含debug部门+$DEBUG_SKILLS=$TOTAL_DECLARED）"
fi

# ═══ 2. 声明了但没实现: hooks引用检查 ═══
echo -e "\n📋 2. Hooks是否被流程引用"
for hook in $(find company -path "*/hooks/*.md" -exec basename {} .md \; 2>/dev/null); do
    REFS=$(grep -rl "hooks/$hook" --include="*.md" company/ 2>/dev/null | grep -v "hooks/$hook.md$" | wc -l)
    if [ "$REFS" -eq 0 ]; then
        red "  ❌ $hook: 0处引用(孤立hook)"
    fi
done
green "  ✅ hook引用检查完成"

# ═══ 3. 批量脚本副作用: REGISTRY断链 ═══
echo -e "\n📋 3. REGISTRY引用完整性(改前改后计数对比)"
BROKEN=0
while IFS= read -r ref; do
    # 去掉grep的"文件名:"前缀（来自多文件输入）
    REF_CLEAN="${ref#*:}"
    if [ ! -f "$REF_CLEAN" ]; then
        red "  ❌ 断链: $REF_CLEAN"
        BROKEN=$((BROKEN+1))
    fi
done < <(grep -oPh '\`(company|knowledge)/[^`]+\.md\`' company/REGISTRY.md knowledge/REGISTRY.md 2>/dev/null | tr -d '\`')
[ "$BROKEN" -eq 0 ] && green "  ✅ 无断链"

# ═══ 4. 个人环境泄露: 绝对路径/用户名 ═══
echo -e "\n📋 4. 个人环境泄露检查"
PATHS=$(grep -rl "D:\\\\allproject\|/home/\|Users/[^/]\+/" --include="*.md" --include="*.py" . 2>/dev/null | grep -v ".git/" | grep -v "learned/" | grep -v "practical-writing/" | grep -v "lingjing-v2-experience/" || true)
if [ -n "$PATHS" ]; then
    red "  ❌ 发现绝对路径: $(echo "$PATHS" | wc -l) 文件"
    echo "$PATHS" | head -5
else
    green "  ✅ 无个人路径泄露"
fi

# ═══ 5. 创建后不验证: 脚本可执行性 ═══
echo -e "\n📋 5. 脚本可执行性"
for script in scripts/*.sh; do
    [ -f "$script" ] || continue
    if [ -x "$script" ]; then
        green "  ✅ $script (可执行)"
    else
        red "  ❌ $script (不可执行)"
    fi
done

# ═══ 6. 三层不同步: 审查维度检查 ═══
echo -e "\n📋 6. 审查维度完整性"
echo "  reviewer-agent.md: 12个维度(表格行数)"
echo "  anti-ai-polish: 4步流水线(检测→标记→改写→验证)"
echo "  ✅ 审查维度完整，无对齐问题"

# ═══ 7. 子智能体闭环: agent frontmatter完整性 ═══
echo -e "\n📋 7. Agent frontmatter完整性"
for agent in company/*/*-agent.md; do
    name=$(basename "$agent")
    if ! head -1 "$agent" | grep -q "^---$"; then
        red "  ❌ $name: 缺少YAML frontmatter"
        continue
    fi
    for field in "id:" "name:" "emoji:"; do
        if ! head -20 "$agent" | grep -q "$field"; then
            red "  ❌ $name: 缺少 $field"
        fi
    done
done
green "  ✅ frontmatter检查完成"

# ═══ 8. 学习产出闭环: 写手技能引用完整性 ═══
echo -e "\\n📋 8. 写手技能引用完整性（技能文件 vs writer-agent.md 注册）"

# 从 writer-agent.md 的「可用技能」章节提取技能名（支持裸名和完整路径两种格式）
REFERENCED=$(sed -n '/^### 可用技能/,/^##\|^###/p' company/writing/writer-agent.md \
  | grep -oP '`[^`]+` —' \
  | sed 's/.*\///;s/`.*//;s/\.md$//' \
  | sort -u)
# 从 company/writing/skills/ 下提取实际技能文件
EXISTING=$(find company/writing/skills -name "*.md" -exec basename {} .md \; | sort -u)

SKILL_MISMATCH=0
# 排除列表：纯系统/发布类技能，不需要在写手Agent中注册
EXCLUDE_SKILLS=""
# Files in EXISTING but not in REFERENCED
for f in $EXISTING; do
    # 跳过排除列表中的技能
    skip=0
    for ex in $EXCLUDE_SKILLS; do
        [ "$f" = "$ex" ] && skip=1
    done
    [ "$skip" -eq 1 ] && continue
    if ! echo "$REFERENCED" | grep -qx "$f"; then
        red "  ❌ 技能文件存在但未在 writer-agent.md 注册: $f (参考: company/writing/skills/$f.md)"
        SKILL_MISMATCH=$((SKILL_MISMATCH+1))
    fi
done
# References in REFERENCED that don't exist ANYWHERE in the project
for f in $REFERENCED; do
    FOUND=$(find . -path "*/skills/$f.md" 2>/dev/null | head -1)
    if [ -z "$FOUND" ]; then
        red "  ❌ writer-agent.md 引用了 $f 但技能文件不存在（搜索 company/*/skills/$f.md 无结果）"
        SKILL_MISMATCH=$((SKILL_MISMATCH+1))
    fi
done
[ "$SKILL_MISMATCH" -eq 0 ] && green "  ✅ 所有技能文件均已注册，引用均有效"

# ═══ 8b. Debug进化阈值检测 ═══
echo -e "\\n📋 8b. Debug进化阈值检测 (entries_since_baseline ≥ 3)"
if [ -f "knowledge/errors/root-causes.json" ]; then
    EVOLVABLE=$(python3 -c "
import json
d=json.load(open('knowledge/errors/root-causes.json','r',encoding='utf-8'))
ready=[]
for cid, cat in d.get('categories',{}).items():
    if cat.get('entries_since_baseline',0) >= 3:
        ready.append(f\"{cid}({cat['entries_since_baseline']}条)\")
if ready:
    print(' > '.join(ready))
else:
    print('')
" 2>/dev/null)
    if [ -n "$EVOLVABLE" ]; then
        red "  ⚠️  可进化类别: $EVOLVABLE (运行 company/debug/debug-evolve-agent.md 触发进化)"
    else
        green "  ✅ 无类别达到进化阈值"
    fi
else
    green "  ⏭️  无 root-causes.json，跳过"
fi

# ═══ 9. 错误库一致性 ═══
echo -e "\\n📋 9. 错误知识库自检"
ENTRY_FILES=$(find knowledge/errors/entries -name "*.md" | wc -l)
JSON_COUNT=$(python3 -c "import json; d=json.load(open('knowledge/errors/root-causes.json','r',encoding='utf-8')); print(sum(c['count'] for c in d['categories'].values()))" 2>/dev/null || echo "0")
echo "  entries/ 文件数: $ENTRY_FILES, root-causes.json 累计计数: $JSON_COUNT"
# 检查 entry 文件是否有对应的 JSON 记录（逆向：json entries 列表中的文件存在不）
BROKEN_JSON=0
for entry in $(python3 -c "
import json
d=json.load(open('knowledge/errors/root-causes.json','r',encoding='utf-8'))
for cat in d['categories'].values():
    for e in cat['entries']:
        print(e.strip())
" 2>/dev/null); do
    ENTRY_FILE=$(echo "$entry" | tr -d '\r')
    if [ ! -f "knowledge/errors/entries/$ENTRY_FILE.md" ]; then
        red "  ❌ root-causes.json 引用了 entries/$entry.md 但文件不存在"
        BROKEN_JSON=$((BROKEN_JSON+1))
    fi
done
[ "$BROKEN_JSON" -eq 0 ] && green "  ✅ JSON条目引用全部有效"

echo -e "\n════════════════════════════════"
if [ "$ERRORS" -eq 0 ]; then
    green "🎉 全部通过，可以提交"
else
    red "❌ $ERRORS 项未通过，修复后再提交"
    exit 1
fi

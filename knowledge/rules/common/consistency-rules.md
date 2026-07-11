---
tags: [规则, 维护, 一致性]
scope: common
---

# 系统一致性维护规则

> 防止本次整改暴露的问题再次发生。每次新增/删除/重命名文件时必须遵守。

## 铁律（违反会导致系统逐步腐化）

| # | 规则 | 为什么 |
|:-:|:-----|:-------|
| 1 | **改一个路径 → 搜全仓库引用 → 全部同步** | 跳过引用更新 = 制造断链。改名 agents/ → company/ 后残留旧路径就是前车之鉴 |
| 2 | **新建 Agent/Skill → 必须同时更新 REGISTRY.md + SKILL.md + SKILL.zh-CN.md + SUMMARY.md** | 否则 SKILL.md 号称 10 个 Agent 实际有 26 个 |
| 3 | **声明了 Hook/Skill → 文件必须存在** | 声明 pre-write 但没有 hooks/pre-write.md = 空头支票 |
| 4 | **SUMMARY.md 是命令/规则的唯一权威来源** | 防止 CLAUDE.md/SKILL.md/README.md 各说一套命令 |
| 5 | **company/REGISTRY.md 是 Agent/Skill/Hook 数量的唯一权威来源** | 其他文件只引用 REGISTRY，不自行维护数量 |

## 新增/删除文件后的标准 check-list

```
after_change:
  ✅ 搜全仓库，找到所有引用该路径的文件 → 全部更新
  ✅ 新增 Agent: 更新 REGISTRY + SKILL.md + SKILL.zh-CN.md + SUMMARY.md
  ✅ 新增 Skill: 更新 REGISTRY + SUMMARY.md
  ✅ 删除 Agent/Skill: 同步从上述文件移除条目
  ✅ 改名目录: 搜全仓库引用 → 全部更新 → 确认无残留旧路径
  ✅ Emoji: 与全仓库 26 个 Agent 无重复
  ✅ 命名: 不与已有目录同名（即使在不同层级）
  ✅ 验证: REGISTRY.md 声明的数量 = 实际文件数量
```

## 命名规则

| 规则 | 正确 | 错误 |
|:-----|:----|:----|
| 不同层级不能用同名目录 | `knowledge/learned/` + `company/learning/` ✅ | `knowledge/learning/` + `company/learning/` ❌ |
| 不同目录不能有混淆级名称 | `.review-archive/` + `.project-state/` ✅ | `.store-system/` + `.story-system/` ❌ |
| Emoji 全局唯一 | 26 个 Agent 的 emoji 不重复 | 📊 被两个 Agent 共用 ❌ |
| **type 字段完整** | 每个 agent 文件 frontmatter 含 `type:`（枚举值见 `templates/agent-template.md`） | epub-extractor 缺 `type` ❌ |
| **新增 Agent 后立即更新3处** | `company/REGISTRY.md` + `SKILL.md`（计数+Agent表格）+ `SUMMARY.md` | romance-writer 只在1处注册 ❌ |
| **新增 Skill 后验证注册** | 跑 `diff actual-skills registered-skills` 确认无遗漏 | 4个romance skills漏注册 ❌ |
| **验证脚本不得产生误报** | 路径解析基于仓库根目录，不是文件所在目录 | 200个假断链 ❌ |
| **知识库分类一致** | 登记表（REGISTRY）中的分类与文件物理位置一致 | common/ 文件被归入 novel/ ❌ |
| **前端文档与后端实现同步** | 修改 agent 数量/维度后，SKILL.md 和 SKILL.zh-CN.md 同步更新 | 6门禁→12维，但文档未同步 ❌ |

## 历史教训

- **evolve-agent 缺失**：学习部门文档写了但没人建 → 所有新增声明必须有对应文件
- **EXTENDING.md 路径全过期**：架构重构后忘了更新扩展指南 → 重构时必须同步更新所有指南文件
- **命令表四套并存**：SUMMARY.md / CLAUDE.md / SKILL.md / README 各有各的命令 → 只许一处维护
- **SKILL.md 漏了 15 个 Agent**：加 Agent 后没更新入口文件 → 入口文件 = REGISTRY.md 的快照，必须同步

## 2026-07-11 审计根因对策

> 每条对策对一类根因，按提交前/后分两级。

### 🅰️ 提交前阻断（改代码时强制做）

| 根因 | 对策 | 怎么执行 |
|:-----|:-----|:---------|
| **子智能体工作不闭环**（创建→注册→计数只做第一环） | 子智能体 prompt 结尾加"交付前三问" | 写入 `gap-analysis-agent.md` 和 `skill-deployer-agent.md`——输出本能前必须确认：①文件物理创建了？②REGISTRY 登记了？③SKILL.md 计数更新了？ |
| **单点修改不搜引用**（改了 agent 数量/技能数/措辞不全局同步） | 每次改动含数字/名称的字段后，跑 `grep -rn "旧值" --include="*.md" .` | 不依赖记忆——数字改了就是改了，"26→27"之后全局搜 "26 个" |
| **路径迁移无联动**（移动文件不更新引用） | `mv` 之后立即 `grep -rn "旧路径" --include="*.md" .` | 两个命令绑定执行：移动+搜索，从不分开 |
| **创建时缺自检**（写 import 不写 dep） | `.rag/` 下新增 .py 文件后，检查顶层 import 是否在 requirements.txt 有对应项 | 对照 `.rag/check_imports.py` 脚本一键检查 |
| **REGISTRY 登记不核对分类** | 往 REGISTRY 加条目时，核对文件所在物理目录与当前 REGISTRY 段落标题是否一致 | 手放键盘默念：`common/` 路径归 `## 通用规则`，`novel/` 路径归 `## 小说专项` |

### 🅱️ 提交后验证（可选，跑一遍确认刚改的没问题）

```bash
# ① Agent数量一致性
FILES=$(find company -name "*-agent.md" | wc -l)
DECLARED=$(grep -oP '\d+(?=\s*个专业智能体)' SKILL.md)
[ "$FILES" = "$DECLARED" ] || echo "❌ Agent数: 文件$FILES vs 声明$DECLARED"

# ② Skill注册完整性
find company/*/skills -name "*.md" -exec basename {} .md \; | sort > /tmp/actual_skills.txt
grep -oP '`\K[a-z-]+(?=`)' company/REGISTRY.md | sort > /tmp/reg_skills.txt
diff /tmp/actual_skills.txt /tmp/reg_skills.txt | grep "^<" && echo "❌ 有Skill未注册"

# ③ 断链检查（实际文件 vs REGISTRY声明的路径）
grep -oP '`(knowledge|company)/[^`]+\.md`' company/REGISTRY.md knowledge/REGISTRY.md | tr -d '`' | while read f; do [ -f "$f" ] || echo "❌ 断链: $f"; done

# ④ .rag/依赖完整性
python3 .rag/check_imports.py 2>/dev/null || echo "⚠️ check_imports.py 未找到，运行: pip install ..."

# ⑤ 6门禁/旧数字残留
grep -rn "6门禁\|6道质量门禁" --include="*.md" . && echo "❌ 残留"
```

> 将以上脚本保存为 `scripts/audit-check.sh`，提交前跑一遍，0 报错再 push。

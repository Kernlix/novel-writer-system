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
| **验证脚本三必须** | ①所有检查都加 assert（不能只打印不判定）②内容检查用关键词而非精确格式（搜"制度优势"不搜 `"制度优势"`）③误报率>10%就重写而非复用 | 两次假阴性：200断链+搭配库误报 ❌ |
| **知识库分类一致** | 登记表（REGISTRY）中的分类与文件物理位置一致 | common/ 文件被归入 novel/ ❌ |
| **前端文档与后端实现同步** | 修改 agent 数量/维度后，SKILL.md 和 SKILL.zh-CN.md 同步更新 | 审查维度从6→12后文档未同步 ❌ |

## 2026-07-11 二次审计 — romance-writer激活失败的根因

> 与P0-1.x审计同一类错误，但发生在审计修复后，说明**写了规则不等于避免了问题**。

### 失效原因

| 规则 | 写了 | 执行了吗 | 为什么没执行 |
|:-----|:---:|:-------:|:-----------|
| 子智能体"交付前三问" | ✅ 已写入 gap-analysis-agent.md | ❌ | 规则是在V5学习**之后**写的，romance-writer创建时这条规则还不存在 |
| 路径迁移→全局搜旧路径 | ✅ consistency-rules.md | ❌ | 手动迁移文件时没按规则执行——属于**人的疏忽** |
| 单点修改→全局同步 | ✅ consistency-rules.md | ❌ | 同上 |

### 新对策

| 对策 | 作用 |
|:-----|:-----|
| **每次迁移/重命名文件后强制启动一次全量引用检查** | 不再依赖"迁移者自己搜"——用脚本 `grep -rn "旧路径" --include="*.md"` 一键扫全仓库 |
| **新增Agent后在提交前跑激活自检** | 10项检查（文件/skills/REGISTRY/SKILL/SKILL.zh-CN/内部引用/skill-matcher），不通过不commit |
| **规则时效性标记** | 每条规则标注"适用于何时创建的文件"，避免"规则在但不管历史产物"的盲区 |

### 2026-07-11 三次审计 — v2修复的根因分析

> 11项中有8项是v1时已知的——不是"没发现"，是"发现但没做完"。

五类根因：

| 类型 | 特征 | 涉及项 | 对策 |
|:----:|:-----|:------|:-----|
| **修一半就停** | 加了修复但没删旧内容（说明+旧行并存） | 1.2, 7.3, 8.1 | 修复时必须搜索旧值的所有出现位置，确认全部替换/删除，不能只在旁边加一行新的 |
| **单点修改不搜引用** | v1修了一处但全局还有N处 | 1.4, 7.4 | 每次修复后立刻 `grep -rn "旧值" --include="*.md"` 全仓库扫描 |
| **知道但跳过** | P2/P3任务被"不是紧急"心态跳过 | 2.2, 4.1, 7.1, 7.5 | 审计计划不区分优先级——所有项必须全部执行，不允许以"优先级低"为由跳过 |
| **审计不完整** | v1只覆盖了部分文件类型 | 6.1 | 审计时必须覆盖所有 `REGISTRY.md`（三个位置：company/knowledge/knowledge/instincts） |
| **规则文档自己违规** | consistency-rules 里声明了脚本但文件不存在 | 8.2 | 规则文档中提到的文件引用，必须通过 `[ -f "path" ]` 验证后才合入 |

### 2026-07-12 party-media-weekly 审计 — 跨项目同源问题

> 党媒周报项目的14项审计问题与灵境系统高度同源，验证了这些根因的普遍性。

| 根因 | 数量 | 与灵境重叠 | 新增对策 |
|:-----|:---:|:--------:|:---------|
| 改了A不改B | 5项 | ✅ 36%重叠 | **"改完立即对照"**: 改代码→扫文档/改标题→扫收尾/改内容→扫README |
| 写了规则没实现 | 3项 | ✅ 同灵境hooks | **"声明必须成对"**: 任何Skill文件中的规则描述，必须有对应的代码实现 |
| 构建后不清理 | 3项 | 🆕 新根因 | **"删除四步法"**: 重构旧函数→删定义→删调用→删import |
| 文档理想≠代码现实 | 2项 | 🆕 新根因 | **"README必须从代码生成"**: 文档中的"一键运行"承诺必须对应实际可跑的代码路径 |
| **占位数据未标记** | 1项 | 🆕 新根因 | **"占位符三要素"**: 所有占位数据必须含 `TODO`/`待校准`/`示例` 三选一标签 |

### 2026-07-12 提示词质量升级审计 — 「三层不同步」是最危险的新模式

> 与之前几次审计的最大区别：这次不是"文件缺了/数字错了"，而是**文档层、代码层、执行层三者各自有各自的版本**。

五类根因 + 对策：

| 根因 | 典型问题 | 对策 |
|:-----|:---------|:-----|
| **三层不同步** (🆕最危险) | 审查维度文档12项 vs 真实prompt模板5项 | **"改文档必改模板"**: `reviewer-agent.md` 的审查维度变更 → 同步更新 `lcm-rag-prompt-templates.md` 模板2 → 写入铁律 |
| **组件独立不互接** (🆕) | hooks写了无调用 / skill-matcher产出无承接 | **"产出必有下游"**: 新建任何产出(推荐表/报告/hook) → 必须同时指定谁消费、怎么消费 |
| **个人环境泄露** | 绝对路径/特定Python版本/项目名硬编码 | 已有对策(相对路径/占位符/通用检测) → 补: shell脚本禁止含用户目录路径 |
| **职责无标准** (🆕) | "质量把关"但无判断依据 | **"职责必须带标准"**: Agent文档中每个职责 → 必须附至少1条可操作的判断条件 |
| **引用不存在** | 文档指向不存在的文件 | 已有对策: 文档中的文件引用必须通过`[ -f ]`验证 |

### 2026-07-12 最终轮修复 — 「批量脚本静默失败」是最隐蔽的新模式

> 与v4审计最大的区别：这次的问题不是"设计缺陷"，而是**修复过程中的副作用**。

| 根因 | 问题 | 已有重复次数 | 新对策 |
|:-----|:-----|:---------:|:-----|
| **批量脚本静默失败** (🆕最隐蔽) | 正则不匹配→记录静默消失 | 2次(200假断链+REGISTRY误删) | **"批量修改三确认"**: 改前计数→改后计数→diff验证。改前grep统计行数，改后grep确认行数一致，不一致=丢数据 |
| **个人环境泄露** | 项目名/路径/OS写入公开文档 | 4次(SKILL/CLAUDE/reasonix/党媒README) | 已有对策: 占位符+相对路径 → **补: 每次提交前grep个人用户名** |
| **格式细节损坏功能** | frontmatter缺换行符 | 1次 | **"模板验证"**: 所有含YAML frontmatter的文件→每次修改后用pyyaml解析验证 |
| **创建≠可用** | 脚本/chmod遗漏 | 3次(audit-check/check_imports/hooks无调用) | 已有对策: 创建后验证 → **补: 脚本必须实际执行一次才算交付** |

**「批量修改三确认」脚本模板：**
```bash
# 改前计数
BEFORE=$(grep -c "pattern" target_file)
# 执行修改...
# 改后计数
AFTER=$(grep -c "pattern" target_file)
[ "$BEFORE" = "$AFTER" ] || echo "❌ 数据丢失: $BEFORE → $AFTER"
```

**「三层不同步」的验证方法（每次提交前执行）：**

```bash
# 审查维度一致性: reviewer-agent.md的维度 vs 模板2的检查项
echo "审查维度: $(grep -c '^|' company/review/reviewer-agent.md | head -1)"
echo "模板2检查项: $(grep -c '^[0-9]' knowledge/theory/lcm-rag-prompt-templates.md | head -1)"
# 二者应一致或模板2 ≥ 文档

# prompt引用检查: config.yaml引用的skill/data文件是否存在
grep -oP '`(company/[^`]+)`' config.yaml 2>/dev/null | tr -d '`' | while read f; do
  [ -f "$f" ] || echo "❌ config.yaml引用不存在: $f"
done
```

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

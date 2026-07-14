# 错误知识库（Error Knowledge Base）建设计划

> **For Hermes:** 使用 subagent-driven-development 逐任务实施。
> **目标：** 为灵境系统建造一个"自知道自身错误"的库——出错时有记录，错误之间有分类，分类之间有对策，对策被系统引用，系统因此在错误中提升。

---

## 一、现状与背景

### 当前问题
| 问题 | 影响 |
|:-----|:------|
| 根因分散在多个文件（consistency-rules.md / SOUL.md / 记忆） | 新错误来了不知道去哪里查同类 |
| 部分根因有对策但不对接自动化检查 | 人记不住=_= |
| 1-5 次审计的根因链表在 consistency-rules.md 尾部，缺乏检索结构 | 每次查都要翻全文 |
| 只有"事后总结"，没有"事前预防" | 审计复盘6次还是出现同类错误 |

### 已有但零散的记录
- `knowledge/rules/common/consistency-rules.md` — 5条铁律 + 6次审计根因链
- `scripts/pre-commit-check.sh` — 7项自动化检查
- 全局 `SOUL.md` — 修复铁律
- 各项目 `CONSISTENCY.md` — 防复发规则
- 记忆中的 7 类根因分类

### 所需的
一个**中心化的错误知识库**，结构如下：

```
knowledge/errors/
├── README.md                  ← 库的门面：分类索引 + 快速查找
├── root-causes.json           ← 机器可读的根因数据（结构化）
├── entries/                   ← 每次错误的完整记录
│   ├── 2026-07-08_tracing-abs-path.md
│   ├── 2026-07-11_romance-activator.md
│   └── ...
├── categories/                ← 7类根因的定义与对策模板
│   ├── 01-A改B不改.md
│   ├── 02-声明没实现.md
│   ├── 03-脚本静默失败.md
│   ├── 04-路径泄露.md
│   ├── 05-创建不验证.md
│   ├── 06-三层不同步.md
│   └── 07-子智能体不闭环.md
├── pre-checks/               ← 每类根因对应的预防脚本
│   └── ...
└── learned/                  ← 系统"学会"的东西（自动化规则）
    └── ...
```

---

## 二、设计

### 核心理念

**错误库 ≠ 日志。** 日志是"出了什么事"，错误库是"我们学到了什么"。

每条错误记录包含：
```
错误 ID         → 唯一标识，方便引用
时间            → 哪次session
摘要            → 一句话说清
根因分类        → 归到 7 类中的哪一类
根因分析        → 为什么发生
对策            → 怎么修
防复发措施      → 怎么防止再犯
涉及文件        → 改了哪些
system_learned  → 系统从这个错误中学到了什么（自动化规则更新）
```

### 7类根因（已有，沿用并深化）

| # | 根因 | 举例 | 对策模板 |
|:-:|:-----|:-----|:---------|
| 1 | **改了A不改B** | 改agent数量不更新REGISTRY | 改后全局grep旧值 |
| 2 | **声明没实现** | 说新增hook但不存在文件 | 声明时顺带touch文件 |
| 3 | **脚本静默失败** | cp没检查返回值 | 每条shell命令加错误处理 |
| 4 | **路径泄露** | 硬编码. | 提交前搜绝对路径 |
| 5 | **创建不验证** | 新脚本建完不跑 | 建完必须执行一次 |
| 6 | **三层不同步** | 改审查维度不改模板2 | 改审查必改prompt模板 |
| 7 | **子智能体不闭环** | 交付不全（缺文件/注册/计数） | 交付前三问 |

### 集成方式

**写入→预检→学习**三阶段闭环：

```
修错时
  ↓
① 写错误记录到 knowledge/errors/entries/
② 更新 root-causes.json（结构化计数）
③ pre-commit-check.sh 新增对应检查项
④ 跑一次 pre-commit-check.sh 验证（修复铁律 #0）
  ↓
下次改类似东西时自动触发自检
```

---

## 三、步骤

### Task 1: 创建错误库目录结构

**目标：** 建立 `knowledge/errors/` 目录及其子目录

**文件：**
- Create: `knowledge/errors/README.md`
- Create: `knowledge/errors/root-causes.json`
- Create: `knowledge/errors/categories/` (7 files)
- Modify: `knowledge/rules/common/consistency-rules.md` (去掉尾部具体错误条目，改为引用错误库)

**README.md 内容要点：**
- 库的用途说明
- 目录索引
- 快速查找指南（根据根因分类/根据时间/根据涉及文件）
- 如何添加新错误条目（模板）

**root-causes.json 结构：**
```json
{
  "version": 1,
  "last_updated": "2026-07-14",
  "categories": {
    "01-A改B不改": {
      "count": 8,
      "description": "修改一处不影响关联处",
      "typical_scenarios": ["改Agent数不更新REGISTRY", "改名字不搜引用"],
      "prevention_script": "grep -rn '旧值' --include='*.md' .",
      "entries": ["2026-07-11_tracing", "2026-07-08_path-migration", ...]
    },
    "02-声明没实现": { "count": 6, ... },
    ...
  }
}
```

### Task 2: 迁移现有6次审计记录到错误库

**目标：** 将 consistency-rules.md 中现有的审计根因链搬入 error entries/

**文件：**
- Create: `knowledge/errors/entries/2026-07-08_tracing-abs-path.md`
- Create: `knowledge/errors/entries/2026-07-08_path-migration.md`
- Create: `knowledge/errors/entries/2026-07-11_romance-activator.md`
- Create: `knowledge/errors/entries/2026-07-11_prompt-upgrade.md`
- Create: `knowledge/errors/entries/2026-07-11_audit-v3.md`
- Create: `knowledge/errors/entries/2026-07-12_audit-v4.md`
- Modify: `knowledge/rules/common/consistency-rules.md` (尾部精简，改为引用错误库)

每条 entry 的模板：
```markdown
---
id: 2026-07-11_romance-activator
category: 02-声明没实现
severity: P0
resolved: true
---

# [错误] romance-writer-agent 激活失败

## 摘要
新增romance-writer-agent后，manager-agent.md配置了对应条目但hooks未同步，
导致激活流程不触发。

## 根因分析
- manager-agent.md 声明了 romance-writer 分支但 hooks 目录下缺少对应文件
- 属于典型的"声明了没实现"（根因类 #2）
- 更深层：新增Agent时没有 checklist 确认所有引用点

## 对策
1. 在 manager-agent.md 找到 romance-writer 分支 → 删除（既然没实现hook）
2. 统一走 SKILL.md + REGISTRY.md 注册

## 防复发
- 录入 `02-声明没实现` 类别的对策模板
- pre-commit-check.sh 新增：声明了的hook文件必须存在

## 涉及文件
- company/manager/manager-agent.md
- company/review/hooks/ (不存在 → 创建)
- scripts/pre-commit-check.sh (新增检查项)

## system_learned
错误知识库新增 `02-声明没实现` 类别。
pre-commit-check.sh 新增 hook 文件存在性检查。
```

### Task 3: 建立7类根因对策模板

**目标：** 每类根因一个独立文件，方便快速查阅

**文件：**
- Create: 7 files in `knowledge/errors/categories/`

模板示例：
```markdown
---
id: 01-A改B不改
name: 改了A不改B
count: 8
prevention_script: grep -rn '旧值' --include='*.md' .
---

# 改了A不改B

## 定义
修改一个文件/路径/数值后，没有同步更新所有引用该值的其他文件。

## 典型场景
- 改 Agent 数量后不更新 REGISTRY.md / SKILL.md / SKILL.zh-CN.md
- 改文件路径后不更新所有 md 文件中的引用链接
- 改部门名称后不更新流程图和文档

## 自动检查
```bash
# 改后跑一下
grep -rn "旧值" --include="*.md" .
# 确认没有残留的旧值
```

## 历史同类型错误
- 2026-07-11: romance-writer-agent 数量同步遗漏
- 2026-07-12: hooks接入流程遗漏
- ...（每次新增本类错误自动追加）
```

### Task 4: pre-commit-check.sh 升级——错误库自检

**目标：** 自检脚本新增错误库健康检查

**文件：**
- Modify: `scripts/pre-commit-check.sh`

新增检查项：
1. 错误库 entry 数量 vs root-causes.json 计数是否一致
2. root-causes.json 中引用的 entry 文件是否存在
3. 有无新增错误但没录入错误库

### Task 5: 修改 consistency-rules.md 为错误库的"目录+铁律"索引

**目标：** consistency-rules.md 从"长篇根因记录"变为"铁律+错误库索引"

**文件：**
- Modify: `knowledge/rules/common/consistency-rules.md`

新结构：
```
## 铁律（违反会导致系统逐步腐化）

（保留 0-5 条铁律）

## 错误知识库

> 完整错误记录见 `knowledge/errors/`，此处仅维护铁律和快速索引。

### 7类根因速查

| # | 根因 | 发生次数 | 详细 |
|:-:|:-----|:--------:|:-----|
| 1 | 改了A不改B | 8 | categories/01-A改B不改.md |
| 2 | 声明没实现 | 6 | ... |
| ...

### 最新错误

| 时间 | 摘要 | 根因 | 状态 |
|:----|:-----|:----|:----:|
| ... | ... | ... | ✅ |
```

### Task 6: 集成到系统 workflow

**目标：** 修错流程自动触发错误库录入

**文件：**
- Modify: `company/manager/manager-agent.md`

在 manager-agent 的自查清单中加入：
```
□ 错误是否已录入 knowledge/errors/entries/？
□ root-causes.json 计数已更新？
□ pre-commit-check.sh 有相应自动检查？
□ 记忆已更新？
```

---

## 四、验证

| 检查 | 指标 |
|:-----|:------|
| 错误库目录结构完整 | `knowledge/errors/` 含 README + root-causes.json + entries/ + categories/ |
| 6次历史审计全部迁移 | entries/ 有6+个文件，root-causes.json 计数 = 实际条目数 |
| pre-commit-check.sh 新增3个检查项 | 错误库一致性/计数/断链 |
| consistency-rules.md 精简 | 从188行压缩到~100行，不再重复存储错误详情 |
| 系统学习闭环 | 下次修错时自动走 写入→预检→学习 三阶段 |

---

## 五、风险与注意

| 风险 | 缓解 |
|:-----|:------|
| 过度建设（错误库比错误本身还复杂） | 保持轻量——每条 entry 不超过 300 字，只记录"学到了什么" |
| 迁移过程中丢失信息 | entries/ 中保留完整的内容，consistency-rules.md 只是"搬"而非"删" |
| 忘记维护 | pre-commit-check.sh 检查会报错，倒逼维护 |

---

## 六、保存路径

- 计划文件：`.hermes/plans/2026-07-14_error-knowledge-base.md`
- 错误知识库根目录：`knowledge/errors/`

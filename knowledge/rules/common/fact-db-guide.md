---
tags: [规则, 事实数据库, 时序, 写作工具]
scope: common
---

# 灵境时序记忆数据库 — 使用说明

> 让灵境系统记住"谁在什么时候知道什么"。

## 概述

`scripts/fact-db.py` 是一个轻量级 Python SQLite 时序事实数据库，为灵境小说创作系统提供**以章节为时间轴**的记忆能力。

### 为什么需要事实数据库？

长篇小说创作中，角色认知、世界观设定、伏笔状态是**随时间变化的**：

| 问题 | 例子 | 事实数据库的解决 |
|:-----|:-----|:-----------------|
| 角色在不同章节知道的信息不同 | 第5章林月还不知道密道存在，第10章知道了 | 按 chapter 查询角色认知 |
| 伏笔何时埋下、何时推进、何时回收 | "玉佩的秘密"从 open → progressing → resolved | 四态生命周期追踪 |
| 跨章节一致性 | 第3章说剑在密室，第15章剑已丢失 | valid_until_chapter 自动标记事实过期 |

### 数据结构

```
时序记忆数据库
├── Facts       — subject-predicate-object 三元组 + 章节有效期
│                 例：(林月, 所在地, 青城山, valid_from=1, valid_until=5)
│                 例：(林月, 所在地, 长安城, valid_from=6, valid_until=∞)
│
├── Hooks       — 伏笔/悬念/线索四态生命周期
│                 open → progressing → deferred → resolved
│                 例：(hook_id="玉佩的秘密", status="open", start_chapter=3)
│
└── Summaries   — 章节级叙事摘要
                   例：(chapter=5, title="夜探密道", characters="林月, 云影")
```

## 快速开始

### 1. 初始化数据库

```bash
# 在小说项目目录下创建
python scripts/fact-db.py story.db init
```

建议在小说项目目录（而非灵境系统仓库根目录）创建数据库，每个小说项目一个 `.db` 文件。

### 2. 添加事实

```bash
# 角色所在地
python scripts/fact-db.py story.db add-fact \
  --subject 林月 --predicate 所在地 --object 青城山 \
  --valid-from 1 --source 1

# 角色知识状态
python scripts/fact-db.py story.db add-fact \
  --subject 林月 --predicate 知道 --object "密道入口位置" \
  --valid-from 10 --source 10

# 物品归属（带有效期，后来丢了）
python scripts/fact-db.py story.db add-fact \
  --subject 玉佩 --predicate 拥有者 --object 林月 \
  --valid-from 1 --valid-until 15 --source 1
```

### 3. 查询事实

```bash
# 查询某个角色在当前有效的事实
python scripts/fact-db.py story.db get-facts --subject 林月

# 查询某个角色在第5章知道什么
python scripts/fact-db.py story.db get-facts --subject 林月 --chapter 5

# 查询所有"所在地"类型的事实
python scripts/fact-db.py story.db get-facts --predicate 所在地

# 查询多个角色的信息
python scripts/fact-db.py story.db get-facts \
  --character 林月 --character 云影 --chapter 8
```

### 4. 管理伏笔

```bash
# 埋下伏笔
python scripts/fact-db.py story.db add-hook \
  --hook-id "玉佩的秘密" --hook-type 悬念 \
  --start 3 --expected-payoff "揭示林月身世" \
  --notes "玉佩是林月母亲的遗物，内藏地图"

# 推进伏笔
python scripts/fact-db.py story.db advance-hook \
  --hook-id "玉佩的秘密" --chapter 10 --status progressing

# 查看所有活跃伏笔
python scripts/fact-db.py story.db get-hooks --active-only

# 按类型过滤
python scripts/fact-db.py story.db get-hooks --hook-type 伏笔
```

### 5. 管理章节摘要

```bash
# 添加章节摘要
python scripts/fact-db.py story.db add-summary \
  --chapter 5 --title "夜探密道" \
  --characters "林月, 云影, 神秘人" \
  --events "林月在密道中发现玉佩线索" \
  --state-changes "林月得知密道存在→确认玉佩去向" \
  --hook-activity "玉佩的秘密: open→progressing" \
  --mood "紧张, 悬疑" \
  --chapter-type "推进"

# 查看最近3章摘要
python scripts/fact-db.py story.db get-summaries --limit 3

# 按角色筛选
python scripts/fact-db.py story.db get-summaries --character 林月
```

### 6. 导出/导入

```bash
# 导出为 JSON（可跨项目迁移）
python scripts/fact-db.py story.db export --format json

# 导出为 Markdown（供审查阅读）
python scripts/fact-db.py story.db export --format markdown

# 从 JSON 导入
python scripts/fact-db.py story.db import --file backup.json
```

## 在写作流程中使用

### 写作前：加载角色知识

```
1. 查询当前章节之前的角色认知
   → python fact-db.py story.db get-facts --subject 林月 --chapter $CURRENT_CHAPTER

2. 查看活跃伏笔，确保本章节有呼应
   → python fact-db.py story.db get-hooks --active-only

3. 参考上一章摘要保持连续性
   → python fact-db.py story.db get-summaries --limit 1
```

### 写作后：更新数据库

```
1. 添加本章节摘要
   → python fact-db.py story.db add-summary --chapter $CURRENT_CHAPTER ...

2. 新增/更新事实（角色新获得的信息、地点变化等）
   → python fact-db.py story.db add-fact ...

3. 推进或解决伏笔
   → python fact-db.py story.db advance-hook ...
```

### 审查时：一致性校验

```bash
# 1. 检查角色在第N章该知道的信息是否矛盾
python scripts/fact-db.py story.db get-facts --subject 林月 --chapter 15

# 2. 查看所有未回收的伏笔
python scripts/fact-db.py story.db get-hooks --active-only

# 3. 检查某件物品的完整流转历史
python scripts/fact-db.py story.db get-facts --subject 玉佩
```

## 进阶用法

### 事实作废

当角色知道的信息后来被证伪或改变，不是删除事实，而是设置 `valid_until_chapter`：

```bash
# 先查找到事实的 ID
python scripts/fact-db.py story.db get-facts --subject 林月 --predicate 所在地

# 作废（林月第6章后离开了青城山）
python scripts/fact-db.py story.db invalidate-fact --id 1 --chapter 6
```

这样查询第3章时仍然知道林月在青城山，查询第7章时则显示新位置。

### Python API 交互式使用

在脚本或 Python REPL 中直接使用：

```python
from scripts.fact_db import FactDB

db = FactDB("story.db")

# 查询林月在第8章的所有有效事实
facts = db.get_facts(subject="林月", chapter=8)
for f in facts:
    print(f"{f['predicate']}: {f['object']}")

# 获取所有活跃伏笔
hooks = db.get_hooks(active_only=True)

db.close()
```

### 多项目支持

每个小说项目使用独立的 `.db` 文件：

```bash
project_alpha/
└── story.db

project_beta/
└── story.db
```

灵境系统负责人在切换项目时只需指定不同的 `--db` 参数。

## 注意事项

| 场景 | 说明 |
|:-----|:------|
| **数据库在小说项目目录** | `.db` 文件建议放在小说项目目录下，与章节正文并列 |
| **export 做版本备份** | 修改大量事实前先 `export`，以便回滚 |
| **中文角色名（UTF-8）** | 所有字段原生支持中文；Windows 下确保终端编码为 UTF-8 |
| **不修改现有文件** | `fact-db.py` 只新增不修改灵境系统现有文件 |
| **Python 3.8+** | 依赖标准库 `sqlite3`、`json`、`argparse`，无第三方依赖 |

## 参考

- InkOS MemoryDB: `packages/core/src/state/memory-db.ts`（原始 TypeScript 设计参考）
- 灵境系统架构: `CLAUDE.md`

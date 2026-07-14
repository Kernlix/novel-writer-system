---
tags: [知识库, 学习沉淀]
type: reference
description: 通过学习优秀作品沉淀写作技法，持续提升灵境创作能力
updatable: true
---

# 灵境学习系统

> 通过学习不同作品，提炼可复用的写作技法，存入对应知识库。
> 每次学习后将新经验归类归档，灵境的创作能力就会不断进化。

## 两层学习架构

```
用户分享作品
       │
       ▼
  /novel:learn ───→ 6个Agent并行分析
       │                  │
       │            ┌─────┴──────┐
       │            ▼            ▼
       │    Agent专用知识库    通用知识库
       │    (自我提升)        (跨作品复用)
       ▼
   knowledge/    knowledge/learned/
   └── <agent>/learned/ └── <category>/
```

| 层级 | 位置 | 用途 | 更新方式 |
|:----|:-----|:-----|:---------|
| Agent 专用 | `knowledge/<agent>/learned/` | 各Agent从作品学到的技法+自我提升方案 | 通过 `/novel:learn` |
| 通用 | `knowledge/learned/<category>/` | 跨作品可复用的通用写作技法 | 通过 `/novel:learn` 提升 |

## 学习类别

| 类别 | 目录 | 内容说明 |
|:----|:----|:---------|
| ✍️ 写作技法 | `writing-craft/` | 场景描写、节奏控制、对话技巧、叙事结构 |
| 😄 幽默风格 | `humor/` | 幽默手法、反差效果、喜剧节奏、语言包袱 |
| 👤 角色设计 | `character-design/` | 角色设定技巧、有趣的角色原型、人物弧光设计 |
| 📋 情节设计 | `plot-design/` | 情节结构、反转设计、多线叙事、悬疑营造 |
| 🔍 伏笔设定 | `foreshadowing/` | 伏笔埋设技巧、回收节奏、暗示与误导 |

## 学习笔记模板

学习任何作品后，按以下格式记录到 Agent 专属知识库的 `learned/` 目录：

```markdown
---
source: 《作品名》（作者）
learner-agent: writer                          # 学习者
category: scene-construction                   # 技法类别
tags: [技法标签]
learned-date: 2026-06-25
improves: chapter-craft.md                     # 改进的是哪个核心知识文件
improvement-type: technique-add                 # technique-add|technique-refine|perspective-new
upgrade:                                        # [必填] 系统升级目标
  - target: agents/writer-agent.md              # 要升级的系统文件
    type: rule-add                              # rule-add|checklist-add|technique-add|workflow-step|field-add|dimension-add
    location: "质量控制"                         # 在目标文件中的插入位置
    content: "新增规则/检查项的具体内容"            # 要插入的内容
---

# 技法名称

## 原文/原片段

## 技法分析

## 可复用场景

## 自我提升方案

### 对照分析
我目前在这方面是怎么做的？差距在哪里？

### 优化措施
学习后应如何改进？列出具体可执行的操作。

### 应用承诺
下次创作时在什么场景主动应用这个技法？
```

## 学习方式

### 方式一：快速分享（单一片段/技法）
用户分享一段精彩片段 → 负责人分析 → 分类 → 存入 `knowledge/learned/<category>/`

### 方式二：全面学习（完整作品）
用户分享完整作品 → `/novel:learn` → 6个Agent并行分析→提炼→自我提升 → 分别存入各自主管的知识库

## 学习流程

```
阅读作品 → 发现精彩处 → 按模板记录 → 归类存档 → 后续写作中应用
```

每次有新沉淀，直接写入对应目录。灵境系统会在创作时自动加载这些知识库作为参考。

### 本能详情

> 逐章7Agent本能分析，迁移自训练学习库。

| 目录 | 说明 |
|:-----|:------|
| `instinct-details/` | 各卷逐章本能分析文件（95个） |
| `konosuba-v?-gap-analysis-report.md` | V5-V9缺口分析报告（5份） |

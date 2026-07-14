---
id: multi-agent-learning
name: 部门多agents协作学习 Skill
category: 01-创作技巧
command: /novel:learn
description: 对完整作品进行部门多agents并行分析、提炼、自我提升
created: 2026-06-25
updated: 2026-07-14
---

# 🧠 部门多agents协作学习 Skill

## 命令

`/novel:learn`

## 功能

当用户分享一部完整小说或文学作品时，启动部门多agents并行学习流程。每个 Agent 从专业视角完成**分析 → 提炼 → 自我提升**三层递进，将学到的技法转化为自身能力的提升。

## 参与智能体

| Agent | 分析维度 | 自我提升方向 | 输出目录 |
|:------|:---------|:------------|:---------|
| 写手 (writer) | 场景构建、对话、描写、叙事、文风、去AI化写作——该作品如何写得像人写的 | 改进自己的写作手法 | `knowledge/writer/learned/` |
| 剧情架构师 (plot-architect) | 情节结构、节奏、伏笔、反转 | 优化伏笔管理、节奏控制策略 | `knowledge/plot-architect/learned/` |
| 角色设计师 (character-designer) | 角色原型、弧光、关系 | 完善角色设计方法论 | `knowledge/character-designer/learned/` |
| 世界观架构师 (worldbuilding-architect) | 世界规则、力量体系、地理 | 丰富世界观构建模板 | `knowledge/worldbuilding-architect/learned/` |
| 润色师 (polish) | 文风、语言、去AI化 | 扩充去AI化策略库 | `knowledge/polish/learned/` |
| 设定质检员 (setting-qa) | 设定逻辑、一致性 | 升级检查维度 | `knowledge/setting-qa/learned/` |

## 分析维度说明

每个Agent的分析维度定义了学习时关注的方面，涵盖创作中所有关键环节。各维度说明如下：

| 维度 | 说明 |
|:-----|:-----|
| **场景构建** | 场景切入方式、氛围营造、过渡衔接、环境与角色互动 |
| **对话设计** | 对话节奏、个性化、潜台词、打断/抢话/省略技法 |
| **描写技法** | 感官描写、细节选择、视角控制、动静态描写搭配 |
| **叙事技巧** | 视角切换、时间线处理、信息释放、悬念设置 |
| **文风** | 句式长短搭配、修辞手法、语气色彩、文字密度 |
| **去AI化写作** | 分析该作品的语言为什么感觉"像人写的"而不是AI写的——口语化程度、句式多样性、不完美但真实的表达、角色差异化对话等 |
| **场景构建** | 分析作品的空间布局、感官描写、时间标记如何服务于叙事——空间是否有功能性（战斗/对话/情感分区），感官锚点是否形成记忆点 |
| **文风语言** | 分析作品的句式选择、角色对话差异化、去AI化表达——长短句搭配是否自然，角色说话方式是否不同，叙事节奏是否得当 |

## 工作流程

```
用户分享完整作品 → /novel:learn
  │
  ├─ 第1步：负责人构建学习上下文
  │   ├── 识别作品信息（类型、篇幅、风格）
  │   ├── 为每个Agent构建学习-适配提示词
  │   └── 加载各Agent现有知识库作为"当前能力基线"
  │
  ├─ 第2步：并行分派 6 个 Agent ← 核心步骤
  │   └── 每个Agent完成三轮递进：
  │       ① 分析：找出作品中值得学的技法（3-5个）
  │       ② 提炼：抽象为可复用方法论
  │       ③ 自我提升：对照自身 → 制定优化方案
  │
  ├─ 第3步：负责人收集、去重、整合
  │   ├── 合并重叠技法
  │   ├── 检查是否与已有知识重复
  │   ├── 提取每个Agent的"自我提升方案"
  │   └── 生成学习总结报告
  │
  ├─ 第4步：用户确认
  │   ├── 展示每个技法+提升方案
  │   └── 确认写入
  │
  └─ 第5步：写入知识库 + 自我更新
      ├── 技法笔记 → knowledge/<agent>/learned/
      ├── 通用技法提升 → knowledge/learned/<category>/
      ├── 自我提升方案 → 标注在笔记中
      └── 记录到 skill-self-improvement.md
```

## 学习-适配提示词模板

负责人在分派时，为每个 Agent 动态构建提示词。以下是通用模板结构：

### 写手智能体 适配示例

```
你正在学习一部优秀作品《作品名》的写作技法。

【角色】
你是灵境系统的写手智能体，专精场景构建、对话设计和描写技法。

【当前能力基线】
你的现有知识库位于 knowledge/writer/chapter-craft.md，内容如下：
（此处插入现有知识库摘要）

【任务】
对这部作品进行三轮递进学习：

第1轮 — 分析：
从写手视角识别 3-5 个值得学习的技法。
分析维度：场景构建、对话设计、描写技法、叙事技巧、语言风格、去AI化写作
对每个技法，摘录原文片段并分析为什么有效。

第2轮 — 提炼：
将每个技法抽象为可复用的方法论。
- 核心原理是什么？
- 适用于什么类型的小说或场景？
- 与灵境当前做法有何异同？

第3轮 — 自我提升：
对照自身能力，制定优化方案。
- 我目前在这方面的做法和不足？
- 学习后如何改进？（具体可执行的操作）
- 下次写作时在哪些场景主动应用？

第4轮 — 系统升级（必做！）：
对每个技法，指定它应该升级灵境系统的哪个文件。
- 这个技法应该成为哪条写作规则？→ 升级 writer-agent.md
- 这个技法应该成为哪个检查项？→ 升级 post-all-check.md
- 这个技法应该成为哪个新技法章节？→ 升级 chapter-writing.md
- 填写 upgrade 字段：target（目标文件）、type（升级类型）、location（插入位置）、content（具体内容）

【输出格式】
为每个技法输出一个结构化学习笔记，每个笔记独立成文件：

---
source: 《作品名》(作者)
learner-agent: writer
category: scene-construction | dialogue | description | narrative | language | style | anti-ai-writing
tags: [标签1, 标签2]
learned-date: 2026-06-25
improves: chapter-craft.md
improvement-type: technique-add | technique-refine | perspective-new
---

# 技法名称

## 原文/原片段

## 技法分析

## 可复用场景

## 自我提升方案

### 对照分析

### 优化措施

### 应用承诺
```

### 其他Agent适配差异

| Agent | 分析维度 | 参考的现有知识库 | 自我提升方向 |
|:------|:---------|:----------------|:------------|
| writer | 场景/对话/描写/叙事/文风/去AI化写作 | chapter-craft.md + anti-ai-polish.md | 去AI化写作技法扩充 |
| plot-architect | 情节结构、节奏、伏笔、反转 | `arc-management.md` | 伏笔管理策略优化 |
| character-designer | 角色原型、弧光、关系 | `character-evolution.md` | 角色设计方法论完善 |
| worldbuilding-architect | 世界规则、力量体系、地理 | `world-rules.md` | 世界观构建模板丰富 |
| polish | 文风、语言、去AI化 | `ai-detection-signals.md` | 去AI化策略库扩充 |
| setting-qa | 设定逻辑、一致性检查 | `logic-consistency.md` 等 | 检查维度升级 |

## 学习笔记格式

```yaml
---
source: 《作品名》(作者)
learner-agent: writer                          # 学习者
category: scene-construction                   # 技法类别
tags: [场景过渡, 氛围烘托]
learned-date: 2026-06-25
improves: chapter-craft.md                     # 改进的是哪个核心知识文件
improvement-type: technique-add                 # technique-add | technique-refine | perspective-new
upgrade:                                        # 【必填】系统升级目标
  - target: agents/writer-agent.md              # 要升级的系统文件
    type: rule-add                              # rule-add | checklist-add | technique-add | workflow-step | field-add | dimension-add
    location: "质量控制"                         # 在目标文件中的插入位置
    content: "新增规则描述或检查项内容"             # 要插入的具体内容
---

# 技法名称

## 原文/原片段

（摘录或描述原作的精彩片段）

## 技法分析

这段写得好在哪里？核心原理是什么？

## 可复用场景

这个技法适用于什么类型的小说或写作场景？

## 自我提升方案

### 对照分析

我目前在这方面是怎么做的？差距在哪里？

### 优化措施

学习后应如何改进？列出具体可执行的操作。

### 应用承诺

下次写作时，在什么场景主动应用这个技法？
```

## 去重规则

| 重叠类型 | 处理方式 |
|:---------|:---------|
| 多Agent识别同一技法 | 合并为一个笔记，标注多个分析视角 |
| 相同技法不同角度 | 保留各角度优势，取精华整合 |
| 与已有 knowledge/learned/ 内容重复 | 标记为"已有记录"，跳过 |

## 通用提升规则

| 判断条件 | 操作 |
|:---------|:-----|
| 技法不绑定具体作品，可跨作品复用 | → 同时写入 `knowledge/learned/<category>/` |
| 技法与某个 Agent 强绑定 | → 仅写入 `knowledge/<agent>/learned/` |
| 不确定时 | → 问自己：换一本书，这个技法的分析逻辑还能用吗？ |

## 与 `/novel:style-learn` 的区别

| 维度 | `/novel:style-learn` | `/novel:learn` |
|:-----|:---------------------|:---------------|
| 分析者 | 负责人独自完成 | 6 个专业智能体并行 |
| 深度 | 表面风格特征（6维度） | 深层技法提取+应用指南+自我提升 |
| 输出 | 风格配置文件 | 学习笔记写入各自知识库 |
| 自我提升 | 无 | 有：对照分析+优化措施+应用承诺 |

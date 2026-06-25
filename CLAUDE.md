# Claude Code 配置 — 灵境小说创作系统

## 设计原则

- **窄核心，宽边缘** — 核心子系统精简稳定，能力通过 Skills、Hooks、Plugins 扩展
- **最小侵入递增** — 新功能优先走：修改 Skill → 新增 Hook → 新增 Agent → 新增 Plugin 阶梯
- **技能自改进** — Skills 在使用后自动记录效果反馈，积累优化经验
- **多模型路由** — 创意写作用最优模型，结构审查用强逻辑模型，摘要用快速模型

## 项目架构

### 系统路径（灵境核心）
`D:\allproject\GitHub项目\novel-writer-system\`
- `agents/` — 10个智能体
- `skills/` — 创作技能库（6个分类）
- `hooks/` — 自动触发钩子
- `.rag/` — 向量检索数据库
- `.store-system/` — 审查报告存档
- `.era-knowledge/` — 时代背景知识库
- `CLAUDE.md` — 系统配置文件

### 内容路径（全部小说文件）
`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\`
- `章节/` — 正文（63章，写入位置）
- `人物/` — 角色档案
- `大纲/` — 总纲、卷纲、章纲
- `设定集/` — 世界观、力量体系等
- `章节摘要/` — 每章摘要
- `审查报告/` — 审查记录

## 灵境创作系统

### 快速启动
| 关键词 | 功能 |
|------|------|
| `/novel:start` | 🚀 启动创作向导 |
| `/novel:help` | 📖 显示完整命令列表 |
| `/novel:qa` | 🔬 设定质检——检查设定合理性 |

### 智能体系统
完整注册表见 `agents/REGISTRY.md`

| id | 名称 | 类型 | emoji | 职责 | 调用方式 |
|:---|:-----|:-----|:------|:-----|:---------|
| orchestrator | **总指挥** | dispatcher | 🧠 | 任务分发、流程编排、质量把关 | 自动激活 |
| writer | **写手** | dispatcher | ✍️ | 正文写作、场景描写、对话 | Agent(prompt=...) |
| reviewer | **审查官** | dispatcher | 🔍 | 一致性检查、质量评估、逻辑校验 | Agent(prompt=...) |
| character-designer | **角色设计师** | dispatcher | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| plot-architect | **剧情架构师** | dispatcher | 📖 | 大纲规划、分卷、情节设计 | Agent(prompt=...) |
| story-setup | **创作设定** | user | 🏗️ | 世界观+角色+剧情一体化设定 | `/novel:world /novel:characters /novel:outline` |
| polish | **润色师** | user | 🎨 | 去AI化、文风统一、语言优化 | `/novel:anti-ai` |
| short-story | **短故事专项** | user | ⚡ | 中短篇快速创作→投稿全流程 | `/novel:short` |
| era-consistency | **时代审查官** | user | 🏛️ | 技术/知识合理性审查 | `/novel:era` |
| setting-qa | **设定质检员** | user | 🔬 | 设定逻辑质检、矛盾发现、合理性验证 | `/novel:qa` |

### 组件注册表

系统采用**元数据驱动 + 注册表索引**模式。每个组件类型在各自目录下有 `REGISTRY.md` 作为索引：

| 组件类型 | 注册表位置 | 数量 |
|:---------|:-----------|:----:|
| 智能体 (Agent) | `agents/REGISTRY.md` | 10 |
| 技能 (Skill) | `skills/REGISTRY.md` | 33 |
| 钩子 (Hook) | `hooks/REGISTRY.md` | 9 |

新增组件时：创建文件 → 添加标准 frontmatter → 在对应 REGISTRY.md 注册。

### Hooks 索引

完整注册表见 `hooks/REGISTRY.md`

| id | stage | phase | 文件 |
|:---|:------|:------|:-----|
| pre-write | pre | write | hooks/pre-write.md |
| post-write | post | write | hooks/post-write.md |
| post-all-check | post | write | hooks/post-all-check.md |
| pre-review | pre | review | hooks/pre-review.md |
| post-review | post | review | hooks/post-review.md |
| pre-archive | pre | archive | hooks/pre-archive.md |
| post-archive | post | archive | hooks/post-archive.md |
| pre-discuss | pre | discuss | hooks/pre-discuss.md |
| session-init | session | session | hooks/session-init.md |

### Skills 索引

完整注册表见 `skills/REGISTRY.md`

| 类别 | 数量 | 涵盖内容 |
|:----|:----:|:---------|
| 00-创作全流程 | 10 | 初始化→讨论→世界观→角色→大纲→写作→审查→润色→存档→短故事 |
| 01-创作技巧 | 6 | 剧情引爆、解耦写作、Save the Cat、雪花法、风格学习、多智能体学习 |
| 02-网文专项 | 4 | 金手指、投稿、趋势、悬疑写作 |
| 03-质量审查 | 5 | 一致性、时代审查、漏洞检测、设定质检 |
| 04-工具集成 | 7 | 知识图谱、记忆系统、Obsidian同步、进度追踪、RAG搜索、DOCX发布、番茄发布 |
| 05-系统机制 | 1 | 技能自改进 |

### 知识库架构（通用 vs 专项分离）

**通用知识（灵境系统内 `knowledge/`）——所有小说共享：**
- `knowledge/punctuation-guide.md` — 标点符号用法规范
- `knowledge/writing-craft-enhanced.md` — 写作技法大全（含基础+进阶）
- `knowledge/genre-templates.md` — 类型小说模板
- `knowledge/knowledge-architecture-and-classification.md` — 知识库架构与分类规则
- `knowledge/learning/` — **灵境学习系统（持续进化）**
  - `writing-craft/` — 从优秀作品学习的写作技法
  - `humor/` — 幽默风格技巧
  - `character-design/` — 角色设定技法
  - `plot-design/` — 情节设计技法
  - `foreshadowing/` — 伏笔设定技法

**Agent 专用知识库（`agents/knowledge/`）——各 Agent 赖以生存的核心本领：**
- `agents/knowledge/writer/chapter-craft.md` — 写手：章节构建、场景、对话技法
- `agents/knowledge/reviewer/review-standards.md` — 审查官：审查标准、错误拦截
- `agents/knowledge/character-designer/character-evolution.md` — 角色设计师：角色状态管理
- `agents/knowledge/plot-architect/arc-management.md` — 剧情架构师：伏笔管理、节奏控制
- `agents/knowledge/story-setup/setup-standards.md` — 创作设定：角色/剧情/世界观协调指南（已整合原世界观架构师知识）
- `agents/knowledge/polish/ai-detection-signals.md` — 润色师：AI痕迹检测与去AI化策略
- `agents/knowledge/short-story/short-story-craft.md` — 短故事专项：短故事结构与平台适配
- `agents/knowledge/era-consistency/era-check-standards.md` — 时代审查官：技术发展分级与审查标准
- `agents/knowledge/story-setup/setup-standards.md` — 创作设定：角色/剧情/世界观协调指南
- `agents/knowledge/setting-qa/logic-consistency.md` — 设定质检员：逻辑自洽性检查
- `agents/knowledge/setting-qa/power-balance.md` — 设定质检员：力量平衡检查
- `agents/knowledge/setting-qa/timeline-integrity.md` — 设定质检员：时间线完整性检查
- `agents/knowledge/setting-qa/causality-chain.md` — 设定质检员：因果链检查
- `agents/knowledge/setting-qa/resource-economy.md` — 设定质检员：资源经济检查

**专项知识（各小说项目内）——仅当前小说使用：**
- `知识边界/character-knowledge-boundary.md` — 角色知识边界地图
- `大纲/` — 总纲、卷纲、伏笔追踪
- `设定集/` — 世界观、力量体系
- `人物/` — 角色档案

### 知识自动分类规则

每次产生新知识时，按以下原则自动判断归属，无需询问：

| 判断条件 | 归属 |
|:--------|:----|
| 换一本小说还能用？ | → 灵境系统 `knowledge/` |
| 只绑定当前小说剧情/角色？ | → 当前小说项目对应目录 |

详见 `knowledge/knowledge-architecture-and-classification.md`

## 推荐设置
> 思考模式：默认开启（保证准确度）；**仅输出小说正文时关闭**。

## 强制多 Agent 协作规则

每次章节创作必须按以下流程分派任务（详参 agents/orchestrator-agent.md）：

```
pre-write（总指挥自己做）
  → 写手智能体（Agent 调用）→ 产出正文
  → 审查官智能体（Agent 调用）→ 产出审查报告
  → 角色设计师智能体（Agent 调用）→ 产出角色变更
  → 剧情架构师智能体（Agent 调用）→ 产出伏笔更新
  → post-write + post-all-check（总指挥自己做）
```

各智能体 prompt 见 `agents/` 目录。调用方式：
```
Agent(prompt={"从 agents/writer-agent.md 中读取职责和输出格式", "传入上下文包"})
```

## 行为规则
- **输出小说正文时**：关闭思考模式，直接输出纯净文本到 `小说项目/章节/`
- **大纲/设定/人物更新** → 写入 `小说项目/` 对应目录
- **其他场景**（讨论/规划/审查/分析）：思考模式保持开启
- **章节字数**：每章 **2000～4000 字**（仅计中文，不含标点空格数字英文）
- **破折号管控**：正文中尽量减少破折号（——），优先用逗号/句号/冒号替代
- **句号规范**：动作后接感知内容用逗号（他抬头看去，远处有人），不用句号断开；短促心理活动用逗号（他在算，三个月），不用冒号
- **章节末尾**：直接结束，不加"（本章完）"
- **系统术语保密**：评分、面板、任务、成就、腐化值数值等系统内部概念**只能在内心独白或系统提示（【】）中出现**，不得出现在对外对话或对外叙述中
- **修改流程**：修改已有章节也必须走多 Agent 流程（先派审查官分析设定一致性→执行修改→RAG重索引）
- **创作闭环**：每次创作或修改完成后审视 agents/skills/hooks 的可优化点

## 多 Agent 并行调用规则

同一批消息中可并行发送多个 Agent 调用，共享安全检查窗口，防止分类器临时不可用时被拦截：

```python
# 正确：同一批发三个 Agent
Agent(审查官) + Agent(角色设计师) + Agent(剧情架构师)

# 错误：串行等一个回来再发下一个
Agent(审查官) → 等他完成 → Agent(角色设计师)
```

审查官输出的 JSON 文件命名为 `审查报告/chapter_XXX.review.json`，不要使用其他命名格式。

## 进阶机制

- `routines/` — 自动化定时/事件触发流程
- `protocols/model-routing.md` — 多模型路由策略
- `protocols/subagent-isolation.md` — 子智能体隔离（每步独立上下文）
- `protocols/session-branching.md` — 会话分支（What-if 探索）
- `protocols/plugin-architecture.md` — 插件架构（核心功能通过插件扩展）
- `plugins/` — 插件目录（预留）
- `templates/` — 组件创建模板（新增 Agent/Skill/Hook/知识库的模板文件）
- `templates/EXTENDING.md` — 扩展指南（如何新增组件的完整流程）

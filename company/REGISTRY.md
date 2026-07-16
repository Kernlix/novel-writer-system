---
id: company-registry
name: 灵境AI公司注册表
type: company-org
description: 虚拟AI小说创作公司完整组织架构
updated: 2026-06-25
---

# 🏢 灵境AI公司注册表

## 组织架构

```
负责人 (Manager)
├── 写作部门 (Writing Dept)
├── 审核部门 (Review Dept)
├── 学习部门 (Learning Dept)
├── 招募部门 (Recruitment Dept)
└── 知识图书馆 (Knowledge Library)
```

---

## 部门总览

### 负责人部门 (Manager)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| manager | 负责人智能体 | 🏢 | 需求理解、任务分解、部门协调、质量把关 | 自动激活 |
| knowledge-retrieval | 知识检索智能体 | 🔎 | 统一LCM+RAG检索，写作前/审查时提供上下文 | Agent调用 |

**Skills:** `novel-setup`, `novel-discuss`, `archive`, `knowledge-graph`, `memory-system`, `progress-track`, `rag-search`, `knowledge-retrieval`, `obsidian-sync`
**Hooks:** `session-init`, `session-end`, `pre-archive`, `post-archive`, `pre-discuss`

### 写作部门 (Writing)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| writer | 写手智能体 | ✍️ | 正文章节写作、场景描写、对话 | Agent(prompt=...) |
| character-designer | 角色设计师 | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| plot-architect | 剧情架构师 | 📖 | 大纲规划、分卷、情节设计 | Agent(prompt=...) |
| humor-writer | 喜剧写手 | 😂 | 喜剧场景设计、吐槽节奏、缺陷引爆 | Agent(prompt=...) |
| romance-writer | 恋爱写手 | 🤍 | 恋爱喜剧感情线渐进写作、反高潮告白、行动替代告白 | Agent(prompt=...) |
| identity-suspense-writer | 身份悬疑写手 | 🎭 | 秘密身份作为跨章叙事引擎——多重误认、揭露时机管理、信息防火墙 | Agent(prompt=...) |
| pseudo-family-writer | 疑似家族写手 | 👨‍👧 | 非恋爱疑似家族关系——哥哥-妹妹/养父-养女/师徒如父子等疑似亲情动力学 | Agent(prompt=...) |
| skill-matcher | 技法检索Agent | 🧩 | 按章节类型智能匹配技法，输出推荐表 | Agent调用 |
| story-setup | 创作设定 | 🏗️ | 世界观、角色、剧情一体化设定 | `/novel:writing:world` |
| short-story | 短故事专项 | ⚡ | 中短篇快速创作→投稿 | `/novel:writing:short` |
| outline-guardian | 大纲守护者 | 🧭 | 监控章节与大纲一致性，防止偏离主线 | Agent(prompt=...) |

**Skills:** `worldbuilding`, `character-design`, `plot-outline`, `chapter-writing`, `plot-rhythm`, `emotional-arc-design`, `save-the-cat`, `snowflake-method`, `booming-plot`, `decoupled-writing`, `short-story-quick`, `docx-publish`, `webnovel-goldfinger`, `webnovel-submit`, `webnovel-trend`, `webnovel-suspense`, `comedy-scene-design`, `comedic-dialogue`, `defect-comedy-engine`, `comedy-pattern-library`, `comedy-suspension-earned-payoff`, `system-comedy`, `romance-progression`, `romance-anti-climax`, `action-substitute-confession`, `love-triangle-romance`, `isekai-culture-clash`, `masochistic-sacrificial-character`, `demon-contract-reversal`, `anthropomorphic-object-character`, `godhood-dwarfing`, `existential-alliance`, `infiltrator-villain-narrative`, `afterlife-tripartite-narrative`, `ultimate-underdog-showdown`, `theological-depravity-comedy`, `unsentimental-finale`, `pseudo-family`, `identity-suspense`, `memory-erasure-recovery`
**Hooks:** `guard-runtime-write`, `pre-write`, `post-write`

### 审核部门 (Review)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| reviewer | 审查官 | 🔍 | 多维度质量审查（12项审查维度） | Agent(prompt=...) |
| polish | 润色师 | 🎨 | 去AI化（四步流水线：检测→标记→改写→验证）、文风统一、语言优化 | `/novel:review:style` |
| setting-qa | 设定质检员 | 🔬 | 设定逻辑质检、矛盾发现 | `/novel:review:logic` |
| era-consistency | 时代审查官 | 🏛️ | 技术/知识合理性审查 | `/novel:review:era` |
| logic-review | 逻辑审核员 | ⚖️ | 设定矛盾、时间线、因果链 | `/novel:review:logic` |
| style-review | 文风审核员 | ✨ | 文风统一、去AI化、阅读体验 | `/novel:review:style` |
| character-review | 角色审核员 | 🎭 | 人设崩坏、行为合理性 | `/novel:review:character` |
| plot-review | 剧情审核员 | 📊 | 节奏、爽点密度、情绪起伏 | `/novel:review:plot` |

**Skills:** `chapter-review`, `anti-ai-polish`, `consistency-check`, `era-consistency`, `plot-hole-check`, `banned-words`, `setting-qa`, `logic-review`, `style-review`, `character-review`, `plot-review`, `adversarial-review`
**Hooks:** `pre-review`, `post-review`, `adversarial-review`

### 学习部门 (Learning)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| external-study | 外部学习智能体 | 📚 | 学习优秀作品、提取技法 | `/novel:learn:study` |
| internal-analysis | 内部分析智能体 | 📝 | 分析反馈、创作结果、审核报告 | `/novel:learn:analyze` |
| epub-extractor | 电子书提取员 | 📦 | epub/mobi文本提取，按章分块 | Agent调用 |
| evolve-agent | 本能进化Agent | 🧬 | 聚类≥3条同domain本能，进化为正式知识 | 自动触发 |

**Skills:** `multi-agent-learning`, `style-learning`, `skill-self-improvement`, `external-study`, `internal-analysis`, `epub-to-text`, `story-deconstruction`
**Hooks:** `pre-learn`, `post-learn`

### 修错部门 (Debug)

| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| debug-agent | 修错智能体 | 🔧 | 根因分析、修复执行、知识库入库 | 自动激活（pre-commit报错时）/ 用户指派 |
| error-logger-agent | 错误记录智能体 | 📝 | 错误知识库维护、计数同步、条目归档 | 定期（pre-commit时）/ 手动 |
| debug-evolve-agent | 错误进化智能体 | 🧬 | 定期扫描 entries_since_baseline，达到阈值(≥3)后自动进化 | pre-commit时自动扫描 / 手动触发 |

**Skills:** `root-cause-analysis`, `error-entry-standard`
**Hooks:** `pre-debug`, `post-debug`

### 招募部门 (Recruitment)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| gap-analysis | 差距分析智能体 | 🔭 | 分析工作流、Agent质量、系统瓶颈 | `/novel:recruit:gap` |
| job-designer | 岗位设计智能体 | 📋 | 定义新Agent/Skill/Hook需求 | `/novel:recruit:job` |
| skill-engineer | 技能研发智能体 | 🔧 | 设计新Skill（用skill-template） | `/novel:recruit:skill` |
| agent-integrator | 智能体集成智能体 | 🔗 | 配置权限、知识库访问、协作 | `/novel:recruit:integrate` |
| skill-deployer | 技能部署Agent | 🔁 | 学习后自动部署新Skill到写作/审核部门 | 自动触发 |

**Skills:** `recruitment-workflow`
**Hooks:** `pre-recruit`, `post-recruit`

### 知识图书馆 (Knowledge Library)
见 `knowledge/REGISTRY.md`


## 错误知识库

> 系统自省能力——记录每一次错误，防止同类问题。

| 路径 | 用途 |
|:-----|:------|
| `knowledge/errors/entries/` | 每次错误的完整记录 |
| `knowledge/errors/categories/` | 7类根因定义与对策模板 |
| `knowledge/errors/root-causes.json` | 结构化根因数据 |
| `knowledge/errors/README.md` | 库门面+快速索引 |

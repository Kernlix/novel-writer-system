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

**Skills:** `novel-setup`, `novel-discuss`, `archive`, `knowledge-graph`, `memory-system`, `progress-track`, `rag-search`, `obsidian-sync`
**Hooks:** `session-init`, `pre-archive`, `post-archive`, `pre-discuss`

### 写作部门 (Writing)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| writer | 写手智能体 | ✍️ | 正文章节写作、场景描写、对话 | Agent(prompt=...) |
| character-designer | 角色设计师 | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| plot-architect | 剧情架构师 | 📖 | 大纲规划、分卷、情节设计 | Agent(prompt=...) |
| story-setup | 创作设定 | 🏗️ | 世界观、角色、剧情一体化设定 | `/novel:writing:world` |
| short-story | 短故事专项 | ⚡ | 中短篇快速创作→投稿 | `/novel:writing:short` |

**Skills:** `worldbuilding`, `character-design`, `plot-outline`, `chapter-writing`, `short-story-quick`, `booming-plot`, `decoupled-writing`, `save-the-cat`, `snowflake-method`, `webnovel-goldfinger`, `webnovel-submit`, `webnovel-trend`, `webnovel-suspense`, `docx-publish`
**Hooks:** `pre-write`, `post-write`, `post-all-check`

### 审核部门 (Review)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| reviewer | 审查官 | 🔍 | 多维度质量审查（6门禁） | Agent(prompt=...) |
| polish | 润色师 | 🎨 | 去AI化、文风统一、语言优化 | `/novel:review:style` |
| setting-qa | 设定质检员 | 🔬 | 设定逻辑质检、矛盾发现 | `/novel:review:logic` |
| era-consistency | 时代审查官 | 🏛️ | 技术/知识合理性审查 | `/novel:review:era` |
| logic-review | 逻辑审核员 | ⚖️ | 设定矛盾、时间线、因果链 | `/novel:review:logic` |
| style-review | 文风审核员 | ✨ | 文风统一、去AI化、阅读体验 | `/novel:review:style` |
| character-review | 角色审核员 | 🎭 | 人设崩坏、行为合理性 | `/novel:review:character` |
| plot-review | 剧情审核员 | 📊 | 节奏、爽点密度、情绪起伏 | `/novel:review:plot` |

**Skills:** `chapter-review`, `anti-ai-polish`, `consistency-check`, `era-consistency`, `plot-hole-check`, `banned-words`, `setting-qa`, `logic-review`, `style-review`, `character-review`, `plot-review`
**Hooks:** `pre-review`, `post-review`

### 学习部门 (Learning)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| external-study | 外部学习智能体 | 📚 | 学习优秀作品、提取技法 | `/novel:learn:study` |
| internal-analysis | 内部分析智能体 | 📊 | 分析反馈、创作结果、审核报告 | `/novel:learn:analyze` |

**Skills:** `multi-agent-learning`, `style-learning`, `skill-self-improvement`, `external-study`, `internal-analysis`
**Hooks:** `pre-learn`, `post-learn`

### 招募部门 (Recruitment)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| gap-analysis | 差距分析智能体 | 🔎 | 分析工作流、Agent质量、系统瓶颈 | `/novel:recruit:gap` |
| job-designer | 岗位设计智能体 | 📋 | 定义新Agent/Skill/Hook需求 | `/novel:recruit:job` |
| skill-engineer | 技能研发智能体 | 🔧 | 设计新Skill（用skill-template） | `/novel:recruit:skill` |
| agent-integrator | 智能体集成智能体 | 🔗 | 配置权限、知识库访问、协作 | `/novel:recruit:integrate` |

**Skills:** `recruitment-workflow`
**Hooks:** `pre-recruit`, `post-recruit`

### 知识图书馆 (Knowledge Library)
见 `knowledge/REGISTRY.md`

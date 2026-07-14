---
id: knowledge-library
name: 知识图书馆
type: knowledge-index
description: 统一知识库索引——所有小说创作相关知识的分区目录
updated: 2026-06-25
---

# 📚 知识图书馆

> 灵境AI公司的统一知识库。按知识领域分区，各部门Agent可共享阅读。
> 参考 ECC knowledge-ops 的六层知识架构设计。

## 知识分层架构

| 层 | 名称 | 存放内容 | 说明 |
|:-:|:----|:---------|:-----|
| ① | **活跃态** | `大纲/伏笔追踪.md`、`章节/` | 创作中的活跃状态，当前章节、待回收伏笔 |
| ② | **快速记忆** | `memory` 工具 | 跨会话快速上下文（用户偏好、工具配置） |
| ③ | **语义检索** | `.rag/` ChromaDB | 向量库，全文语义搜索 |
| ④ | **知识库** | `knowledge/` | 精选持久知识——通用写作技法、审核标准 |
| ⑤ | **外部存储** | `.rag/lcm.db` | 会话历史持久化 |
| ⑥ | **项目存档** | `小说项目/` | 小说原文、角色档案、设定集（非系统知识） |

> ⚠️ **分层原则：** 活跃态内容不在知识库重复存档；知识库只存"换了小说还用得上"的通用知识。小说专项内容放入项目目录。

## 索引

### 📖 小说理论 (theory/)
| 文件 | 说明 |
|:-----|:------|
| `theory/punctuation-guide.md` | 标点符号用法规范 |
| `theory/writing-craft-enhanced.md` | 写作技法大全（基础+进阶） |
| `theory/genre-templates.md` | 类型小说模板 |
| `theory/architecture-and-classification.md` | 知识库架构与分类规则 |
| `theory/lcm-rag-prompt-templates.md` | LCM+RAG写作提示词模板库（5模板+5功能，适配DeepSeek 1M） |
| `theory/rag-novel-config.md` | 长篇小说RAG配置指南（分块规则/检索参数/场景搭配/部署推荐） |

### ✍️ 写作技法 (writing/)

> 恋爱/感情线写作技法见 `company/writing/skills/`（romance-writer Agent 配套 Skill）

| 文件 | 说明 |
|:-----|:------|
| `writing/chapter-craft.md` | 章节构建、场景、对话技法 |
| `writing/title-design-patterns.md` | **标题设计模式库**（类型库+设计原则+检查清单） |
| `writing/learned/` | 从优秀作品学习的写作技法 |

### 🔍 审核标准 (review/)
| 文件 | 说明 |
|:-----|:------|
| `review/review-standards.md` | 审查标准、错误拦截 |
| `review/ai-detection-signals.md` | AI痕迹检测与去AI化策略 |
| `review/logic-consistency.md` | 逻辑自洽性检查标准 |
| `review/power-balance.md` | 力量平衡检查标准 |
| `review/timeline-integrity.md` | 时间线完整性检查标准 |
| `review/causality-chain.md` | 因果链检查标准 |
| `review/resource-economy.md` | 资源经济检查标准 |
| `review/learned/` | 从外部学习积累的审核技法 |

### 👤 角色设计 (character/)
| 文件 | 说明 |
|:-----|:------|
| `character/character-evolution.md` | 角色状态管理、弧光设计 |
| `character/learned/` | 从外部学习积累的角色技法 |

### 📖 剧情设计 (plot/)
| 文件 | 说明 |
|:-----|:------|
| `plot/arc-management.md` | 伏笔管理、节奏控制 |
| `plot/learned/` | 从外部学习积累的剧情技法 |

### 🌍 世界观 (world/)
| 文件 | 说明 |
|:-----|:------|
| `world/world-rules.md` | 世界观一致性、力量体系 |
| `world/setup-standards.md` | 设定协调指南 |
| `world/learned/` | 从外部学习积累的世界观技法 |

### ⚡ 短故事 (short-story/)
| 文件 | 说明 |
|:-----|:------|
| `short-story/short-story-craft.md` | 短故事结构与平台适配 |

### 🏛️ 时代背景 (era/)
| 文件 | 说明 |
|:-----|:------|
| `era/era-check-standards.md` | 时代审查标准 |
| (其他时代知识文件) | 技术发展分级、穿越者知识可用性 |

### 🧠 学习成果 (learning/)
| 子目录 | 说明 |
|:-------|:------|
| `learning/character-design/` | 从作品学习的角色设计技法 |
| `learning/README.md` | 学习系统总览（含本能模型说明） |
| `learning/instinct-learning-system.md` | 本能学习系统完整文档 |
| `learning/writing-craft/` | 写作技法 |
| `learning/writing-craft/lingjing-v2-experience.md` | 灵境系统第2卷创作经验沉淀（6条核心经验） |
| `learning/humor/` | 幽默风格技巧 |
| `learning/foreshadowing/` | 伏笔设定技法 |

### 🧬 本能库 (instincts/)
| 子目录 | 说明 |
|:-------|:------|
| `instincts/REGISTRY.md` | 本能注册总表 |
| `instincts/project/` | 小说专项本能 |
| `instincts/global/` | 通用本能 |
| `instincts/clusters/` | 本能聚类 |

### 📋 规则库 (rules/)
| 子目录 | 说明 |
|:-------|:------|
| `rules/REGISTRY.md` | 规则索引总表 |
| `rules/common/` | 通用规则（对话/场景/权力关系/自查） |
| `rules/novel/` | 小说专项规则（系统术语保密） |

## 🔧 错误知识库 (errors/)

> 由 `company/debug/` 修错部门管理。

| 路径 | 说明 |
|:-----|:------|
| `errors/README.md` | 库门面+7类根因速查 |
| `errors/root-causes.json` | 结构化根因数据 |
| `errors/entries/` | 每次错误的完整记录（6次历史+持续新增） |
| `errors/categories/` | 7类根因定义与对策模板 |
| `errors/pre-checks/` | 预防脚本（自动进化产出） |
| `errors/learned/` | 固化认知（跨实例提炼的规律） |

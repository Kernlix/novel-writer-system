# 🎭 灵境 · 小说创作智能体系统

> 入口文件 — 加载此文件即启动灵境创作系统。

## 📋 当前项目

**转生深渊领主，我靠种田苟成邪神**
- 章节：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\章节\`（已写 82 章）
- 角色：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\人物\`
- 大纲：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\大纲\`
- 设定：`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\设定集\`

### 快速启动
在 Claude Code 中输入以下任一命令进入工作流：

| 命令 | 功能 |
|------|------|
| `/novel:start` | 🚀 **启动创作向导** — 新建项目或继续已有作品 |
| `/novel:help` | 📖 显示完整命令列表 |

## 🧠 智能体系统

系统包含 10 个专业智能体，分工协作。完整注册表见 `company/REGISTRY.md`：

| 智能体 | 类型 | emoji | 职责 | 调用方式 |
|:-------|:-----|:------|:-----|:---------|
| **负责人** | dispatcher | 🧠 | 任务分发、流程编排、质量把关 | 自动激活 |
| **写手** | dispatcher | ✍️ | 正文写作、场景描写、对话 | Agent(prompt=...) |
| **审查官** | dispatcher | 🔍 | 一致性检查、质量评估、逻辑校验 | Agent(prompt=...) |
| **角色设计师** | dispatcher | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| **剧情架构师** | dispatcher | 📖 | 大纲规划、分卷、情节设计 | Agent(prompt=...) |
| **润色师** | user | 🎨 | 去AI化、文风统一、语言优化 | `/novel:anti-ai` |
| **短故事专项** | user | ⚡ | 中短篇快速创作→投稿全流程 | `/novel:short` |
| **时代审查官** | user | 🏛️ | 技术/知识合理性审查 | `/novel:era` |
| **创作设定** | user | 🏗️ | 世界观+角色+剧情一体化设定 | `/novel:world /novel:characters /novel:outline` |
| **设定质检员** | user | 🔬 | 设定逻辑质检、矛盾发现、合理性验证 | `/novel:qa` |

## 📂 Skills 索引

### 创作全流程
- `company/process/chapter-creation.md` — 章节创作流程
- `company/process/chapter-modify.md` — 章节修改流程
- `SUMMARY.md` — 命令/流程/规则速查
- `knowledge/theory/lcm-rag-prompt-templates.md` — 提示词模板（5模板+5功能）

### 创作技巧
- company/writing/skills/booming-plot.md — 剧情引爆
- company/writing/skills/snowflake-method.md — 雪花法大纲
- company/writing/skills/save-the-cat.md — Save the Cat 节拍表
- company/writing/skills/decoupled-writing.md — 解耦写作法
- company/learning/skills/style-learning.md — 风格学习

### 网文专项
- company/writing/skills/webnovel-suspense.md — 🔥 悬疑惊悚写作指南
- company/writing/skills/webnovel-trend.md — 扫榜/趋势分析
- company/writing/skills/webnovel-goldfinger.md — 金手指设计
- company/writing/skills/webnovel-submit.md — 投稿/平台适配

### 质量审查
- company/review/skills/consistency-check.md — 一致性检查
- company/review/skills/banned-words.md — 违禁词检查
- company/review/skills/plot-hole-check.md — 漏洞检测
- company/review/skills/setting-qa.md — 🔬 设定质检

### 工具集成
- company/manager/skills/knowledge-graph.md — 知识图谱管理
- company/manager/skills/memory-system.md — 记忆系统
- company/manager/skills/progress-track.md — 进度追踪
- company/manager/skills/obsidian-sync.md — Obsidian 同步
- company/writing/skills/docx-publish.md — 🔥 DOCX生成与投稿准备

## 🔄 通用工作流

### 长篇连载模式
1. /novel:discuss    → 讨论创意、确定方向
2. /novel:world      → 搭建世界观
3. /novel:characters → 设计角色
4. /novel:outline    → 规划大纲
5. /novel:qa         → 🔬 设定质检（检查设定合理性）
6. /novel:write      → 逐章写作
7. /novel:review     → 审查修改
8. /novel:anti-ai    → 去AI化
9. /novel:archive    → 更新知识库
     ↻ 重复 6-9

### 短故事参赛模式
1. /novel:short      → 启动短故事专项智能体
2. 概念策划 → 大纲 → 写作（全篇）
3. 审查润色 → DOCX打包 → 投稿发送
     → 一次性完成，全篇完稿后再投稿

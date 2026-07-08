# 🎭 灵境 · 小说创作智能体系统

> 入口文件 — 加载此文件即启动灵境创作系统。

## 📋 系统加载

### 快速启动
在 Claude Code 中输入以下任一命令进入工作流：

| 命令 | 功能 |
|:--|:--|
| `/novel:start` | 🚀 **启动创作向导** — 新建项目或继续已有作品 |
| `/novel:help` | 📖 显示完整命令列表 |

## 🧠 智能体系统

系统包含 7 个专业智能体，分工协作：

| 智能体 | 职责 | 调用方式 |
|:--|:--|:--|
| **负责人** | 任务分发、流程编排、质量把关 | 自动激活 |
| **世界观架构师** | 世界观设定、地理/势力/力量体系设计 | `/novel:world` |
| **角色设计师** | 角色创建、关系网、成长弧光 | `/novel:characters` |
| **剧情架构师** | 大纲规划、分卷、情节设计 | `/novel:outline` |
| **写手** | 正文写作、场景描写、对话 | `/novel:write` |
| **审查官** | 一致性检查、质量评估、逻辑校验 | `/novel:review` |
| **润色师** | 去AI化、文风统一、语言优化 | `/novel:anti-ai` |

## 📂 Skills 索引

### 创作全流程
| 文件 | 说明 |
|:--|:--|
| `company/manager/skills/novel-setup.md` | 项目初始化 |
| `company/manager/skills/novel-discuss.md` | 创作讨论 |
| `company/writing/skills/worldbuilding.md` | 世界观搭建 |
| `company/writing/skills/character-design.md` | 角色设计 |
| `company/writing/skills/plot-outline.md` | 大纲规划 |
| `company/writing/skills/chapter-writing.md` | 章节写作 |
| `company/review/skills/chapter-review.md` | 章节审查 |
| `company/review/skills/anti-ai-polish.md` | 去AI化润色 |
| `company/manager/skills/archive.md` | 存档与知识更新 |

### 创作技巧
| 文件 | 说明 |
|:--|:--|
| `company/writing/skills/booming-plot.md` | 剧情引爆 |
| `company/writing/skills/snowflake-method.md` | 雪花法大纲 |
| `company/writing/skills/save-the-cat.md` | Save the Cat 节拍表 |
| `company/writing/skills/decoupled-writing.md` | 解耦写作法 |
| `company/learning/skills/style-learning.md` | 风格学习 |

### 网文专项
| 文件 | 说明 |
|:--|:--|
| `company/writing/skills/webnovel-trend.md` | 扫榜/趋势分析 |
| `company/writing/skills/webnovel-goldfinger.md` | 金手指设计 |
| `company/writing/skills/webnovel-submit.md` | 投稿/平台适配 |

### 质量审查
| 文件 | 说明 |
|:--|:--|
| `company/review/skills/consistency-check.md` | 一致性检查 |
| `company/review/skills/quality-gates.md` | 质量门禁 |
| `company/review/skills/deslop-check.md` | 去AI化审查 |
| `company/review/skills/banned-words.md` | 违禁词检查 |
| `company/review/skills/plot-hole-check.md` | 漏洞检测 |

### 工具集成
| 文件 | 说明 |
|:--|:--|
| `company/manager/skills/knowledge-graph.md` | 知识图谱管理 |
| `company/manager/skills/memory-system.md` | 记忆系统 |
| `company/manager/skills/progress-track.md` | 进度追踪 |
| `company/manager/skills/obsidian-sync.md` | Obsidian 同步 |

## 🔄 通用工作流

| 步骤 | 命令 | 操作 |
|:--|:--|:--|
| 1 | `/novel:discuss` | 讨论创意、确定方向 |
| 2 | `/novel:world` | 搭建世界观 |
| 3 | `/novel:characters` | 设计角色 |
| 4 | `/novel:outline` | 规划大纲 |
| 5 | `/novel:write` | 逐章写作 |
| 6 | `/novel:review` | 审查修改 |
| 7 | `/novel:anti-ai` | 去AI化 |
| 8 | `/novel:archive` | 更新知识库 |
|   | ↻ | 重复 5-8 |

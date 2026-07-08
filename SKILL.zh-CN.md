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
| `SUMMARY.md` | 命令/流程/规则速查 |
| `company/process/chapter-creation.md` | 章节创作流程 |
| `company/process/chapter-modify.md` | 章节修改流程 |
| `knowledge/theory/lcm-rag-prompt-templates.md` | 提示词模板（5模板+5功能） |

### 检查清单
| 文件 | 说明 |
|:--|:--|
| `knowledge/rules/common/dialogue-quality.md` | 对话质量检查 |
| `knowledge/rules/common/scene-immersion.md` | 场景沉浸感检查 |
| `knowledge/rules/common/power-relationship.md` | 权力关系检查 |
| `knowledge/rules/common/self-check-quickref.md` | 写手自查速查 |
| `knowledge/rules/novel/system-term-secrecy.md` | 系统术语保密规则 |

### 本能学习
| 文件 | 说明 |
|:--|:--|
| `knowledge/learning/instinct-learning-system.md` | 本能学习系统设计 |
| `knowledge/instincts/REGISTRY.md` | 本能注册总表 |

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

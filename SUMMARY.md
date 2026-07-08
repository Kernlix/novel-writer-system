---
tags: [速查, 索引]
---

# 灵境系统速查

> 所有命令、流程、规则的统一入口。

## 快速命令

| 命令 | 用途 | 调用部门 |
|:----|:-----|:---------|
| `/novel:start` | 创作向导 | 负责人 |
| `/novel:write` | 章节写作 | 写手 |
| `/novel:review` | 章节审查 | 审查官 |
| `/novel:learn` | 学习作品 | 学习部门 |
| `/novel:search` | RAG语义搜索 | 知识检索 |
| `/novel:search:deep` | LCM+RAG深度查询 | 知识检索 |
| `/novel:search:volume` | 跨卷LCM历史检索 | 知识检索 |

## 核心流程

| 流程 | 位置 |
|:----|:------|
| 创建新章节 | `company/process/chapter-creation.md` |
| 修改已有章节 | `company/process/chapter-modify.md` |
| 学习进化 | `company/learning/learning-department.md` |

## 规则清单

| 规则 | 位置 | 谁用 |
|:----|:------|:-----|
| 对话质量 | `knowledge/rules/common/dialogue-quality.md` | 写手/审查官 |
| 场景沉浸 | `knowledge/rules/common/scene-immersion.md` | 写手 |
| 权力关系 | `knowledge/rules/common/power-relationship.md` | 写手/审查官 |
| 写手自查速查 | `knowledge/rules/common/self-check-quickref.md` | 写手 |
| 系统术语保密 | `knowledge/rules/novel/system-term-secrecy.md` | 全部 |

## 本能库

| 位置 | 说明 |
|:-----|:------|
| `knowledge/instincts/REGISTRY.md` | 本能注册总表 |
| `knowledge/instincts/global/` | 通用本能 |
| `knowledge/instincts/project/` | 小说专项本能 |
| `knowledge/learning/instinct-learning-system.md` | 本能系统设计文档 |

## 知识库目录

| 位置 | 内容 |
|:-----|:------|
| `knowledge/theory/` | 写作理论（标点/技法/模板） |
| `knowledge/writing/` | 写作技法（章节/场景/标题） |
| `knowledge/review/` | 审查标准 |
| `knowledge/learning/` | 学习成果 |

## 升级日志

每次系统升级后记录到 `.story-system/upgrade-log.md`

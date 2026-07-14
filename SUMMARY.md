---
tags: [速查, 索引]
---

# 灵境系统速查

> 所有命令、流程、规则的统一入口。

## 快速命令

> 本表是灵境系统命令的**唯一权威来源**。其他文件（CLAUDE.md/SKILL.md/README.md）只保留高频入口+跳转链接到此。

### 高频入口

| 命令 | 用途 | 调用部门 |
|:----|:-----|:---------|
| `/novel:start` | 创作向导 | 负责人 |
| `/novel:write` | 章节写作 | 写手 |
| `/novel:review` | 章节审查（= `/novel:review:chapter`） | 审查官 |
| `/novel:learn` | 学习作品 | 学习部门 |
| `/novel:deconstruct` | 📖 拆文学习（四步法） | 学习部门 |
| `/novel:search` | RAG语义搜索 | 知识检索 |
| `/novel:search:deep` | LCM+RAG深度查询 | 知识检索 |
| `/novel:evolve` | 手动触发本能进化 | 进化Agent |

### 部门专项命令

| 命令 | 用途 |
|:----|:-----|
| `/novel:review:chapter` | 全流程审查入口 |
| `/novel:review:logic` | 逻辑/设定审查 |
| `/novel:review:style` | 文风/去AI化审查 |
| `/novel:review:character` | 角色审查 |
| `/novel:review:plot` | 剧情节奏审查 |
| `/novel:review:era` | 时代/技术合理性审查 |
| `/novel:learn:study` | 外部学习(提取技法) |
| `/novel:learn:analyze` | 内部分析(审查报告/反馈) |
| `/novel:deconstruct` | 📖 系统化拆文学习(四步法) |
| `/novel:recruit:gap` | 差距分析(手动触发) |
| `/novel:recruit:job` | 岗位设计 |
| `/novel:recruit:skill` | 技能研发 |
| `/novel:recruit:integrate` | Agent集成 |
| `/novel:writing:world` | 世界观设定 |
| `/novel:writing:short` | 短故事专项 |

> ℹ️ 冒号命名空间（`/novel:<部门>:<操作>`）是完整命令格式；高频入口（`/novel:write`）是别名。完整列表见 `company/REGISTRY.md` 各部门调用方式字段。

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
| `knowledge/learned/instinct-learning-system.md` | 本能系统设计文档 |

## 知识库目录

| 位置 | 内容 |
|:-----|:------|
| `knowledge/theory/` | 写作理论（标点/技法/模板） |
| `knowledge/writing/` | 写作技法（章节/场景/标题/感情线/异世界文化反差） |
| `knowledge/review/` | 审查标准 |
| `knowledge/learned/` | 学习成果 |
| `knowledge/instincts/` | 本能库（持续进化） |

## 新招募（V5学习后）

| 类型 | 名称 | 说明 |
|:-----|:-----|:------|
| Agent | 🤍 **romance-writer** | 恋爱写手——CP感情线四阶段管理 |
| Skill | `romance-progression` | 感情线渐进四阶段模型 |
| Skill | `romance-anti-climax` | 反高潮告白调度 |
| Skill | `action-substitute-confession` | 行动替代告白技法 |
| Skill | `isekai-culture-clash` | 异世界文化反差喜剧 |

> 完整缺口分析见: `训练学习库/素晴小说/analysis/v5-gap-analysis-report.md`
## 喜剧写手 😂

| 类型 | 文件 | 来源 |
|:-----|:------|:----:|
| Agent | `company/writing/humor-writer-agent.md` | 写作部门第4Agent |
| Skill | `comedy-scene-design.md` | V1 反高潮+反差笑点 |
| Skill | `comedic-dialogue.md` | V1 漫才对话+吐槽节奏 |
| Skill | `defect-comedy-engine.md` | V1 缺陷引爆链 |
| Skill | `comedy-pattern-library.md` | V2 9种高级格式 |
| Skill | `system-comedy.md` | V3 体制/法庭喜剧 |
| Skill | `plot-rhythm.md` | V1-3 剧情跌宕/反转/悬念 |
| Skill | `emotional-arc-design.md` | V1-3 人物情感弧线 |
| Skill | `masochistic-sacrificial-character.md` | V7 受虐牺牲型角色心理 |
| Skill | `demon-contract-reversal.md` | V7 恶魔契约反转叙事 |
| Skill | `anthropomorphic-object-character.md` | V8 神器拟人化角色写作 |
| Skill | `godhood-dwarfing.md` | V9 神格矮化学 |

## 升级日志

每次系统升级后记录到 `.project-state/upgrade-log.md`

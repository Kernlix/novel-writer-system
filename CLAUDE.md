# Claude Code 配置 — 灵境小说创作系统

## 设计原则

- **窄核心，宽边缘** — 核心子系统精简稳定，能力通过 Skills、Hooks、Plugins 扩展
- **最小侵入递增** — 新功能优先走：修改 Skill → 新增 Hook → 新增 Agent → 新增 Plugin 阶梯
- **技能自改进** — Skills 在使用后自动记录效果反馈，积累优化经验
- **多模型路由** — 创意写作用最优模型，结构审查用强逻辑模型，摘要用快速模型

## 项目架构

### 系统路径（灵境核心）
`D:\allproject\GitHub项目\novel-writer-system\`
- `company/` — 🏢 **虚拟AI公司**（5个部门 + 知识图书馆）
  - `manager/` — 负责人部门（Agent + Skills + Hooks）
  - `writing/` — 写作部门（Agent + Skills + Hooks）
  - `review/` — 审核部门（Agent + Skills + Hooks）
  - `learning/` — 学习部门（Agent + Skills + Hooks）
  - `recruitment/` — 招募部门（Agent + Skills + Hooks）
  - `knowledge-library/` — 知识图书馆索引
- `knowledge/` — 📚 **知识图书馆**（统一知识库）
- `.rag/` — 🔧 **工具集成**（RAG引擎/分卷管理/Reranker服务/重建脚本）
- `.story-system/` — 章节跟踪与升级记录
- `.store-system/` — 审查报告存档
- `templates/` — 组件创建模板
- `protocols/` — 协议文档
- `CLAUDE.md` — 系统配置文件

### 内容路径（全部小说文件）
`D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\`
- `章节/` — 正文（63章，写入位置）
- `人物/` — 角色档案
- `大纲/` — 总纲、卷纲、章纲
- `设定集/` — 世界观、力量体系等
- `章节摘要/` — 每章摘要
- `审查报告/` — 审查记录
- `.lcm/` — LCM 无损上下文引擎数据库

## 灵境AI公司架构

完整注册表见 `company/REGISTRY.md`

### 负责人部门 (Manager)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| manager | **负责人智能体** | 🏢 | 需求理解、任务分解、部门协调、质量把关 | 自动激活 |

### 写作部门 (Writing)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| writer | **写手智能体** | ✍️ | 正文写作、场景描写、对话 | Agent(prompt=...) |
| character-designer | **角色设计师** | 👤 | 角色创建、关系网、成长弧光 | Agent(prompt=...) |
| plot-architect | **剧情架构师** | 📖 | 大纲规划、分卷、伏笔管理 | Agent(prompt=...) |
| story-setup | **创作设定** | 🏗️ | 世界观+角色+剧情一体化设定 | `/novel:writing:world` |
| short-story | **短故事专项** | ⚡ | 中短篇快速创作→投稿 | `/novel:writing:short` |

### 审核部门 (Review)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| reviewer | **审查官** | 🔍 | 多维质量审查（6门禁） | Agent(prompt=...) |
| polish | **润色师** | 🎨 | 去AI化、文风统一 | `/novel:review:style` |
| setting-qa | **设定质检员** | 🔬 | 设定逻辑质检、矛盾发现 | `/novel:review:logic` |
| era-consistency | **时代审查官** | 🏛️ | 技术/知识合理性审查 | `/novel:review:era` |
| logic-review | **逻辑审核员** | ⚖️ | 设定矛盾、时间线 | `/novel:review:logic` |
| style-review | **文风审核员** | ✨ | 文风统一、去AI化 | `/novel:review:style` |
| character-review | **角色审核员** | 🎭 | 人设崩坏、行为合理性 | `/novel:review:character` |
| plot-review | **剧情审核员** | 📊 | 节奏、爽点密度 | `/novel:review:plot` |

### 学习部门 (Learning)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| external-study | **外部学习** | 📚 | 学习优秀作品、提取技法 | `/novel:learn:study` |
| internal-analysis | **内部分析** | 📊 | 分析反馈、审核报告 | `/novel:learn:analyze` |

### 招募部门 (Recruitment)
| id | 名称 | emoji | 职责 | 调用方式 |
|:---|:-----|:------|:-----|:---------|
| gap-analysis | **差距分析** | 🔎 | 分析系统瓶颈 | `/novel:recruit:gap` |
| job-designer | **岗位设计** | 📋 | 定义新Agent/Skill需求 | `/novel:recruit:job` |
| skill-engineer | **技能研发** | 🔧 | 设计新Skill | `/novel:recruit:skill` |
| agent-integrator | **Agent集成** | 🔗 | 配置权限/协作 | `/novel:recruit:integrate` |

### 快速启动
| 关键词 | 功能 | 部门 |
|:-------|:-----|:------|
| `/novel:start` | 🚀 启动创作向导 | Manager |
| `/novel:help` | 📖 显示完整命令列表 | Manager |
| `/novel:writing:world` | 🌍 世界观搭建 | Writing |
| `/novel:writing:characters` | 👤 角色设计 | Writing |
| `/novel:writing:outline` | 📖 大纲规划 | Writing |
| `/novel:writing:write` | ✍️ 章节写作 | Writing |
| `/novel:writing:short` | ⚡ 短故事创作 | Writing |
| `/novel:review:chapter` | 🔍 章节审查 | Review |
| `/novel:review:style` | 🎨 文风审核/润色 | Review |
| `/novel:review:logic` | 🔬 逻辑/设定审核 | Review |
| `/novel:review:era` | 🏛️ 时代审查 | Review |
| `/novel:review:character` | 🎭 角色审核 | Review |
| `/novel:review:plot` | 📊 剧情审核 | Review |
| `/novel:learn:study` | 📚 学习外部作品 | Learning |
| `/novel:learn:analyze` | 📊 内部分析 | Learning |
| `/novel:recruit:gap` | 🔎 差距分析 | Recruitment |
| `/novel:recruit:job` | 📋 岗位设计 | Recruitment |
| `/novel:recruit:skill` | 🔧 技能研发 | Recruitment |
| `/novel:recruit:integrate` | 🔗 集成新Agent | Recruitment |

## 进化闭环

```
创作 → 审核 → 学习 → 招募 → 升级 → 更强创作
```

每当系统发现能力短板时，通过"学习→升级"或"分析→招募→集成"的闭环不断提升。

### 知识图书馆

统一知识库位于 `knowledge/`，按板块分区。所有部门的Agent均可读取。

| 板块 | 路径 | 内容 |
|:-----|:------|:------|
| 📖 小说理论 | `knowledge/theory/` | 标点规范、写作技法、类型模板 |
| ✍️ 写作技法 | `knowledge/writing/` | 章节构建、场景对话技法 |
| 🔍 审核标准 | `knowledge/review/` | 审查标准、AI检测、逻辑检查 |
| 👤 角色设计 | `knowledge/character/` | 角色状态管理、弧光设计 |
| 📖 剧情设计 | `knowledge/plot/` | 伏笔管理、节奏控制 |
| 🌍 世界观 | `knowledge/world/` | 世界观一致性、力量体系 |
| ⚡ 短故事 | `knowledge/short-story/` | 短故事结构 |
| 🏛️ 时代背景 | `knowledge/era/` | 技术发展分级 |
| 🧠 学习成果 | `knowledge/learning/` | 从优秀作品学习的技法 |

完整索引见 `knowledge/REGISTRY.md`

### 组件注册表

系统采用**元数据驱动 + 注册表索引**模式：

| 组件类型 | 注册表位置 |
|:---------|:-----------|
| 公司架构 (Company) | `company/REGISTRY.md` |
| 知识库 (Knowledge) | `knowledge/REGISTRY.md` |

新增组件时：创建文件 → 添加标准 frontmatter → 在对应 REGISTRY.md 注册。

## LCM 无损上下文引擎（已集成）
LCM 按小说卷号**分卷存储**，每卷独立管理：

```
小说项目/.lcm/
├── 卷1/lcm.db       ← 第1卷《穿越之始》(1-40章)
├── 卷2/lcm.db       ← 第2卷《暗流初涌》(41-81章) ◀ 当前
├── 卷3/lcm.db       ← 第3卷《腐化之影》(待写)
├── 卷4/lcm.db       ← 第4卷《封印之根》(待写)
├── 卷5/lcm.db       ← 第5卷《诸方集结》(待写)
```
分卷管理工具位于系统 `.rag/volume_mgr.py`。

### 分卷命令
| 命令 | 说明 |
|:----|:-----|
| `volume_mgr.py status` | 查看分卷状态 |
| `volume_mgr.py switch N` | 切换至第N卷（归档旧卷） |
| `volume_mgr.py search "Q"` | 跨所有卷检索 LCM 历史 |
| `volume_mgr.py lcm-rag "Q"` | LCM+RAG 协同深度查询 |

### 实用工具
- **`lcm_grep`** — 当前卷会话搜索
- **`lcm_expand`** — 展开摘要
- **`lcm_status`** — LCM 运行状态
- **`.rag/volume_mgr.py`** — 分卷管理 + 跨卷检索 + LCM+RAG 协同查询
- **`RAG 索引`** — 已含 volume 元数据，结果标注卷号

## 推荐设置
> 思考模式：默认开启（保证准确度）；**仅输出小说正文时关闭**。

## 部门多agents协作流程

> ⚠️ 任何内容产出/修改（正文/标题/角色/设定）都必须走完整多Agent流程。

**章节创作流程：**
```
负责人把握大方向 → 派发任务
  → 写作部门（写手+角色+剧情同步协作）
  → 审核部门（全面审查）→ ✅通过 / ❌打回循环
  → 负责人执行更新 + 汇总报告 → 提交用户
```

**标题/内容修改流程：**
```
负责人确定修改范围 → 写手执行修改
  → 审查官审查 → ✅通过 / ❌打回循环
  → 负责人汇总报告 → 提交用户
```

详细流程见 `company/manager/manager-agent.md`

## 行为规则
- **输出小说正文时**：关闭思考模式，直接输出纯净文本到 `小说项目/章节/`
- **大纲/设定/人物更新** → 写入 `小说项目/` 对应目录
- **其他场景**（讨论/规划/审查/分析）：思考模式保持开启
- **章节字数**：每章 **不低于2000字**（仅计中文，不含标点空格数字英文）
- **破折号管控**：正文中尽量减少破折号（——），优先用逗号/句号/冒号替代
- **句号规范**：动作后接感知内容用逗号（他抬头看去，远处有人），不用句号断开；短促心理活动用逗号（他在算，三个月），不用冒号
- **章节末尾**：直接结束，不加"（本章完）"
- **系统术语保密**：评分、面板、任务、成就、腐化值数值等系统内部概念**只能在内心独白或系统提示（【】）中出现**，不得出现在对外对话或对外叙述中
- **修改流程**：修改已有章节也必须走多 Agent 流程（先派审查官分析设定一致性→执行修改→RAG重索引）
- **创作闭环**：每次创作或修改完成后审视 company/agents/skills/hooks 的可优化点

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

- `protocols/model-routing.md` — 多模型路由策略
- `protocols/subagent-isolation.md` — 子智能体隔离（每步独立上下文）
- `protocols/session-branching.md` — 会话分支（What-if 探索）
- `protocols/plugin-architecture.md` — 插件架构（核心功能通过插件扩展）
- `templates/` — 组件创建模板（新增Agent/Skill/Hook的模板文件）

---
id: learning-department
name: 学习部门概览
type: department-readme
department: learning
emoji: 📚
description: 灵境系统学习部门——6个Agent、6个Skill、3个Hook。本能积累→聚类→进化三级管道 + 学习管线（一键自动化） + 知识管线（分析→Skill→注册）
created: 2026-06-25
updated: 2026-07-19
---

# 📚 学习部门 (Learning Department)

## 部门使命
持续提升整个系统的创作能力。通过**本能积累→聚类→进化**的三级学习管道，让每一次创作和审查都自然地沉淀为系统能力。

## 核心架构

```
创作/审查中发现模式
    │
    ▼
本能(Instinct)     ← 原子级，10-20行，一条规则
    │
    ▼ (confidence ≥ 0.7)
聚类(Cluster)       ← 多本能归组
    │
    ▼ (≥3条成熟本能)
进化(Evolve)       ← 转为正式 knowledge/ 文件
    │
    ▼
系统升级           ← 更新 agent/skill/hook
```

## 上下文预算管理机制

### 设计理念

借鉴 InkOS 上下文预算管理理念，确保在有限 Token 预算内高效完成分析任务，避免单次分析膨胀拖垮系统或超限截断导致分析不完整。

### 批次分析 Token 预算上限

| 分析场景 | 预算上限 | 说明 |
|:---------|:---------|:-----|
| 6Agent 并行学习（单批次） | 32K tokens | 每批次包含 6 个 Agent 同步分析，总 Token 消耗（含维度框架 + 分析 + 本能产出） |
| 单 Agent 单轮分析 | 8K tokens | 单个 Agent 在「分析→提炼→沉淀」三轮递进中的一轮最大消耗 |
| knowledge-pipeline 批处理 | 16K tokens | 知识管线扫描 + 技法提取 + Skill 生成的单次最大消耗 |
| 审查官审查批次 | 12K tokens | 单次审查任务（本能重叠检测 + 完整性校验）的最大消耗 |
| 内部本能聚类/进化 | 8K tokens | 单次聚类或进化操作的最大消耗 |

> 预算上限在线程调度层硬编码，不可被 Agent 自身的提示词覆盖。

### 每次 Agent 调用的上下文量控制

| 控制点 | 机制 | 数值 |
|:-------|:-----|:-----|
| 最大输入上下文 | 每次 LLM 调用时，输入上下文（system + 分析材料 + 历史指令）严格限制 | 6K tokens |
| 历史保留窗口 | 只保留当前批次分析材料 + 维度框架摘要，不携带历史批次上下文 | 最近 1 个批次 |
| 分析结果输出上限 | 单次输出的本能条数限制，避免单轮产出过多本能导致质量下降 | ≤ 5 条/轮 |
| 维度框架摘要 | 传入 Agent 前对维度框架进行摘要压缩 | 从原始 ≤ 4K 压缩至 ≤ 1K |
| 本能模板定长 | 每条本能采用定长模板写入，自动裁剪超长描述 | 固定 300 tokens/条 |

### 自动压缩策略

当上下文消耗超过预算阈值的 70% 时，触发自动压缩：

1. **维度框架压缩**：将原始维度框架文档自动摘要为「维度名 + 检查要点（≤3点）」格式
2. **分析材料截断**：按优先级保留材料——维度框架 > 当前分析章节 > 历史本能引用 > 示例文本
3. **本能引用精简**：仅保留当前批次新产出本能的完整内容；旧本能引用只保留 `id + confidence` 摘要
4. **轮次压缩**：在「分析→提炼→沉淀」三轮递进中，若第一轮输出低于预算 50%，后续轮次自动合并为一次输出
5. **中间产物丢弃**：分析过程的中间推理和草稿不再保留到最终输出，仅保留最终本能

> 压缩策略默认开启。若用户明确要求「完整分析模式」，可临时关闭压缩，但批次预算上限不变——超出部分会被最外层截断器丢弃。

### 预算监控

每次分析任务完成后，自动记录 Token 消耗到 `.project-state/context-budget-log.md`：

```json
{
  "task": "6Agent学习批次",
  "batch_id": "learn-20260719-001",
  "budget_limit": 32000,
  "actual_consumption": 28450,
  "compression_triggered": true,
  "compression_ratio": "12.3%",
  "agents": [
    {"name": "写手", "consumption": 5200, "compressed": false},
    {"name": "剧情", "consumption": 6100, "compressed": true},
    {"name": "角色", "consumption": 4800, "compressed": false},
    {"name": "世界观", "consumption": 5500, "compressed": false},
    {"name": "润色", "consumption": 3800, "compressed": false},
    {"name": "质检", "consumption": 3050, "compressed": false}
  ]
}
```

### 违反预算的处理

| 情况 | 处理方式 |
|:----|:---------|
| 单 Agent 调用超限 | 由最外层硬截断器裁剪，截断部分丢弃，Agent 不重试 |
| 批次总预算超限 | 按 Agent 分析优先级降序截断（质检→润色→世界观→角色→剧情→写手，最后者保留） |
| 连续 3 批次超限 | 自动下调批次预算上限 20%，并记录到升级日志 |
| 压缩后仍超限 | 强制进入「快速模式」：维度框架摘要×0.5、本能产出上限降为 3 条/轮 |

## 下属Agent

| Agent | 职责 | 定义文件 |
|:------|:------|:---------|
| external-study-agent | 外部学习：从优秀作品中提取技法，先沉淀为本能再进化 | `external-study-agent.md` |
| internal-analysis-agent | 内部分析：从用户反馈、创作结果、审查报告中提取本能 | `internal-analysis-agent.md` |
| evolve-agent | **本能进化**：将置信度≥0.7的本能聚类、进化为正式知识 | `evolve-agent.md` |
| epub-extractor-agent | epub文本提取 | `epub-extractor-agent.md` |
| knowledge-pipeline-agent | **知识管线**：从分析结果自动提取技法→生成Skill→注册到Agent | `knowledge-pipeline-agent.md` |
| **dimension-framework-agent** | **维度分析**：确定作品类型→选择/设计分析框架→输出维度文档→监督分析一致性 | `dimension-framework-agent.md` |

### 下属Skill

| Skill | 用途 |
|:------|:------|
| `multi-agent-learning` | 6Agent并行学习流程 |
| `external-study` | 外部作品学习 |
| `story-deconstruction` | 拆文四步法（扫榜→拆结构→拆人设→拆节奏） |
| `epub-to-text` | epub文本提取 |
| `style-learning` | 风格学习 |
| `knowledge-pipeline` | 知识管线：分析→技法提炼→Skill生成→Agent注册 |

### 激活检查

> 所有学习产出必须通过「学习产出激活检查」：文件存在→REGISTRY注册→SKILL.md更新→归属Agent引用→writer-agent引用（写作类）→pre-commit验证。**少一项=学习未完成**。

详见 `external-study-agent.md` 的「学习产出激活检查（强制）」章节。

## 本能注册

所有本能必须注册在 `knowledge/instincts/REGISTRY.md` 中。

| 范围 | 路径 | 说明 |
|:----|:-----|:------|
| project（小说专项） | `knowledge/instincts/project/` | 换本小说就用不上 |
| global（通用） | `knowledge/instincts/global/` | 换本小说还用得上 |
| clusters（聚类） | `knowledge/instincts/clusters/` | 多本能归组后 |

详见 `knowledge/learned/instinct-learning-system.md`

## 外部学习强制协作流程

> ⚠️ 强制规则：本流程不可跳过、不可简化。学习完成后没有系统升级 = 流程未完成。
> ⚠️ 当有新的学习Agent加入时，本流程必须同步更新，将其纳入协作。
>
> 🔧 **自动化替代方案**：以下6步流程可通过 `scripts/learning-pipeline.py` 一键启动。
> 使用 `--batch N --chapters N1-N2` 参数自动完成第1步~第6步的任务生成和学习计划更新。
> 详见「自动化学习管线」章节和 `hooks/auto-learn.md`。

```
第0步：epub文本提取（如有epub文件）
  └── 📦 epub提取员：提取文本 → 按章分块 → 格式化输出

第1步：🏢 负责人把握大方向
  ├── 🔧 执行 `company/learning/hooks/pre-learn.md`（确认学习源文件、加载各Agent能力基线）
  ├── 用户提供学习材料
  └── 确认学习目标 + 派发任务

📐 第2步：维度分析框架确定 ⚠️必做
  ├── 🤖 dimension-framework-agent 自动执行
  ├── 分析作品类型 → 选择对应框架
  ├── 确定通用维度（5个）+ 专项维度（根据类型）
  ├── 输出：维度框架文档 → `knowledge/learned/{作品名}/维度框架.md`
  └── 框架锁定后，本作品所有章节分析必须使用同一套维度

📚 第3步：学习部门启动（6个Agent并行分析）⚠️必做
  ├── ✍️ 写手Agent → 场景/对话/叙事技法
  ├── 📖 剧情Agent → 情节/节奏/伏笔
  ├── 👤 角色Agent → 人物/弧光/关系
  ├── 🏗️ 世界观Agent → 设定/力量体系
  ├── 🎨 润色Agent → 文风/语言/去AI化
  └── 🔬 质检Agent → 设定逻辑/一致性

  每个Agent完成三轮递进：
    ① 分析 → ② 提炼 → ③ 沉淀为本能 → ④ 系统升级

🔍 第4步：审查官审查学习成果 ⚠️必做
  ├── 本能之间是否重叠？
  ├── 是否与已有本能重复？→ 合并或升 confidence
  ├── 每个本能是否带有 scope 和 domain 字段？
  ├── ✅ 全部通过 → 进入下一步
  └── ❌ 缺必要字段 → 打回补充

🏢 用户确认 → 注册本能
  ├── project本能 → knowledge/instincts/project/
  ├── global本能　→ knowledge/instincts/global/
  └── 注册到 instincts/REGISTRY.md

⚠️ 强制系统升级（必做，不可跳过）
  ├── 🔧 执行 `company/learning/hooks/post-learn.md`（强制检查清单：upgrade字段/系统文件更新/升级日志）
  ├── 本能进化路径：
  │   ├── 如果有 ≥3 条同 domain 本能且 confidence ≥ 0.7
  │   │    → 进化Agent自动聚类
  │   │    → 生成正式 knowledge/ 文件草稿
  │   │    → 负责人确认后写入
  │   │    → 更新对应 company/skills/hooks 文件
  │   └── 如果不足3条 → 暂存，等更多本能积累
  └── 记录到 .project-state/upgrade-log.md

🏢 负责人汇总报告 → 提交用户
  ├── 📚 学习了什么作品
  ├── 🧬 沉淀了N条本能
  ├── 🔗 聚类了M组（如有）
  ├── ⚙️ 升级了K个系统文件
  └── 📎 升级日志已记录

第5步：自动缺口分析（学习→招募联动）⚠️必做
  ├── gap-analysis Agent 读取本次学习产出的所有 instincts
  ├── ……
  └── 招募阈值规则见 `knowledge/rules/common/recruitment-threshold.md`

第6步：自动部署到写作/审核部门 ⚠️必做
  ├── 🔁 部署Agent读取新建/更新的 Skills
  ├── 按 Skill 的 domain 自动归类
  │   ├── comedy → 更新 humor-writer + skill-matcher
  │   ├── emotional/character → 更新 character-agent + skill-matcher
  │   ├── plot/rhythm → 更新 plot-agent + skill-matcher
  │   └── 所有 Skill → 更新 reviewer + SUMMARY + REGISTRY
  └── 输出部署报告：哪些Agent被更新了

第6b步：知识管线（分析→Skill→注册）⚡可选
  ├── 🔗 knowledge-pipeline 扫描 knowledge/learned/ 分析目录
  ├── 从分析结果中提取可复用技法（≥2维度交叉验证）
  ├── 自动生成 Skill 文件 → 写入 company/<department>/skills/
  ├── 注册到 REGISTRY + writer-agent + skill-matcher
  └── 适用于：批量分析已完成但尚未转化为Skill的存量分析结果
```

## 内部分析流程

```
🏢 负责人接收指令 → 确认分析范围
  ↓
📊 内部分析Agent读取数据
  ├── 用户反馈记录
  ├── 近期审查报告
  └── 创作进度数据
  ↓
📊 输出改良建议 → 以本能形式沉淀
  ├── 有价值的模式 → 创建 instinct 文件
  ├── 需改进的问题 → 创建 instinct 文件（含对比示例）
  └── 已有本能 → 提升 confidence 或补充 obs_count
  ↓
🏢 负责人审阅
  ├── ✅ 采纳 → 注册本能
  └── ❌ 不采纳 → 说明原因
```

## 进化闭环

```
创作 → 审核 → 本能沉淀 → 聚类 → 进化 → 升级 → 创作（下次更强大）
```

每次本能积累都让系统离"自动化学习"更近一步。**没有升级日志 = 学习未完成。**

---

## 🤖 自动化学习管线（新增）

> 🚀 **从「文档驱动」升级为「脚本驱动」** — 学习部门全面自动化。

`scripts/learning-pipeline.py` 将外部学习6步手动流程封装为**一键脚本**。

### 使用方式

```bash
# 启动新批次学习
python scripts/learning-pipeline.py --batch 31 --chapters 291-300

# 查看进行进度
python scripts/learning-pipeline.py --status

# 验证批次完整性
python scripts/learning-pipeline.py --batch 31 --verify

# 标记批次完成
python scripts/learning-pipeline.py --batch 31 --update-plan
```

### 管线自动化流程

```
负责人输入「学习第291-300章」
                    │
                    ▼
┌─ scripts/learning-pipeline.py ──────────────────────┐
│ stage-1: 自动查行号（从源文件提取章节行号范围）        │
│ stage-2: 自动派发3个分析代理（生成任务文件）           │
│ stage-3: 预验证文件完整性（检查已有/缺失文件）         │
│ stage-4: 准备综合分析任务文件                         │
│ stage-5: 准备知识管线任务文件                         │
│ stage-6: 自动更新学习计划（标记 ⏳ 进行中）            │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
          代理A → 代理B → 代理C（并行分析）
                    │
                    ▼
        python learning-pipeline.py --batch 31 --verify
                    │
                    ▼
              综合分析代理
                    │
                    ▼
              知识管线代理
                    │
                    ▼
        python learning-pipeline.py --batch 31 --update-plan
```

### 自动推算能力

| 场景 | 命令 | 行为 |
|:-----|:-----|:-----|
| 指定批次+范围 | `--batch 31 --chapters 291-300` | 完整执行 |
| 自动批次 | `--chapters 291-300`（无 `--batch`） | 从学习计划自动推算批次号 |
| 自动范围 | `--batch 31`（无 `--chapters`） | 按10章/批自动推算章节范围 |
| 最终余量 | `--batch 136 --chapters 1351-1361` | 自动适配不足10章的情况 |

### 对应的钩子

- **`hooks/auto-learn.md`** — 自动化学习管线钩子，定义触发条件和详细流程
- **`hooks/pre-learn.md`** — 学习前准备钩子（已存在）
- **`hooks/post-learn.md`** — 学习后系统升级钩子（已存在）

### 新增文件一览

| 文件 | 用途 |
|:-----|:------|
| `scripts/learning-pipeline.py` | 核心自动化脚本 |
| `company/learning/hooks/auto-learn.md` | 自动化学习管线钩子定义 |

---

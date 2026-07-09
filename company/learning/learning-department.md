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

## 下属Agent

| Agent | 职责 |
|:------|:------|
| external-study-agent | 外部学习：从优秀作品中提取技法，先沉淀为本能再进化 |
| internal-analysis-agent | 内部分析：从用户反馈、创作结果、审查报告中提取本能 |
| evolve-agent | **本能进化**：将置信度≥0.7的本能聚类、进化为正式知识 |

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

```
第0步：epub文本提取（如有epub文件）
  └── 📦 epub提取员：提取文本 → 按章分块 → 格式化输出

第1步：🏢 负责人把握大方向
  ├── 用户提供学习材料
  └── 确认学习目标 + 派发任务

📚 学习部门启动（6个Agent并行分析）
  ├── ✍️ 写手Agent → 场景/对话/叙事技法
  ├── 📖 剧情Agent → 情节/节奏/伏笔
  ├── 👤 角色Agent → 人物/弧光/关系
  ├── 🏗️ 世界观Agent → 设定/力量体系
  ├── 🎨 润色Agent → 文风/语言/去AI化
  └── 🔬 质检Agent → 设定逻辑/一致性

  每个Agent完成三轮递进：
    ① 分析 → ② 提炼 → ③ 沉淀为本能 → ④ 系统升级

  （各Agent产出一组本能，直接进入审查）

🔍 审查官审查学习成果
  ├── 本能之间是否重叠？
  ├── 是否与已有本能重复？→ 合并或升 conficence
  ├── 每个本能是否带有 scope 和 domain 字段？
  ├── ✅ 全部通过 → 进入下一步
  └── ❌ 缺必要字段 → 打回补充

🏢 用户确认 → 注册本能
  ├── project本能 → knowledge/instincts/project/
  ├── global本能　→ knowledge/instincts/global/
  └── 注册到 instincts/REGISTRY.md

⚠️ 强制系统升级（必做，不可跳过）
  ├── 本能进化路径：
  │   ├── 如果有 ≥3 条同 domain 本能且 confidence ≥ 0.7
  │   │    → 进化Agent自动聚类
  │   │    → 生成正式 knowledge/ 文件草稿
  │   │    → 负责人确认后写入
  │   │    → 更新对应 agents/skills/hooks 文件
  │   └── 如果不足3条 → 暂存，等更多本能积累
  └── 记录到 .story-system/upgrade-log.md

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

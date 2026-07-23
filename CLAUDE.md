# 灵境小说创作系统

## 设计原则

- **窄核心，宽边缘** — 核心子系统精简，能力通过 Skills、Hooks 扩展
- **最小侵入递增** — 新功能优先走：修改 Skill → 新增 Hook → 新增 Agent
- **写作上不设限** — 仅输出正文时关闭思考模式；字数不低于2000汉字无上限
- **跨平台** — 路径统一使用相对于仓库根目录的相对路径，兼容 Windows/Linux/macOS

## 项目架构

```
novel-writer-system/            ← 灵境系统（仓库根目录）
├── company/               ← 虚拟AI公司（6部门 + process流程层）
│   ├── manager/           ← 负责人部门
│   ├── writing/           ← 写作部门
│   │   └── skills/        ← 技法库（246个，11分类）
│   │       ├── battle/    ← ⚔️ 战斗/对抗（16个）
│   │       ├── plot/      ← 📖 剧情/结构（39个）
│   │       ├── dialogue/  ← 💬 对话技法（10个）
│   │       ├── horror/    ← 👻 恐怖/悬疑（16个）
│   │       ├── emotion/   ← 💕 情感/恋爱（15个）
│   │       ├── game/      ← ♟️ 博弈/推理（42个）
│   │       ├── character/ ← 👤 角色设计（16个）
│   │       ├── world/     ← 🌍 世界观/超自然（31个）
│   │       ├── comedy/    ← 😂 喜剧技法（10个）
│   │       ├── reversal/  ← 🔄 反转/揭示（24个）
│   │       └── meta/      ← 🔧 工具/技术（29个）
│   ├── review/            ← 审核部门
│   ├── learning/          ← 学习部门
│   ├── debug/             ← 修错部门
│   ├── recruitment/       ← 招募部门
│   ├── process/           ← 章节创作/修改流程
│   └── REGISTRY.md
├── knowledge/             ← 知识图书馆
│   ├── rules/common/      ← 通用规则清单
│   ├── rules/novel/       ← 本小说专项规则
│   ├── theory/            ← 写作理论
│   ├── instincts/         ← 本能库
│   ├── errors/            ← 错误知识库
│   └── learned/           ← 学习产出（逐章分析+综合分析）
├── .rag/                  ← RAG引擎/分卷管理
└── company/REGISTRY.md     ← 完整部门列表
```

## 核心流程

```
负责人把握方向 → 维度分析框架确定 → 写作部门(6Agent并行) → 审查官 → 缺口分析 → 部署
```

详见 `company/learning/learning-department.md`（学习部门6步流程）

## 关键命令

| 命令 | 用途 |
|:----|:------|
| `/novel:write` | 章节写作 |
| `/novel:review` | 章节审查 |
| `/novel:learn` | 学习作品 |
| `/novel:search:deep` | LCM+RAG深度查询 |

> ℹ️ 完整命令表见 `SUMMARY.md`（系统唯一权威来源）

## 快速参考

| 内容 | 位置 |
|:----|:------|
| 写作流程 | `knowledge/rules/common/self-check-quickref.md` |
| 对话规则 | `knowledge/rules/common/dialogue-quality.md` |
| 场景规则 | `knowledge/rules/common/scene-immersion.md` |
| 本能学习 | `knowledge/learned/instinct-learning-system.md` |
| 提示词模板 | `knowledge/theory/lcm-rag-prompt-templates.md` |
| RAG配置 | `knowledge/theory/rag-novel-config.md` |
| 技法检索 | `company/writing/skill-matcher-agent.md` |
| 技法分类 | `company/writing/skills/`（11个子目录） |

# 灵境小说创作系统

## 设计原则

- **窄核心，宽边缘** — 核心子系统精简，能力通过 Skills、Hooks 扩展
- **最小侵入递增** — 新功能优先走：修改 Skill → 新增 Hook → 新增 Agent
- **写作上不设限** — 仅输出正文时关闭思考模式；字数不低于2000汉字无上限

## 项目架构

```
D:\allproject\GitHub项目\novel-writer-system\     ← 灵境系统
├── company/               ← 虚拟AI公司（5部门）
│   ├── manager/           ← 负责人部门
│   ├── writing/           ← 写作部门
│   ├── review/            ← 审核部门
│   ├── learning/          ← 学习部门
│   └── recruitment/       ← 招募部门
├── knowledge/             ← 知识图书馆
│   ├── rules/common/      ← 通用规则清单
│   ├── rules/novel/       ← 本小说专项规则
│   ├── theory/            ← 写作理论
│   └── instincts/         ← 本能库
├── .rag/                  ← RAG引擎/分卷管理
└── company/REGISTRY.md     ← 完整部门列表

D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\  ← 小说文件
```

## 核心流程

```
负责人把握方向 → 写作部门(写手+角色+剧情) → 审查官(打回循环) → 负责人汇总报告
```

详见 `company/process/chapter-creation.md`（待拆分）

## 关键命令

| 命令 | 用途 |
|:----|:------|
| `/novel:start` | 创作向导 |
| `/novel:write` | 章节写作 |
| `/novel:review` | 章节审查 |
| `/novel:learn` | 学习作品 |
| `/novel:search` | RAG语义搜索 |

## 快速参考

| 内容 | 位置 |
|:----|:------|
| 写作流程 | `knowledge/rules/common/self-check-quickref.md` |
| 对话规则 | `knowledge/rules/common/dialogue-quality.md` |
| 场景规则 | `knowledge/rules/common/scene-immersion.md` |
| 本能学习 | `knowledge/learning/instinct-learning-system.md` |
| 提示词模板 | `knowledge/theory/lcm-rag-prompt-templates.md` |
| RAG配置 | `knowledge/theory/rag-novel-config.md` |

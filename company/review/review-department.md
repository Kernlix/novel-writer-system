---
id: review-department
name: 审核部门概览
type: department-readme
emoji: 🔍
department: review
description: 灵境系统审核部门——8个Agent、6个Skill、3个Hook
created: 2026-07-17
updated: 2026-07-17
---

# 🔍 审核部门 (Review Department)

## 部门使命
负责所有内容的质量控制，多维度交叉验证。

## 下属Agent
| Agent | 职责 |
|:------|:------|
| reviewer-agent | 多维质量审查（12项审查维度：基础/叙事/角色/情节/语言/一致性） |
| polish-agent | 去AI化、文风统一、语言优化 |
| setting-qa-agent | 设定逻辑质检、矛盾发现、合理性验证 |
| era-consistency-agent | 技术/知识合理性审查、时代背景一致性 |
| logic-review-agent | 专项：设定矛盾、时间线错误、因果链断裂 |
| style-review-agent | 专项：文风统一、AI痕迹检测、阅读体验 |
| character-review-agent | 专项：人设崩坏、行为合理性、成长曲线 |
| plot-review-agent | 专项：节奏问题、爽点密度、情绪起伏 |

## 审核流程
```
写作完成 → 基础审查 (reviewer 12项审查维度)
  → 专项审查 (按需调用 logic/style/character/plot)
  → 润色优化 (polish)
  → 设定质检 (setting-qa)
  → 时代审查 (era-consistency)
  → 报告汇总
```

## 命令
- `/novel:review:chapter` — 全流程章节审查
- `/novel:review:logic` — 逻辑审核
- `/novel:review:style` — 文风审核
- `/novel:review:character` — 角色审核
- `/novel:review:plot` — 剧情审核
- `/novel:review:era` — 时代审查

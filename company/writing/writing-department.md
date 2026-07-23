---
id: writing-department
name: 写作部门概览
type: department-readme
emoji: ✍️
department: writing
description: 灵境系统写作部门——12个写手Agent、48个Skill、3个Hook
created: 2026-06-21
updated: 2026-07-17
---

# ✍️ 写作部门 (Writing Department)

## 部门使命
负责小说创作的所有内容生产环节。

## 下属Agent
| Agent | 职责 |
|:------|:------|
| writer-agent | 正文章节写作、场景描写、对话 |
| character-agent | 角色创建、关系网络、成长弧光跟踪 |
| plot-agent | 大纲规划、分卷、情节设计、伏笔管理 |
| story-setup-agent | 世界观/角色/剧情一体化初始设定 |
| short-story-agent | 中短篇快速创作全流程 |
| humor-writer-agent | 喜剧场景设计、吐槽节奏、缺陷引爆 |
| romance-writer-agent | 恋爱喜剧感情线渐进写作、反高潮告白 |
| identity-suspense-writer-agent | 秘密身份跨章叙事引擎、多重误认、信息防火墙 |
| pseudo-family-writer-agent | 非恋爱疑似家族关系写作 |
| skill-matcher-agent | 按章节类型智能匹配技法，输出推荐表 |
| outline-guardian-agent | 监控章节与大纲一致性，防止偏离主线 |
| timeline-agent | 时间线设计、事件排序、时间矛盾检测 |

## 创作流程
```
世界观搭建 (story-setup)
  → 角色设计 (story-setup / character)
  → 大纲规划 (plot)
  → 章节写作 (writer)
  → 审查 (→ 审核部门)
  → 角色状态更新 (character)
  → 剧情更新 (plot)
```

## 命令
- `/novel:writing:world` — 世界观搭建
- `/novel:writing:characters` — 角色设计
- `/novel:writing:outline` — 大纲规划
- `/novel:writing:write` — 章节写作
- `/novel:writing:short` — 短故事创作

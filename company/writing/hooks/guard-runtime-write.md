---
id: guard-runtime-write
name: 写中防护 hook
hook: guard-runtime-write
department: writing
stage: pre
phase: before-write
runs-on: writer-agent
created: 2026-07-14
updated: 2026-07-14
description: 写正文前检查当前操作是否涉及不该改的文件（设定集/大纲/角色档案），防止误改
---

# 写中防护 Hook

## 检查清单

- [ ] 确定当前写作任务的目标文件路径（章节文件）
- [ ] 检查本次写操作涉及的所有文件，确认**没有任何一个**属于以下分类：
  - `设定集/`（世界观、力量体系、地理、文化设定）
  - `大纲/`（总纲、卷大纲、章纲）
  - `角色/`（角色档案、关系网、成长弧线）
- [ ] 如果发现涉及上述分类文件，**立即终止**并告警：`⚠️ guard-runtime-write 拦截：写操作目标包含受保护文件（设定集/大纲/角色档案），请确认意图`
- [ ] 确认目标仅为合法的章节正文文件（`正文/` 目录下）
- [ ] 记录本次检查通过（供后续审计追踪）

## 保护范围

| 路径 | 保护级别 |
|:-----|:---------|
| `设定集/**/*.md` | 🔒 禁止写入（仅允许 story-setup-agent 通过专用流程修改） |
| `大纲/**/*.md` | 🔒 禁止写入（仅允许 plot-architect 通过流程修改） |
| `角色/**/*.md` | 🔒 禁止写入（仅允许 character-designer 通过流程修改） |
| `正文/**/*.md` | ✅ 允许写入（本次写作的目标范围） |

## 使用

在 writer-agent 写作流程的**第 0 步之前**执行此 hook：检查通过后才进入 pre-write hook → 正常写作流程。

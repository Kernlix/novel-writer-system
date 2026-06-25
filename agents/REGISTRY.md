---
id: agents-registry
name: 智能体注册表
type: registry
description: 所有Agent的索引表——类型、调用方式、知识库映射
updated: 2026-06-25
---

# 智能体注册表 (Agent Registry)

> 总计：10 个智能体（5 个 orchestrator-dispatched，5 个 user-invoked）

## 注册表

| id | 名称 | 类型 | emoji | 调用方式 | 知识库 |
|:---|:-----|:-----|:------|:---------|:-------|
| orchestrator | 总指挥智能体 | orchestrator-dispatched | 🧠 | 自动激活 | (无) |
| writer | 写手智能体 | orchestrator-dispatched | ✍️ | Agent(prompt=...) | agents/knowledge/writer/ |
| reviewer | 审查官智能体 | orchestrator-dispatched | 🔍 | Agent(prompt=...) | agents/knowledge/reviewer/ |
| character-designer | 角色设计师智能体 | orchestrator-dispatched | 👤 | Agent(prompt=...) | agents/knowledge/character-designer/ |
| plot-architect | 剧情架构师智能体 | orchestrator-dispatched | 📖 | Agent(prompt=...) | agents/knowledge/plot-architect/ |
| polish | 润色师智能体 | user-invoked | 🎨 | /novel:anti-ai | agents/knowledge/polish/ |
| short-story | 短故事专项智能体 | user-invoked | ⚡ | /novel:short | agents/knowledge/short-story/ |
| era-consistency | 时代背景审查官智能体 | user-invoked | 🏛️ | /novel:era | agents/knowledge/era-consistency/ |
| setting-qa | 设定质检员智能体 | user-invoked | 🔬 | /novel:qa | agents/knowledge/setting-qa/ |
| story-setup | 创作设定智能体 | user-invoked | 🏗️ | /novel:world /novel:characters /novel:outline | agents/knowledge/story-setup/ |

## 类型说明

- **orchestrator-dispatched**：仅由总指挥通过 `Agent()` 工具调用，不直接与用户对话
- **user-invoked**：用户通过命令或自然语言直接调用

## 添加新智能体

参见 `templates/agent-template.md` 和 `templates/EXTENDING.md`

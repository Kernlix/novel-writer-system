---
id: extending-guide
name: 灵境系统扩展指南
type: guide
updated: 2026-07-09
description: 如何新增 Agent/Skill/Hook/知识库的完整流程。所有路径基于实际 company/ + knowledge/ 结构。
---

# 灵境系统扩展指南

> 所有组件遵循「元数据驱动 + 注册表索引」模式。路径以 `company/<部门>/` 为基础，不再是旧的 `agents/`/`skills/`/`hooks/` 顶层目录。

## 新增 Agent

### 步骤

1. **确定归属部门**：写作部门（writing）/ 审核部门（review）/ 学习部门（learning）/ 招募部门（recruitment）/ 负责人部门（manager）
2. **创建文件**：`company/<部门>/<agent-id>-agent.md`
3. **填写 frontmatter**：`id`、`name`、`type`、`emoji`、`department`、`invocation`、`description`
4. **决定类型**：
   - `orchestrator-dispatched`：由负责人通过 Agent 工具调用，不直接响应用户
   - `user-invoked`：用户通过 `/novel:xxx` 命令直接调用
5. **注册**：在 `company/REGISTRY.md` 对应部门表格中添加一行
6. **更新 CLAUDE.md**（如需）和 `SUMMARY.md`

### 注意事项
- agent-id 使用小写英文，连字符分隔（如 `character-designer`）
- emoji 保持唯一，不要与其他 Agent 重复
- 文件名建议与 agent-id 一致（如 `character-designer-agent.md`），但不强制

## 新增 Skill

### 步骤

1. **放入对应部门的 skills/ 目录**：`company/<部门>/skills/<skill-id>.md`
2. **注册**：在 `company/REGISTRY.md` 对应部门的 **Skills:** 行中添加 skill-id
3. **更新 SUMMARY.md**（如需）的速查表

### 与旧结构的区别
- ❌ 不再使用 `skills/<NN-类别>/` 编号分类文件夹
- ✅ 现在按部门组织：`company/writing/skills/`、`company/learning/skills/` 等
- ✅ 所有 Skill 的注册入口统一为 `company/REGISTRY.md`

## 新增 Hook

### 步骤

1. **放入对应部门的 hooks/ 目录**：`company/<部门>/hooks/<hook-id>.md`
2. **命名规范**：`<pre|post|session>-<phase>`（如 `pre-write`、`post-review`、`session-init`）
3. **注册**：在 `company/REGISTRY.md` 对应部门的 **Hooks:** 行中添加 hook-id

## 新增知识库

### 通用知识（所有小说共用）
放入 `knowledge/` 对应子目录：

| 目录 | 用途 |
|:----|:-----|
| `knowledge/rules/common/` | 通用规则清单 |
| `knowledge/rules/novel/` | 小说专项规则 |
| `knowledge/theory/` | 写作理论 |
| `knowledge/learned/` | 学习成果 |
| `knowledge/instincts/` | 本能库 |

### 分类原则
**换一本小说还能用的知识 → 放灵境系统；只绑定当前小说的 → 放项目目录。**

## 注册表维护

每新增一个组件，必须在对应位置注册：

| 组件类型 | 注册位置 |
|:---------|:---------|
| Agent | `company/REGISTRY.md` 对应部门表格 |
| Skill | `company/REGISTRY.md` 对应部门 **Skills:** 行 |
| Hook | `company/REGISTRY.md` 对应部门 **Hooks:** 行 |
| 知识库 | `knowledge/REGISTRY.md` |
| 本能 | `knowledge/instincts/REGISTRY.md` |

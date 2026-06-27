---
id: extending-guide
name: 灵境系统扩展指南
type: guide
description: 如何新增 Agent/Skill/Hook/知识库的完整流程
---

# 灵境系统扩展指南

> 本文档说明如何为灵境系统新增组件。所有组件遵循 **"元数据驱动 + 注册表索引"** 模式。

---

## 新增 Agent

### 步骤

1. **复制模板**：`templates/agent-template.md` → `agents/<agent-id>.md`
2. **填写元数据**：参考已有 Agent 的 frontmatter 格式
3. **决定类型**：
   - `orchestrator-dispatched`：由负责人通过 Agent 工具调用，不直接响应
   - `user-invoked`：用户通过 `/novel:xxx` 命令直接调用
4. **创建知识库**：在 `knowledge/<agent-id>/` 下创建初始知识库文件（可空，后续完善）
5. **注册**：在 `agents/REGISTRY.md` 表格中添加一行
6. **更新 CLAUDE.md**：
   - 智能体表格中补上行
   - 架构说明更新 agent 数量
7. **如果是 user-invoked 类型**：还需在 `skills/` 对应目录创建 Skill 文件

### 注意事项
- agent-id 使用小写英文，连字符分隔（如 `character-designer`）
- emoji 保持唯一，不要与其他 Agent 重复
- orchestrator-dispatched 类 Agent 不需要 Skill 文件

---

## 新增 Skill

### 步骤

1. **复制模板**：`templates/skill-template.md` → `skills/<NN-类别>/<skill-id>.md`
2. **放入正确目录**：
   - `00-创作全流程/` — 完整的创作流水线
   - `01-创作技巧/` — 通用写作技法
   - `02-网文专项/` — 网文特定技法
   - `03-质量审查/` — 审查与质量门禁
   - `04-工具集成/` — 工具整合与发布
   - `05-系统机制/` — 系统自改进
3. **注册**：在 `skills/REGISTRY.md` 对应类别下添加一行
4. **更新 CLAUDE.md**（如需）

---

## 新增 Hook

### 步骤

1. **复制模板**：`templates/hook-template.md` → `hooks/<hook-id>.md`
2. **命名规范**：`<pre|post|session>-<phase>`
   - `pre-write`、`post-write`、`pre-review`、`post-review` 等
3. **stage 分类**：
   - `pre` — 执行前的准备工作
   - `post` — 执行后的收尾工作
   - `session` — 会话级别的生命周期管理
4. **phase 分类**：
   - `write` — 创作阶段
   - `review` — 审查阶段
   - `archive` — 存档阶段
   - `discuss` — 讨论阶段
   - `session` — 会话管理
5. **注册**：在 `hooks/REGISTRY.md` 表格中添加一行

---

## 新增知识库

### 通用知识（所有小说共用）

放入 `knowledge/` 对应子目录：

| 目录 | 用途 |
|:----|:-----|
| `knowledge/` 根目录 | 标点、写作技巧、分类规则等 |
| `knowledge/genre/` | 各类型小说通用知识 |
| `knowledge/learning/` | 从优秀作品学习的技法 |

### Agent 专用知识

放入 `knowledge/<agent-id>/` 目录：
- 放在 `knowledge/` 下的知识库只在该 Agent 被调用时加载
- 一个 Agent 可以有多个知识库文件

### 小说专项知识

放入对应小说项目目录：
- `人物/`、`大纲/`、`设定集/` 等

### 分类原则

参见 `knowledge/knowledge-classification.md`：**换一本小说还能用的知识 → 放灵境系统；只绑定当前小说的 → 放项目目录。**

---

## 注册表维护

每新增一个组件，必须在对应的注册表中添加一行：

| 组件类型 | 注册表位置 |
|:---------|:-----------|
| Agent | `agents/REGISTRY.md` |
| Skill | `skills/REGISTRY.md` |
| Hook | `hooks/REGISTRY.md` |

注册表是系统的"电话本"——找组件先查注册表，比翻目录高效。

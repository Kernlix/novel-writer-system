---
id: agent-template
name: 智能体创建模板
type: template
description: 用于创建新的智能体文件，包含标准frontmatter和章节结构
---

# <emoji> <名称> (English Name)

## 元数据

```yaml
---
id: <agent-id>                     # 唯一标识，小写英文，连字符分隔
name: <中文名> (English Name)       # 完整名称
type: orchestrator-dispatched       # orchestrator-dispatched | user-invoked | worker | internal-service | department-manager
emoji: <emoji>                      # 单个表情符号
invocation: <调用方式>              # Agent(prompt=...) 或 /novel:xxx
description: <一行职责说明>          # 最多20字
knowledge-base: knowledge/<agent-id>/  # 对应知识库路径（或 none）
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

## 职责

1. <职责一>
2. <职责二>
3. <职责三>

## 输入

<本智能体接收的输入数据>

## 输出

<本智能体产生的输出数据>

## 输出格式

```<格式>
<示例输出>
```

## 核心能力

<如果是 user-invoked 类型，列出核心能力或命令>

---

> **扩展说明：**
> - 新建 Agent 后，在 `company/REGISTRY.md` 注册表中添加一行
> - 在 `knowledge/` 下创建对应的知识库目录和初始文件
> - 在 CLAUDE.md 的智能体表格中补上行
> - 如果 agent-type 是 user-invoked，还需在 skills/ 中创建对应的 Skill 文件

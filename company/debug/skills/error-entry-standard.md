---
id: error-entry-standard
name: 错误条目写作规范 Skill
skill: error-entry-standard
agent: error-logger-agent
description: 错误条目的标准格式和写作规范
---

# 错误条目写作规范 Skill

## 模板

```markdown
---
id: YYYY-MM-DD_简短描述
category: XX-根因名称
severity: P0/P1/P2
resolved: true/false
---

# [错误] 一句话摘要

## 摘要
发生了什么

## 根因分析
- 类别：属于7类中的哪一类
- 根因：为什么发生

## 对策
怎么修的

## 防复发
怎么防止再犯

## 涉及文件
- 列表

## system_learned
系统从这个错误中学到了什么
```

## 要求
- 摘要不超过50字
- 根因分析要有层次（表层原因→深层原因）
- 对策要可操作（具体命令/步骤）
- 防复发要用自动化手段（脚本检查/grep命令），不依赖人工记忆

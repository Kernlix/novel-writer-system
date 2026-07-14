---
id: 2026-07-14_orphan-hooks
category: 02-声明没实现
severity: P1
resolved: true
---

# [错误] 5个hook文件存在但未被流程引用

## 摘要
pre/post-archive、pre-discuss、session-init、pre-review 共5个hook文件已在 `company/` 下创建，但未被任何流程文档（chapter-creation.md / manager-agent.md / reviewer-agent.md）引用，属于"声明了(文件存在)但没实现(无调用点)"。

## 根因分析
- 类别：02-声明没实现
- 根因：创建hook文件时未确保在对应流程文档中添加调用点

## 对策
1. 在 chapter-creation.md 中添加 pre/post-archive、session-init 调用
2. 在 manager-agent.md 中添加 pre-discuss 调用
3. 在 reviewer-agent.md 中添加 pre-review 调用

## 防复发
pre-commit-check.sh 检查项2会检测孤立hook（find所有hook → grep引用数 → 0引用则报错）

## 涉及文件
- company/process/chapter-creation.md
- company/manager/manager-agent.md
- company/review/reviewer-agent.md
- 5个hook文件: pre-archive, post-archive, pre-discuss, session-init, pre-review

## system_learned
新增 02-声明没实现 类别错误记录。
pre-commit-check.sh 已包含检查项2（hooks是否被流程引用），可阻断该类型复发。

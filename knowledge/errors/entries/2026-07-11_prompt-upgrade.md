---
id: 2026-07-11_prompt-upgrade
category: 06-三层不同步
severity: P0
resolved: true
---

# [错误] 审查维度文档12项 vs 真实prompt模板5项——文档/代码/执行三层各版本

## 摘要
审查维度文档12项 vs 真实prompt模板5项——文档/代码/执行三层各版本

## 根因分析
- 类别：06-三层不同步
- 根因：改reviewer-agent.md审查维度没同步改模板2和gates字段

## 对策
同步更新reviewer-agent.md / lcm-rag-prompt-templates.md / gates字段

## 防复发
改文档必改模板→三层对齐

## 涉及文件
（见 consistency-rules.md 历史记录）

## system_learned
新增 06-三层不同步 类别对策模板。
pre-commit-check.sh 已新增对应检查项。

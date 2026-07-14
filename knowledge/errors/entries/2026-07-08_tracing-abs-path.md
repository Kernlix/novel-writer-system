---
id: 2026-07-08_tracing-abs-path
category: 04-路径泄露
severity: P1
resolved: true
---

# [错误] tracing_cli.py和session-init使用绝对路径，导致跨平台不兼容

## 摘要
tracing_cli.py和session-init使用绝对路径，导致跨平台不兼容

## 根因分析
- 类别：04-路径泄露
- 根因：.rag/tracing_cli.py 的 ABS_PROJECT_DIR 是死路径；session-init 也是硬编码

## 对策
改用相对路径 + 占位符替换

## 防复发
改后全局grep绝对路径+用户名

## 涉及文件
（见 consistency-rules.md 历史记录）

## system_learned
新增 04-路径泄露 类别对策模板。
pre-commit-check.sh 已新增对应检查项。

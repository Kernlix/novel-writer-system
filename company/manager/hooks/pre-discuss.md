---
id: pre-discuss
name: 讨论前准备
hook: pre-discuss
stage: pre
phase: before-discussion
department: manager
runs-on: discuss-trigger
description: 创作讨论前汇总当前章节状态、审查报告、待决议题
---

# 讨论前准备

## 执行步骤

1. 读取最近一次审查报告，提取待决议题
2. 汇总当前章节的伏笔回收状态（从 `大纲/伏笔追踪.md`）
3. 列出需要负责人决策的事项（角色走向/剧情分叉/设定矛盾）
4. 输出讨论议程摘要供负责人审阅

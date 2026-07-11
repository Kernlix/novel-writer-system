---
id: pre-review
name: 审查前准备
hook: pre-review
stage: pre
phase: before-review
department: review
runs-on: review-trigger
description: 审查开始前加载当前章节的全套参考数据（角色档案/大纲/伏笔/设定）
---

# 审查前准备

## 执行步骤

1. 搜索相关知识库：`lcm-rag "第N章 关键词" --caller reviewer`
2. 加载涉及角色的最新档案（`人物/` 目录）
3. 核对当卷大纲中本章的预期内容
4. 从 `大纲/伏笔追踪.md` 提取应在本章推进/回收的伏笔
5. 输出审查参考清单供审查官使用

---
id: post-review
name: 审查后处理钩子
hook: post-review
stage: post
phase: review
runs-on: after-review
description: 审查后记录更新
created: 2026-06-21
updated: 2026-06-25
---

# 审查后处理钩子

## 触发时机
章节审查完成后自动触发。

## 执行流程
1. 保存审查报告到 `审查报告/`
2. 将审查结果记录到 RAG（标记已审查章节）
3. 如有需要修改的问题项，生成修改建议清单

---
id: post-review
name: 审查后归档
hook: post-review
stage: post
phase: after-review
department: review
runs-on: review-complete
description: 审查完成后归档报告、更新进度、通知负责人审查结果
---

# 审查后归档

## 执行步骤

1. 将审查报告保存到 `审查报告/` 目录（格式：`第N章-审查报告.md`）
2. 更新 `.project-state/progress.md` 标记该章审查状态
3. 如审查通过 → 通知负责人，章节可定稿
4. 如审查打回 → 通知负责人打回原因，附修复建议
5. 更新 `大纲/伏笔追踪.md` 中本章的伏笔状态变更

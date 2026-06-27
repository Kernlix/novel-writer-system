---
id: pre-archive
name: 存档前验证钩子
hook: pre-archive
stage: pre
phase: archive
runs-on: before-archive
description: 存档前验证章节完整性和一致性
created: 2026-06-21
updated: 2026-06-25
---

# 存档前验证钩子

## 触发时机
执行 `/novel:archive` 前自动触发。

## 执行流程
1. 验证章节字数在目标范围内
2. 检查角色状态是否已更新
3. 检查伏笔使用记录
4. 确认前章摘要已生成

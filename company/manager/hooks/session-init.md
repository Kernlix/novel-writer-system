---
id: session-init
name: 会话初始化钩子
hook: session-init
stage: session
phase: session
runs-on: session-start
description: 会话初始化
created: 2026-06-21
updated: 2026-06-25
---

# 会话初始化钩子

## 触发时机
每次启动 Claude Code 进入项目目录时自动触发。

## 执行流程
1. 检测项目结构完整性
2. 恢复上次会话状态（检查点）
3. 加载当前进度（已完成章节、当前章节）
4. 检查待处理的审查/修改任务
5. 提示待处理事项

## 输出
- 项目状态摘要
- 待办事项列表
- 上次会话的上下文

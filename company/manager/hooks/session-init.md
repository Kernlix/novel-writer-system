---
id: session-init
name: 会话初始化
hook: session-init
stage: pre
phase: before-session
department: manager
runs-on: session-start
description: 新会话开始时初始化项目上下文，检查工作目录和文件状态
---

# 会话初始化

## 触发时机

每次新会话（/new 或首次启动）时自动执行。

## 执行步骤

1. 检查工作目录是否指向正确的项目路径
2. 确认 `D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神\` 目录存在
3. 读取 `大纲/总纲.md` 和当前卷大纲，确认创作上下文
4. 检查 `.project-state/progress.md` 了解当前进度
5. 输出会话就绪摘要（当前卷/章/待办）

---
id: session-end
name: 会话结束清理 hook
hook: session-end
department: manager
stage: post
phase: after-session
runs-on: manager-agent
created: 2026-07-14
updated: 2026-07-14
description: 会话结束时自动压缩上下文、清理临时数据
---

# 会话结束清理 Hook

## 触发时机

每次会话结束（用户退出、`/novel:stop`、或超时自动结束）时执行。

## 执行步骤

1. **上下文归档** — 将当前会话的关键状态写入 `.project-state/session-archive.md`
   - 当前卷/章进度
   - 本次会话完成的决策和变更摘要
   - 待办事项列表（续写时需要恢复的上下文）
2. **清理临时文件** — 删除本次会话生成的临时数据
   - `.rag/tmp/` 下的临时检索缓存（超过 1 小时的）
   - 临时草稿文件（`/tmp/novel-*`）
3. **压缩记忆** — 将本次会话产生的关键决策写入记忆系统
   - 写入 `company/manager/skills/memory-system.md` 定义的短期记忆存储
   - 标记重要决策和约定，供下次会话恢复
4. **会话摘要** — 输出会话结束报告
   - 本次会话工作内容摘要
   - 剩余待办事项
   - 下次启动建议

## 归档格式

```markdown
## 会话存档: YYYY-MM-DD HH:mm

### 状态
- 当前卷: XX
- 当前章: 第 XX 章 - 标题
- 进度: N/M 场景

### 关键决策
- ...

### 待办
- [ ] ...
```

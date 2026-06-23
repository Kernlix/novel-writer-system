# ⏰ 创作自动化（Routines）

## 功能
定时/事件触发的自动化创作任务。

## 使用方法
```
cron create "<schedule>" --prompt "<task>" --skills "<skills>" --deliver <platform>
```

## 内置 Routine

### 1. 每日审查 @daily
```bash
cron create "0 8 * * *" \
  --prompt "审查昨天的章节。检查：角色一致性、情节漏洞、节奏分析。输出简要报告。" \
  --skills "03-质量审查/consistency-check, 03-质量审查/deslop-check" \
  --deliver local
```

### 2. 每周进度报告 @weekly
```bash
cron create "0 9 * * 1" \
  --prompt "统计上周写作进度。对比大纲进度、字数统计、角色状态变更。输出周报。" \
  --skills "04-工具集成/progress-track" \
  --deliver local
```

### 3. RAG 索引更新 @on-change
```bash
hook subscribe chapter-save \
  --events "archive" \
  --prompt "执行 RAG 索引更新：将新章节编入向量数据库。" \
  --skills "04-工具集成/rag-search" \
  --deliver local
```

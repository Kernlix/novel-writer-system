# 🔧 修错部门 (Debug Department)

> 系统出了问题有人管。

## 职责

| Agent | 职责 |
|:------|:------|
| 🔧 debug-agent | 修错智能体：收到错误信号→查库→分析→修复→入库 |
| 📝 error-logger-agent | 错误记录智能体：日常维护错误知识库完整性 |
| 🧬 debug-evolve-agent | 错误进化智能体：扫描 entries_since_baseline 达阈值后自动进化 |

## 值班主任制
默认由 debug-agent 值班。

## 工作流

```
错误发生
  ↓ 读取上下文
  ↓ 查 knowledge/errors/categories/ 匹配同类
  ↓ 查 knowledge/errors/entries/ 查已有方案
  ↓ hooks/pre-debug（自查清单）
  ↓ 根因分析 → 分类 → 修复
  ↓ 验证（pre-commit-check.sh）
  ↓ hooks/post-debug（自动录入知识库）
  ↓ 关闭
```

## 引用

- 根因分析: `skills/root-cause-analysis.md`
- 条目规范: `skills/error-entry-standard.md`
- 修错前: `hooks/pre-debug.md`
- 修错后: `hooks/post-debug.md`
- 错误知识库: `knowledge/errors/`

---
id: post-write
name: 写后自动质检 hook
hook: post-write
department: writing
stage: post
phase: after-writing
runs-on: writer-agent
created: 2026-07-14
updated: 2026-07-14
description: 写完后自动基础质检（检查字数达标、无元引用、无破折号超标）
---

# 写后自动质检 Hook

## 质检清单

- [ ] **字数达标**：正文（不含 frontmatter）汉字数 ≥ 2000
- [ ] **无元引用**：正文不含 `（本章完）`、`（未完待续）`、`作者注`、`PS` 等元文字
- [ ] **破折号不超标**：连续破折号不超过 4 个（规范为 —— 或 ————）
- [ ] **标点规范**：引号成对、省略号 `……` 为 2 个字符（非 `。。。`）
- [ ] **去AI味检查**：执行 `anti-ai-polish` skill（四步流水线：检测→标记→改写→验证），P0问题（AI高频词/完美排比/对话过完整/叙述客观化）必须解决，P1/P2记录到报告中
- [ ] 以上任一未通过 → 返回写手修改后再提交

---
id: pre-debug
name: 修错前自查 hook
hook: pre-debug
department: debug
stage: before-fix
phase: preparation
runs-on: debug-agent
created: 2026-07-14
updated: 2026-07-14
description: 修错开始前——查同类+确认可复现
---

# 修错前自查 Hook

## 检查清单

- [ ] 错误现象可复现
- [ ] `knowledge/errors/entries/` 是否有同类错误？
      - 有 → 读取已有对策作为参考
      - 无 → 准备新建 entry
- [ ] `knowledge/errors/categories/` 哪类最匹配？
- [ ] 记录修错开始时间

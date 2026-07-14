---
id: post-debug
name: 修错后入库 hook
hook: post-debug
department: debug
description: 修复完成后——自动录入知识库+更新计数+验证
---

# 修错后入库 Hook

## 检查清单

- [ ] 修复经验证通过（跑 pre-commit-check.sh）
- [ ] 创建了 entry 文件到 `knowledge/errors/entries/`
- [ ] 更新了 `knowledge/errors/root-causes.json` 计数
- [ ] 如有新根因 → 创建新的 `categories/` 文件
- [ ] memory/SOUL.md 已同步

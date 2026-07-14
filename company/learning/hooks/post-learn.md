---
id: post-learn
name: 学习后系统升级钩子
hook: post-learn
stage: post
phase: learn
department: learning
runs-on: after-learning
description: 强制系统升级——将学习成果写入company/skills/hooks
severity: blocking
created: 2026-06-25
---

# 学习后系统升级钩子

> ⚠️ 本钩子为强制步骤。没有执行系统升级 = 学习流程未完成。

## 强制检查清单
- [ ] 每个学习笔记的 upgrade 字段已填写
- [ ] 缺失 upgrade 字段的笔记已退回去补充
- [ ] 升级已应用到目标 company/skills/hooks 文件
- [ ] 升级日志已写入 `.project-state/upgrade-log.md`
- [ ] **Skill激活检查已通过**——新创建的Skill已通过 `external-study-agent.md` 中的「学习产出激活检查」（含 writer-agent.md 注册、REGISTRY 更新、pre-commit-check 通过）

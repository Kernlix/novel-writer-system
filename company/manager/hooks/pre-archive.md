---
id: pre-archive
name: 归档前检查
hook: pre-archive
stage: pre
phase: before-archive
department: manager
runs-on: archive-trigger
description: 第N卷完结归档前，检查所有章节文件、审查报告、角色档案已完整
---

# 卷归档前检查

## 执行步骤

1. 遍历当前卷所有章节文件，确认无缺失
2. 检查每章审查报告均已存档
3. 确认角色变化已回写到人物/ 目录
4. 更新 `.project-state/progress.md` 标记卷完成
5. 调用 `volume_mgr.py archive` 归档LCM数据库

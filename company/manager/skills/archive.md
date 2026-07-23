---
id: archive
name: 项目归档
type: skill
agent: manager
description: 项目归档流程——压缩上下文、保存状态、清理临时文件
---

# 项目归档 Skill

## 触发条件
章节/卷完成、会话结束、用户要求归档时。

## 流程
1. 执行 `company/manager/hooks/pre-archive.md` — 备份当前状态
2. 汇总本阶段创作成果（章节、审查报告、本能记录）
3. 压缩会话上下文为摘要
4. 清理临时文件和中间产物
5. 执行 `company/manager/hooks/post-archive.md` — 校验归档完整性
6. 更新项目进度记录

## 输出
- 归档摘要
- 进度更新
- 临时文件清理确认

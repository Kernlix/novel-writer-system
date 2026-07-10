---
id: external-study-skill
name: 外部学习 Skill
department: learning
command: /novel:learn:study
description: 对优秀作品进行多Agent并行分析学习，强制升级系统
---

# 📚 外部学习 Skill

## 命令
`/novel:learn:study`

## 功能
学习外部作品，提取技法，强制升级系统。封装了原有的 multi-agent-learning 工作流。

## 工作流程

> ⚠️ 强制规则：本流程不可跳过、不可简化。没有系统升级 = 学习未完成。

1. 负责人把握大方向 → 派发任务给学习部门
2. 分派6个Agent并行分析（写手/剧情/角色/世界观/润色/质检）
   - 每个Agent完成三轮递进：分析→提炼→自我提升→填写upgrade字段
3. 审查官审查：技法重叠检查 + upgrade字段完整性检查
4. ✅ 通过 → 用户确认 → 写入知识图书馆
5. ❌ 缺upgrade字段 → 打回补充 → 循环直到完整
6. **强制系统升级**：根据upgrade字段写入对应agents/skills/hooks
7. 记录升级日志到 `.project-state/upgrade-log.md`
8. 负责人汇总报告 → 提交用户

## 输出
- 技法笔记 → `knowledge/<dept>/learned/`
- 系统升级 → 对应agents/skills/hooks文件
- 升级日志 → `.project-state/upgrade-log.md`

---
id: novel-discuss
name: 创作讨论
type: skill
agent: manager
description: 创作讨论流程——汇总当前状态、组织多Agent会商、形成决策
---

# 创作讨论 Skill

## 触发条件
用户发起创作方向讨论、情节选择、风格决策等需要多角度分析的议题时。

## 流程
1. 执行 `company/manager/hooks/pre-discuss.md` 汇总当前状态
2. 提炼讨论焦点，明确需要哪些Agent参与
3. 派发讨论任务到相关部门（写作/审核/学习）
4. 汇总各方意见，形成对比分析
5. 提出推荐方案，由用户最终决定

## 输出
- 多角度分析报告
- 推荐方案 + 理由
- 用户决策记录

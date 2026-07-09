---
tags: [规则, 招募, 阈值]
scope: common
---

# 招募触发阈值规则

> 决定什么时候该新增 Agent/Skill，什么时候只需扩充已有能力。

## 核心阈值

| 条件 | 行动 |
|:----|:-----|
| 同 domain ≥3 条无覆盖 instinct | 🔴 自动触发招募部门 |
| 同 domain 1-2 条无覆盖 instinct | 🟡 扩充已有 Skill 的覆盖范围 |
| 全部 instinct 已被已有 Agent/Skill 覆盖 | 🟢 跳过，不触发 |

## 新增 Agent 的判断标准

满足以下**全部三条**，才走招募流程创建新 Agent：

1. **domain 独立**：该 domain 无法被划入现有任何 Agent 的职责范围
2. **instinct 充足**：同 domain ≥3 条本能需要此能力支撑
3. **频次够高**：该 domain 的能力在创作中会高频使用（不是一次性的）

## 新增 Skill 的判断标准

以下情况创建新 Skill，不创建 Agent：

- domain 可归属已有 Agent（如"搞笑对话"归写手Agent）
- instinct 数量不足 (1-2条)
- 该能力是对已有 Agent 的**增强**而非**独立职能**

## 新增部门的判断标准

以下情况才考虑新增部门：

- 该领域的能力需求跨越 ≥2 个现有部门的边界
- 需要一套完整的 Agent+Skill+Hook 体系支撑
- 现有部门无法通过增加 Agent 解决

## 示例

| 场景 | 判断 |
|:-----|:-----|
| 学到 4 条喜剧技法 instinct，现有润色师只做去AI化 | 🔴 新增 humor-writer Agent |
| 学到 1 条缺陷设计 instinct，character-agent 已有角色弧光 Skill | 🟡 扩充角色Skill |
| 学到 5 条对话 instinct，writer-agent 已有对话质量 checklist | 🟢 无需招募（已覆盖） |
| 学到 3 条配音/广播剧相关 instinct | 🔴 可能需新增"音频制作部门" |

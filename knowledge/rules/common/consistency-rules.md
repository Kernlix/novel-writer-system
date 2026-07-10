---
tags: [规则, 维护, 一致性]
scope: common
---

# 系统一致性维护规则

> 防止本次整改暴露的问题再次发生。每次新增/删除/重命名文件时必须遵守。

## 铁律（违反会导致系统逐步腐化）

| # | 规则 | 为什么 |
|:-:|:-----|:-------|
| 1 | **改一个路径 → 搜全仓库引用 → 全部同步** | 跳过引用更新 = 制造断链。改名 agents/ → company/ 后残留旧路径就是前车之鉴 |
| 2 | **新建 Agent/Skill → 必须同时更新 REGISTRY.md + SKILL.md + SKILL.zh-CN.md + SUMMARY.md** | 否则 SKILL.md 号称 10 个 Agent 实际有 26 个 |
| 3 | **声明了 Hook/Skill → 文件必须存在** | 声明 pre-write 但没有 hooks/pre-write.md = 空头支票 |
| 4 | **SUMMARY.md 是命令/规则的唯一权威来源** | 防止 CLAUDE.md/SKILL.md/README.md 各说一套命令 |
| 5 | **company/REGISTRY.md 是 Agent/Skill/Hook 数量的唯一权威来源** | 其他文件只引用 REGISTRY，不自行维护数量 |

## 新增/删除文件后的标准 check-list

```
after_change:
  ✅ 搜全仓库，找到所有引用该路径的文件 → 全部更新
  ✅ 新增 Agent: 更新 REGISTRY + SKILL.md + SKILL.zh-CN.md + SUMMARY.md
  ✅ 新增 Skill: 更新 REGISTRY + SUMMARY.md
  ✅ 删除 Agent/Skill: 同步从上述文件移除条目
  ✅ 改名目录: 搜全仓库引用 → 全部更新 → 确认无残留旧路径
  ✅ Emoji: 与全仓库 26 个 Agent 无重复
  ✅ 命名: 不与已有目录同名（即使在不同层级）
  ✅ 验证: REGISTRY.md 声明的数量 = 实际文件数量
```

## 命名规则

| 规则 | 正确 | 错误 |
|:-----|:----|:----|
| 不同层级不能用同名目录 | `knowledge/learned/` + `company/learning/` ✅ | `knowledge/learning/` + `company/learning/` ❌ |
| 不同目录不能有混淆级名称 | `.review-archive/` + `.project-state/` ✅ | `.store-system/` + `.story-system/` ❌ |
| Emoji 全局唯一 | 26 个 Agent 的 emoji 不重复 | 📊 被两个 Agent 共用 ❌ |
| **验证脚本不得产生误报** | 路径解析基于仓库根目录，不是文件所在目录 | 200个假断链 ❌ |

## 历史教训

- **evolve-agent 缺失**：学习部门文档写了但没人建 → 所有新增声明必须有对应文件
- **EXTENDING.md 路径全过期**：架构重构后忘了更新扩展指南 → 重构时必须同步更新所有指南文件
- **命令表四套并存**：SUMMARY.md / CLAUDE.md / SKILL.md / README 各有各的命令 → 只许一处维护
- **SKILL.md 漏了 15 个 Agent**：加 Agent 后没更新入口文件 → 入口文件 = REGISTRY.md 的快照，必须同步

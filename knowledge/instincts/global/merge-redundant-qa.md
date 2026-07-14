---
id: "dialogue:merge-redundant-qa"
trigger: "角色之间的信息确认型对话"
action: "将多轮一问一答合并为一轮，减少机械式问答节奏"
confidence: 0.8
domain: "dialogue"
scope: "global"
source: "第61章修复经验"
created: 2026-07-06
obs_count: 3
---

## 本能说明

当两个角色在确认已知信息时，多轮一问一答会让对话节奏变慢、显得机械。

- ❌ 「下矿了？」「下了。」「和铁锤一起？」「对。」
- ✅ 「下矿了？和铁锤一起？」「下了。」

## 相关本能

- dialogue:key-line-weight（关键台词要撑住铺垫）

## 进化状态

- [ ] 已聚类（关联本能 /cluster 文件）
- [ ] 已升级（对应 knowledge/ 文件）

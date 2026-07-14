---
tags: [规则, 维护, 一致性]
scope: common
---

# 系统一致性维护规则

> 错误全量记录见 `knowledge/errors/`，本文件仅维护铁律和索引。

## 铁律（违反会导致系统逐步腐化）

| # | 规则 | 为什么 |
|:-:|:-----|:-------|
| **0** | **修复铁律：修错时同步分析根因→分类→写对策→推记忆** | 只修不分析=同一类错误反复犯。六次审计证明：8/11项是v1已知的，因没分析根因而复发 |
| 1 | **改一个路径 → 搜全仓库引用 → 全部同步** | 跳过引用更新 = 制造断链 |
| 2 | **新建 Agent/Skill → 必须同时更新 REGISTRY.md + SKILL.md + SKILL.zh-CN.md + SUMMARY.md** | 否则数字不一致 |
| 3 | **声明了 Hook/Skill → 文件必须存在** | 声明 pre-write 但没有 hooks/pre-write.md = 空头支票 |
| 4 | **SUMMARY.md 是命令/规则的唯一权威来源** | 防止各说一套命令 |
| 5 | **company/REGISTRY.md 是 Agent/Skill/Hook 数量的唯一权威来源** | 其他文件只引用 REGISTRY，不自行维护数量 |

## 错误知识库

完整错误记录 → `knowledge/errors/`

### 7类根因速查

| # | 根因 | 发生次数 | 详情 |
|:-:|:-----|:--------:|:-----|
| 1 | 改了A不改B | 8 | `knowledge/errors/categories/01-改了A不改B.md` |
| 2 | 声明没实现 | 6 | `knowledge/errors/categories/02-声明没实现.md` |
| 3 | 脚本静默失败 | 4 | `knowledge/errors/categories/03-脚本静默失败.md` |
| 4 | 路径泄露 | 4 | `knowledge/errors/categories/04-路径泄露.md` |
| 5 | 创建不验证 | 3 | `knowledge/errors/categories/05-创建不验证.md` |
| 6 | 三层不同步 | 2 | `knowledge/errors/categories/06-三层不同步.md` |
| 7 | 子智能体不闭环 | 2 | `knowledge/errors/categories/07-子智能体不闭环.md` |

### 6次历史审计

> 均已完成修复。每次提交前跑 `scripts/pre-commit-check.sh` 确认。

| # | 时间 | 审计内容 | 根因 | 错误记录 |
|:-:|:----|:---------|:----|:---------|
| v1 | 2026-07-08 | tracing绝对路径 | 路径泄露 | `entries/2026-07-08_tracing-abs-path.md` |
| v2 | 2026-07-08 | 路径迁移残留 | 改了A不改B | `entries/2026-07-08_path-migration.md` |
| v3 | 2026-07-11 | romance-activator | 声明没实现 | `entries/2026-07-11_romance-activator.md` |
| v4 | 2026-07-11 | 提示词三层不同步 | 三层不同步 | `entries/2026-07-11_prompt-upgrade.md` |
| v5 | 2026-07-11 | 批量脚本静默失败 | 脚本静默失败 | `entries/2026-07-11_batch-silent.md` |
| v6 | 2026-07-12 | 最终轮子智能体不闭环 | 子智能体不闭环 | `entries/2026-07-12_v5-patches.md` |

## 新增/删除文件后的标准 check-list

```yaml
after_change:
  ✅ 搜全仓库，找到所有引用该路径的文件 → 全部更新
  ✅ 新增 Agent: 更新 REGISTRY + SKILL.md + SKILL.zh-CN.md + SUMMARY.md
  ✅ 新增 Skill: 更新 REGISTRY + SUMMARY.md
  ✅ 删除 Agent/Skill: 同步从上述文件移除条目
  ✅ 改名目录: 搜全仓库引用 → 全部更新 → 确认无残留旧路径
  ✅ Emoji: 与全仓库 Agent 无重复
  ✅ 命名: 不与已有目录同名（即使在不同层级）
  ✅ 错误是否已录入 knowledge/errors/entries/？
  ✅ root-causes.json 计数已更新？
  ✅ pre-commit-check.sh 有对应自动检查？
  ✅ 记忆已更新？
```

## 命名规则

- Agent 文件：`{name}-agent.md`
- Skill 文件：`{name}.md`（无后缀）
- Hook 文件：`{action}-{event}.md`
- 配置文件：`config.yaml`
- README：`README.md`

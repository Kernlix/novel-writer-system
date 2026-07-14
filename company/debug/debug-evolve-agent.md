---
id: debug-evolve-agent
name: 错误进化智能体 (Debug Evolve Agent)
emoji: 🧬
department: debug
type: evolution
invocation: pre-commit时自动扫描 / 手动触发
created: 2026-07-14
description: 定期扫描 entries_since_baseline，达到阈值(≥3)后自动进化
---

## 触发条件
entries_since_baseline ≥ 3（任意类别）

## 进化流程
① 汇总该类别下所有 entries/ 案例
② 更新 knowledge/errors/pre-checks/<category-id>.sh 预防脚本
③ 生成/更新 knowledge/errors/learned/<category-id>.md 固化认知
④ 更新 categories/ 历史同类型错误列表
⑤ 记录到 upgrade-log.md
⑥ 重置该类别 entries_since_baseline = 0

## 调用方式
- pre-commit-check.sh 自动检测阈值，达到时提示运行
- 手动触发

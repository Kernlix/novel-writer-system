---
id: 2026-07-11_romance-activator
category: 02-声明没实现
severity: P0
resolved: true
---

# [错误] manager-agent.md声明了romance-writer分支但hooks不存在

## 摘要
manager-agent.md声明了romance-writer分支但hooks不存在

## 根因分析
- 类别：02-声明没实现
- 根因：新增Agent时没有checklist确认所有引用点

## 对策
删除未实现的hook配置，统一走REGISTRY注册

## 防复发
声明必须顺带创建文件+pre-commit检查hook存在性

## 涉及文件
（见 consistency-rules.md 历史记录）

## system_learned
新增 02-声明没实现 类别对策模板。
pre-commit-check.sh 已新增对应检查项。

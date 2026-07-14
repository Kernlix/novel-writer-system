---
id: 2026-07-11_batch-silent
category: 03-脚本静默失败
severity: P0
resolved: true
---

# [错误] 批量替换中正则不匹配导致记录静默丢失（REGISTRY误删200条+假断链）

## 摘要
批量替换中正则不匹配导致记录静默丢失（REGISTRY误删200条+假断链）

## 根因分析
- 类别：03-脚本静默失败
- 根因：perl/sed替换失败没报错，数据丢了不知道

## 对策
批量操作加改前/改后计数对比

## 防复发
批量修改三确认：改前计数→改后计数→diff

## 涉及文件
（见 consistency-rules.md 历史记录）

## system_learned
新增 03-脚本静默失败 类别对策模板。
pre-commit-check.sh 已新增对应检查项。

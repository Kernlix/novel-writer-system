---
id: 2026-07-08_path-migration
category: 01-改了A不改B
severity: P1
resolved: true
---

# [错误] agents/重命名为company/后，文档引用未全部更新

## 摘要
agents/重命名为company/后，文档引用未全部更新

## 根因分析
- 类别：01-改了A不改B
- 根因：改名后没搜全仓库引用，旧路径残留

## 对策
mv + 立即grep旧路径，两条命令绑定

## 防复发
路径迁移必带联动搜索

## 涉及文件
（见 consistency-rules.md 历史记录）

## system_learned
新增 01-改了A不改B 类别对策模板。
pre-commit-check.sh 已新增对应检查项。

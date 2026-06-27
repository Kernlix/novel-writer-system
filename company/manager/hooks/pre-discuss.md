---
id: pre-discuss
name: 讨论前检索钩子
hook: pre-discuss
stage: pre
phase: discuss
runs-on: before-discuss
description: 讨论前准备工作
created: 2026-06-21
updated: 2026-06-25
---

# 讨论前检索钩子

## 触发时机
执行 `/novel:discuss` 前自动触发。

## 执行流程
1. 通过 RAG 检索当前讨论主题的相关上下文
2. 查询角色档案、世界观设定、前文摘要
3. 将检索到的参考信息提供给讨论会话

## 输出
RAG 检索到的相关上下文摘要。

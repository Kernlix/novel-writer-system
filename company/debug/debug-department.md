---
id: debug-department
name: 修错部门概览
type: department-readme
emoji: 🔧
department: debug
description: 灵境系统修错部门——3个Agent、2个Skill、2个Hook
created: 2026-07-17
updated: 2026-07-17
---

# 🔧 修错部门 (Debug Department)

> 系统出了问题有人管。

## 部门使命
系统错误的根因分析、修复执行、知识库入库，防止同类错误重复发生。

## 下属Agent
| Agent | 职责 |
|:------|:------|
| debug-agent | 修错智能体：收到错误信号→查库→分析→修复→入库 |
| error-logger-agent | 错误记录智能体：日常维护错误知识库完整性 |
| debug-evolve-agent | 错误进化智能体：扫描 entries_since_baseline 达阈值后自动进化 |

## 下属Skill
| Skill | 用途 |
|:------|:------|
| root-cause-analysis | 根因分析方法论——7类根因定义与对策模板 |
| error-entry-standard | 错误条目标准格式——确保每条记录可追溯、可复用 |

## 下属Hook
| Hook | 触发时机 |
|:-----|:---------|
| pre-debug | 修错前——执行自查清单、加载已有方案 |
| post-debug | 修错后——自动录入知识库、更新计数 |

## 值班主任制
默认由 debug-agent 值班。pre-commit报错时自动激活。

## 工作流
```
错误发生
  → 查 knowledge/errors/categories/ 匹配同类
  → 查 knowledge/errors/entries/ 查已有方案
  → hooks/pre-debug（自查清单）
  → 根因分析 → 分类 → 修复
  → 验证（pre-commit-check.sh）
  → hooks/post-debug（自动录入知识库）
  → 关闭
```

---
id: manager-department
name: 负责人部门概览
type: department-readme
emoji: 🏢
department: manager
description: 灵境系统负责人部门——2个Agent、5个Skill、5个Hook
created: 2026-07-17
updated: 2026-07-17
---

# 🏢 负责人部门 (Manager Department)

## 部门使命
用户（甲方）的唯一对接窗口。负责需求理解、任务分解、部门协调、质量把关。

## 下属Agent
| Agent | 职责 |
|:------|:------|
| manager-agent | 需求理解、任务规划、部门协调、质量把关、战略决策 |
| knowledge-retrieval-agent | 统一LCM+RAG检索，写作前/审查时提供上下文 |

## 下属Skill
| Skill | 用途 |
|:------|:------|
| novel-setup | 新小说项目初始化——目录结构、配置、注册 |
| novel-discuss | 创作讨论——汇总状态、组织多Agent会商 |
| archive | 项目归档——压缩上下文、保存状态、清理临时文件 |
| rag-search | RAG语义搜索——向量检索小说知识库 |
| knowledge-retrieval | 统一知识检索——RAG+LCM+跨卷联合检索 |

## 下属Hook
| Hook | 触发时机 |
|:-----|:---------|
| session-init | 新会话时——初始化会话上下文 |
| session-end | 会话结束时——压缩上下文、清理临时数据 |
| pre-discuss | 创作讨论前——汇总当前状态 |
| pre-archive | 归档前——备份当前状态 |
| post-archive | 归档后——校验归档完整性 |

## 工作流程
```
接收用户指令
  → 理解需求、制定计划
  → 派发到对应部门（写作/审核/学习/招募/修错）
  → 汇总各部门结果
  → 提交用户决策
```

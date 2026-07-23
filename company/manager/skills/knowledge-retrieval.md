---
id: knowledge-retrieval
name: 知识检索
type: skill
agent: manager
description: 统一知识检索——RAG语义搜索 + LCM上下文回溯 + 跨卷历史检索
---

# 知识检索 Skill

## 触发条件
写作前准备、审查时校验、任何Agent需要查证信息时。

## 流程
1. 确定检索范围（当前卷/跨卷/全局）
2. RAG语义搜索：`python3 .rag/volume_mgr.py lcm-rag "查询" --caller <调用者>`
3. LCM上下文回溯：`volume_mgr.py search "关键词"`
4. 合并去重，按相关性排序
5. 返回结构化结果

## 检索策略
- **精确查询**：角色名、地名、具体事件 → 直接搜索
- **模糊查询**：主题、风格、模式 → RAG语义搜索
- **跨卷查询**：历史伏笔、角色发展轨迹 → 多卷联合检索

## 输出
- 结构化知识片段
- 来源文件 + 行号
- 检索时间戳

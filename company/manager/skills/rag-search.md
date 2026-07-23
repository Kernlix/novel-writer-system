---
id: rag-search
name: RAG检索
type: skill
agent: manager
description: RAG语义搜索——调用向量检索引擎查询小说知识库
---

# RAG检索 Skill

## 触发条件
任何Agent需要查询小说设定、角色、情节等上下文信息时。

## 流程
1. 接收查询请求（关键词/自然语言问题）
2. 调用 `.rag/volume_mgr.py lcm-rag "查询内容" --caller <调用者>`
3. 解析返回结果，提取相关片段
4. 按相关性排序，返回Top-N结果

## 常用查询模式
- `lcm-rag "角色名的性格特点"` — 角色信息
- `lcm-rag "第N章涉及的伏笔"` — 伏笔回溯
- `lcm-rag "世界观设定：力量体系"` — 设定查询
- `search "关键词"` — LCM历史回溯

## 输出
- 相关知识片段列表
- 来源文件路径
- 相关性评分

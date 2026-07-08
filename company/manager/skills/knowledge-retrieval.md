---
id: knowledge-retrieval
name: 知识检索专用 Skill
category: 04-工具集成
command: /novel:search:deep
description: 调用知识检索智能体进行 LCM+RAG 协同深度查询
---

# 🔎 知识检索专用 Skill

> 写作前查上下文、审查时核一致性——都通过这个 Skill 调用知识检索智能体。

## 快速命令

```bash
# 切换到工作目录
cd D:\allproject\GitHub项目\novel-writer-system\.rag

# LCM+RAG 协同深度查询（推荐——一次调用同时查RAG全文+LCM会话历史）
PYTHONPATH="" /c/Python314/python.exe volume_mgr.py lcm-rag "你的深度问题"

# 仅RAG语义搜索
PYTHONPATH="" /c/Python314/python.exe query.py --novel "小说项目路径" --rerank "问题"

# 仅跨卷LCM历史检索
PYTHONPATH="" /c/Python314/python.exe volume_mgr.py search "关键词"
```

## 写作前调用示例

写第82章前，写手调用知识检索智能体：

```
→ lcm-rag "第82章需要承接哪些伏笔？深渊裂缝的当前状态"
→ lcm-rag "第2卷末尾封印墙的设定细节"
```

## 审查时调用示例

审查官审查第82章时调用：

```
→ lcm-rag "红袍法师马尔斯第一次登场时的描写细节"
→ lcm-rag "陈默的腐化值变化历程"
→ volume_mgr.py search "封印 设计 讨论"  ← 查之前的创作讨论
```

## 与普通RAG搜索的关系

| 维度 | 普通RAG (`/novel:search`) | 深度检索 (`/novel:search:deep`) |
|:-----|:--------------------------|:-------------------------------|
| 搜索范围 | 当前RAG索引（全文语义） | RAG + 所有卷LCM会话历史 |
| 能看到 | "写了什么" | "写了什么" + "当时怎么讨论决定的" |
| 适合场景 | 快速定位内容 | 深入理解创作决策 |
| 调用方式 | `query.py` | `volume_mgr.py lcm-rag "问题"` |

# 🎯 多模型路由配置

## 概述
不同写作任务使用不同模型，最大化质量与成本比。

## 推荐路由

| 任务 | 推荐模型 | 原因 |
|:--|:--|:--|
| ✍️ 创意写作 | Claude Sonnet | 最佳文笔和创意 |
| 📋 大纲规划 | GPT-4o / Claude | 强结构分析能力 |
| 🔍 审查检查 | Claude Haiku / GPT-4o-mini | 快速且准确 |
| 📝 摘要生成 | Gemini Flash / Claude Haiku | 快速处理 |
| 🤖 RAG 检索 | 本地嵌入模型 | 隐私保护 |
| 🎨 去AI化润色 | Claude Sonnet | 最自然的改写 |

## 配置方法
在 `.env` 或 `config.yaml` 中配置各模型 API Key：
```
PRIMARY_MODEL=claude-sonnet-4-20250514
EDIT_MODEL=gpt-4o
REVIEW_MODEL=claude-haiku-3-5
SUMMARY_MODEL=gemini-2.5-flash
LOCAL_MODEL=ollama/qwen3-embedding:4b
```

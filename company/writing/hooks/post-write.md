---
id: post-write
name: 写作后处理钩子
hook: post-write
stage: post
phase: write
runs-on: after-write
description: 写作后字数验证、破折号审计、RAG重索引
created: 2026-06-21
updated: 2026-06-25
---

# 写作后处理钩子

## 触发时机
每章写作完成后自动触发。

## 执行流程
1. 更新角色状态（能力变化、关系变化、心理状态）
2. 更新进度追踪（已完成章节数、字数统计）
3. 记录本章摘要（写入 `章节摘要/`)
4. 检查伏笔使用情况
5. 更新存档信息

## 字数与破折号一键验证

```python
import re, sys
def validate_chapter(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    body = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)
    chinese = len(re.findall(r'[一-鿿]', body))
    assert 2000 <= chinese <= 4000, f'字数超出范围：{chinese}'
    dashes = body.count('——')  # —— 算一个
    if dashes > 3:
        print(f'⚠️ 破折号过多：{dashes} 处，建议减少')
    print(f'字数：{chinese} | 破折号：{dashes}')
    return chinese, dashes
```

## RAG 快速重索引（仅最新一章）

```python
import sys; sys.path.insert(0, 'D:\\allproject\\GitHub项目\\novel-writer-system\\.rag')
from engine import NovelRAG
rag = NovelRAG(novel_root='D:\\allproject\\小说项目\\转生深渊领主，我靠种田苟成邪神')
rag.reindex_latest_chapter('D:\\allproject\\小说项目\\转生深渊领主，我靠种田苟成邪神\\章节')
print('RAG 最新章节已更新')
```

## 输出
- 角色状态快照
- 进度摘要
- 伏笔使用记录
- 字数验证结果
- 破折号审计结果
- RAG 索引状态

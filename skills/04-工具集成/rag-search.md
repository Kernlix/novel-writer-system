# 🔍 RAG 语义检索 Skill

## 命令
`/novel:search`

## 功能
基于 ChromaDB + Ollama 的语义检索，用自然语言搜索小说全文内容。

## 检索范围

| 集合 | 内容 | 适合查什么 |
|:--|:--|:--|
| `chapters` | 已完成的章节正文 | 情节细节、角色对话、场景描写 |
| `characters` | 人物档案（人物/目录） | 角色设定、能力等级、关系网 |
| `outlines` | 大纲文件（大纲/目录） | 剧情规划、伏笔安排、爽点设计 |
| `settings` | 设定文件（设定集/根目录*.md） | 世界观规则、力量体系、种族设定 |

## 用法

```python
# 从 Python 调用
import sys; sys.path.insert(0, 'D:\\allproject')
from rag.engine import NovelRAG
rag = NovelRAG(novel_root='D:\\allproject\\小说项目\\转生深渊领主，我靠种田苟成邪神')

# 语义搜索全部集合
results = rag.query('深渊裂缝在哪几章出现过', n_results=3)

# 只搜章节
results = rag.query('狼牙血契仪式', kinds=['chapters'], n_results=2)

# 只搜人物档案
results = rag.query('艾琳的等级和能力', kinds=['characters'], n_results=3)
```

## 集成到工作流

### 写作前
```python
# 查之前相关章节的内容，避免重复或矛盾
results = rag.query('黯钢武器的设定', kinds=['chapters', 'settings'], n_results=3)
```

### 审查时
```python
# 查某个设定/伏笔前文是怎么写的
results = rag.query('马尔斯第一次出现', kinds=['chapters'], n_results=2)
```

### 一致性核查
```python
# 查某个概念在不同位置的描述是否一致
results = rag.query('腐化值多少了', kinds=['chapters'], n_results=5)
```

## 与 grep 的对比

| 场景 | grep | RAG |
|:--|:--|:--|
| 精确关键词搜索 | ✅ 准确 | ❌ 可能漏 |
| 模糊语义搜索 | ❌ 要猜词 | ✅ 自然语言即可 |
| 跨概念关联 | ❌ 需多次grep | ✅ 一次查询 |
| "紫色的火在哪出现过" | 需猜"紫色""火焰"等词 | ✅ 直接搜 |

> 建议：精确查用 grep，模糊查/跨概念查用 RAG，两者互补。

## RAG 维护原则（重要）

### 何时需要更新索引
- 章节正文修改（改字词、改内容） → 只需重新索引改过的文件
- 新增章节 → 只需索引新增的文件
- 人物/设定文件变更 → 对应文件的索引更新

### 什么时候不要动索引
- 纯文本搜索需求（用 grep 更快，且不消耗 Ollama）
- 实验性修改（确认定稿后再更新，避免无效索引）

### 更新方法
```python
import sys, re
sys.path.insert(0, 'D:\\allproject')
from rag.engine import NovelRAG
from pathlib import Path

root = Path('D:\\allproject\\小说项目\\转生深渊领主，我靠种田苟成邪神')
rag = NovelRAG(novel_root=root)

# ✅ 只重新索引改过的文件（推荐）
for fp in [root / '章节' / '第52章-训狼师构想.md']:
    m = re.search(r'(\d+)', fp.stem)
    cn = int(m.group(1)) if m else 0
    rag.index_file('chapters', fp, doc_id=f'ch{cn:04d}', metadata={'chapter': cn})

# ❌ 不要全量重建（耗时、无必要）
rag.index_novel()  # 不要调这个
```

### 核心原则
**改几个文件就只索引几个文件，不动整个库。** 全量重建只有在首次建立索引时才需要做一次。

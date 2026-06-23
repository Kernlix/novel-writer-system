# 🌿 会话分支机制

## 概述
像 Git 分支一样创建会话分支，安全探索不同剧情走向。

## 使用场景

### 场景 1：What-If 剧情探索
```
主线（v1）──→ 第5章 ──→ 第6章 ──→ ...
                │
                ├──→ 分支：如果主角选择背叛 ←── 探索不同走向
                │
                └──→ 分支：如果配角没有死亡 ←── 对比效果
```

### 场景 2：版本对比
```
草稿 A：详细描写版
草稿 B：快节奏版
审查后选择：合并草稿 A 的描写 + 草稿 B 的节奏
```

## 操作命令

| 命令 | 功能 |
|:--|:--|
| `branch create <name>` | 从当前位置创建分支 |
| `branch switch <name>` | 切换到已有分支 |
| `branch list` | 列出所有分支 |
| `branch diff <a> <b>` | 对比两个分支差异 |
| `branch merge <from> <to>` | 合并分支内容 |
| `branch delete <name>` | 删除分支 |

## 存储结构
```
.story-system/
├── branches/
│   ├── main/                 # 主线
│   │   ├── chapters/
│   │   └── characters/
│   ├── what-if-betrayal/     # 分支1
│   │   ├── chapters/
│   │   ├── characters/
│   │   └── parent: main      # 继承自主线
│   └── what-if-no-death/     # 分支2
│       ├── chapters/
│       └── parent: main
└── branch-index.json         # 分支关系图
```

## 分支生命周期
```
Create → Active → (Merge → Delete)
                → (Archive → Keep)
                → (Drop → Delete)
```

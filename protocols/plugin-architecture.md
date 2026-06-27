# 🔌 插件架构

## 概述
非核心功能通过插件扩展，保持核心精简。

## 插件目录结构
```
plugins/
├── <plugin-name>/
│   ├── __init__.py      # 插件入口
│   ├── plugin.yaml      # 插件元数据
│   ├── README.md        # 插件文档
│   └── ...              # 插件模块
└── INSTALLED            # 已启用插件列表
```

## plugin.yaml 规范
```yaml
name: character-tracker
version: 1.0.0
description: 角色弧光跟踪
author: LingJing
type: analysis          # analysis | tool | ui | storage
hooks:
  - post-write          # 写作后触发
  - pre-review          # 审查前触发
dependencies:
  - company/review/skills/consistency-check.md
```

## 内建插件清单

| 插件 | 状态 | 功能 |
|:--|:--:|:--|
| `character-tracker` | 📋 待实现 | 角色成长弧光可视化跟踪 |
| `tension-analyzer` | 📋 待实现 | 章节张力曲线分析 |
| `timeline-validator` | 📋 待实现 | 时间线一致性检查 |
| `wordcount-dashboard` | 📋 待实现 | 写作统计面板 |
| `voice-analyzer` | 📋 待实现 | 角色对话风格一致性分析 |
| `world-bible` | 📋 待实现 | 世界观知识库管理 |

## 插件开发规范
1. 每个插件一个目录，独立命名空间
2. 通过 Hooks 与核心系统通信，不直接修改核心文件
3. 插件失败不影响核心系统运行

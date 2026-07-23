---
id: auto-learn
name: 自动化学习管线钩子
hook: auto-learn
stage: pre
phase: learn
department: learning
runs-on: learning-pipeline-invoke
description: 自动化学习管线入口——通过 `scripts/learning-pipeline.py` 实现一键批量学习
severity: recommended
created: 2026-07-19
---

# 自动化学习管线钩子

> 将学习部门的6步手动流程（查行号→派代理→验证→综合分析→知识管线→更新计划）封装为**一键脚本**。
> 
> **负责人只需输入「学习第X-Y章」** → 系统自动完成全部流程。

## 触发条件

当用户指令匹配以下任一模式时，自动激活本管线：

| 用户指令模式 | 示例 | 对应脚本参数 |
|:-------------|:-----|:-------------|
| `学习第N1-N2章` | 学习第291-300章 | `--batch auto --chapters 291-300` |
| `学习第N批` | 学习第31批 | `--batch 31 --chapters auto` |
| `继续学习` | 继续学习 | 自动推算下一批 |
| `/novel:learn` | /novel:learn | 交互式选择 |

## 使用方法

```bash
# 标准用法：启动新批次学习
python scripts/learning-pipeline.py --batch 31 --chapters 291-300

# 查看当前进度
python scripts/learning-pipeline.py --status

# 验证批次完整性
python scripts/learning-pipeline.py --batch 31 --verify

# 标记批次完成（综合分析+知识管线均已完成时）
python scripts/learning-pipeline.py --batch 31 --update-plan

# 仅查看章节行号信息
python scripts/learning-pipeline.py --chapters 291-300 --dry-run
```

## 自动化流程详解

```
负责人输入「学习第291-300章」
         │
         ▼
┌─────────────────────────────────────────────────────┐
│ scripts/learning-pipeline.py                        │
│                                                     │
│  stage-1: 自动查找章节行号                            │
│   ├── 扫描源文件 "第N章" 标题行                       │
│   ├── 确定每章的行号范围                              │
│   └── 打印行号表（供验证）                            │
│                                                     │
│  stage-2: 派发3个分析代理                             │
│   ├── 代理A（第291-294章，4章）                       │
│   ├── 代理B（第295-297章，3章）                       │
│   └── 代理C（第298-300章，3章）                       │
│                                                     │
│  stage-3: 预验证文件完整性                            │
│   ├── 检查已有分析文件                                │
│   └── 列出缺失文件                                   │
│                                                     │
│  stage-4: 准备综合分析任务                            │
│   └── 生成综合分析任务文件                            │
│                                                     │
│  stage-5: 准备知识管线任务                            │
│   └── 生成知识管线任务文件                            │
│                                                     │
│  stage-6: 更新学习计划                                │
│   └── 标记为 ⏳ 进行中                               │
└─────────────────────────────────────────────────────┘
         │
         ▼
代理A执行(4章)  代理B执行(3章)  代理C执行(3章)
         │              │              │
         └──────────────┴──────────────┘
                      │
                      ▼
          验证：所有10个分析文件存在？
                      │
                 ┌────┴────┐
                 │ 是      │ 否
                 ▼         ▼
         综合分析代理    等待代理完成
                 │
                 ▼
         知识管线代理
           ├── 缺口分析
           ├── Skill创建/合并
           ├── 三文件注册
           └── 更新学习计划 ✅
                 │
                 ▼
          python learning-pipeline.py --batch 31 --update-plan
```

## 自动推算批次号

当不指定 `--batch` 参数时，脚本自动从 `学习计划.md` 推算下一个批次号：

```bash
# 自动推算：如果已有30批，则自动设为第31批
python scripts/learning-pipeline.py --chapters 291-300
```

## 自动推算章节范围

当不指定 `--chapters` 参数仅指定 `--batch` 时：

```bash
# 从学习计划推算第31批的章节范围（标准10章/批）
python scripts/learning-pipeline.py --batch 31
```

## 余量章节处理

当接近全书结尾时，最后一批可能不足10章：

```bash
# 第136批：第1351-1361章（共11章，含完结感言）
python scripts/learning-pipeline.py --batch 136 --chapters 1351-1361
```

管线自动按 4-3-(剩余) 比例分配代理。

## 配合现有流程

| 原始手动步骤 | 自动化后操作 |
|:-------------|:-------------|
| 如鱼查章节行号 | 脚本自动完成 |
| 如鱼派3个分析代理 | 脚本生成任务文件 |
| 如鱼验证文件 | `--verify` 一键验证 |
| 如鱼派综合分析代理 | 脚本生成任务文件 |
| 如鱼派知识管线代理 | 脚本生成任务文件 |
| 如鱼更新学习计划 | 脚本自动完成 |

## 目录结构

```
scripts/
  └── learning-pipeline.py         ← 核心自动化脚本

knowledge/learned/十日终焉/
  ├── 学习计划.md                   ← 自动更新
  ├── batch-{NNN}-任务-代理A(第1-4章).md   ← 自动生成
  ├── batch-{NNN}-任务-代理B(第5-7章).md   ← 自动生成
  ├── batch-{NNN}-任务-代理C(第8-10章).md  ← 自动生成
  ├── batch-{NNN}-任务-综合分析.md         ← 自动生成
  ├── batch-{NNN}-任务-知识管线.md         ← 自动生成
  ├── 第{N}章-{标题}.md                  ← 代理产出
  └── 第{N1}-{N2}章-综合分析.md          ← 代理产出
```

## 依赖

- Python 3.10+
- 源文件：`十日终焉+作者：杀虫队队员（完结）.txt`
- 无第三方包依赖（仅使用标准库）

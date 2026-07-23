---
id: 2026-07-17_audit-9issues
category: 多类别综合审计
severity: P1
resolved: true
date: 2026-07-17
---

# [错误] 2026-07-17 系统审计：9个问题（18处断链）

## 摘要

2026-07-17 系统一致性审计发现9个问题，共涉及18处断链。问题分布在3个根因类别中，已全部修复但未走debug部门7步入库流程，本entry为补录。

## 问题清单

### 根因01-改了A不改B（2个）

1. **SKILL.md Agent计数35，实际37**
   - 修改Agent时未同步更新SKILL.md中的声明数字
   - 修复：更新SKILL.md Agent计数为37

2. **SKILL.md Skill计数44，实际48**
   - 新增Skill时未同步更新SKILL.md中的声明数字
   - 修复：更新SKILL.md Skill计数为48

### 根因02-声明没实现（5个）

3. **shadow-narrative-writer 注册了但文件不存在**
   - REGISTRY中注册了该Agent，但对应的agent.md文件从未创建
   - 修复：删除REGISTRY中的虚假注册 / 创建对应文件

4. **十日终焉4个Skill的agent字段指向不存在的death-game-writer**
   - 创建Skill时填入了不存在的Agent名称
   - 修复：修正agent字段为实际存在的Agent

5. **审核部门6个Skill注册了但文件不存在**
   - REGISTRY中列出了6个Skill，但对应.md文件不存在
   - 修复：删除虚假注册或创建对应文件

6. **学习部门2个Skill注册了但文件不存在**
   - REGISTRY中列出了2个Skill，但对应.md文件不存在
   - 修复：删除虚假注册或创建对应文件

7. **写作部门3个幽灵Skill（worldbuilding, character-design, plot-outline）**
   - 在某处被声明但文件从未创建
   - 修复：删除虚假注册或创建对应文件

### 根因07-子智能体不闭环（5个）

8. **writing-department.md只列出5个Agent，实际12个**
   - 部门概览文件从未随Agent增长而更新
   - 修复：更新writing-department.md列出全部12个Agent

9. **recruitment-department.md遗漏skill-deployer-agent**
   - 部门概览文件未包含已创建的Agent
   - 修复：补充skill-deployer-agent到列表

10. **5个已存在Skill未注册到REGISTRY**
    - Skill文件已创建但未在REGISTRY中注册
    - 修复：补充注册

11. **十日终焉学习产出未完全激活（agent字段指向不存在的Agent）**
    - 学习产出的Skill中agent字段指向不存在的Agent
    - 修复：修正agent字段

12. **部门概览文件从未随Agent增长而更新**
    - 各部门.md概览文件中的Agent/Skill列表落后于实际
    - 修复：全面更新各部门概览文件

## 根因分析

| 根因类别 | 问题数 | 占比 |
|:---------|:------:|:----:|
| 01-改了A不改B | 2 | 22% |
| 02-声明没实现 | 5 | 56% |
| 07-子智能体不闭环 | 5 | 56% |

**共性根因：** 增删Agent/Skill时只改了一处，未全局同步。REGISTRY、部门概览、SKILL.md计数三者之间缺乏自动一致性检查。

## 对策

1. 所有问题已修复（断链已消除）
2. 本entry补录入库，更新root-causes.json计数
3. 增强pre-commit-check.sh覆盖部门概览文件检查

## 防复发

1. **pre-commit-check.sh 已有检查项：**
   - 检查项1：Agent/Skill计数一致性
   - 检查项3：REGISTRY断链
   - 检查项8：写手技能引用完整性

2. **本次新增检查项：**
   - 部门概览文件Agent/Skill列表完整性
   - REGISTRY中Skill的agent字段有效性

3. **流程约束：**
   - Agent/Skill增删后必须跑pre-commit-check.sh
   - 部门概览文件修改后必须跑pre-commit-check.sh

## 涉及文件

- SKILL.md（Agent/Skill计数修正）
- company/REGISTRY.md（断链清理）
- company/writing/writing-department.md（Agent列表更新）
- company/recruitment/recruitment-department.md（Agent列表更新）
- company/learning/learning-department.md（如适用）
- 5个十日终焉Skill文件（agent字段修正）
- 6个审核部门Skill（注册清理/文件创建）
- 2个学习部门Skill（注册清理/文件创建）
- 3个写作部门幽灵Skill（注册清理/文件创建）

## system_learned

本次为一次性补录，9个问题跨越3个根因类别。核心教训：
1. REGISTRY是Agent/Skill的"真相源"，增删操作必须以REGISTRY为准
2. 部门概览文件是"第二真相源"，必须随Agent/Skill变化同步更新
3. pre-commit-check.sh是最后防线，必须在每次Agent/Skill变更后执行

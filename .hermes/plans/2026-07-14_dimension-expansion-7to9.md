# 分析维度扩展计划——7维度→9维度 + 学习框架检查

> **目标：** 将素晴分析用的7维度框架扩展为9维度，新增"场景构建"和"文风语言"两个维度；同时检查学习框架的6Agent是否需要扩展。

---

## 一、现状

### 当前两套分析框架

| 框架 | 用途 | 维度数 |
|:----|:-----|:------|
| **7维度本能分析** | 素晴系列/本能级分析（角色动机+喜剧机制） | 7个本能维度 |
| **6Agent学习框架** | 通用作品技法分析（multi-agent-learning.md） | 6个专业Agent |

### 7维度当前覆盖
```
1. 生存本能
2. 性/繁衍本能
3. 群居/归属本能
4. 探求/好奇本能
5. 闘争本能
6. 支配本能
7. 収集/创造本能

待加：
8. 场景构建 ← 🆕
9. 文风语言 ← 🆕
```

### 6Agent当前覆盖
```
writer         → 场景构建、对话、描写、叙事、文风、去AI化 ✅（已有）
plot-architect → 情节结构、节奏、伏笔 ✅
character-designer → 角色原型、弧光、关系 ✅
worldbuilding  → 世界规则、力量体系 ✅
polish         → 文风、语言、去AI化 ✅
setting-qa     → 设定逻辑、一致性 ✅
```

---

## 二、方案

### 2.1 7维度→9维度扩展

在 `knowledge/learned/instinct-learning-system.md` 和所有相关文件中，将7维度扩展为9维度：

**新增维度8：场景构建（Scene Construction）**
- 空间布局与地理逻辑
- 感官锚点（视觉/听觉/嗅觉/触觉）
- 时间标记与环境变化
- 空间的功能性（战斗/对话/情感场景的分区设计）

**新增维度9：文风语言（Style & Language）**
- 句式多样性（长短句交替、避免完美对称）
- 角色差异化对话（每个人说话方式不同）
- 去AI化写作（口语化、不完美表达、省略与打断）
- 叙事节奏控制（描写/对话/行动的比例）

### 2.2 本能分析模板更新（9维度输出格式）

所有本能分析文件的开头模板从7维度更新为9维度，确保后续分析自动使用新格式。

### 2.3 学习框架检查结论

**6Agent无需新增。** 理由：
- "场景构建"已由 `writer` Agent 覆盖
- "文风语言"已由 `writer` + `polish` 双Agent覆盖
- 现有6Agent已经是按**专业领域**（场景/剧情/角色/世界观/润色/质检）划分，各司其职

**但需要修改：** `multi-agent-learning.md` 的提示词模板和维度说明章节，明确把"场景构建"和"文风语言"作为独立分析维度列出（当前只列在写手的子维度中）。

---

## 三、步骤

### Task 1：更新本能学习框架文档

**Files:**
- Modify: `knowledge/learned/instinct-learning-system.md`
  - 7维度→9维度表格更新
  - 新增维度8、维度9的定义说明
  - 本能ID命名规则扩展（增加 scene/ 和 style/ 前缀）

### Task 2：更新分析模板

**Files:**
- Modify: `knowledge/learned/instinct-learning-system.md`（分析模板部分）
  - 本能输出模板增加 scene 和 style 两个维度

### Task 3：更新学习框架的维度说明

**Files:**
- Modify: `company/learning/skills/multi-agent-learning.md`
  - 分析维度说明章节当前只有6个维度定义，更新为包含场景构建和文风语言的完整说明
  - 写手Agent的维度说明中明确将"场景构建"和"文风语言/去AI化"列为独立分析维度而非子维度

### Task 4：创建场景构建和文风语言的知识参考

**Files:**
- Create: `knowledge/rules/common/scene-construction.md`（场景构建维度的参考检查清单）
- Create: `knowledge/rules/common/style-language-deai.md`（文风语言+去AI化的参考检查清单）

（可选——如果觉得现有规则文件已够用可以跳过）

### Task 5：验证

```bash
bash scripts/pre-commit-check.sh
# 期望：全部通过
```

---

## 四、风险与注意

- **两套框架不要混淆**：7维度本能分析（本能级）vs 6Agent学习框架（技法级）是不同的东西。扩展后前者变成9维度，后者保持6Agent不变
- **已有分析文件不回溯修改**：灯1-7和素晴17卷已用7维度分析完，不回头改——新维度从下次学习开始生效
- **去AI化已经纳入**：文风语言维度中包含了去AI化，与现有的 `anti-ai-polish` skill 和 writer-agent 的去AI化指引形成三层覆盖（写前预防+分析维度+写后验证）

---

## 五、保存路径

- 计划文件：`.hermes/plans/2026-07-14_dimension-expansion-7to9.md`

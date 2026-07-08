---
tags: [知识库, 学习沉淀, instinct]
type: reference
description: 灵境本能学习系统——基于ECC持续学习v2.1模式改造，原子级本能→聚类→升级的进化路径
updatable: true
---

# 灵境本能学习系统

> 借鉴 ECC Continuous Learning v2.1 的 instinct 架构，将灵境学习部门从"一次性大知识文件"升级为"原子本能→置信度积累→自动进化的持续学习系统"。

---

## 两层学习架构

```
创作/审查过程中发现模式
       │
       ▼
 本能(Instinct) ─────── 原子级，单触发+单行动
  │         │
  │   置信度 < 0.7      │
  │         ▼           │
  │     暂存，不生效     │
  │                     ▼
  │              置信度 ≥ 0.7
  │                     │
  │                     ▼
  │              聚类(Cluster) ──→ 相关本能归组
  │                                   │
  │                                   ▼
  │                          进化(Evolve) ──→ 知识库文件
  │                                   │         skill升级
  │                                   │         agent升级
  │                                   ▼
  │                             .story-system/upgrade-log.md
```

---

## 一、本能模型（Instinct）

### 什么是本能

本能是最小学习单元——一条「什么场景下做什么事」的规则，带置信度评分：

```yaml
# 示例：一条本能
trigger: "写铁锤的对话时"
action: "用短句、不用修饰词、用行动代替情绪表达"
confidence: 0.7
source: "第61章审查反馈——铁锤台词太通用"
scope: project
```

### 本能文件格式

每个本能是一个独立 `.md` 文件，存储在 `knowledge/instincts/` 下：

```markdown
---
id: dialogue:ironhammer-short-speech
trigger: "写铁锤的对话时"
action: "用短句、不用修饰词、用行动代替情绪表达"
confidence: 0.7
domain: "dialogue"
scope: "project"              # project | global
source: "第61章审查反馈"
created: 2026-07-06
obs_count: 3                   # 观察到该模式的次数
---

## 本能说明

铁锤（矮人锻造大师）的语言特征是简短、直接、不修饰。
- ❌ 铁锤说了一大段解释自己心情的话
- ✅ 铁锤嘟囔了一句"还挺能哭"，然后回去打了半天铁

## 相关本能

- dialogue:elven-calm-tone（艾琳语气平淡）
- dialogue:lilith-lazy-tease（莉莉丝慵懒逗趣）

## 进化状态

- [ ] 已聚类（关联本能 /cluster 文件）
- [ ] 已升级（对应 knowledge/ 文件）
```

### 本能 vs 传统知识文件的区别

| | 传统知识文件 | 本能（Instinct） |
|:--|:-----------|:----------------|
| 体积 | 几十行/几百行 | 10-20行 |
| 粒度 | 整篇技法 | 单条规则 |
| 创建条件 | 需要完整分析 | 观察到即可创建 |
| 置信度 | 无，创建即生效 | 0.3-0.9，达标才生效 |
| 范围 | 固定 | project/global 可切换 |

### 置信度评分

| 分数 | 含义 | 行为 |
|:---:|:----|:----|
| 0.3 | 试探性 | 记录但不使用 |
| 0.5 | 中等 | 写手可参考 |
| 0.7 | 强 | 自动生效，写手必须遵守 |
| 0.9 | 确定 | 核心规则，审查官检查 |

**涨分条件：**
- 同一模式被重复观察到（obs_count +1）
- 用户未纠正该行为
- 多个来源的线索指向同一结论

**降分条件：**
- 用户明确纠正
- 长时间未观察到该模式
- 出现矛盾证据

---

## 二、范围隔离（Scope）

| 范围 | 目录 | 判断标准 |
|:----|:-----|:---------|
| **project（小说专项）** | `knowledge/instincts/project/` | 换一本小说就用不上了（角色语气、本作独有设定） |
| **global（通用）** | `knowledge/instincts/global/` | 换一本小说还用得上（对话技法、场景描写原则） |

判断标准沿用灵境已有的规则：**"换一本小说还用得上吗？用得上→global，用不上→project。"**

---

## 三、进化路径

```
本能(confidence ≥ 0.7)
  → 聚类：多个相关本能归入同一 cluster 文件
  → 进化：cluster 内容成熟后，转为正式 knowledge/ 文件
  → 升级：同步更新对应 agent/skill/hook 文件
  → 记录：.story-system/upgrade-log.md
```

### 触发进化的条件

- 同一 domain 下有 ≥3 条置信度 ≥ 0.7 的本能
- 用户主动执行 `/novel:evolve`
- 招募部门差距分析时发现该领域知识不足

---

## 四、学习方式

### 方式一：快速本能（日常创作中沉淀）

每次写作/审查完成后，负责人审视是否有值得记录的本能：

```
写作/审查中发现"这个写法不错/这个坑别再踩"
  → 创建一条本能（10-20行）
  → 设置 scope 和初始 confidence
  → 存入 knowledge/instincts/
```

### 方式二：全面学习（完整作品分析）

沿用原有6Agent并行流程，但产出物变为：

```
以前：直接写整篇 knowledge/ 文件
现在：先写一组本能 → 聚类 → 再进化为正式知识文件
```

### 方式三：本能进化

```
/novel:evolve
  └── 读取所有 confidence ≥ 0.7 的本能
  └── 按 domain 聚类
  └── 建议合并哪些本能
  └── 生成正式 knowledge/ 文件草稿
  └── 负责人确认 → 写入
```

---

## 五、目录结构

```
knowledge/
├── instincts/                      ← 本能存储
│   ├── project/                    ← 小说专项本能
│   │   ├── dialogue-ironhammer.md
│   │   ├── chenmo-programmer.md
│   │   └── ...
│   ├── global/                     ← 通用本能
│   │   ├── merge-redundant-qa.md
│   │   └── ...
│   └── clusters/                   ← 本能聚类
│       ├── dialogue-quality.md     ← 对话质量相关本能组
│       └── scene-immersion.md
├── learning/                       ← 正式知识（进化后）
│   └── writing-craft/
│       └── lingjing-v2-experience.md
└── REGISTRY.md
```

每个本能文件需在 `knowledge/instincts/REGISTRY.md` 中注册。

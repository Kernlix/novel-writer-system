# 灵境系统 — 外部 Skill 加载机制

> 灵感来源：InkOS 的 Capability Skills 系统  
> （参考 `inkos/packages/core/src/skills/external-loader.ts` + `skills/SKILL.md` 声明式清单）

---

## 目录结构

```
company/writing/skills/
├── <skill-id>.md              ← 内建 Skill（直接放在 skills/ 根目录）
└── external/
    ├── README.md               ← 本文件：使用说明
    └── <external-skill-id>/
        ├── SKILL.md            ← 外部 Skill 的声明式清单（含 YAML frontmatter）
        └── ...                 ← （可选）辅助文件
```

每个外部 Skill 都存放在 `company/writing/skills/external/<skill-id>/` 子目录中，  
以 `SKILL.md` 为入口声明文件。

---

## 快速开始

### 安装外部 Skill

```bash
# 从包含 SKILL.md 的目录安装
python scripts/external-skill-loader.py install path/to/some-skill-dir/

# 直接从 SKILL.md 文件安装
python scripts/external-skill-loader.py install path/to/some-skill-dir/SKILL.md
```

安装过程：
1. 解析 `SKILL.md` 的 YAML frontmatter，提取 id/name/description/triggers/sessionKinds
2. 复制到 `company/writing/skills/external/<skill-id>/SKILL.md`
3. 自动注册到 `company/REGISTRY.md` 的外部技能段

### 扫描目录发现外部 Skill

```bash
# 扫描一个或多个目录，查找含 SKILL.md 的目录
python scripts/external-skill-loader.py scan ~/my-external-skills/ /shared/team-skills/
```

三层发现策略（参考 InkOS）：
1. **第一层**：扫描目录自身是否有 `SKILL.md`
2. **第二层**：扫描子目录，检查每个子目录是否有 `SKILL.md`
3. 去重并返回所有含有效 `SKILL.md` 的目录

### 列出已安装的外部 Skill

```bash
python scripts/external-skill-loader.py list
```

输出示例：

```
已安装的外部 Skill:
  ID                       名称                           触发器                      Agent
  ------------------------ ------------------------------ ------------------------ ------------
  mystery-plot-engine      悬疑情节引擎                   悬疑, 推理                  writer

  共 1 个外部 Skill
```

### 卸载外部 Skill

```bash
# 按 skill id 卸载
python scripts/external-skill-loader.py uninstall mystery-plot-engine
```

卸载过程：
1. 删除 `company/writing/skills/external/<skill-id>/`
2. 从 `company/REGISTRY.md` 移除注册信息（所有 Skill 卸载后自动移除外部技能段）

---

## SKILL.md 格式规范

每个外部 Skill 必须以 `SKILL.md` 为文件名，包含 **YAML frontmatter** 和 **Markdown 正文**。

### frontmatter 字段

```yaml
---
id: my-skill-id               # 必填。全局唯一标识符，用于注册和引用
name: 我的外部 Skill           # 必填。人类可读的名称
skill: my-skill-id            # 推荐。技能标识，通常与 id 一致
agent: writer                 # 推荐。目标 Agent 类型 (writer|reviewer|manager|...)
description: "Skill 的详细描述" # 必填。说明技能用途
created: 2026-07-19            # 推荐。创建日期
source: "来源说明"             # 推荐。技能来源（如：从某作品分析提炼）
triggers:                     # 推荐。触发关键词列表
  - 悬念
  - 反转
  - 反预期
sessionKinds:                 # 推荐。适用的会话类型
  - writing
  - planning
contextNeeds:                 # 可选。上下文需求声明
  - id: my-context
    purpose: 参考本 Skill 的完整内容
    sources:
      - company/writing/skills/external/my-skill-id/SKILL.md
---
```

### 字段说明

| 字段 | 必填 | 类型 | 说明 |
|:-----|:-----|:-----|:------|
| `id` | **是** | `string` | 唯一标识符，用于安装/卸载/引用。应使用 kebab-case |
| `name` | **是** | `string` | 人类可读的中/英文名称 |
| `skill` | 推荐 | `string` | 技能标识，通常与 `id` 一致 |
| `agent` | 推荐 | `string` | 指定该 Skill 服务于哪个 Agent：`writer`, `reviewer`, `manager`, `learning` 等 |
| `description` | **是** | `string` | 简要描述，安装时将注册到 REGISTRY.md |
| `created` | 否 | `string` | 创建日期（YYYY-MM-DD） |
| `source` | 否 | `string` | 来源说明，如"从《小说名》第X章分析提炼" |
| `triggers` | 否 | `string[]` | 触发关键词列表，用于技能自动匹配 |
| `sessionKinds` | 否 | `string[]` | 适用的会话类型：`writing`, `planning`, `review`, `learning` |
| `contextNeeds` | 否 | `object[]` | 上下文需求声明，每个条目包含 `id`/`purpose`/`sources` |

### 正文要求

- 使用标准 Markdown 格式
- 建议从 `##` 级别标题开始（`#` 保留给 frontmatter 中的 name）
- 正文中可包含示例、代码块、列表等 Markdown 元素
- 正文同样受版本控制，纳入 REGISTRY.md 索引

### 完整示例

```yaml
---
id: plot-twist-builder
name: 情节反转构建器
skill: plot-twist-builder
agent: writer
description: 构建多层级情节反转——虚假铺垫、信任建立后崩溃、双关信息揭示。
created: 2026-07-19
source: 《十日终焉》第X章 11维度分析
triggers:
  - 反转
  - 陷阱
  - 误解
  - 双关揭示
sessionKinds:
  - writing
  - planning
contextNeeds:
  - id: plot-twist-context
    purpose: 参考情节反转构建器的完整内容
    sources:
      - company/writing/skills/external/plot-twist-builder/SKILL.md
---

## 技法体系

### 1. 虚假铺垫
在早期章节建立看似无害的信息点……
```

---

## 与 Skill Matcher 的协同

`skill-matcher-agent.md` 从 `company/writing/skills/`（含 `external/` 子目录）检索匹配的技能：

- 外部 Skill 的 `triggers` 字段用于自动匹配写作场景
- `sessionKinds` 字段决定该 Skill 在哪些会话类型中激活
- `agent` 字段指定目标 Agent

安装后无需额外配置即可被 Skill Matcher 发现和使用。

---

## 设计原则（参考 InkOS）

| 原则 | 说明 |
|:-----|:------|
| **声明式清单** | 每个外部 Skill 以 `SKILL.md` 为入口，YAML frontmatter 声明元数据 |
| **三层发现** | 目录自身 → 子目录 → 环境变量（预留扩展） |
| **最小侵入** | 不修改内建 Skill，外部 Skill 隔离在 `external/` 子目录 |
| **可追溯** | 每个外部 Skill 记录来源、创建日期，便于审计 |
| **可卸载** | 通过 loader 一键卸载，不残留注册信息 |

---

## 进阶用法

### 批量安装多个 Skill

```bash
for dir in ~/my-skills/*/; do
  python scripts/external-skill-loader.py install "$dir"
done
```

### 作为 CI/CD 流水线的一步

```bash
# 扫描但不修改
python scripts/external-skill-loader.py scan $SKILL_DIR

# 检查外部 Skill 是否已注册
python scripts/external-skill-loader.py list
```

### 团队共享

通过 Git 子模块将共享 Skill 仓库引入项目，通过 loader 安装：

```bash
git submodule add https://github.com/team/shared-writing-skills.git _shared-skills
python scripts/external-skill-loader.py install _shared-skills/my-plot-trick/
```

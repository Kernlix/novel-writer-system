# 修错部门（Debug Department）建设计划

> **For Hermes:** 使用 subagent-driven-development 逐任务实施。
> **目标：** 将灵境系统的"修错"行为从被动反应升级为主动部门管理——有专门的Agent、Skill、Hook来统一管理错误修复和知识库维护。

---

## 一、现状

### 当前散落在各处的修错相关文件

| 位置 | 内容 | 问题 |
|:-----|:------|:-----|
| `knowledge/errors/` | 错误知识库（刚建） | 有数据无管理，没人负责维护 |
| `consistency-rules.md` | 铁律+根因速查 | 在 rules/common/ 下，不属于任何部门 |
| `pre-commit-check.sh` | 自动化检查 | 在 scripts/ 下，无归属 |
| `manager-agent.md` | 错误库引用流程 | 只写了"可引用"，未指定负责人 |
| `SOUL.md` | 修复铁律 | 全局规则但缺执行者 |

### 缺少什么
- 一个**专责部门**来管理"修错"这件事
- 一个**修错Agent**——当错误发生后负责分析根因、录入知识库、推动修复
- 一个**错误记录Agent**——负责维护知识库的完整性
- 配套的**Skill**（根因分析法、错误条目写作规范）
- 配套的**Hook**（修错前自查、修错后自动入录）
- 一个**部门README**说明职责范围和工作流程

### 设计原则
- **最小侵入**：新建 `company/debug/` 目录，不影响现有部门结构
- **开箱即用**：新建完就能跑，不需要改现有 Agent 的调用链路
- **知识库归属**：`knowledge/errors/` 的逻辑所有者→修错部门

---

## 二、方案

```
company/debug/                     ← 修错部门
├── README.md                      ← 部门门面：职责/分工/工作流
├── debug-agent.md                 ← 修错智能体（核心执行者）
├── error-logger-agent.md          ← 错误记录智能体（知识库管理员）
├── skills/                        ← 修错技能
│   ├── root-cause-analysis.md     ← 根因分析法（7类根因定位）
│   └── error-entry-standard.md    ← 错误条目写作规范
└── hooks/                         ← 修错流程钩子
    ├── pre-debug.md               ← 修错前：自查清单+查同类错误
    └── post-debug.md              ← 修错后：自动录入知识库+更新计数
```

### 各文件职责

#### `README.md`
部门首页，含：
- 部门使命："系统出了问题有人管"
- 值班主任制：默认由 debug-agent 值班
- 工作流总图

#### `debug-agent.md`
核心修错Agent，当系统检测到错误时被激活：
1. 读取错误上下文
2. 查 `knowledge/errors/categories/` → 匹配同类错误
3. 查 `knowledge/errors/entries/` → 是否有同类已有的修复方案
4. 执行根因分析 → 分类到7类之一
5. 生成修复方案
6. 调用 `hooks/post-debug.md` → 录入知识库

#### `error-logger-agent.md`
知识库维护Agent：
1. 定期检查 `entries/` 文件数与 `root-causes.json` 一致性
2. 为每个新错误分配唯一ID、创建 entry 文件
3. 更新 JSON 计数
4. 更新 README.md 速查表
5. 标记已过时的 entry（如果确认不再适用）

#### Skills

**`root-cause-analysis.md`** — 根因分析法 skill
- 7类根因的定位检查清单
- 每类根因的追问模式
- 案例对照表

**`error-entry-standard.md`** — 错误条目写作规范 skill
- entry 文件的格式模板
- 必须包含的字段
- 好/差示例对比

#### Hooks

**`pre-debug.md`** — 修错前 hook
- □ 确认错误现象可复现
- □ 搜索 knowledge/errors/ 是否有同类错误
- □ 如有同类→读取已有对策再动手
- □ 如无同类→准备新建 entry

**`post-debug.md`** — 修错后 hook
- □ 修复是否已验证通过（pre-commit-check）
- □ 新错误已创建 entry 文件
- □ root-causes.json 计数已更新
- □ categories/ 对应模板已补充
- □ 如发现新根因→新建 categories/ 文件
- □ 记忆已同步

---

## 三、步骤

### Task 1: 创建部门目录

**目标：** 建立 `company/debug/` 目录及子目录

**文件：**
- Create: `company/debug/README.md`
- Create: `company/debug/.gitkeep`
- Create: `company/debug/skills/.gitkeep`
- Create: `company/debug/hooks/.gitkeep`
- Modify: `company/REGISTRY.md` → 注册新部门

**README.md 内容：**
```markdown
# 🔧 修错部门 (Debug Department)

> 系统出了问题有人管——修错Agent负责根因分析+修复，错误记录Agent负责知识库维护。

## 职责
- **修错智能体** (debug-agent): 收到错误信号→查库→分析→修复→入库
- **错误记录智能体** (error-logger-agent): 日常维护错误知识库的完整性

## 值班主任制
默认由 debug-agent 值班。
当 pre-commit-check.sh 报错或 manager 发现系统异常时自动路由到本部门。

## 工作流
错误发生 → 读取上下文 → 查 knowledge/errors/ → 执行 pre-debug hook
→ 分析根因 → 修复 → 验证 → 执行 post-debug hook → 关闭
```

### Task 2: 创建 Skills

**目标：** 修错专用的方法论

**文件：**
- Create: `company/debug/skills/root-cause-analysis.md`
- Create: `company/debug/skills/error-entry-standard.md`

**root-cause-analysis.md 要点：**
- 7类根因的定位问题链（每类3-5个追问）
- 示例：当 pre-commit 报"Agent数不一致"→ 属于"改了A不改B" → 搜全仓库旧数字

**error-entry-standard.md 要点：**
```yaml
entry 模板:
  id: YYYY-MM-DD_简短描述.md
  必含字段:
    - 摘要（一句话）
    - 根因分析（含归类到7类中的哪一类）
    - 对策（具体怎么修的）
    - 防复发（怎么防止再犯）
    - 涉及文件列表
```

### Task 3: 创建 Hooks

**目标：** 修错前后的标准化检查

**文件：**
- Create: `company/debug/hooks/pre-debug.md`
- Create: `company/debug/hooks/post-debug.md`

**pre-debug.md 核心逻辑：**
```
当收到修错指令时：
1. 检查 `knowledge/errors/entries/` 是否有同类错误
   有 → 输出已有对策作为参考
   无 → 准备新建 entry
2. 确认错误可复现
3. 记录修错开始时间
```

**post-debug.md 核心逻辑：**
```
修复完成后：
1. 跑一次 pre-commit-check.sh 验证
2. 若通过→创建 entry 文件
3. 更新 root-causes.json 对应类别的计数
4. 更新 knowledge/errors/README.md 速查表
5. 更新记忆
```

### Task 4: 创建 Agents

**目标：** 两个核心Agent

**文件：**
- Create: `company/debug/debug-agent.md`
- Create: `company/debug/error-logger-agent.md`

**debug-agent.md 结构：**
```yaml
---
id: debug-agent
name: 修错智能体
emoji: 🔧
department: debug
description: 根因分析、修复执行、知识库入库
---
读取错误上下文 → cats/匹配同类 → entries/查已有方案 → 根因分析
→ 生成修复方案 → hooks/post-debug
```

**error-logger-agent.md 结构：**
```yaml
---
id: error-logger-agent
name: 错误记录智能体
emoji: 📝
department: debug
description: 错误知识库维护、计数同步、条目归档
---
扫描 entries/ vs root-causes.json → 标记不一致 → 创建新条目
→ 更新计数 → 归档旧条目
```

### Task 5: 迁移 knowledge/errors/ 归属

**目标：** 将错误知识库的"管理权"正式划归修错部门

**文件：**
- Modify: `knowledge/errors/README.md` → 顶部加"本库由 debug 部门管理"
- Modify: `company/REGISTRY.md` → 部门表新增 debug 部门行，注册 debug-agent + error-logger-agent + 2个skills + 2个hooks
- Modify: `company/manager/manager-agent.md` → 在部门委派表中新增"系统错误/异常"→ debug 部门

### Task 6: 注册+更新计数

**目标：** 让系统知道有了新部门和新Agent

**文件：**
- Modify: `SKILL.md` → Skills: 27→29（新增2个）
- Modify: `SKILL.zh-CN.md` → 同步
- Modify: `company/REGISTRY.md` → Agent总数更新
- Modify: `SOUL.md` → 新增 debug 部门记录

---

## 四、验证

| 检查 | 指标 |
|:-----|:------|
| 目录完整 | `company/debug/` 含 README + 2个Agent + 2个Skills + 2个Hooks |
| REGISTRY注册 | 部门表有 debug 行、Agent/Skill/Hook 计数正确 |
| 知识库归属 | `knowledge/errors/README.md` 注明由 debug 部门管理 |
| Manager引用 | 部门委派表有"系统错误/异常"→ debug  |
| pre-commit-check | 无新增断链 |
| 修错可执行 | debug-agent能引用所有 skills 和 hooks |

---

## 五、风险与注意

- **不覆盖现有流程**：debug 部门是新增，不替换 manager 的异常处理职责
- **不自动触发**：初期手动调用，后续再加自动路由
- **保持轻量**：2个Agent + 2个Skills + 2个Hooks，不建冗余

---

## 六、保存路径

- 计划文件：`.hermes/plans/2026-07-14_debug-department.md`

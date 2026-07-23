# 自动化学习管线 — 第51批 知识管线任务

> 生成时间: 2026-07-23

---

## 任务: 知识管线

章节范围: 第501章 ~ 第510章


### 前提条件

- 综合分析报告已存在

### 操作步骤


#### 3.1 缺口分析
- 检查本批是否有新的写作技法
- 对比已有 Skill 列表（`company/REGISTRY.md`）
- 判断：新建 Skill / 合并到已有 Skill / 无需新增

#### 3.2 Skill 创建（如有新技法）
- 文件命名：`company/writing/skills/{名称}.md`
- 格式：frontmatter（id/name/skill/agent/description/created/source）+ 技法 + 配合指南

#### 3.3 注册（三文件同步）
1. `company/REGISTRY.md` — Skills 列表追加
2. `company/writing/writer-agent.md` — 可用技能表新增
3. `company/writing/skill-matcher-agent.md` — 章节类型映射表新增
# 🔎 招募部门 (Recruitment Department)

## 部门使命
系统的"进化引擎"——持续发现能力缺口，设计新能力并集成到系统中。

## 下属Agent
| Agent | 职责 |
|:------|:------|
| gap-analysis-agent | 差距分析：分析工作流、Agent质量、系统瓶颈 |
| job-designer-agent | 岗位设计：定义新Agent/Skill/Hook需求规范 |
| skill-engineer-agent | 技能研发：使用模板设计新Skill |
| agent-integrator-agent | Agent集成：配置权限、知识库访问、协作流程 |

## 招募流程

> ⚠️ 强制规则：新Agent加入后必须更新部门工作流，确保被纳入部门多agents协作。

```
🔧 执行 company/recruitment/hooks/pre-recruit.md（备份REGISTRY.md、记录当前数量）
  ↓
能力评估 → 缺口分析 → 岗位设计 → 技能研发
  → Agent集成
  → 更新对应部门工作流（写作/审核/学习）
  → 更新部门多agents协作流程描述
  → 注册上线
  ↓
🔧 执行 company/recruitment/hooks/post-recruit.md（校验文件位置/REGISTRY更新/权限配置）
  ↓
通知用户
```

## 命令
- `/novel:recruit:gap` — 启动差距分析
- `/novel:recruit:job` — 设计新岗位
- `/novel:recruit:skill` — 研发新技能
- `/novel:recruit:integrate` — 集成新Agent

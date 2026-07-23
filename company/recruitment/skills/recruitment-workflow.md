---
id: recruitment-workflow
name: 招募工作流
type: skill
agent: recruitment
description: 完整的Agent/Skill招募流程——从缺口分析到部署上线
---

# 招募工作流 Skill

## 触发条件
- 学习部门产出新能力需要集成
- 用户发现系统能力缺口
- gap-analysis自动检测到瓶颈

## 流程

```
1. pre-recruit Hook — 备份REGISTRY.md、记录当前Agent/Skill数量
   ↓
2. 差距分析 (gap-analysis-agent)
   - 分析当前工作流瓶颈
   - 评估现有Agent质量
   - 确定是否需要新Agent或新Skill
   ↓
3. 岗位设计 (job-designer-agent)
   - 定义新Agent/Skill需求规范
   - 输出岗位说明书
   ↓
4. 技能研发 (skill-engineer-agent)
   - 使用skill-template设计新Skill
   - 编写SKILL.md + 配套文件
   ↓
5. Agent集成 (agent-integrator-agent)
   - 配置权限和知识库访问
   - 设置协作流程
   ↓
6. 部署 (skill-deployer-agent)
   - 更新对应部门的Agent引用
   - 注册到REGISTRY
   ↓
7. post-recruit Hook — 校验文件位置/REGISTRY更新/权限配置
   ↓
8. 通知用户
```

## 强制规则
- 新Agent加入后必须更新部门工作流
- 新Skill必须被至少1个Agent引用
- 必须更新REGISTRY.md

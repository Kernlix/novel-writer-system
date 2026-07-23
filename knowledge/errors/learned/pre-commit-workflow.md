# Pre-commit 工作流规范

> 由 debug-agent 在 2026-07-17 审计后固化。

## 何时必须跑 pre-commit-check.sh

以下4种场景，**必须**在提交前执行 `bash scripts/pre-commit-check.sh`：

### 场景1：学习部门产出后
- 学习部门产出新Skill时，必须验证：
  - Skill文件确实存在
  - REGISTRY中已注册
  - agent字段指向的Agent确实存在
  - 部门概览文件已更新

### 场景2：REGISTRY修改后
- 任何对 `company/REGISTRY.md` 或 `knowledge/REGISTRY.md` 的修改
- 必须验证：
  - 所有引用的文件路径存在（断链检查）
  - Agent/Skill计数与SKILL.md一致

### 场景3：Agent/Skill增删后
- 新增或删除任何Agent（*-agent.md）或Skill（skills/*.md）
- 必须验证：
  - REGISTRY已同步更新
  - SKILL.md中的计数已同步更新
  - 对应部门概览文件已同步更新
  - 无孤立文件（存在但未注册）

### 场景4：部门概览文件修改后
- 任何 `company/*/` 下的 `*-department.md` 文件修改
- 必须验证：
  - 列出的Agent全部存在
  - 列出的Skill全部存在
  - 未遗漏已创建的Agent/Skill

## 执行方式

```bash
bash scripts/pre-commit-check.sh
```

返回0=通过，返回1=有错误需修复。

## 违规后果

跳过pre-commit检查导致的问题，将按根因01/02/07录入错误知识库，并计入debug-agent的进化阈值计数。

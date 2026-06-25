---
id: hook-template
name: 钩子创建模板
type: template
description: 用于创建新的钩子文件，包含标准frontmatter和阶段分类
---

# <名称>钩子

## 元数据

```yaml
---
id: <hook-id>                      # 唯一标识，小写英文，连字符分隔
name: <中文名>钩子                   # 完整名称
hook: <hook-id>                    # 与id相同
stage: <pre|post|session>          # pre=执行前，post=执行后，session=会话级
phase: <write|review|archive|discuss|session>  # 所属阶段
runs-on: <触发时机说明>              # 描述何时触发
description: <一行描述>             # 最多20字
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---
```

## 触发时机

<详细说明钩子的触发条件>

## 执行流程

1. <步骤一>
2. <步骤二>
3. <步骤三>

## 输出

<钩子产生的输出数据>

## 失败处理

- <异常情况一：处理方式>
- <异常情况二：处理方式>

---

> **扩展说明：**
> - 新建 Hook 后，在 `hooks/REGISTRY.md` 中添加一行
> - Hook 命名约定：`<pre|post|session>-<phase>`，如 `pre-write`、`post-review`
> - stage/phase 分类决定该 hook 在创作流程的哪个环节被触发

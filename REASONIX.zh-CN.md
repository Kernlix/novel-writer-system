# 🤖 Reasonix 使用指南

> 在 Reasonix（AI 编程代理）环境中使用灵境小说创作系统。

---

## 🎯 方式一：直接调用 Skill

安装后，本系统已在 Reasonix 中注册为 skill。在任何对话中直接使用：

```
/novel-writer 我想写一本关于星际殖民的科幻小说
```

Reasonix 会自动加载灵境系统，启动创作模式。

---

## 🎯 方式二：分步使用

当你已经在 Reasonix 对话中时，可以逐步使用灵境的功能：

### 开始创作
```
请启动灵境小说创作系统，我想开始写小说
```
或：
```
/novel-writer /novel:start
```

### 设定世界观
```
/novel-writer 帮我搭建一个科幻世界观，/
novel:world
```

### 角色设计
```
/novel-writer 设计三个主要角色，/novel:characters
```

### 写正文
```
/novel-writer 写第一章开篇，/novel:write
```

### 去AI化
```
/novel-writer 帮我润色这段文字，去掉AI味，/novel:anti-ai
```

---

## 🎯 方式三：在 Reasonix 项目中安装

如果你想在 Reasonix 项目中永久集成：

```bash
# 将仓库克隆到 Reasonix 工作区
cd your-reasonix-project
git clone https://github.com/Kernlix/novel-writer-system.git skills/novel-writer

# 在 AGENTS.md 中引用
echo "- [novel-writer](skills/novel-writer/SKILL.md) — 灵境小说创作系统" >> AGENTS.md
```

---

## 📋 可用命令速查

| 命令 | 功能 |
|------|------|
| `/novel-writer` | 直接调用灵境系统 |
| `/novel-writer /novel:start` | 启动创作向导 |
| `/novel-writer /novel:world` | 世界观搭建 |
| `/novel-writer /novel:characters` | 角色设计 |
| `/novel-writer /novel:outline` | 大纲规划 |
| `/novel-writer /novel:write` | 正文写作 |
| `/novel-writer /novel:review` | 章节审查 |
| `/novel-writer /novel:anti-ai` | 去AI化润色 |
| `/novel-writer /novel:booming` | 剧情引爆 |
| `/novel-writer /novel:progress` | 查看进度 |
| `/novel-writer /novel:help` | 显示帮助 |

> 💡 **简化用法**：直接描述需求即可，不需要严格遵循命令格式。
> 例如：「帮我设计一个修仙世界观」会自动触发 `/novel:world`。

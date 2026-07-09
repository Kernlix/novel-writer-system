# 📚 灵境 · 小说创作智能体系统

> **LingJing** — 集部门多agents协作、模块化 Skills、知识图谱于一体的 AI 小说创作系统。

整合 GitHub 上最优秀的开源小说写作项目精华，为你量身打造的统一创作工具箱。

[🇬🇧 **English**](README.md)

---

## ✨ 系统特色

| 特性 | 说明 |
|------|------|
| 🧠 **部门多agents协作** | 7 个专业智能体分工协作 |
| 🧩 **模块化 Skills** | 30+ 独立 skill 覆盖创作全流程 |
| 📖 **双模式支持** | 长篇小说流水线 + 短篇快速创作 |
| 🎭 **去AI化引擎** | 多层检测与润色，输出自然流畅 |
| 📊 **知识图谱** | 角色/地点/事件关系持久化 |
| 🌐 **多平台适配** | 起点/番茄/晋江等平台优化 |

---

## 🚀 快速安装

### Windows
```powershell
iex "& { $(irm https://raw.githubusercontent.com/nosoultool/novel-writer-system/main/install.ps1) }"
```

### macOS / Linux
```bash
bash <(curl -s https://raw.githubusercontent.com/nosoultool/novel-writer-system/main/install.sh)
```

---

## 📖 7 种使用方式

### 🥇 Reasonix

```bash
/novel-writer 我想写一本修仙小说
/novel-writer /novel:world    搭建世界观
/novel-writer /novel:write    写正文
```

> 详细用法见 [REASONIX.zh-CN.md](REASONIX.zh-CN.md)

### 🥇 Claude Code（全功能推荐）

```bash
cd novel-writer-system
claude
# 输入 /novel:start
```

### 🥈 Codex CLI · 🥉 Cursor IDE · 🏅 Windsurf · 📱 ChatGPT/Kimi · 📄 手动阅读

详见各平台说明。

---

## 📜 完整命令一览

```
🚀 创作流程        🌍 设定管理           📋 大纲
  /novel:start       /novel:world          /novel:outline
  /novel:discuss     /novel:characters     /novel:snowflake

✍️ 写作              🔍 审查               🎨 润色
  /novel:write        /novel:review         /novel:anti-ai
  /novel:decoupled    /novel:check          /novel:booming
                      /novel:quality        /novel:style-learn
                      /novel:deslop
                      /novel:plot-hole

📦 网文专项          🛠️ 工具
  /novel:hook         /novel:archive
  /novel:shuang       /novel:knowledge
  /novel:trend        /novel:memory
  /novel:goldfinger   /novel:progress
  /novel:submit
```

---

## 🙏 致谢与许可证

### 许可证
本系统采用 **MIT License** — 你可以自由使用、修改、分发，包括商业用途。

### 设计启发

> ⚠️ **许可证声明**：本系统从以下开源项目中汲取灵感，但所有代码/文件均为独立实现。下表所列外部许可证仅适用于原项目，本系统使用 MIT 许可证发布。

本系统的设计思路受以下开源项目启发，在此致谢：

| 项目 | 许可证 | 贡献 |
|------|--------|------|
| [awesome-novel-skill](https://github.com/modoojunko/awesome-novel-skill) | GPL-3.0 | 部门多agents协作工作流与记忆系统 |
| [tianming-skill](https://github.com/zy-zmc/tianming-skill) | CC BY-NC-SA 4.0 | 模块化提示词工程与质量门禁 |
| [chinese-webnovel-skills](https://github.com/tance-mang/chinese-webnovel-skills) | MIT | 33 个网文 Skills 与平台适配 |
| [claude-novel-skills](https://github.com/fnb666888/claude-novel-skills) | MIT | 解耦写作法与风格学习 |
| [story-skills](https://github.com/ati9527/story-skills) | — | 网文 AI Agent 工具集 |
| [vibe-noveling](https://github.com/TulanCN/vibe-noveling) | MIT | 网文创作工作流与 SSoT 修订 |

本系统为独立创作，未复制上述项目的源代码。

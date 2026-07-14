# 📚 LingJing — Novel Creation Multi-Agent System

> **LingJing** — An AI-powered novel creation system integrating multi-agent collaboration, modular Skills, and a knowledge graph.

A unified creative toolbox built from the best open-source novel-writing projects on GitHub, tailored for you.

[🇨🇳 **简体中文**](README.zh-CN.md)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent Collaboration** | 7 specialized agents working together |
| 🧩 **Modular Skills** | 35+ independent skills covering the full creative workflow |
| 📖 **Dual-Mode Support** | Long-form novel pipeline + short story rapid creation |
| 🎭 **De-AI Engine** | Multi-layer detection and polish for natural, human-like output |
| 📊 **Knowledge Graph** | Persistent relationships between characters, locations, and events |
| 🌐 **Multi-Platform Adaptation** | Optimized for Qidian, Fanqie, Jinjiang, and more |

---

## 🚀 Quick Install

### Windows
```powershell
iex "& { $(irm https://raw.githubusercontent.com/Kernlix/novel-writer-system/main/install.ps1) }"
```

### macOS / Linux
```bash
bash <(curl -s https://raw.githubusercontent.com/Kernlix/novel-writer-system/main/install.sh)
```

---

## 📖 How to Use (7 Ways)

### 🥇 Claude Code（完整功能，推荐）
```bash
cd novel-writer-system
claude
# 输入 /novel:start 即可进入创作向导
```

### 🥈 OpenCode CLI
```bash
cd novel-writer-system
opencode
```

### 🥉 Cursor / Windsurf / VS Code
将 `SKILL.md` 拖入 IDE 的 AI 对话窗口即可加载系统。

### 📱 Hermes Agent（当前在用）
在 Hermes 桌面端加载 `CLAUDE.md`，自动激活灵境系统。

### 📄 ChatGPT / Kimi / 其他LLM
手动复制 `SKILL.md` 内容作为系统提示词。

### 🔧 服务器集成
通过 `/novel:search` 的 RAG 引擎提供跨会话知识检索。

### 📚 纯文档查阅
直接阅读 `SUMMARY.md`（命令速查）或 `knowledge/` 下的规则和模板。

> ℹ️ 完整命令表见 `SUMMARY.md`（系统唯一权威来源）

---

## 🙏 Acknowledgements & License

### License
This system is licensed under the **MIT License** — you are free to use, modify, and distribute it, including for commercial purposes.

### Design Inspiration
## 致谢 / Acknowledgments

> ⚠️ **许可证声明**：本系统从以下开源项目中汲取灵感，但所有代码/文件均为独立实现，未直接复制上述项目的代码。下表所列外部许可证仅适用于原项目，本系统使用 MIT 许可证发布。

The design of this system was inspired by the following open-source projects:

| Project | License | Contribution |
|---------|---------|--------------|
| [awesome-novel-skill](https://github.com/modoojunko/awesome-novel-skill) | GPL-3.0 | Multi-Agent collaboration workflow & memory system |
| [tianming-skill](https://github.com/zy-zmc/tianming-skill) | CC BY-NC-SA 4.0 | Modular prompt engineering & quality gates |
| [chinese-webnovel-skills](https://github.com/tance-mang/chinese-webnovel-skills) | MIT | 33 web novel skills & platform adaptation |
| [claude-novel-skills](https://github.com/fnb666888/claude-novel-skills) | MIT | Decoupled writing method & style learning |
| [story-skills](https://github.com/ati9527/story-skills) | — | Web novel AI agent toolset |
| [vibe-noveling](https://github.com/TulanCN/vibe-noveling) | MIT | Web novel creation workflow & SSoT revision |

This system is an independent creation and does not copy source code from the above projects.
